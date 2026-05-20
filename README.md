# Translate Agent - 智能翻译助手

基于 FastAPI 和 LangChain 构建的智能翻译系统，支持 EPUB/TXT 文档上传、句子级翻译和 AI 评分功能。

## 📋 项目简介

Translate Agent 是一个功能强大的翻译辅助工具，能够：
- 上传 EPUB 或 TXT 格式的文章
- 自动将文章拆分为句子
- 使用 DeepSeek AI 模型进行高质量翻译
- 对用户翻译进行 AI 评分和点评
- 提供完整的 RESTful API 接口

## ✨ 主要特性

- **文档处理**：支持 EPUB 和 TXT 文件格式，自动提取文本并智能分句
- **AI 翻译**：集成 DeepSeek 大语言模型，提供上下文感知的句子翻译
- **翻译评审**：AI 对用户翻译进行评分（0-100）并提供专业点评
- **多语言支持**：支持英语、德语、西班牙语、法语、意大利语、日语、荷兰语、波兰语、俄语等多种语言
- **数据持久化**：使用 MySQL 数据库存储文章、句子和翻译结果
- **RESTful API**：提供完整的 API 接口，方便集成和扩展
- **Docker 部署**：支持 Docker 和 Docker Compose 一键部署

## 🛠️ 技术栈

### 后端框架
- **FastAPI** (>=0.111.0) - 高性能异步 Web 框架
- **Uvicorn** (>=0.30.0) - ASGI 服务器

### AI & LangChain
- **LangChain** (1.2.13) - LLM 应用开发框架
- **LangChain-Core** (1.2.23)
- **LangChain-Community** (0.4.1)
- **LangChain-OpenAI** (>=1.0.0)
- **DeepSeek API** - 大语言模型服务

### 数据库
- **SQLAlchemy** (>=2.0.0) - ORM 框架
- **PyMySQL** (>=1.1.0) - MySQL 驱动
- **MySQL 5.7** - 关系型数据库

### 文档处理
- **EbookLib** (>=0.20) - EPUB 文件处理
- **BeautifulSoup4** (>=4.14.0) - HTML/XML 解析
- **lxml** (>=6.0.0) - XML/HTML 处理
- **pySBD** (>=0.3.4) - 句子分割工具

### 其他依赖
- **python-dotenv** (1.0.0) - 环境变量管理
- **python-multipart** (>=0.0.9) - 文件上传支持
- **charset-normalizer** (>=3.0.0) - 字符编码检测
- **requests** (>=2.32.0) - HTTP 客户端

## 📦 安装与部署

### 前置要求

- Python 3.11+
- MySQL 5.7+
- Docker & Docker Compose（可选，用于容器化部署）
- DeepSeek API Key

### 方式一：本地部署

#### 1. 克隆项目

