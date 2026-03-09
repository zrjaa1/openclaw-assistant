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
  let buffer = '';
  let gotDone = false;

  const requestTask = wx.cloud.callContainer({
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
    enableChunkedTransfer: true,
    responseType: 'text',
    success(res) {
      if (res.statusCode === 403) {
        onError('对话次数已用完，请充值后继续使用。');
        return;
      }
      if (res.statusCode !== 200) {
        onError(res.data.detail || '请求失败');
        return;
      }
      // Process any remaining data in buffer
      if (res.data) {
        const text = typeof res.data === 'string' ? res.data : '';
        processSSEBuffer(text);
      }
      // Ensure we always finalize
      if (!gotDone) {
        onDone({ conversationId: null });
      }
    },
    fail(err) {
      if (!gotDone) {
        onError('网络请求失败，请检查网络连接。');
      }
    },
  });

  function processSSEBuffer(text) {
    buffer += text;
    const parts = buffer.split('\n');
    // Keep the last incomplete line in buffer
    buffer = parts.pop() || '';

    for (const line of parts) {
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
          }
        } catch (e) {
          // skip invalid JSON
        }
      }
    }
  }

  // Handle real-time chunks as they arrive
  if (requestTask && requestTask.onChunkReceived) {
    requestTask.onChunkReceived(function (res) {
      if (res.data) {
        let text;
        if (res.data instanceof ArrayBuffer) {
          text = String.fromCharCode.apply(null, new Uint8Array(res.data));
        } else {
          text = String(res.data);
        }
        processSSEBuffer(text);
      }
    });
  }

  return requestTask;
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
