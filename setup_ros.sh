#!/bin/bash
# setup_ros.sh - 这个脚本只在第一次运行
if [ ! -f ~/.ros_configured ]; then
    echo "首次配置 ROS 环境..."
    
    # 在第一次初始化环境时，强制清理可能属于宿主机（Mac）的编译产物
    echo "正在清理可能存在的旧编译产物 (build, install, log)，防止路径冲突..."
    rm -rf /root/ros2_ws/build /root/ros2_ws/install /root/ros2_ws/log

    # 写入基础 ROS 环境到 bashrc
    echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
    
    # 写入动态判断项目编译环境的逻辑到 bashrc（因为此时 install 已经被删除了）
    echo 'if [ -f /root/ros2_ws/install/setup.bash ]; then' >> ~/.bashrc
    echo '    source /root/ros2_ws/install/setup.bash' >> ~/.bashrc
    echo 'fi' >> ~/.bashrc

    touch ~/.ros_configured
    echo "ROS 环境配置完成"
fi

# 当前会话也激活
source /opt/ros/humble/setup.bash
if [ -f /root/ros2_ws/install/setup.bash ]; then
    source /root/ros2_ws/install/setup.bash
fi

exec "$@"