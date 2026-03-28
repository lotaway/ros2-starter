import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    ExecuteProcess,
    IncludeLaunchDescription,
    RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    pkg_description_path = get_package_share_directory("charging_robot_description")
    pkg_sim_path = get_package_share_directory("charging_sim")

    # Process Xacro
    xacro_file = os.path.join(pkg_description_path, "urdf", "charging_robot_gz.urdf.xacro")
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()

    # World file
    world_file = os.path.join(pkg_sim_path, "worlds", "parking_lot_gz.world")

    # 1. Gazebo (新版本 ros_gz_sim)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [
                os.path.join(
                    get_package_share_directory("ros_gz_sim"),
                    "launch",
                    "gz_sim.launch.py",
                )
            ]
        ),
        launch_arguments={
            "gz_args": ["-r -v4 ", world_file],
            "on_exit_shutdown": "true",
        }.items(),
    )

    # 2. Robot State Publisher
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        name="robot_state_publisher",
        output="screen",
        parameters=[{"robot_description": robot_desc}],
    )

    # 3. Spawn Robot (新版本 ros_gz_sim create)
    spawn_robot = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=[
            "-name",
            "charging_robot",
            "-topic",
            "robot_description",
            "-z",
            "0.0",
        ],
        output="screen",
    )

    # 4. Set Gazebo resource path
    set_env_vars = AppendEnvironmentVariable(
        "GZ_SIM_RESOURCE_PATH", os.path.join(pkg_description_path, "models")
    )

    # 5. Joint State Broadcaster
    load_joint_state_broadcaster = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "joint_state_broadcaster",
        ],
        output="screen",
    )

    # 6. Arm Controller
    load_arm_controller = ExecuteProcess(
        cmd=[
            "ros2",
            "control",
            "load_controller",
            "--set-state",
            "active",
            "arm_controller",
        ],
        output="screen",
    )

    return LaunchDescription(
        [
            set_env_vars,
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=spawn_robot,
                    on_exit=[load_joint_state_broadcaster],
                )
            ),
            RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=load_joint_state_broadcaster,
                    on_exit=[load_arm_controller],
                )
            ),
            gazebo,
            robot_state_publisher,
            spawn_robot,
        ]
    )
