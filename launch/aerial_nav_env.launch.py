import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_dir = get_package_share_directory('aerial_nav_env')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    world_file = os.path.join(pkg_dir, 'worlds', 'aerial_nav.world')
    models_dir = os.path.join(pkg_dir, 'models')
    gazebo_default_models = '/usr/share/gazebo-11/models'
    existing_model_path = os.environ.get('GAZEBO_MODEL_PATH', '')
    path_parts = [models_dir, gazebo_default_models]
    if existing_model_path:
        path_parts.append(existing_model_path)
    model_path = ':'.join(path_parts)

    return LaunchDescription([
        DeclareLaunchArgument(
            'gui',
            default_value='true',
            description='Launch Gazebo with the GUI (set false for headless)'
        ),
        DeclareLaunchArgument(
            'verbose',
            default_value='false',
            description='Enable verbose Gazebo output'
        ),
        SetEnvironmentVariable('GAZEBO_MODEL_PATH', model_path),
        SetEnvironmentVariable('GAZEBO_MODEL_DATABASE_URI', ''),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(gazebo_ros_dir, 'launch', 'gazebo.launch.py')
            ),
            launch_arguments={
                'world': world_file,
                'gui': LaunchConfiguration('gui'),
                'verbose': LaunchConfiguration('verbose'),
            }.items(),
        ),
    ])