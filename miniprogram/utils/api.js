const app = getApp();

/**
 * Send chat message and receive streaming response.
 * @param {string} message - User message
 * @param {number|null} conversationId - Existing conversation ID or null
 * @param {function} onChunk - Called with each text chunk
 * @param {function} onDone - Called when stream ends, receives { conversationId }
 * @param {function} onError - Called on error
 */
function sendMessage(message, conversationId, onChunk, onDone, onError) {
  // Note: wx.cloud.callContainer does not support chunked/streaming transfer.
  // The full SSE response is received at once and parsed in the success callback.
  wx.cloud.callContainer({
    config: {
      env: app.globalData.cloudEnv,
    },
    path: '/api/chat',
    method: 'POST',
    header: {
      'X-WX-SERVICE': app.globalData.serviceName,
      'Authorization': `Bearer ${app.globalData.token}`,
      'content-type': 'application/json',
    },
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
  wx.cloud.callContainer({
    config: {
      env: app.globalData.cloudEnv,
    },
    path: '/api/quota',
    method: 'GET',
    header: {
      'X-WX-SERVICE': app.globalData.serviceName,
      'Authorization': `Bearer ${app.globalData.token}`,
    },
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

module.exports = { sendMessage, getQuota };
