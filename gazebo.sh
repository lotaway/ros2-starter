# /bin/bash

# Load ROS2 base environment

if [ -f "/opt/ros/humble/setup.bash" ]; then

    source /opt/ros/humble/setup.bash

fi



# Load local capture/install environment

if [ -f "install/setup.bash" ]; then

    source install/setup.bash

else

    echo "Error: install/setup.bash not found. Please run 'colcon build' first."

    exit 1

fi



# Launch simulation

ros2 launch charge_port simulation.launch.py