cmake_minimum_required(VERSION 3.8)
project(charging_robot_description)

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install directories
install(DIRECTORY urdf config models
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
