import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

def generate_launch_description():
    pkg_name = 'yahboomcar_description'
    pkg_share = get_package_share_directory(pkg_name)
    pkg_parent = os.path.dirname(pkg_share)
    
    # ==========================================================
    # 1. ARGUMENTS & ENVIRONMENT
    # ==========================================================
    declare_world_arg = DeclareLaunchArgument(
        'world',
        default_value='empty_world.sdf',
        description='SDF world file to load'
    )
    
    set_gz_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[os.path.join(pkg_share, 'worlds'), ':', pkg_parent]
    )

    # ==========================================================
    # 2. ROBOT DESCRIPTION (TF Tree)
    # ==========================================================
    xacro_file = os.path.join(pkg_share, 'urdf', 'master_R2.urdf.xacro')
    robot_description = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)
    
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{
            'robot_description': robot_description,
            'use_sim_time': True
        }]
    )
    
    # ==========================================================
    # 3. GAZEBO SIM
    # ==========================================================
    gz_sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')
        ),
        launch_arguments={'gz_args': ['-r ', LaunchConfiguration('world')]}.items()
    )
    
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=['-topic', 'robot_description', '-name', 'yahboomcar_R2', '-z', '0.1'],
        output='screen'
    )

    # ==========================================================
    # 4. SENSOR BRIDGE (Links Gazebo topics to ROS 2)
    # ==========================================================
    bridge_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            # Sensors
            '/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan',
            '/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
            '/camera_info@sensor_msgs/msg/CameraInfo[gz.msgs.CameraInfo',
            
            # Kinematics
            '/cmd_vel@geometry_msgs/msg/Twist]gz.msgs.Twist',
            '/odom@nav_msgs/msg/Odometry[gz.msgs.Odometry',
            '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
            
            # Clock
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            
            # TF DYNAMIC 
            '/model/yahboomcar_R2/tf@tf2_msgs/msg/TFMessage[gz.msgs.Pose_V' # this is the topic Gazebo uses for TF, we will remap it to /tf below
        ], 
        remappings=[
            # Renombramos el tópico encapsulado de Gazebo al estándar de ROS 2
            ('/model/yahboomcar_R2/tf', '/tf')
        ],
        output='screen'
    )

    # ==========================================================
    # 5. RVIZ VISUALIZATION
    # ==========================================================
    rviz_config_path = os.path.join(pkg_share, 'rviz', 'yahboomcar.rviz')
    
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )
    
    return LaunchDescription([
        declare_world_arg,
        set_gz_resource_path,
        rsp_node,
        gz_sim,
        spawn_entity,
        bridge_node,
        rviz_node
    ])