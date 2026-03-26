#!/bin/bash
# install_dependencies.sh - 补充镜像缺失的仿真和控制核心组件

set -e

echo "正在同步仿真依赖环境..."
sudo apt update

# 安装经检测确认缺失的 ROS 2 仿真及控制插件包
sudo apt install -y \
    ros-humble-gazebo-ros-pkgs \
    ros-humble-gazebo-ros2-control \
    ros-humble-ros2-control \
    ros-humble-ros2-controllers \
    gdb \
    python3-pip
    
echo "------------------------------------"
echo "依赖环境同步完成。"

