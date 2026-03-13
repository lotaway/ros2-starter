# 1. Detect OS and set Python version accordingly
OS_TYPE=$(uname)
if [ "$OS_TYPE" == "Darwin" ]; then
    echo "Detected macOS (ARM64). Using Python 3.11 for compatibility with Robostack Gazebo plugins."
    PYTHON_VERSION="3.11"
else
    echo "Detected Linux/WSL/Windows. Using standard Python 3.10."
    PYTHON_VERSION="3.10"
fi

ENV_NAME="ros2_humble"

# 2. Clear existing environment to ensure a clean slate
echo "Removing existing environment $ENV_NAME..."
mamba env remove -n $ENV_NAME -y

# 3. Create environment
# We install python immediately to ensure the environment is valid
echo "Creating environment $ENV_NAME with python=$PYTHON_VERSION..."
mamba create -n $ENV_NAME python=$PYTHON_VERSION -y --override-channels -c conda-forge -c robostack-staging

# 4. Configure environment-specific channels (using -n to be safe)
echo "Configuring channels for $ENV_NAME..."
conda config --env --set channel_priority strict -n $ENV_NAME
conda config --env --add channels conda-forge -n $ENV_NAME
conda config --env --add channels robostack-staging -n $ENV_NAME

# 5. Install ROS2 Humble and essential tools
# CRITICAL: Use '-n $ENV_NAME' to avoid accidental installation into 'base'
echo "Installing ROS2 packages into $ENV_NAME..."
mamba install -y -n $ENV_NAME --override-channels -c robostack-staging -c conda-forge \
  ros-humble-desktop-full \
  cmake pkg-config make ninja \
  colcon-common-extensions catkin_tools rosdep \
  ros-humble-gazebo-ros-pkgs \
  ros-humble-gazebo-ros2-control \
  ros-humble-xacro \
  ros-humble-cv-bridge \
  ros-humble-image-transport

# 6. Check installation using mamba run
echo "Verifying installation..."
mamba run -n $ENV_NAME ros2 pkg list | grep gazebo_ros

# 7. Install project dependencies via pip using mamba run
# This ensures pip uses the python interpreter INSIDE the environment
echo "Installing pip requirements into $ENV_NAME..."
mamba run -n $ENV_NAME pip install -r charge-port/requirements.txt

echo "----------------------------------------------------------------"
echo "Setup complete. Environment '$ENV_NAME' is ready."
echo "To activate it manually in your shell, use:"
echo "  mamba activate $ENV_NAME"
echo "If that fails, use the direct source method:"
echo "  source $(conda info --base)/etc/profile.d/conda.sh && conda activate $ENV_NAME"
echo "----------------------------------------------------------------"