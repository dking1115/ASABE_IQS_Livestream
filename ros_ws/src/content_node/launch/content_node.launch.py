import os

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import (IncludeLaunchDescription)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():


    return LaunchDescription([

        Node(
            package='content_node',
            executable='content_node',
            parameters=[],
            output='screen',
        ),

        Node(package = "tf2_ros", 
            executable = "static_transform_publisher",
            arguments = ["0", "0", "0", "0", "0", "0", "initiator", "camera_3"]),
        Node(package = "tf2_ros", 
            executable = "static_transform_publisher",
            arguments = ["0", "34.", "0", "0", "0", "0", "initiator", "camera_2"]),

    ])
