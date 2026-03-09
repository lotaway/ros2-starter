cmake_minimum_required(VERSION 3.8)
project(charge_port)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Generate custom messages
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/ChargingStatus.msg"
  DEPENDENCIES sensor_msgs std_msgs
)

# C++ Include directories
include_directories(
  include
  ${OpenCV_INCLUDE_DIRS}
)

# C++ Hardware Node
add_executable(hardware_node src/hardware_node.cpp)
ament_target_dependencies(hardware_node
  rclcpp
  sensor_msgs
  std_msgs
  cv_bridge
  image_transport
)
target_link_libraries(hardware_node ${OpenCV_LIBRARIES})

# Install C++ targets
install(TARGETS
  hardware_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install Python scripts

install(PROGRAMS
  scripts/detection_node.py
  scripts/train_charging.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install config and other files
install(DIRECTORY config dataset
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
