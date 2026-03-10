const app = getApp();

/**
 * Make a cloud container request, auto-retrying once on 401 after re-login.
 */
function callWithAuth(options, retried) {
  const opts = Object.assign({}, options, {
    config: { env: app.globalData.cloudEnv },
    header: Object.assign({
      'X-WX-SERVICE': app.globalData.serviceName,
      'Authorization': `Bearer ${app.globalData.token}`,
      'content-type': 'application/json',
    }, options.header || {}),
  });

  const originalSuccess = opts.success;
  opts.success = function (res) {
    if (res.statusCode === 401 && !retried) {
      app.reLogin().then(() => {
        callWithAuth(options, true);
      }).catch(() => {
        if (originalSuccess) originalSuccess(res);
      });
      return;
    }
    if (originalSuccess) originalSuccess(res);
  };

  wx.cloud.callContainer(opts);
}

/**
 * Send chat message and receive streaming response.
 * @param {string} message - User message
 * @param {number|null} conversationId - Existing conversation ID or null
 * @param {function} onChunk - Called with each text chunk
 * @param {function} onDone - Called when stream ends, receives { conversationId }
 * @param {function} onError - Called on error
 */
function sendMessage(message, conversationId, onChunk, onDone, onError) {
  callWithAuth({
    path: '/api/chat',
    method: 'POST',
    data: {
      message: message,
      conversation_id: conversationId,
    },
    dataType: 'text',
    success(res) {
      if (res.statusCode === 403) {
        onError('对话次数已用完，请充值后继续使用。');
        return;
      }
      if (res.statusCode !== 200) {
        const detail = (typeof res.data === 'string') ? res.data : (res.data && res.data.detail) || '请求失败';
        onError(detail);
        return;
      }

      // Parse SSE events from the full response body
      const text = typeof res.data === 'string' ? res.data : JSON.stringify(res.data);
      const lines = text.split('\n');
      let gotDone = false;

      for (const line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('data: ')) {
          try {
            const data = JSON.parse(trimmed.slice(6));
            if (data.type === 'message') {
              onChunk(data.content);
            } else if (data.type === 'done') {
              gotDone = true;
              onDone({ conversationId: data.conversation_id });
            } else if (data.type === 'error') {
              gotDone = true;
              onError(data.content);
              return;
            }
          } catch (e) {
            // skip invalid JSON
          }
        }
      }

      if (!gotDone) {
        onDone({ conversationId: null });
      }
    },
    fail(err) {
      onError('网络请求失败，请检查网络连接。');
    },
  });
}

/**
 * Get remaining quota for current user.
 */
function getQuota(callback) {
  callWithAuth({
    path: '/api/quota',
    method: 'GET',
    success(res) {
      if (res.statusCode === 200) {
        callback(null, res.data.remaining);
      } else {
        callback('获取余额失败');
      }
    },
    fail() {
      callback('网络请求失败');
    },
  });
}

/**
 * Load the user's latest conversation with message history.
 */
function getLatestConversation(callback) {
  callWithAuth({
    path: '/api/conversation/latest',
    method: 'GET',
    success(res) {
      if (res.statusCode === 200) {
        callback(null, res.data);
      } else {
        callback('加载对话失败');
      }
    },
    fail() {
      callback('网络请求失败');
    },
  });
}

module.exports = { sendMessage, getQuota, getLatestConversation };
