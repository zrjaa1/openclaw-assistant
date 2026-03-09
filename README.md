# OpenClaw Assistant

OpenClaw 安装与使用助手 —— 帮助非技术用户轻松安装和配置 OpenClaw。

## 架构

```
微信小程序 → Python 后端 (FastAPI) → Dify Cloud (RAG + LLM)
```

- **后端**: Python FastAPI，处理用户认证、对话转发、quota 管理
- **前端**: 微信小程序，聊天 UI + 命令一键复制
- **AI**: Dify Cloud 提供 RAG 知识库 + LLM（Qwen）

## 快速开始

### 后端

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 Dify API Key、微信 AppID 等

# 3. 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 微信小程序

1. 打开微信开发者工具
2. 导入 `miniprogram/` 目录
3. 修改 `app.js` 中的 `baseUrl` 为你的后端地址
4. 修改 `project.config.json` 中的 `appid` 为你的小程序 AppID

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/login` | 微信登录 |
| POST | `/api/chat` | 发送消息（SSE 流式返回） |
| GET | `/api/quota` | 查询剩余对话次数 |
| GET | `/api/health` | 健康检查 |

## 配置 Dify

1. 注册 [Dify Cloud](https://cloud.dify.ai)
2. 创建应用 → 选择"聊天助手"
3. 上传 `docs/` 目录下的知识库文档
4. 配置 System Prompt 和 LLM 模型（推荐 Qwen）
5. 获取 API Key 填入 `.env`

## License

MIT
