#!/bin/bash

# 1. 加载系统 ROS2 Humble 环境
source /opt/ros/humble/setup.bash

# 2. 加载项目本地编译环境
if [ -f "install/setup.bash" ]; then
    source install/setup.bash
else
    echo "错误: 未找到 install/setup.bash，请先运行 colcon build"
    exit 1
fi

# 3. 启动仿真
ros2 launch charge_port simulation.launch.py