 # /bin/bash
# colcon build with compile commands for VSCode IntelliSense
colcon build --symlink-install --cmake-args -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
