/**
 * Minimal mock for the WeChat `wx` global object used in miniprogram code.
 * This file is loaded via jest.config.js setupFiles.
 */

global.wx = {
  cloud: {
    init: jest.fn(),
    callContainer: jest.fn(),
  },
  login: jest.fn(),
  setClipboardData: jest.fn(),
  showToast: jest.fn(),
};

// App() captures app definition
global._capturedAppDef = null;
global.App = jest.fn((def) => {
  global._capturedAppDef = def;
});

// Page() captures page definition
global._capturedPageDef = null;
global.Page = jest.fn((def) => {
  global._capturedPageDef = def;
});

// getApp() returns a mutable object — tests set its properties
global._mockAppData = {
  globalData: { cloudEnv: '', serviceName: '', token: '' },
};
global.getApp = jest.fn(() => global._mockAppData);
