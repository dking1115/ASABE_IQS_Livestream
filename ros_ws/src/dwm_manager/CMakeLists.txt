cmake_minimum_required(VERSION 3.5)
project(dwm_manager)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)

# Build the executable
add_executable(dwm_manager src/dwm_manager.cpp)

# Link against ROS libraries
ament_target_dependencies(dwm_manager rclcpp geometry_msgs tf2_ros)

# Install the executable
install(TARGETS
  dwm_manager
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
