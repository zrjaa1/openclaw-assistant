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
  const requestTask = wx.request({
    url: `${app.globalData.baseUrl}/api/chat`,
    method: 'POST',
    enableChunkedTransfer: true,
    header: {
      'Authorization': `Bearer ${app.globalData.token}`,
      'Content-Type': 'application/json',
    },
    data: {
      message: message,
      conversation_id: conversationId,
    },
    success(res) {
      if (res.statusCode === 403) {
        onError('对话次数已用完，请充值后继续使用。');
        return;
      }
      if (res.statusCode !== 200) {
        onError(res.data.detail || '请求失败');
        return;
      }
      // Parse SSE data from response
      const text = res.data;
      if (typeof text === 'string') {
        const lines = text.split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              if (data.type === 'message') {
                onChunk(data.content);
              } else if (data.type === 'done') {
                onDone({ conversationId: data.conversation_id });
              } else if (data.type === 'error') {
                onError(data.content);
              }
            } catch (e) {
              // skip invalid JSON
            }
          }
        }
      }
    },
    fail(err) {
      onError('网络请求失败，请检查网络连接。');
    },
  });

  return requestTask;
}

/**
 * Get remaining quota for current user.
 */
function getQuota(callback) {
  wx.request({
    url: `${app.globalData.baseUrl}/api/quota`,
    method: 'GET',
    header: {
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
