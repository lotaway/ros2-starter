import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    pkg_sim = get_package_share_directory('charging_sim')
    pkg_perception = get_package_share_directory('charging_perception')
    pkg_behavior = get_package_share_directory('charging_behavior')
    pkg_bringup = get_package_share_directory('charging_bringup')

    use_sim = LaunchConfiguration('use_sim', default='true')

    return LaunchDescription([
        DeclareLaunchArgument('use_sim', default='true', description='Launch Gazebo simulation'),
        # 1. 启动仿真
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(pkg_sim, 'launch', 'simulation.launch.py'))
        ),
        # 2. 启动感知模块
        Node(package='charging_perception', executable='detection_node', name='detection_node', output='screen'),
        # 3. 启动行为管理 (任务中心)
        Node(package='charging_behavior', executable='task_manager', name='task_manager', output='screen'),
        # 4. 启动硬件驱动 (或者作为 HAL 使用)
        Node(
            package='charging_bringup', 
            executable='hardware_node', 
            name='hardware_node',
            output='screen', 
            parameters=[{'use_simulation': use_sim}]
        )
    ])
