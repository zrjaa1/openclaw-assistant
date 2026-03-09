App({
  globalData: {
    token: '',
    baseUrl: 'https://your-server.com',  // TODO: 替换为你的后端地址
  },

  onLaunch() {
    this.login();
  },

  login() {
    const that = this;
    wx.login({
      success(res) {
        if (!res.code) {
          console.error('wx.login failed');
          return;
        }
        wx.request({
          url: `${that.globalData.baseUrl}/api/login`,
          method: 'POST',
          data: { code: res.code },
          success(resp) {
            if (resp.statusCode === 200) {
              that.globalData.token = resp.data.token;
              // Notify pages that login is done
              if (that.loginCallback) {
                that.loginCallback(resp.data);
              }
            } else {
              console.error('Login failed:', resp.data);
            }
          },
          fail(err) {
            console.error('Login request failed:', err);
          },
        });
      },
    });
  },
});
