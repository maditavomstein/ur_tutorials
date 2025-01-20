#from launch_ros.actions import Node
#from launch_ros.parameter_descriptions import ParameterFile
#ParameterFile unused, remove? / ParameterValue also not needed?
from launch_ros.substitutions import FindPackageShare

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
#OpaqueFunction for userdefined python logic within the launch file - not needed
from launch.launch_description_sources import PythonLaunchDescriptionSource
#from launch.conditions import IfCondition
from launch.substitutions import (
#    Command,
#    FindExecutable,
    LaunchConfiguration, #This substitution retrieves the value of a launch configuration parameter.
    PathJoinSubstitution, #This substitution joins multiple path components into a single path.
)
#removed TextSubstitution since not available in Humble and not even used in this script?


def generate_launch_description():
    #ur_type = LaunchConfiguration("ur_type")
    #robot_ip = LaunchConfiguration("robot_ip")
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument(
            "ur_type",
            description="Type/series of used UR robot.",
            choices=[
                "ur3",
                "ur3e",
                "ur5",
                "ur5e",
                "ur10",
                "ur10e",
                "ur16e",
                "ur20",
                "ur30",
            ],
            default_value="ur20",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "robot_ip",
            default_value="192.168.56.101",  # put your robot's IP address here
            description="IP address by which the robot can be reached.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument("launch_rviz", default_value="true", description="Launch RViz?")
    )

    ################################################################
    declared_arguments.append(
        DeclareLaunchArgument(
            "use_fake_hardware",
            default_value="false",
            description="Start robot with fake hardware mirroring command to its states.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "fake_sensor_commands",
            default_value="false",
            description="Enable fake command interfaces for sensors used for simple simulations. "
            "Used only if 'use_fake_hardware' parameter is true.",
        )
    )

    #Initialize Arguments
    ur_type = LaunchConfiguration("ur_type")
    robot_ip = LaunchConfiguration("robot_ip")
    launch_rviz = LaunchConfiguration("launch_rviz")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")


    return LaunchDescription(
        declared_arguments
        + [
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [
                        PathJoinSubstitution(
                            [
                                FindPackageShare("ur_robot_driver"),
                                "launch",
                                "ur_control.launch.py",
                            ]
                        )
                    ]
                ),
                launch_arguments={
                    "ur_type": ur_type,
                    "robot_ip": robot_ip,
                    "tf_prefix": [LaunchConfiguration("ur_type"), "_"],
                    "runtime_config_package": "my_robot_cell_control",
                    "controllers_file": "ros2_controllers.yaml",
                    "description_package": "my_robot_cell_control",
                    "description_file": "my_robot_cell_controlled.urdf.xacro",
                    "kinematics_params_file": PathJoinSubstitution(
                        [
                            FindPackageShare("my_robot_cell_control"),
                            "config",
                            "my_robot_calibration.yaml",
                        ]
                    ),
                    "launch_rviz": launch_rviz,
                    "use_fake_hardware": use_fake_hardware,
                    "fake_sensor_commands": fake_sensor_commands,
                }.items(),
            ),
        ]
    )
