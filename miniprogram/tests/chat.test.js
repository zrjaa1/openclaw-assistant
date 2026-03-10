/**
 * Tests for pages/chat/chat.js — page lifecycle, message handling, code extraction.
 */

let pageDef;

beforeEach(() => {
  jest.clearAllMocks();
  global._capturedPageDef = null;
  Object.assign(global._mockAppData, {
    globalData: {
      cloudEnv: 'test-env',
      serviceName: 'test-service',
      token: 'valid-token',
    },
  });
  require('../pages/chat/chat');
  pageDef = global._capturedPageDef;
});

afterEach(() => {
  jest.resetModules();
});

// ---------------------------------------------------------------------------
// extractCode
// ---------------------------------------------------------------------------

describe('extractCode', () => {
  test('extracts code from single code block', () => {
    const content = 'Here is code:\n```bash\nnpm install\n```\nDone.';
    expect(pageDef.extractCode(content)).toBe('npm install');
  });

  test('extracts and joins multiple code blocks', () => {
    const content = '```\nfirst\n```\ntext\n```js\nsecond\n```';
    expect(pageDef.extractCode(content)).toBe('first\nsecond');
  });

  test('returns empty string when no code blocks', () => {
    expect(pageDef.extractCode('no code here')).toBe('');
  });

  test('handles code block with no language specifier', () => {
    const content = '```\nhello world\n```';
    expect(pageDef.extractCode(content)).toBe('hello world');
  });
});

// ---------------------------------------------------------------------------
// onInput
// ---------------------------------------------------------------------------

describe('onInput', () => {
  test('updates inputText from event detail', () => {
    const setData = jest.fn();
    const page = { setData, data: { ...pageDef.data } };

    pageDef.onInput.call(page, { detail: { value: 'test input' } });

    expect(setData).toHaveBeenCalledWith({ inputText: 'test input' });
  });
});

// ---------------------------------------------------------------------------
// onSend
// ---------------------------------------------------------------------------

describe('onSend', () => {
  test('does nothing when input is empty', () => {
    const setData = jest.fn();
    const page = {
      setData,
      data: { ...pageDef.data, inputText: '  ', isTyping: false },
    };

    pageDef.onSend.call(page);

    expect(setData).not.toHaveBeenCalled();
  });

  test('does nothing when already typing', () => {
    const setData = jest.fn();
    const page = {
      setData,
      data: { ...pageDef.data, inputText: 'hello', isTyping: true },
    };

    pageDef.onSend.call(page);

    expect(setData).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// onCopyCode
// ---------------------------------------------------------------------------

describe('onCopyCode', () => {
  test('copies code content to clipboard', () => {
    pageDef.onCopyCode({ currentTarget: { dataset: { content: 'npm install' } } });

    expect(wx.setClipboardData).toHaveBeenCalledWith(
      expect.objectContaining({ data: 'npm install' })
    );
  });

  test('does nothing when content is empty', () => {
    pageDef.onCopyCode({ currentTarget: { dataset: { content: '' } } });

    expect(wx.setClipboardData).not.toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// onLoad
// ---------------------------------------------------------------------------

describe('onLoad', () => {
  test('loads quota and conversation when token is available', () => {
    const page = {
      data: { ...pageDef.data },
      setData: jest.fn(),
      loadQuota: jest.fn(),
      loadLatestConversation: jest.fn(),
    };

    pageDef.onLoad.call(page);

    expect(page.loadQuota).toHaveBeenCalled();
    expect(page.loadLatestConversation).toHaveBeenCalled();
  });

  test('sets loginCallback when token is not available', () => {
    global._mockAppData.globalData.token = '';

    const page = {
      data: { ...pageDef.data },
      setData: jest.fn(),
      loadLatestConversation: jest.fn(),
    };

    pageDef.onLoad.call(page);

    expect(global._mockAppData.loginCallback).toBeDefined();
  });
});
