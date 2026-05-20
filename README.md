# Yahboom R2 Robot Simulation in Gazebo

This ROS 2 package contains the URDF descriptions, meshes, and launch files for simulating the Yahboom R2 robot in Gazebo.

## Requirements

This simulation is built and tested for **ROS 2 Jazzy**. To run the simulation and all the tools (including SLAM Toolbox, Gazebo Bridge, and RViz), you need to install the following dependencies:

```bash
sudo apt update
sudo apt install ros-jazzy-xacro \
                 ros-jazzy-ros-gz \
                 ros-jazzy-slam-toolbox \
                 ros-jazzy-robot-state-publisher \
                 ros-jazzy-rviz2 \
                 ros-jazzy-joint-state-publisher
```

*(You can also find all the dependencies listed in `requirements.txt`)*

## Building the Package

To build the package, navigate to your ROS 2 workspace root and run:

```bash
colcon build --packages-select yahboomcar_description
source install/setup.bash
```

## Running the Simulation

You can launch the robot simulation in Gazebo using the provided launch file.

### Empty World (Default)

To run the simulation in an empty world, execute the launch command without any additional arguments:

```bash
ros2 launch yahboomcar_description gazebo_R2.launch.py
```

### Warehouse World

To run the simulation in the warehouse environment, pass the `world` argument with the value `warehouse.sdf`:

```bash
ros2 launch yahboomcar_description gazebo_R2.launch.py world:=warehouse.sdf
```
