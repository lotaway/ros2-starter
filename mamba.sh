# 1. Detect OS and set Python version accordingly
OS_TYPE=$(uname)
if [ "$OS_TYPE" == "Darwin" ]; then
    echo "Detected macOS (ARM64). Using Python 3.11 for compatibility with Robostack Gazebo plugins."
    PYTHON_VERSION="3.11"
    CHANNELS="-c conda-forge -c robostack-staging"
else
    echo "Detected Linux/WSL/Windows. Using standard Python 3.10."
    PYTHON_VERSION="3.10"
    CHANNELS="-c conda-forge -c robostack-humble"
fi

# 2. Clear existing environment to ensure a clean slate
mamba env remove -n ros2_humble -y

# 3. Recreate environment
# Using --override-channels to ensure we only use the specified ROS-compatible channels
mamba create -n ros2_humble python=$PYTHON_VERSION -y --override-channels -c conda-forge -c robostack-staging

# 4. Initialize shell for mamba
eval "$(conda shell.bash hook)"
mamba activate ros2_humble

# 5. Configure environment-specific channel priority
conda config --env --add channels conda-forge
conda config --env --add channels robostack-staging
conda config --env --set channel_priority strict

# 6. Install ROS2 Humble and essential tools
# We use the detected $PYTHON_VERSION and avoid 'compilers' to prevent zlib conflicts
mamba install -y --override-channels -c robostack-staging -c conda-forge \
  python=$PYTHON_VERSION \
  ros-humble-desktop-full \
  cmake pkg-config make ninja \
  colcon-common-extensions catkin_tools rosdep \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-xacro \
  ros-humble-cv-bridge \
  ros-humble-image-transport

# 7. Check installation
ros2 pkg list | grep gazebo_ros

# 8. Install project dependencies via pip
pip install -r charge-port/requirements.txt

echo "Setup complete. Currently using Python $PYTHON_VERSION."
echo "To use the environment: mamba activate ros2_humble"