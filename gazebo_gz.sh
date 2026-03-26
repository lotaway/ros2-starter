#!/bin/bash

# 1. 加载 mamba 环境中 ROS2 Humble
source ~/miniforge3/etc/profile.d/conda.sh
conda activate ros2_humble

# 2. 设置 XQuartz 显示
export DISPLAY=:0

# 3. 加载项目本地编译环境
if [ -f "install/setup.bash" ]; then
    source install/setup.bash
else
    echo "错误: 未找到 install/setup.bash，请先运行 colcon build"
    exit 1
fi

# 4. 启动新版本 Gazebo 仿真 (ros_gz_sim)
ros2 launch charge_port simulation_gz.launch.py
