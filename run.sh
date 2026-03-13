eval "$(conda shell.bash hook)"
mamba activate ros2_humble

# Terminal 1: run talker
mamba activate ros2_humble
ros2 run demo_nodes_cpp talker

# Terminal 2: run listener
mamba activate ros2_humble
ros2 run demo_nodes_py listener