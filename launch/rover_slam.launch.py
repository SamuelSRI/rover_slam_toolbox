#!/usr/bin/env python3

from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description() -> LaunchDescription:
    rover_slam_share = Path(
        get_package_share_directory("rover_slam_toolbox")
    )

    slam_toolbox_share = Path(
        get_package_share_directory("slam_toolbox")
    )

    default_params_file = str(
        rover_slam_share / "config" / "slam_toolbox.yaml"
    )

    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")

    slam_toolbox_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            str(
                slam_toolbox_share
                / "launch"
                / "online_async_launch.py"
            )
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "slam_params_file": params_file,
            "autostart": "true",
            "use_lifecycle_manager": "false",
        }.items(),
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use simulation clock",
            ),

            DeclareLaunchArgument(
                "params_file",
                default_value=default_params_file,
                description="slam_toolbox parameter file",
            ),

            slam_toolbox_launch,
        ]
    )
