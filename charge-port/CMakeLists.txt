cmake_minimum_required(VERSION 3.10)
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
# C++ Hardware Node
add_executable(hardware_node 
  src/hardware_node.cpp
  src/utils.cpp
)

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
  scripts/arm_test_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install config and other files
install(DIRECTORY config dataset launch urdf worlds models
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()

  # C++ Unit Tests
  find_package(ament_cmake_gtest REQUIRED)
  ament_add_gtest(test_utils test/test_utils.cpp)
  target_include_directories(test_utils PUBLIC include)
  target_sources(test_utils PRIVATE src/utils.cpp)

  # Python Unit Tests
  find_package(ament_cmake_pytest REQUIRED)
  ament_add_pytest_test(test_detection test/test_detection.py)

  # Integration Tests
  # Note: launch_testing usually uses pytest as runner
  ament_add_pytest_test(test_integration test/test_integration.py
    APPEND_LIBRARY_DIRS "${CMAKE_CURRENT_BINARY_DIR}"
  )
endif()

ament_package()
