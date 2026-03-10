/**
 * Tests for app.js — login, reLogin, and initialization.
 */

let appDef;

beforeEach(() => {
  jest.clearAllMocks();
  global._capturedAppDef = null;
  require('../app');
  appDef = global._capturedAppDef;
});

afterEach(() => {
  jest.resetModules();
});

// ---------------------------------------------------------------------------
// onLaunch
// ---------------------------------------------------------------------------

describe('onLaunch', () => {
  test('initializes cloud and calls login', () => {
    const loginSpy = jest.fn();
    const app = {
      globalData: { cloudEnv: 'test-env', serviceName: 'svc', token: '' },
      login: loginSpy,
    };

    appDef.onLaunch.call(app);

    expect(wx.cloud.init).toHaveBeenCalledWith({ env: 'test-env' });
    expect(loginSpy).toHaveBeenCalled();
  });
});

// ---------------------------------------------------------------------------
// login
// ---------------------------------------------------------------------------

describe('login', () => {
  function makeApp() {
    return {
      globalData: { cloudEnv: 'test-env', serviceName: 'svc', token: '' },
    };
  }

  test('stores token on successful login', () => {
    wx.login.mockImplementation(({ success }) => success({ code: 'c' }));
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 200, data: { token: 'new-token', remaining_quota: 20 } });
    });

    const app = makeApp();
    appDef.login.call(app);

    expect(app.globalData.token).toBe('new-token');
    // Consume the promise to avoid unhandled rejection
    return app._loginPromise;
  });

  test('calls loginCallback when set', () => {
    const cb = jest.fn();
    wx.login.mockImplementation(({ success }) => success({ code: 'c' }));
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 200, data: { token: 't', remaining_quota: 5 } });
    });

    const app = { ...makeApp(), loginCallback: cb };
    appDef.login.call(app);

    expect(cb).toHaveBeenCalledWith({ token: 't', remaining_quota: 5 });
    return app._loginPromise;
  });

  test('invokes callback with error on login failure', async () => {
    const cb = jest.fn();
    wx.login.mockImplementation(({ success }) => success({ code: 'c' }));
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 500, data: 'error' });
    });

    const app = makeApp();
    appDef.login.call(app, cb);

    expect(cb).toHaveBeenCalledWith('error');
    expect(app.globalData.token).toBe('');
    // Consume the rejection to avoid unhandled promise warning
    await expect(app._loginPromise).rejects.toThrow('Login failed');
  });

  test('does not call API when wx.login returns no code', async () => {
    wx.login.mockImplementation(({ success }) => success({}));

    const app = makeApp();
    appDef.login.call(app);

    expect(wx.cloud.callContainer).not.toHaveBeenCalled();
    await expect(app._loginPromise).rejects.toThrow('wx.login failed');
  });

  test('handles network failure', async () => {
    const cb = jest.fn();
    wx.login.mockImplementation(({ success }) => success({ code: 'c' }));
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.fail({ errMsg: 'network error' });
    });

    const app = makeApp();
    appDef.login.call(app, cb);

    expect(cb).toHaveBeenCalledWith({ errMsg: 'network error' });
    await expect(app._loginPromise).rejects.toEqual({ errMsg: 'network error' });
  });
});

// ---------------------------------------------------------------------------
// reLogin
// ---------------------------------------------------------------------------

describe('reLogin', () => {
  function makeApp() {
    return {
      globalData: { cloudEnv: 'test-env', serviceName: 'svc', token: '' },
      login: appDef.login,
      reLogin: appDef.reLogin,
    };
  }

  test('resolves on successful login', async () => {
    wx.login.mockImplementation(({ success }) => success({ code: 'c' }));
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 200, data: { token: 'refreshed', remaining_quota: 10 } });
    });

    const app = makeApp();
    await app.reLogin();

    expect(app.globalData.token).toBe('refreshed');
  });

  test('rejects on failed login', async () => {
    wx.login.mockImplementation(({ success }) => success({ code: 'c' }));
    wx.cloud.callContainer.mockImplementation((opts) => {
      opts.success({ statusCode: 500, data: 'error' });
    });

    const app = makeApp();
    await expect(app.reLogin()).rejects.toThrow('Login failed');
  });
});
