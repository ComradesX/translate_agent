# Translate Agent

Translate Agent 是一个面向文章精读和句子级翻译练习的智能翻译助手。项目基于 FastAPI、LangChain 和 DeepSeek API 构建，支持上传 EPUB/TXT 文档，自动切分句子，按上下文生成 AI 翻译，并对用户翻译进行评分和点评。

## 项目介绍

项目主要功能：

- 上传 EPUB 或 TXT 文章，并将文章内容保存到 MySQL。
- 自动按语言切分文章句子，支持句子列表分页浏览。
- 在前端按句子进行翻译练习，显示当前句子的上下文。
- 使用 DeepSeek 模型生成句子级 AI 翻译。
- 提交用户翻译后，由 AI 给出评分和点评。
- 保存 AI 翻译、用户翻译历史和点评结果。
- 提供 FastAPI REST 接口，并内置一个轻量 Web 前端。

主要目录：

```text
.
├── main.py                         # FastAPI 应用入口
├── src/controllers                 # API 控制器
├── src/models                      # SQLAlchemy 数据模型
├── src/chain                       # LangChain 翻译与点评链
├── src/prompts                     # 翻译和点评提示词
├── src/resource/web                # 前端页面资源
├── db_file/translate_agent.sql     # 数据库初始化 SQL
├── docker-compose.yml              # Docker Compose 部署配置
├── Dockerfile                      # 应用镜像构建文件
└── requirements.txt                # Python 依赖
```

## 依赖要求

本地运行需要：

- Python 3.11+
- MySQL 5.7+ 或兼容版本
- DeepSeek API Key
- 可选：Docker 和 Docker Compose，用于容器化部署

Python 主要依赖：

- FastAPI / Uvicorn：Web 服务
- SQLAlchemy / PyMySQL：数据库访问
- LangChain / LangChain OpenAI：LLM 调用编排
- EbookLib / BeautifulSoup4 / lxml：EPUB 文本提取
- pySBD：文章分句
- python-dotenv：读取 `.env` 配置

安装依赖：

```bash
pip install -r requirements.txt
```

## 配置要求

项目通过 `.env` 文件读取配置。可以从示例文件复制：

```bash
cp .env.example .env
```

常用配置项：

```env
APP_ENV=local
APP_PORT=8890

DEEPSEEK_API_KEY=sk-
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_BASE_MODEL=deepseek-v4-flash
DEEPSEEK_BASE_MODEL_PRO=deepseek-v4-pro

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_ROOT_PASSWORD=root_pwd
MYSQL_DATABASE=translate_agent
MYSQL_USER=root
MYSQL_PASSWORD=root_pwd
MYSQL_CHARSET=utf8mb4
MYSQL_POOL_SIZE=10
MYSQL_MAX_OVERFLOW=20
MYSQL_POOL_TIMEOUT=30
MYSQL_POOL_RECYCLE=3600
```

配置说明：

- `APP_PORT`：应用 HTTP 端口，默认 `8890`。
- `DEEPSEEK_API_KEY`：DeepSeek API Key，必须配置。
- `DEEPSEEK_BASE_URL`：DeepSeek API 地址。
- `DEEPSEEK_BASE_MODEL`：普通翻译使用的模型。
- `DEEPSEEK_BASE_MODEL_PRO`：翻译点评使用的模型。
- `MYSQL_HOST` / `MYSQL_PORT`：MySQL 地址和端口。本地 Docker Compose 默认把 MySQL 映射到宿主机 `3307`。
- `MYSQL_DATABASE`：数据库名，默认 `translate_agent`。
- `MYSQL_USER` / `MYSQL_PASSWORD`：数据库账号和密码。

首次运行前需要初始化数据库表结构和示例数据：

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p translate_agent < db_file/translate_agent.sql
```

如果使用的是非 Docker MySQL，请把命令中的主机、端口、账号和数据库名替换为你的实际配置。

## 部署方式

### 方式一：本地运行

1. 创建并激活虚拟环境：

```bash
python -m venv .venv
source .venv/bin/activate
```

2. 安装依赖：

```bash
pip install -r requirements.txt
```

3. 准备 `.env`：

```bash
cp .env.example .env
```

编辑 `.env`，填入 `DEEPSEEK_API_KEY` 和 MySQL 配置。

4. 准备数据库：

```bash
mysql -h 127.0.0.1 -P 3307 -u root -p -e "CREATE DATABASE IF NOT EXISTS translate_agent DEFAULT CHARSET utf8mb4;"
mysql -h 127.0.0.1 -P 3307 -u root -p translate_agent < db_file/translate_agent.sql
```

5. 启动服务：

```bash
uvicorn main:app --host 127.0.0.1 --port 8890 --reload
```

访问地址：

- Web 前端：http://127.0.0.1:8890/web/
- API 文档：http://127.0.0.1:8890/docs

### 方式二：Docker Compose 部署

1. 准备 `.env`：

```bash
cp .env.example .env
```

至少需要填写 `DEEPSEEK_API_KEY`。Docker Compose 会启动 MySQL 和应用服务，应用容器内部会使用 `MYSQL_HOST=mysql`、`MYSQL_PORT=3306` 连接数据库。

2. 启动服务：

```bash
docker compose up -d --build
```

3. 初始化数据库：

```bash
docker exec -i translate_agent_mysql mysql -u root -proot_pwd translate_agent < db_file/translate_agent.sql
```

如果你在 `.env` 中修改了 `MYSQL_ROOT_PASSWORD` 或 `MYSQL_DATABASE`，请同步修改上面的命令。

4. 查看服务状态：

```bash
docker compose ps
docker compose logs -f app
```

5. 访问服务：

- Web 前端：http://127.0.0.1:8890/web/
- API 文档：http://127.0.0.1:8890/docs

停止服务：

```bash
docker compose down
```

如需同时删除 MySQL 容器数据，请删除 `volumes/container_data/mysql` 目录后重新启动。

## 常用接口

- `GET /articles`：查询文章列表
- `POST /articles/upload-epub`：上传 EPUB/TXT 并切分句子
- `GET /article-sentences`：查询文章句子
- `POST /translations/llm`：生成 AI 翻译
- `POST /translations/review`：提交用户翻译并生成 AI 点评
- `GET /llm-sentence-translations`：查询 AI 翻译记录
- `GET /user-sentence-translations`：查询用户翻译记录

