# 🌐 Distributed File Storage System

一个简洁高效的分布式文件存储系统，支持文件切块、多节点冗余存储、容错恢复与客户端上传下载接口。该项目采用 Python + FastAPI + MySQL + Docker，结合分布式系统设计理念，适合系统学习、项目展示与工程实践。

---
部署流程

- pip install -r requirements.txt #安装依赖

- docker-compose up -d #将docker-compose.yml在docker中进行部署容器的操作

- 或者直接拉取 MySQL 镜像并运行容器
docker run -d \
  --name dfs-mysql \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=test0 \
  -p 3306:3306 \
  mysql:8.0

docker exec -it dfs-mysql \
  mysql -uroot -p123456 test0 < docs/schema.sql  #创建项目所需表


- uvicorn metadata_server.app:app --reload #启动本地服务节点

- python3 -m storage_nodes.node 9001 #(默认是启动9001端口，其他端口同理)

- python3 -m storage_nodes.node 9002 #启动多个存储节点（按需执行）

‘’‘

- python3 -m client.cli upload tests/test.txt #上传test.txt文件,不同的chunk都会保存在./data文件夹下

- python3 -m client.cli download tests/storage_data/download_data.txt --file_id 1 #get属于file_id = 1 的chunk部分并合并为一个txt文件

## 🧭 项目背景

本项目旨在模拟一个简化版的分布式文件系统，实现文件上传、分块存储、多副本冗余、元数据管理和存储节点管理等核心功能，重点在于架构设计、模块化实现和系统性训练。

---

## ✨ 核心功能

- ✅ 大文件上传与自动切块（支持自定义大小）
- ✅ 元数据服务（文件信息、块分布、节点管理）
- ✅ 分块多副本冗余（可自定义副本数）
- ✅ 客户端 CLI 工具（上传、下载、查询状态）
- ✅ 存储节点模拟（多节点可水平扩展）
- ✅ 节点心跳检测与容错恢复
- ✅ 控制器自动调度块的分配与副本修复
- ✅ Docker Compose 一键部署（支持本地集群模拟）

---

## 🛠️ 技术栈

| 组件             | 技术方案                     |
|------------------|------------------------------|
| 后端框架         | FastAPI (Python 3.10)        |
| 数据持久化       | MySQL 8.0                    |
| 存储节点         | Python + Flask (可扩展为 C++)|
| 文件客户端       | Python CLI + requests        |
| 分布式调度器     | Python 控制模块              |
| 节点部署         | Docker + Docker Compose      |
| 测试工具         | pytest + httpx               |

---

## 🧱 项目架构图

            +---------------------+
            |     Client CLI      |
            +----------+----------+
                       |
                 Upload/Download
                       |
                +------v------+
                | Metadata API |
                +------+-------+
                       |
       +---------------+----------------+
       |                                |
+------v------+                  +------v------+
|  Scheduler  |  ------->        |   MySQL DB   |
+------+------+\                 +-------------+
       |       \______
       |               \
+----------v---------+ +---v-------------------+
| Storage Node A | | Storage Node B ... |
+--------------------+ +-----------------------+


---

## 📁 项目结构说明

```bash
DistributedFileSystem/
├── client/               # 客户端：切块上传、下载、命令行接口
├── metadata_server/      # FastAPI 服务：文件元信息、节点注册
├── storage_nodes/        # 模拟存储节点（支持动态添加）
├── controller/           # 调度器：块副本分配与恢复
├── common/               # 工具方法（hash、切块、配置）
├── tests/                # 单元测试、接口测试
├── docs/                 # 架构图、接口文档、设计说明
├── docker-compose.yml    # 一键部署多个组件
├── requirements.txt      # Python 依赖
├── README.md             # 项目说明
└── .env                  # 环境变量（MySQL 配置等）

DistributedFileSystem/
├── client/                           # 客户端上传文件的模块
│   ├── cli.py                        # 客户端命令行入口
│   └── client_api.py                # 客户端逻辑：切块、上传、与元数据服务交互
│
├── metadata_server/                 # 元数据服务
│   ├── app.py                        # FastAPI 主程序入口
│   ├── db.py                         # 数据库连接（SQLAlchemy）
│   ├── models.py                     # ORM 模型
│   └── routes/                       # 路由模块
│       ├── __init__.py
│       ├── file.py                  # 文件相关路由：注册文件、查询元数据
│       └── node.py                  # 存储节点注册、心跳等
│
├── storage_nodes/                   # 存储节点模拟服务
│   ├── node.py                      # FastAPI 接收文件块
│   └── data/                        # 模拟存储位置（块文件会保存在这里）
│
├── common/                          # 公共代码模块
│   └── utils.py                     # 工具函数，如文件校验和、时间戳等
│
├── controller/                      # 计划中的调度模块（Week 2 开始开发）
│   └── scheduler.py                 # 节点调度、负载均衡逻辑
│
├── tests/                           # 测试模块
│   └── test_register.py             # 测试元数据注册和接口交互
│
├── docs/                            # 文档与设计
│   ├── schema.sql                   # MySQL 表结构定义
│   ├── week2_summary.md             # 第 2 周总结文档
│   ├── week1_summary.md             # 第 1 周总结文档
│   └── architecture.drawio          # 架构图（你可以用 Draw.io 或 Markdown 画）
│
├── requirements.txt                 # Python 依赖包列表
├── README.md                        # 项目说明文件
└── .gitignore                       # 忽略文件配置
