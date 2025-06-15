# IPC (网络摄像机) 图像捕获工具

一个使用RTSP协议从网络摄像机捕获单帧图像的简单工具。

## 功能特性

- 通过RTSP连接到网络摄像机。
- 捕获单帧图像并将其保存为图片文件。
- 通过 `config.json` 文件配置摄像机参数。
- 记录应用程序事件日志。
- 对关键操作进行性能监控。
- 为核心模块打包了单元测试。

## 安装与使用

本项目使用虚拟环境来管理依赖关系，以避免与系统范围的软件包发生冲突。

1.  **创建并激活虚拟环境：**
    ```bash
    # 创建虚拟环境
    python -m venv venv

    # 激活环境 (在 Windows 上)
    .\\venv\\Scripts\\activate
    ```
    *对于 MacOS/Linux, 请使用 `source venv/bin/activate`.*

2.  **安装依赖：**
    激活虚拟环境后，安装所需的软件包。
    ```bash
    pip install -r requirements.txt
    ```
    *如果下载速度慢，您可以使用国内镜像源：*
    ```bash
    pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
    ```

3.  **配置摄像机：**
    - 编辑 `config.json` 文件，填入您摄像机的IP地址、凭据、`rtsp_path` 和一个唯一的 `camera_id`。

4.  **运行应用程序：**
    ```bash
    python main.py
    ```

捕获的图像将保存在 `output` 目录中，并以时间戳和摄像机ID命名。

## 项目结构
```
.
├── .gitignore
├── config.json
├── main.py
├── requirements.txt
├── README.md
├── venv/
├── @Docs/
│   ├── ARCH-技术架构设计.md
│   ├── REQ-华夏V83-CV100摄像机图片捕获工具.md
│   └── TASK-任务执行清单.md
├── docs
│   └── data_flow.md
├── src
│   ├── __init__.py
│   ├── camera
│   │   ├── __init__.py
│   │   └── rtsp_client.py
│   ├── config
│   │   ├── __init__.py
│   │   └── config_manager.py
│   ├── core
│   │   ├── __init__.py
│   │   └── state_machine.py
│   ├── models
│   │   ├── __init__.py
│   │   └── camera_models.py
│   └── utils
│       ├── __init__.py
│       ├── image_processor.py
│       ├── logger.py
│       └── monitor.py
└── tests
    ├── __init__.py
    ├── test_config.py
    ├── test_image_processor.py
    └── test_rtsp_client.py
```