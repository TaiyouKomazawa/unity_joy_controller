import os

from ament_index_python import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.actions import GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import TextSubstitution
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace


def generate_launch_description():
    ip_launch_arg = DeclareLaunchArgument(
        'ip', default_value=TextSubstitution(text='192.168.0.11')
    )
    port_launch_arg = DeclareLaunchArgument(
        'port', default_value=TextSubstitution(text='10000')
    )

    linear_launch_arg = DeclareLaunchArgument(
        'linear_max', default_value=TextSubstitution(text='0.2')  # [m/s]
    )
    angular_launch_arg = DeclareLaunchArgument(
        'angular_max', default_value=TextSubstitution(text='0.7') #[rad/s]
    )

    linear_t_launch_arg = DeclareLaunchArgument(
        'linear_t_max', default_value=TextSubstitution(text='0.35')  # [m/s]
    )
    angular_t_launch_arg = DeclareLaunchArgument(
        'angular_t_max', default_value=TextSubstitution(text='1.4') #[rad/s]
    )

    return LaunchDescription([
        ip_launch_arg,
        port_launch_arg,
        linear_launch_arg,
        angular_launch_arg,
        linear_t_launch_arg,
        angular_t_launch_arg,
        Node(
            package='ros_tcp_endpoint',
            executable='default_server_endpoint',
            emulate_tty=True,
            respawn=True,
            parameters=[
                {'ROS_IP':      LaunchConfiguration('ip')},
                {'ROS_TCP_PORT':LaunchConfiguration('port')},
            ],
        ),
        Node(
            package='teleop_twist_joy',
            executable='teleop_node',
            remappings=[('joy', '/android/joy'), ('cmd_vel', '/cmd_vel')],
            parameters=[
                {'require_enable_button':   True},
                {'enable_turbo_button':     1},
                {'enable_button':           0},
                {'axis_linear.x':           1},
                {'axis_linear.y':           0},
                {'axis_angular.yaw':        2},
                {'scale_linear.x':          LaunchConfiguration('linear_max')},
                {'scale_linear.y':          ['-', LaunchConfiguration('linear_max')]},
                {'scale_angular.yaw':       ['-', LaunchConfiguration('angular_max')]},
                {'scale_linear_turbo.x':    LaunchConfiguration('linear_t_max')},
                {'scale_linear_turbo.y':          ['-', LaunchConfiguration('linear_t_max')]},
                {'scale_angular_turbo.yaw':       ['-', LaunchConfiguration('angular_t_max')]}
            ],
        )
    ])
