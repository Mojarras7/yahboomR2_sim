# Yahboom R2 Robot Simulation in Gazebo

This ROS 2 package contains the URDF descriptions, meshes, and launch files for simulating the Yahboom R2 robot in Gazebo.

## Requirements

This simulation assumes you already have **ROS 2 Jazzy** and its core tools installed. The main specific requirement for this setup is **SLAM Toolbox**. 

If you are missing any dependencies, you can install them all at once using the `requirements.txt` file by running:

```bash
xargs -a requirements.txt sudo apt install -y
```

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
