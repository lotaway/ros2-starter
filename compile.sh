 # /bin/bash
# colcon build with compile commands for VSCode IntelliSense
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
# colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON -DCMAKE_BUILD_TYPE=Debug
# colcon build --packages-up-to ros2-starter --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON