cmake_minimum_required(VERSION 3.8)
project(my_robot_cell_control)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
#find_package(controller_manager REQUIRED) brauche ich das vllt?
#find_package(robot_state_publisher REQUIRED) brauche ich das vllt?


install(
  DIRECTORY launch config urdf rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
