# OpenClaw Assistant

OpenClaw 安装与使用助手 —— 帮助非技术用户轻松安装和配置 OpenClaw。

## 架构

```
微信小程序  ┐
            ├→ Python 后端 (FastAPI) → Dify Cloud (RAG + LLM)
Web 前端   ┘
```

- **后端**: Python FastAPI，处理用户认证、对话转发、quota 管理
- **前端**: 微信小程序 + Web 前端（`/web/`），聊天 UI + 命令一键复制
- **AI**: Dify Cloud 提供 RAG 知识库 + LLM（Qwen）
- **认证**: 微信用户通过 `openid` 登录；Web 用户通过用户名/密码注册登录

## 项目结构

```
app/
├── api/
│   ├── auth.py          # 微信登录 + JWT
│   ├── web_auth.py      # Web 注册/登录（用户名+密码+bcrypt）
│   ├── chat.py          # 聊天（SSE 流式）
│   └── quota.py         # 对话次数查询
├── db/
│   └── database.py      # SQLAlchemy 模型（User, Conversation, Message）
├── services/
│   ├── dify_service.py  # Dify API 调用
│   ├── quota_service.py # Quota 扣减逻辑
│   └── wechat_service.py
├── config.py            # 环境变量配置
└── main.py              # FastAPI 入口
web/
└── index.html           # Web 前端（单文件，Tailwind CSS CDN）
miniprogram/             # 微信小程序
tests/                   # pytest 测试（58 tests）
```

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

### 本地测试（不依赖微信云托管）

后端是标准 FastAPI 应用，可以完全在本地运行：

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 最小化 .env（SQLite 默认，无需 MySQL）
cat > .env << 'EOF'
JWT_SECRET=dev-secret-change-in-prod
DIFY_API_KEY=app-your-dify-key-here
DATABASE_URL=sqlite:///openclaw_assistant.db
DEFAULT_FREE_QUOTA=20
EOF

# 3. 启动
uvicorn app.main:app --reload --port 8000

# 4. 打开浏览器访问 http://localhost:8000/web/
#    注册账号 → 登录 → 发送消息（需要有效的 Dify API Key 才能收到回复）
```

**不配 Dify API Key 也能测试**：注册、登录、UI 加载、quota 查询都能正常工作，只有发送消息会返回 Dify 连接错误。

### 运行测试

```bash
pip install -r requirements.txt -r requirements-test.txt
python3 -m pytest tests/ -v
```

所有 58 个测试均不依赖外部服务（Dify/微信 API 已 mock）。

### 微信小程序

1. 打开微信开发者工具
2. 导入 `miniprogram/` 目录
3. 修改 `app.js` 中的 `baseUrl` 为你的后端地址
4. 修改 `project.config.json` 中的 `appid` 为你的小程序 AppID

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/login` | 微信登录 |
| POST | `/api/web/register` | Web 用户注册（用户名+密码） |
| POST | `/api/web/login` | Web 用户登录 |
| POST | `/api/chat` | 发送消息（SSE 流式返回） |
| GET | `/api/conversation/latest` | 获取最近对话记录 |
| GET | `/api/quota` | 查询剩余对话次数 |
| GET | `/api/health` | 健康检查 |
| GET | `/web/` | Web 前端（静态文件） |

## 配置 Dify

1. 注册 [Dify Cloud](https://cloud.dify.ai)
2. 创建应用 → 选择"聊天助手"
3. 上传 `docs/` 目录下的知识库文档
4. 配置 System Prompt 和 LLM 模型（推荐 Qwen）
5. 获取 API Key 填入 `.env`

## License

MIT
