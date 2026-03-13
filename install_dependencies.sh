#!/bin/bash
# install_dependencies.sh - 记录并安装项目所需的所有额外依赖环境

set -e

echo "正在更新包列表并安装核心依赖..."
sudo apt-get update

# 1. 确保核心仿真插件完整
# 虽然已在镜像中，但此处可作为强制更新和完整性检查
sudo apt-get install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-xacro \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers

# 2. 视觉与硬件通信依赖
sudo apt-get install -y \
    ros-humble-cv-bridge \
    ros-humble-image-transport \
    python3-opencv

# 3. 安装 Python 侧的检测库 (如果镜像没有)
pip3 install ultralytics

echo "------------------------------------"
echo "所有依赖安装完成！"
