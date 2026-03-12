# 1. Remove existing environment and recreate
# mamba env remove -n ros2_humble -y
mamba create -n ros2_humble python=3.10 -y

# 2. Initialize shell for mamba (required to use 'mamba activate' in script)
eval "$(conda shell.bash hook)"
mamba activate ros2_humble

# 3. Install ROS2 Hubble Desktop Full and Gazebo plugins
mamba install -y -c conda-forge -c robostack-humble \
  ros-humble-desktop-full \
  compilers cmake pkg-config make ninja \
  colcon-common-extensions catkin_tools rosdep \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-xacro

# 4. Check gazebo install success or not
ros2 pkg list | grep gazebo_ros

# Install project dependencies
pip install -r charge-port/requirements.txt

# Terminal 1: run talker
mamba activate ros2_humble
ros2 run demo_nodes_cpp talker

# Terminal 2: run listener
mamba activate ros2_humble
ros2 run demo_nodes_py listener
