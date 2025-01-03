# 在线人才招聘系统

该项目是一个在线人才招聘网站，采用前后端分离架构，前端使用 Vue3 和 Element Plus，后端使用 FastAPI 和 MySQL，系统包含普通用户、企业用户和管理员等功能模块。

## 目录结构

- `bend/`：后端代码目录
- `fend/`：前端代码目录
- `requirements.txt`：后端依赖包

## 环境要求

- Python 3
- Node.js (用于前端)
- MySQL (用于后端数据库)
- Nginx (用于项目部署)

## 1. 创建虚拟环境

首先在项目根目录中创建一个虚拟环境：

```bash
python3 -m venv .venv
```

## 2. 激活虚拟环境

- **macOS/Linux**:

  ```bash
  source .venv/bin/activate
  ```

- **Windows**:

  ```bash
  .venv\Scripts\activate
  ```

## 3. 运行后端

使用 Uvicorn 启动 FastAPI 后端服务：

```bash
uvicorn main:app --reload --port 5005
```

启动后，访问 `http://127.0.0.1:5005` 可以看到 API 服务在运行。

## 4. 安装前端依赖

确保已经安装了 `npm`，然后进入 `fend/` 目录并安装前端依赖：

```bash
cd fend/
npm install
```

## 5. 运行前端

使用以下命令启动前端开发服务器：

```bash
npm run dev
```

启动后，访问 `http://localhost:5137` 即可看到前端界面。

## 项目结构

```
├── bend/
│   ├── main.py          # FastAPI 后端应用入口
│   ├── requirements.txt # 后端依赖
│   └── ...
└── fend/
    ├── src/             # 前端源码
    ├── package.json     # 前端依赖
    └── ...
```

## 贡献

欢迎提交问题、拉取请求 (PR)，一起改善这个项目！

## License

此项目采用 [MIT License](LICENSE) 许可证。
