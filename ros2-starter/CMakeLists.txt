cmake_minimum_required(VERSION 3.8)
project(ros2-starter)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)

# ===== C++部分 =====
# 添加C++可执行文件
add_executable(cpp_talker src/cpp_talker.cpp)
ament_target_dependencies(cpp_talker rclcpp std_msgs)

# 安装C++可执行文件
install(TARGETS
  cpp_talker
  DESTINATION lib/${PROJECT_NAME}
)

# ===== Python部分 =====
# 安装Python脚本
install(PROGRAMS
  scripts/py_listener.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()