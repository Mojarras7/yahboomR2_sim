# yahboomcar_description

This ROS 2 package contains the URDF descriptions, meshes, and launch files for simulating the Yahboom R2 robot in Gazebo.

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
ros2 launch yahboomcar_description gazebo_R2.launch.py world:=warehouse
```
