"""Tests for chat message formatting fixes (ref #21).

Validates:
- User bubble has word-break CSS to prevent long command overflow
- renderMarkdown() heuristically wraps CLI command lines as code blocks
- Existing triple-backtick code blocks still render correctly (no regression)
"""

import re
from pathlib import Path

import pytest

HTML_PATH = Path(__file__).resolve().parent.parent / "web" / "index.html"


@pytest.fixture(scope="module")
def html():
    return HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def css_block(html):
    """Extract the content of the <style> block."""
    match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    assert match, "<style> block not found in index.html"
    return match.group(1)


@pytest.fixture(scope="module")
def js_code(html):
    """Extract the main JS block (largest <script> tag)."""
    blocks = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
    return max(blocks, key=len)


# ---------------------------------------------------------------------------
# AC1: User bubble word-break (long commands wrap cleanly)
# ---------------------------------------------------------------------------


def test_long_command_user_bubble_css_class_defined(css_block):
    """CSS must define .user-bubble with word-break or overflow-wrap."""
    assert ".user-bubble" in css_block, (
        ".user-bubble CSS class must be defined in <style> block"
    )
    bubble_block_match = re.search(
        r"\.user-bubble\s*\{([^}]*)\}", css_block, re.DOTALL
    )
    assert bubble_block_match, ".user-bubble rule block not found"
    rule_body = bubble_block_match.group(1)
    has_word_break = "word-break" in rule_body
    has_overflow_wrap = "overflow-wrap" in rule_body
    assert has_word_break or has_overflow_wrap, (
        ".user-bubble must set word-break or overflow-wrap to handle long commands"
    )


def test_long_command_user_bubble_class_applied_to_user_messages(js_code):
    """appendMessage() must apply .user-bubble class to user message bubbles."""
    # Find the user bubble className assignment in appendMessage
    assert "user-bubble" in js_code, (
        "'user-bubble' class must be applied to user bubble elements in JS"
    )
    # Verify it appears alongside the accent-500 user bubble styling
    match = re.search(r"bg-accent-500[^'\"]*user-bubble|user-bubble[^'\"]*bg-accent-500", js_code)
    assert match, (
        "user-bubble class must be on the same element as bg-accent-500 (user message bubble)"
    )


# ---------------------------------------------------------------------------
# AC2: Command detection in assistant messages
# ---------------------------------------------------------------------------


def test_command_detection_cli_prefix_pattern_exists(js_code):
    """renderMarkdown() must define a CLI prefix regex for command detection."""
    assert "CLI_PREFIX" in js_code, (
        "CLI_PREFIX regex must be defined in renderMarkdown()"
    )


def test_command_detection_includes_openclaw(js_code):
    """CLI_PREFIX must include 'openclaw' as a detectable command."""
    cli_match = re.search(r"CLI_PREFIX\s*=\s*/(.+?)/[ig]*", js_code)
    assert cli_match, "CLI_PREFIX regex pattern not found"
    pattern_body = cli_match.group(1)
    assert "openclaw" in pattern_body, (
        "CLI_PREFIX must detect 'openclaw' commands"
    )


def test_command_detection_includes_common_clis(js_code):
    """CLI_PREFIX should include common CLI tools: curl, npm, pip, iwr."""
    cli_match = re.search(r"CLI_PREFIX\s*=\s*/(.+?)/[ig]*", js_code)
    assert cli_match, "CLI_PREFIX regex pattern not found"
    pattern_body = cli_match.group(1)
    for cmd in ["curl", "npm", "pip", "iwr"]:
        assert cmd in pattern_body, f"CLI_PREFIX must detect '{cmd}' commands"


def test_command_detection_wraps_in_pre_code(js_code):
    """Command detection must wrap matched lines in <pre><code> blocks."""
    # Find the CLI detection logic block
    assert "CLI_PREFIX.test" in js_code, (
        "CLI_PREFIX.test() must be used to check each line"
    )
    # Must produce a pre/code block
    cli_section_match = re.search(
        r"CLI_PREFIX\.test\(trimmed\)(.*?)return line;", js_code, re.DOTALL
    )
    assert cli_section_match, "CLI detection block not found in renderMarkdown"
    block = cli_section_match.group(1)
    assert "<pre" in block and "<code>" in block, (
        "Detected CLI lines must be wrapped in <pre><code> elements"
    )


def test_command_detection_adds_copy_button(js_code):
    """Detected command lines should include a copy button, consistent with code blocks."""
    cli_section_match = re.search(
        r"CLI_PREFIX\.test\(trimmed\)(.*?)return line;", js_code, re.DOTALL
    )
    assert cli_section_match, "CLI detection block not found"
    block = cli_section_match.group(1)
    assert "copyCode" in block, (
        "Auto-detected command blocks should include a copyCode button"
    )


def test_command_detection_skips_html_residuals(js_code):
    """Command detection must skip residual lines from already-converted code blocks."""
    # The guard for HTML-containing lines (e.g., trailing </code></pre>)
    assert "trimmed.includes('</')" in js_code or "includes('</')" in js_code, (
        "Command detection must skip lines that already contain HTML closing tags "
        "(residuals from multi-line fenced code block conversion)"
    )


# ---------------------------------------------------------------------------
# AC3: Existing triple-backtick code blocks still render (no regression)
# ---------------------------------------------------------------------------


def test_existing_code_blocks_still_work_regex_present(js_code):
    """The triple-backtick regex must still exist in renderMarkdown()."""
    assert "```" in js_code or r"\`\`\`" in js_code or "```" in js_code, (
        "Triple-backtick code block regex must be present in renderMarkdown()"
    )
    # Check the actual regex pattern
    assert re.search(r"\\`\\`\\`|```", js_code), (
        "Backtick code block regex not found in JS"
    )


def test_existing_code_blocks_produce_pre_code(js_code):
    """Triple-backtick processing must still produce <pre><code> output."""
    # Find the code block replacement in renderMarkdown (the backtick handler)
    backtick_match = re.search(
        r"text\s*=\s*text\.replace\(/```(.*?)/g",
        js_code,
        re.DOTALL,
    )
    assert backtick_match, "Triple-backtick text.replace() not found in renderMarkdown"


def test_command_detection_after_code_block_processing(js_code):
    """Command detection must run AFTER triple-backtick processing to avoid re-wrapping."""
    # Find positions of both blocks in the JS
    code_block_pos = js_code.find("```")
    cli_prefix_pos = js_code.find("CLI_PREFIX")
    assert code_block_pos != -1, "Triple-backtick handling not found"
    assert cli_prefix_pos != -1, "CLI_PREFIX not found"
    assert code_block_pos < cli_prefix_pos, (
        "CLI_PREFIX detection must appear AFTER triple-backtick code block processing "
        "so that fenced code blocks are not double-processed"
    )
