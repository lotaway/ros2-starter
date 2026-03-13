cmake_minimum_required(VERSION 3.10)
project(ros2-starter)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(action_tutorials_interfaces REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_components REQUIRED)

# Include directory for this package
include_directories(include)

# ===== C++ Topic 部分 =====
add_executable(cpp_talker src/cpp_talker.cpp)
ament_target_dependencies(cpp_talker rclcpp std_msgs)

# ===== C++ Service 部分 =====
add_executable(cpp_add_two_ints_server src/cpp_add_two_ints_server.cpp)
ament_target_dependencies(cpp_add_two_ints_server rclcpp example_interfaces)

add_executable(cpp_add_two_ints_client src/cpp_add_two_ints_client.cpp)
ament_target_dependencies(cpp_add_two_ints_client rclcpp example_interfaces)

# ===== C++ Action 部分 =====
add_executable(cpp_fibonacci_action_server src/cpp_fibonacci_action_server.cpp)
ament_target_dependencies(cpp_fibonacci_action_server rclcpp rclcpp_action rclcpp_components action_tutorials_interfaces)

add_executable(cpp_fibonacci_action_client src/cpp_fibonacci_action_client.cpp)
ament_target_dependencies(cpp_fibonacci_action_client rclcpp rclcpp_action rclcpp_components action_tutorials_interfaces)

# 安装 C++ 可执行文件
install(TARGETS
  cpp_talker
  cpp_add_two_ints_server
  cpp_add_two_ints_client
  cpp_fibonacci_action_server
  cpp_fibonacci_action_client
  DESTINATION lib/${PROJECT_NAME}
)

# ===== Python 部分 =====
# 安装 Python 脚本
install(PROGRAMS
  scripts/py_listener.py
  scripts/py_add_two_ints_client.py
  scripts/py_fibonacci_action_client.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
