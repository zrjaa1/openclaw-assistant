const api = require('../../utils/api');
const app = getApp();

let msgIdCounter = 0;

Page({
  data: {
    messages: [],
    inputText: '',
    isTyping: false,
    currentResponse: '',
    scrollToId: '',
    conversationId: null,
    remainingQuota: -1,  // -1 means not loaded yet
  },

  onLoad() {
    this._initChat();
  },

  onShow() {
    // Re-init on every foreground resume so that after a re-login
    // (triggered by app.onShow) we reload conversation and quota.
    // Use _loginPromise to wait for any in-flight login to finish.
    if (app._loginPromise) {
      app._loginPromise.then(() => {
        this.loadQuota();
        this.loadLatestConversation();
      }).catch(() => {});
    }
  },

  _initChat() {
    // Wait for login then load quota and restore conversation
    if (app.globalData.token) {
      this.loadQuota();
      this.loadLatestConversation();
    } else {
      app.loginCallback = (data) => {
        this.setData({ remainingQuota: data.remaining_quota });
        this.loadLatestConversation();
      };
    }
  },

  loadLatestConversation() {
    api.getLatestConversation((err, data) => {
      if (err || !data || !data.conversation_id) return;

      const messages = (data.messages || []).map((m) => {
        const id = ++msgIdCounter;
        const hasCode = m.role === 'assistant' && (m.content.includes('```') || m.content.includes('> '));
        return {
          id,
          role: m.role,
          content: m.content,
          hasCode,
          codeContent: hasCode ? this.extractCode(m.content) : '',
        };
      });

      this.setData({
        messages,
        conversationId: data.conversation_id,
        scrollToId: messages.length ? `msg-${messages[messages.length - 1].id}` : '',
      });
    });
  },

  loadQuota() {
    api.getQuota((err, remaining) => {
      if (!err) {
        this.setData({ remainingQuota: remaining });
      }
    });
  },

  onInput(e) {
    this.setData({ inputText: e.detail.value });
  },

  onSend() {
    const text = this.data.inputText.trim();
    if (!text || this.data.isTyping) return;

    // Add user message
    const userMsgId = ++msgIdCounter;
    const userMsg = {
      id: userMsgId,
      role: 'user',
      content: text,
    };

    this.setData({
      messages: [...this.data.messages, userMsg],
      inputText: '',
      isTyping: true,
      currentResponse: '',
      scrollToId: `msg-${userMsgId}`,
    });

    // Send to backend
    api.sendMessage(
      text,
      this.data.conversationId,
      // onChunk
      (chunk) => {
        this.setData({
          currentResponse: this.data.currentResponse + chunk,
          scrollToId: 'bottom-anchor',
        });
      },
      // onDone
      (result) => {
        const assistantMsgId = ++msgIdCounter;
        const fullContent = this.data.currentResponse;
        const hasCode = fullContent.includes('```') || fullContent.includes('> ');
        const codeContent = this.extractCode(fullContent);

        const assistantMsg = {
          id: assistantMsgId,
          role: 'assistant',
          content: fullContent,
          hasCode: hasCode,
          codeContent: codeContent,
        };

        this.setData({
          messages: [...this.data.messages, assistantMsg],
          isTyping: false,
          currentResponse: '',
          conversationId: result.conversationId || this.data.conversationId,
          scrollToId: `msg-${assistantMsgId}`,
        });

        // Refresh quota
        this.loadQuota();
      },
      // onError
      (errMsg) => {
        const assistantMsgId = ++msgIdCounter;
        const errorMsg = {
          id: assistantMsgId,
          role: 'assistant',
          content: `抱歉，出现了问题：${errMsg}`,
          hasCode: false,
        };

        this.setData({
          messages: [...this.data.messages, errorMsg],
          isTyping: false,
          currentResponse: '',
        });
      }
    );
  },

  extractCode(content) {
    // Extract content between ``` blocks
    const matches = content.match(/```[\s\S]*?\n([\s\S]*?)```/g);
    if (matches) {
      return matches
        .map((m) => m.replace(/```\w*\n?/g, '').replace(/```/g, '').trim())
        .join('\n');
    }
    return '';
  },

  onCopyCode(e) {
    const content = e.currentTarget.dataset.content;
    if (!content) return;

    wx.setClipboardData({
      data: content,
      success() {
        wx.showToast({ title: '已复制', icon: 'success' });
      },
    });
  },
});
