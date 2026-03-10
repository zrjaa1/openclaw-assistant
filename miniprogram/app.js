App({
  globalData: {
    token: '',
    cloudEnv: 'openclaw-assistant-7ddog43bea1e1',
    serviceName: 'openclaw-assistant',  // 云托管服务名称，请在控制台确认
  },

  onLaunch() {
    wx.cloud.init({
      env: this.globalData.cloudEnv,
    });
    this.login();
  },

  login(callback) {
    const that = this;
    that._loginPromise = new Promise((resolve, reject) => {
      wx.login({
        success(res) {
          if (!res.code) {
            console.error('wx.login failed');
            reject(new Error('wx.login failed'));
            return;
          }
          wx.cloud.callContainer({
            config: {
              env: that.globalData.cloudEnv,
            },
            path: '/api/login',
            method: 'POST',
            header: {
              'X-WX-SERVICE': that.globalData.serviceName,
              'content-type': 'application/json',
            },
            data: { code: res.code },
            success(resp) {
              if (resp.statusCode === 200) {
                that.globalData.token = resp.data.token;
                if (that.loginCallback) {
                  that.loginCallback(resp.data);
                }
                if (callback) callback(null, resp.data);
                resolve(resp.data);
              } else {
                console.error('Login failed:', resp.data);
                if (callback) callback(resp.data);
                reject(new Error('Login failed'));
              }
            },
            fail(err) {
              console.error('Login request failed:', err);
              if (callback) callback(err);
              reject(err);
            },
          });
        },
        fail(err) {
          reject(err);
        },
      });
    });
  },

  reLogin() {
    this.login();
    return this._loginPromise;
  },
});
