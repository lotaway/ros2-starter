cmake_minimum_required(VERSION 3.8)
project(charging_bringup)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(image_transport REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(include)

# Executables
add_executable(hardware_node src/hardware_node.cpp src/utils.cpp)
ament_target_dependencies(hardware_node rclcpp std_msgs image_transport cv_bridge OpenCV)

# Install
install(TARGETS hardware_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
