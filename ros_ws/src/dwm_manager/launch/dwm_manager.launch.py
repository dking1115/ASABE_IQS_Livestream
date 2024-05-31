import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (IncludeLaunchDescription)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    dwm1001_driver_path = get_package_share_directory('dwm1001_launch')
    dwm1001_driver_launch_dir = os.path.join(dwm1001_driver_path, 'launch')


    return LaunchDescription([

        Node(
            package='dwm_manager',
            executable='dwm_manager',
            parameters=[],
            output='screen',
        ),

        Node(
            package='joy',
            executable='joy_node',
            parameters=[],
            output='screen',
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(dwm1001_driver_launch_dir, 'passive_node.launch.py')),
            launch_arguments={}.items()),

        Node(package = "tf2_ros", 
            executable = "static_transform_publisher",
            arguments = ["11.0", "17.0", "0", "0", "0", "0", "initiator", "track_center"]),

    ])
