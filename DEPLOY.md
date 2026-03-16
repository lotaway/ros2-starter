# 项目发布与 Docker 打包指南

本文档介绍如何将 `charge_port` 项目打包并部署到机器人平台。

## 1. 准备工作
确保你的代码已经通过仿真测试，且已安装 Docker 环境。

## 2. 打包镜像 (Build)
在开发机（你的电脑）执行，生成名为 `charge_bot` 的镜像：

```bash
docker build -f Dockerfile.release -t charge_bot:v1.0 .
```

## 3. 导出镜像 (Export)
由于机器人可能无法直接联网下载大镜像，建议导出为压缩包：

```bash
docker save charge_bot:v1.0 | gzip > charge_bot_v1.0.tar.gz
```

## 4. 在机器人上部署 (Deploy)

### 拷贝文件
使用 USB 或 `scp` 将 `charge_bot_v1.0.tar.gz` 拷贝到机器人。

### 加载镜像
```bash
docker load < charge_bot_v1.0.tar.gz
```

### 启动运行
机器人不需要安装任何 ROS 和 Python 环境，只需要有 Docker 即可：
```bash
docker run -it --rm --net=host --privileged charge_bot:v1.0
```

## 5. 注意事项
*   **硬件权限**：如果机器人上需要串口或 USB 摄像头，启动时必须带 `--privileged` 参数。
*   **跨平台**：如果你的电脑是 Intel 芯片，而机器人是 ARM（如树莓派/Jetson），打包时需要使用 `docker buildx build --platform linux/arm64`。
*   **模型文件**：生产镜像中默认不带大体积模型。建议将模型文件放在机器人本地，启动时通过 `-v /home/robot/models:/app/install/charge_port/share/charge_port/models` 挂载进去。
