/**
 * Tests for utils/api.js — callWithAuth, sendMessage, getQuota, getLatestConversation.
 */

let api;

beforeEach(() => {
  jest.clearAllMocks();
  // Set up getApp() return value
  Object.assign(global._mockAppData, {
    globalData: {
      cloudEnv: 'test-env',
      serviceName: 'test-service',
      token: 'valid-token',
    },
    reLogin: jest.fn(() => Promise.resolve()),
  });
  api = require('../utils/api');
});

afterEach(() => {
  jest.resetModules();
});

// ---------------------------------------------------------------------------
// sendMessage
// ---------------------------------------------------------------------------

describe('sendMessage', () => {
  test('calls callContainer with correct auth headers', () => {
    wx.cloud.callContainer.mockImplementation(() => {});

    api.sendMessage('hello', null, jest.fn(), jest.fn(), jest.fn());

    expect(wx.cloud.callContainer).toHaveBeenCalledTimes(1);
    const opts = wx.cloud.callContainer.mock.calls[0][0];
    expect(opts.path).toBe('/api/chat');
    expect(opts.method).toBe('POST');
    expect(opts.header['Authorization']).toBe('Bearer valid-token');
    expect(opts.header['X-WX-SERVICE']).toBe('test-service');
    expect(opts.data).toEqual({ message: 'hello', conversation_id: null });
  });

  test('parses SSE message and done events', () => {
    const onChunk = jest.fn();
    const onDone = jest.fn();
    const onError = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({
        statusCode: 200,
        data: [
          'data: {"type":"message","content":"Hello"}',
          'data: {"type":"message","content":" world"}',
          'data: {"type":"done","conversation_id":42}',
        ].join('\n'),
      });
    });

    api.sendMessage('hi', null, onChunk, onDone, onError);

    expect(onChunk).toHaveBeenCalledTimes(2);
    expect(onChunk).toHaveBeenNthCalledWith(1, 'Hello');
    expect(onChunk).toHaveBeenNthCalledWith(2, ' world');
    expect(onDone).toHaveBeenCalledWith({ conversationId: 42 });
    expect(onError).not.toHaveBeenCalled();
  });

  test('calls onError on 403 quota exhausted', () => {
    const onError = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 403, data: {} });
    });

    api.sendMessage('hi', null, jest.fn(), jest.fn(), onError);

    expect(onError).toHaveBeenCalledWith('对话次数已用完，请充值后继续使用。');
  });

  test('calls onError on non-200 status', () => {
    const onError = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 500, data: 'Internal Server Error' });
    });

    api.sendMessage('hi', null, jest.fn(), jest.fn(), onError);

    expect(onError).toHaveBeenCalledWith('Internal Server Error');
  });

  test('calls onError on network failure', () => {
    const onError = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.fail({ errMsg: 'request:fail' });
    });

    api.sendMessage('hi', null, jest.fn(), jest.fn(), onError);

    expect(onError).toHaveBeenCalledWith('网络请求失败，请检查网络连接。');
  });

  test('calls onDone with null conversationId when no done event', () => {
    const onDone = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({
        statusCode: 200,
        data: 'data: {"type":"message","content":"hi"}\n',
      });
    });

    api.sendMessage('hi', null, jest.fn(), onDone, jest.fn());

    expect(onDone).toHaveBeenCalledWith({ conversationId: null });
  });

  test('handles SSE error event', () => {
    const onError = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({
        statusCode: 200,
        data: 'data: {"type":"error","content":"something broke"}',
      });
    });

    api.sendMessage('hi', null, jest.fn(), jest.fn(), onError);

    expect(onError).toHaveBeenCalledWith('something broke');
  });

  test('skips invalid JSON lines in SSE', () => {
    const onChunk = jest.fn();
    const onDone = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({
        statusCode: 200,
        data: [
          'data: not-json',
          'data: {"type":"message","content":"ok"}',
          'data: {"type":"done","conversation_id":1}',
        ].join('\n'),
      });
    });

    api.sendMessage('hi', null, onChunk, onDone, jest.fn());

    expect(onChunk).toHaveBeenCalledTimes(1);
    expect(onChunk).toHaveBeenCalledWith('ok');
  });

  test('passes conversation_id to backend', () => {
    wx.cloud.callContainer.mockImplementation(() => {});

    api.sendMessage('hello', 42, jest.fn(), jest.fn(), jest.fn());

    const opts = wx.cloud.callContainer.mock.calls[0][0];
    expect(opts.data.conversation_id).toBe(42);
  });
});

// ---------------------------------------------------------------------------
// 401 auto-retry
// ---------------------------------------------------------------------------

describe('401 auto-retry', () => {
  test('retries once after re-login on 401', async () => {
    let callCount = 0;
    wx.cloud.callContainer.mockImplementation((opts) => {
      callCount++;
      if (callCount === 1) {
        opts.success({ statusCode: 401, data: { detail: 'Invalid token' } });
      } else {
        opts.success({
          statusCode: 200,
          data: 'data: {"type":"done","conversation_id":1}',
        });
      }
    });

    const onDone = jest.fn();
    api.sendMessage('hi', null, jest.fn(), onDone, jest.fn());

    // Wait for async reLogin promise chain
    await new Promise((r) => setTimeout(r, 10));

    expect(global._mockAppData.reLogin).toHaveBeenCalledTimes(1);
    expect(wx.cloud.callContainer).toHaveBeenCalledTimes(2);
  });

  test('does not retry more than once on repeated 401', async () => {
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 401, data: { detail: 'Invalid token' } });
    });

    api.sendMessage('hi', null, jest.fn(), jest.fn(), jest.fn());

    await new Promise((r) => setTimeout(r, 10));

    // First call + one retry = 2 total
    expect(wx.cloud.callContainer).toHaveBeenCalledTimes(2);
  });
});

// ---------------------------------------------------------------------------
// getQuota
// ---------------------------------------------------------------------------

describe('getQuota', () => {
  test('returns remaining quota on success', () => {
    const callback = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 200, data: { remaining: 15 } });
    });

    api.getQuota(callback);

    expect(callback).toHaveBeenCalledWith(null, 15);
  });

  test('returns error on non-200', () => {
    const callback = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 500, data: {} });
    });

    api.getQuota(callback);

    expect(callback).toHaveBeenCalledWith('获取余额失败');
  });

  test('returns error on network failure', () => {
    const callback = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.fail({});
    });

    api.getQuota(callback);

    expect(callback).toHaveBeenCalledWith('网络请求失败');
  });
});

// ---------------------------------------------------------------------------
// getLatestConversation
// ---------------------------------------------------------------------------

describe('getLatestConversation', () => {
  test('returns conversation data on success', () => {
    const callback = jest.fn();
    const mockData = {
      conversation_id: 1,
      messages: [{ role: 'user', content: 'hi' }],
    };

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 200, data: mockData });
    });

    api.getLatestConversation(callback);

    expect(callback).toHaveBeenCalledWith(null, mockData);
  });

  test('returns error on non-200', () => {
    const callback = jest.fn();

    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 500, data: {} });
    });

    api.getLatestConversation(callback);

    expect(callback).toHaveBeenCalledWith('加载对话失败');
  });
});
