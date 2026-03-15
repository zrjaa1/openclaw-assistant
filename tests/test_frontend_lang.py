"""Tests for the frontend language toggle functionality.

Validates that both the auth and chat screens have working language toggles
that share the same i18n system (toggleLang / applyLang).
"""

import re
from pathlib import Path

import pytest

HTML_PATH = Path(__file__).resolve().parent.parent / "web" / "index.html"


@pytest.fixture(scope="module")
def html():
    return HTML_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def js_code(html):
    """Extract the main JS block (largest <script> tag)."""
    blocks = re.findall(r"<script>(.*?)</script>", html, re.DOTALL)
    return max(blocks, key=len)


# --- Structure tests ---


def test_auth_lang_toggle_exists_in_html(html):
    """The auth screen must have a lang toggle button with id='auth-lang-toggle'."""
    assert 'id="auth-lang-toggle"' in html


def test_chat_lang_toggle_exists_in_html(html):
    """The chat screen must have a lang toggle button with id='lang-toggle'."""
    assert 'id="lang-toggle"' in html


def test_no_duplicate_toggle_ids(html):
    """Each toggle button ID must appear exactly once in the HTML."""
    assert html.count('id="auth-lang-toggle"') == 1
    assert html.count('id="lang-toggle"') == 1


def test_auth_toggle_not_covered_by_overlapping_element(html):
    """The auth toggle's container must have z-index to prevent overlap."""
    # Find the line with auth-lang-toggle and its parent div
    lines = html.split("\n")
    for i, line in enumerate(lines):
        if "auth-lang-toggle" in line and "<button" in line:
            # Check the parent div (line above or same container)
            context = "\n".join(lines[max(0, i - 3):i + 1])
            assert "z-10" in context or "z-20" in context, (
                "auth-lang-toggle container needs z-index to stay above the card"
            )
            break
    else:
        pytest.fail("auth-lang-toggle button not found in HTML")


# --- i18n system tests ---


def test_strings_defined_for_both_languages(js_code):
    """Both 'en' and 'zh' string sets must be defined."""
    assert re.search(r"STRINGS\s*=\s*\{", js_code), "STRINGS object not found"
    assert "'en'" in js_code or "en:" in js_code, "English strings missing"
    assert "'zh'" in js_code or "zh:" in js_code, "Chinese strings missing"


def test_toggle_lang_function_exists(js_code):
    """toggleLang must exist and toggle between 'zh' and 'en'."""
    assert "function toggleLang" in js_code
    # Must toggle the value
    assert "currentLang === 'zh' ? 'en' : 'zh'" in js_code


def test_toggle_saves_to_localstorage(js_code):
    """toggleLang must persist the choice to localStorage."""
    # Find the toggleLang function body
    match = re.search(r"function toggleLang\(\)\s*\{(.*?)\n\}", js_code, re.DOTALL)
    assert match, "toggleLang function not found"
    body = match.group(1)
    assert "localStorage.setItem" in body, "toggleLang must save to localStorage"
    assert "'lang'" in body, "toggleLang must save with key 'lang'"


def test_apply_lang_updates_both_toggles(js_code):
    """applyLang must update text for both auth-lang-toggle and lang-toggle."""
    match = re.search(r"function applyLang\(\)\s*\{(.*?)\n\}", js_code, re.DOTALL)
    assert match, "applyLang function not found"
    body = match.group(1)
    assert "auth-lang-toggle" in body, "applyLang must update auth screen toggle"
    assert "lang-toggle" in body, "applyLang must update chat screen toggle"


def test_both_toggles_bound_to_toggle_lang(js_code):
    """Both toggle buttons must be wired to call toggleLang."""
    # Either via addEventListener or onclick attribute
    auth_bound = (
        "auth-lang-toggle" in js_code
        and ("addEventListener" in js_code or "onclick" in js_code)
    )
    chat_bound = (
        "'lang-toggle'" in js_code
        and ("addEventListener" in js_code or "onclick" in js_code)
    )
    assert auth_bound, "auth-lang-toggle must be bound to toggleLang"
    assert chat_bound, "lang-toggle must be bound to toggleLang"


def test_auto_detect_language(js_code):
    """Language detection must check navigator.language for 'zh' prefix."""
    assert "navigator.language" in js_code
    assert "startsWith('zh')" in js_code or "startsWith(\"zh\")" in js_code


def test_localstorage_override_requires_explicit_flag(js_code):
    """localStorage lang should only be trusted if explicitly set by user."""
    assert "lang-explicit" in js_code, (
        "Must track explicit user choice to avoid stale localStorage overriding auto-detect"
    )
