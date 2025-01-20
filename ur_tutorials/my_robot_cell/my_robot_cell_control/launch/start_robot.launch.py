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
    # Declare arguments
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
    declared_arguments.append(
        DeclareLaunchArgument(
            "runtime_config_package",
            default_value="my_robot_cell_control",
            description="package in which .yaml are",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "controllers_file",
            default_value="ros2_controllers.yaml",
            description="name of controllers .yaml",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_package",
            default_value="my_robot_cell_control",
            description="description package",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "description_file",
            default_value="my_robot_cell_controlled.urdf.xacro",
            description="URDF/XACRO description file with the robot.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "kinematics_params_file",
            default_value=PathJoinSubstitution(
                [
                    FindPackageShare(LaunchConfiguration("runtime_config_package")),
                    "config",
                    "my_robot_calibration.yaml",
                ]
            ),
            description="The calibration configuration of the actual robot used.",
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "initial_joint_controller",
            default_value="scaled_joint_trajectory_controller",
            description="Initially loaded robot controller.",
            choices=[
                "scaled_joint_trajectory_controller",
                "joint_trajectory_controller",
                "forward_velocity_controller",
                "forward_position_controller",
            ],
        )
    )
    declared_arguments.append(
        DeclareLaunchArgument(
            "activate_joint_controller",
            default_value="true",
            description="Activate loaded joint controller.",
        )
    )

    #Initialize Arguments
    ur_type = LaunchConfiguration("ur_type")
    robot_ip = LaunchConfiguration("robot_ip")
    launch_rviz = LaunchConfiguration("launch_rviz")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    fake_sensor_commands = LaunchConfiguration("fake_sensor_commands")
    runtime_config_package = LaunchConfiguration("runtime_config_package")
    controllers_file = LaunchConfiguration("controllers_file")
    description_package = LaunchConfiguration("description_package")
    description_file = LaunchConfiguration("description_file")
    kinematics_params_file = LaunchConfiguration("kinematics_params_file")
    initial_joint_controller = LaunchConfiguration("initial_joint_controller")
    activate_joint_controller = LaunchConfiguration("activate_joint_controller")
    

    base_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([PathJoinSubstitution([FindPackageShare("ur_robot_driver"),"launch"]), "/ur_control.launch.py"]),
        launch_arguments={
            "ur_type": ur_type,
            "robot_ip": robot_ip,
            "tf_prefix": [LaunchConfiguration("ur_type"), "_"],
            "launch_rviz": launch_rviz,
            "use_fake_hardware": use_fake_hardware,
            "fake_sensor_commands": fake_sensor_commands,
            "runtime_config_package": runtime_config_package,
            "controllers_file": controllers_file,
            "description_package": description_package,
            "description_file": description_file,
            "kinematics_params_file": kinematics_params_file,
            "initial_joint_controller": initial_joint_controller,
            "activate_joint_controller": activate_joint_controller,
        }.items(),
    )

    return LaunchDescription(declared_arguments + [base_launch])
    


    # return LaunchDescription(
    #     declared_arguments
    #     + [
    #         IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource(
    #                 [
    #                     PathJoinSubstitution(
    #                         [
    #                             FindPackageShare("ur_robot_driver"),
    #                             "launch",
    #                             "ur_control.launch.py",
    #                         ]
    #                     )
    #                 ]
    #             ),
    #             launch_arguments={
    #                 "ur_type": ur_type,
    #                 "robot_ip": robot_ip,
    #                 "tf_prefix": [LaunchConfiguration("ur_type"), "_"],
    #                 "runtime_config_package": "my_robot_cell_control",
    #                 "controllers_file": "ros2_controllers.yaml",
    #                 "description_package": "my_robot_cell_control",
    #                 "description_file": "my_robot_cell_controlled.urdf.xacro",
    #                 "kinematics_params_file": PathJoinSubstitution(
    #                     [
    #                         FindPackageShare("my_robot_cell_control"),
    #                         "config",
    #                         "my_robot_calibration.yaml",
    #                     ]
    #                 ),
    #                 "launch_rviz": launch_rviz,
    #                 "use_fake_hardware": use_fake_hardware,
    #                 "fake_sensor_commands": fake_sensor_commands,
    #             }.items(),
    #         ),
    #     ]
    # )
