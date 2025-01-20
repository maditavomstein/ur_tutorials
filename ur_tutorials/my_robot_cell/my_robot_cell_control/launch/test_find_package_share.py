from launch_ros.substitutions import FindPackageShare
from launch import LaunchContext

context = LaunchContext()
substitution = FindPackageShare("my_robot_cell_control")
print(substitution.perform(context))
