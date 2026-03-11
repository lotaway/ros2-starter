# Create a conda environment named ros2_humble with Python 3.10 (recommended for Humble)
mamba create -n ros2_humble python=3.10
# Activate the environment
mamba activate ros2_humble

# Install full desktop version (includes rviz2, demo nodes, etc.) & build tools (for compiling packages)
mamba install -c conda-forge -c robostack-staging ros-humble-desktop-full compilers cmake pkg-config make ninja colcon-common-extensions catkin_tools rosdep

# Install project dependencies
pip install -r charge-port/requirements.txt

# Terminal 1: run talker
mamba activate ros2_humble
ros2 run demo_nodes_cpp talker

# Terminal 2: run listener
mamba activate ros2_humble
ros2 run demo_nodes_py listener
