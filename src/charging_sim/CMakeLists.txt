cmake_minimum_required(VERSION 3.8)
project(charging_sim)

# Find dependencies
find_package(ament_cmake REQUIRED)

# Install directories
install(DIRECTORY worlds launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
