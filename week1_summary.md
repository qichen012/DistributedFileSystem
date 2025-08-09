# 第一周总结 - 分布式文件存储系统项目

## 📅 周期
- 时间：第 1 周（Day 1 ~ Day 7）
- 技术栈：Python、FastAPI、Docker、MySQL

---

## ✅ 本周完成的任务

### 1. 开发环境搭建
- 在本地安装 Python 3.9+
- 安装并配置 **VS Code**
- 安装 **Docker Desktop**，用于创建 MySQL 容器
- 初始化 Git 仓库，方便后续版本管理

---

### 2. 项目初始化
- 创建项目文件夹结构：
DistributedFileSystem/
├── client/                           # 客户端上传文件的模块
│   └── client_api.py                # 客户端逻辑：切块、上传、与元数据服务交互
│
├── metadata_server/                 # 元数据服务
│   ├── app.py                        # FastAPI 主程序入口
│   ├── db.py                         # 数据库连接（SQLAlchemy）
│   ├── models.py                     # ORM 模型
│   └── routes/                       # 路由模块
│       ├── __init__.py
│       ├── file.py                  # 文件相关路由：注册文件、查询元数据
│       └── node.py                  # 存储节点注册
│
├── storage_nodes/                   # 存储节点模拟服务
│   ├── node.py                      # FastAPI 接收文件块
│   └── data/                        # 模拟存储位置（块文件会保存在这里）
│
├── docs/                            # 文档与设计
│   ├── schema.sql                   # MySQL 表结构定义
│   └── architecture.drawio          # 架构图（见README.md文件底部）
│
├── requirements.txt                 # Python 依赖包列表
├── README.md                        # 项目说明文件
└── .gitignore                       # 忽略文件配置
└── week1_summary.md                 # 第 1 周总结文档

- 使用 `pip install -r requirements.txt` 安装依赖

---

### 3. MySQL 数据库搭建（Docker 容器）
- 编写 `docker-compose.yml` 启动 MySQL 容器：
```yaml
version: "3.8"
services:
  mysql:
    image: mysql:8.0
    container_name: dfs-mysql
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: metadata
    ports:
      - "3306:3306"
    volumes:
      - ./mysql_data:/var/lib/mysql
      
---

启动数据库：
    docker-compose up -d

---

### 4. 元数据服务（Metadata Server）初步实现
- 使用 FastAPI 创建基础接口：
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Metadata Server is running"}

---

- 使用 Uvicorn 启动服务：
uvicorn metadata_server.app:app --reload