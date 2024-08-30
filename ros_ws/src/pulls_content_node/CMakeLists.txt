cmake_minimum_required(VERSION 3.5)
project(pulls_content_node)

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(iqs_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)

# Build the executable
add_executable(content_node src/content_node.cpp)

# Link against ROS libraries
ament_target_dependencies(content_node rclcpp geometry_msgs tf2_ros iqs_msgs sensor_msgs)

# Install the executable
install(TARGETS
  content_node
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
