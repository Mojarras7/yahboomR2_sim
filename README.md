# Yahboom R2 Robot Simulation

Gazebo simulation digital twin for the Yahboom Rosmaster R2 Ackermann platform running on ROS 2 Jazzy.

## System Overview

This repository provides the simulation environment, URDF descriptions, sensor plugin integrations, and SLAM mapping configuration for the Yahboom Rosmaster R2 mobile robot. It enables developing and validating autonomous navigation pipelines inside Gazebo Sim before deploying them to the physical Jetson Nano hardware.

> **NOTE**: For physical deployment on the NVIDIA Jetson Nano running ROS 2 Foxy with Nav2 and YOLOv8 perception, refer to the physical robot repository at [antoniofp/smart_warehouse_robot](https://github.com/antoniofp/smart_warehouse_robot).

## Project Scope & Engineering Contributions

To maintain clear technical provenance:

- **Vendor Assets**: Original 3D CAD STL mesh files and chassis link geometry were sourced from the onboard filesystem of the physical Yahboom Rosmaster R2 robot.
- **Simulation Engineering by Alejandro Mojarras - Lead Developer**:
  - Restructured and ported the robot description to ROS 2 Jazzy and Gazebo Sim.
  - Implemented the modular Xacro macro architecture in `urdf/plugins/` for LiDAR, camera, IMU, and joint state publishing.
  - Derived physical Ackermann kinematic parameters with a wheel base of 0.2353 m, track width of 0.1685 m, and wheel radius of 0.033 m, configuring the `gz-sim-ackermann-steering-system` plugin.
  - Built the simulated environments, including `warehouse.sdf` with industrial racking, pallets, and boundary walls.
  - Integrated and tuned SLAM Toolbox in `mapper_params_online_async.yaml` for real-time laser scan matching and loop closure in simulation.
  - Configured `ros_gz_bridge` and dynamic TF remapping to bridge Gazebo topics into standard ROS 2 interfaces.
  - Developed the unified launcher `gazebo_R2.launch.py` and custom RViz display layout.
- **Project Collaborators**:
  - **J. Antonio Fernández** [@antoniofp](https://github.com/antoniofp): Navigation testing and repository host for the physical platform stack.
  - **Manuel Arámbula** [@Marambulag](https://github.com/Marambulag): Warehouse project collaboration and verification.

## Requirements

The simulation stack is configured for Ubuntu 24.04 LTS and ROS 2 Jazzy Jalisco.

### Required System Packages

Install necessary ROS 2 Jazzy dependencies listed in `requirements.txt`:

```bash
xargs -a requirements.txt sudo apt install -y
```

Key dependencies:
- `ros-jazzy-ros-gz`: Gazebo Sim core and bridge utilities.
- `ros-jazzy-slam-toolbox`: 2D SLAM mapping and localization.
- `ros-jazzy-robot-state-publisher` and `ros-jazzy-joint-state-publisher`: Coordinate frame transforms.
- `ros-jazzy-nav2-bringup` and `ros-jazzy-navigation2`: Nav2 stack.
- `ros-jazzy-rviz2`: Visualization.

## Building the Package

From the root of your ROS 2 workspace, such as `~/ros2_ws`:

```bash
colcon build --packages-select yahboomcar_description
source install/setup.bash
```

## Running the Simulation

The simulation is launched through `gazebo_R2.launch.py`.

### 1. Default Empty World

Launches Gazebo with a ground plane, spawns the robot description, activates sensor bridges, starts SLAM Toolbox mapping, and opens RViz:

```bash
ros2 launch yahboomcar_description gazebo_R2.launch.py
```

### 2. Warehouse Environment

Pass the `world` argument to load the simulated warehouse environment:

```bash
ros2 launch yahboomcar_description gazebo_R2.launch.py world:=warehouse.sdf
```

## Bridged Topics & Telemetry Interface

The `ros_gz_bridge` parameter bridge maps Gazebo Sim topics into ROS 2 message formats:

| Gazebo Topic | ROS 2 Topic | Message Type | Direction |
| :--- | :--- | :--- | :--- |
| `/scan` | `/scan` | `sensor_msgs/msg/LaserScan` | Gazebo $\to$ ROS 2 |
| `/image_raw` | `/image_raw` | `sensor_msgs/msg/Image` | Gazebo $\to$ ROS 2 |
| `/camera_info` | `/camera_info` | `sensor_msgs/msg/CameraInfo` | Gazebo $\to$ ROS 2 |
| `/imu/data` | `/imu/data` | `sensor_msgs/msg/Imu` | Gazebo $\to$ ROS 2 |
| `/cmd_vel` | `/cmd_vel` | `geometry_msgs/msg/Twist` | ROS 2 $\to$ Gazebo |
| `/odom` | `/odom` | `nav_msgs/msg/Odometry` | Gazebo $\to$ ROS 2 |
| `/joint_states` | `/joint_states` | `sensor_msgs/msg/JointState` | Gazebo $\to$ ROS 2 |
| `/clock` | `/clock` | `rosgraph_msgs/msg/Clock` | Gazebo $\to$ ROS 2 |
| `/model/yahboomcar_R2/tf` | `/tf` | `tf2_msgs/msg/TFMessage` | Gazebo $\to$ ROS 2 |

## Manual Teleoperation

To drive the vehicle and test SLAM mapping via keyboard:

```bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

## Package Structure

```text
yahboomcar_description/
├── config/             # SLAM Toolbox online async parameters
├── launch/             # gazebo_R2.launch.py unified launcher
├── media/textures/     # Surface materials for warehouse world
├── meshes/             # STL mesh geometry files from vendor chassis
├── rviz/               # Pre-configured RViz display profile
├── urdf/               # Parametric Xacro robot model and Gazebo plugins
└── worlds/             # SDF simulation worlds empty_world.sdf and warehouse.sdf
```

## Authors & Maintainers

- **Alejandro Mojarras** [@Mojarras7](https://github.com/Mojarras7) — Lead Developer for Gazebo simulation and digital twin
- **J. Antonio Fernández** [@antoniofp](https://github.com/antoniofp) — Contributor
- **Manuel Arámbula** [@Marambulag](https://github.com/Marambulag) — Contributor

## References

- [Physical Robot Deployment Repository](https://github.com/antoniofp/smart_warehouse_robot)
- [ROS 2 Jazzy Documentation](https://docs.ros.org/en/jazzy/)
- [Gazebo Sim Documentation](https://gazebosim.org/docs)
