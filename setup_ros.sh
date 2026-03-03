#!/bin/bash
# setup_ros.sh - 这个脚本只在第一次运行
if [ ! -f ~/.ros_configured ]; then
    echo "首次配置 ROS 环境..."
    echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
    if [ -f /root/ros2_ws/install/setup.bash ]; then
        echo 'source /root/ros2_ws/install/setup.bash' >> ~/.bashrc
    fi
    touch ~/.ros_configured
    echo "ROS 环境配置完成"
fi

# 当前会话也激活
source /opt/ros/humble/setup.bash
if [ -f /root/ros2_ws/install/setup.bash ]; then
    source /root/ros2_ws/install/setup.bash
fi

exec "$@"