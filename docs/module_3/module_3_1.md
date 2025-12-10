---
id: module_3_1
title: "Module 3.1 - Chapter 1: Isaac Sim Basics"
sidebar_position: 1
---

# Module 3.1 - Chapter 1: Isaac Sim Basics

## 1.0 Introduction

NVIDIA Isaac Sim represents a cutting-edge simulation platform specifically designed for robotics development, offering high-fidelity physics simulation, photorealistic rendering, and seamless integration with the ROS 2 ecosystem. This chapter introduces the fundamental concepts of Isaac Sim, focusing on its application to humanoid robot simulation, Visual Simultaneous Localization and Mapping (VSLAM), and navigation using the Nav2 stack.

Isaac Sim leverages NVIDIA's Omniverse platform to provide an extensible, multi-GPU scalable simulation environment that enables researchers and engineers to develop, test, and validate humanoid robot algorithms in a safe and cost-effective virtual environment before deployment on physical hardware.

## 1.1 Isaac Sim Setup and Environment Configuration

### 1.1.1 Installation and Prerequisites

Isaac Sim requires specific hardware and software prerequisites to function optimally. The simulation environment benefits from NVIDIA GPUs with CUDA support, though CPU-based simulation is possible for basic scenarios.

```bash
# Install Isaac Sim prerequisites
# Ensure NVIDIA GPU drivers are installed
nvidia-smi

# Install Isaac Sim using Omniverse Launcher or direct download
# For direct installation:
wget https://developer.nvidia.com/isaac-sim-release-isaacsim-4-0-0-release
```

### 1.1.2 Environment Configuration

The Isaac Sim environment is configured through a combination of configuration files and runtime parameters. The primary configuration involves setting up the physics engine, rendering pipeline, and ROS 2 bridge.

```yaml
# Isaac Sim configuration file (config.yaml)
physics:
  engine: "PhysX"
  gravity: [0, 0, -9.81]
  solver_type: "TGS"
  solver_position_iteration_count: 8
  solver_velocity_iteration_count: 1
  enable_gpu: true

rendering:
  resolution:
    width: 1920
    height: 1080
  enable_lights: true
  enable_shadows: true
  msaa_samples: 4

ros_bridge:
  enable: true
  ros_distro: "humble"
  namespace: "isaac_sim"
  bridge_frequency: 60

robot_settings:
  joint_damping: 0.1
  joint_friction: 0.01
  max_velocity: 10.0
  max_effort: 1000.0
```

### 1.1.3 Launching Isaac Sim

Isaac Sim can be launched through various methods, including the Omniverse Launcher, command line, or Python scripts:

```bash
# Launch Isaac Sim from command line
./isaac-sim.sh --ext-folder "exts" --config "config.yaml"

# Or using Python API
python -c "import omni; omni.main.main()"
```

## 1.2 Physics Simulation in Isaac Sim

### 1.2.1 Collision Detection and Response

Isaac Sim utilizes NVIDIA PhysX for high-performance collision detection and response. The physics engine handles complex interactions between humanoid robot joints, environmental objects, and dynamic obstacles.

```python
# Example Python code for configuring collision properties
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.prims import get_prim_at_path
from pxr import Gf

# Initialize the simulation world
world = World(stage_units_in_meters=1.0)

# Configure collision properties for a humanoid robot
def configure_robot_collision(robot_path):
    robot_prim = get_prim_at_path(robot_path)

    # Set collision properties
    collision_api = UsdPhysics.CollisionAPI.Apply(robot_prim)
    collision_api.CreateCollisionEnabledAttr().Set(True)

    # Configure friction properties
    friction_api = UsdPhysics.FrictionAPI.Apply(robot_prim)
    friction_api.CreateStaticFrictionAttr().Set(0.5)
    friction_api.CreateDynamicFrictionAttr().Set(0.3)

    # Configure restitution (bounciness)
    material_api = UsdShade.MaterialBindingAPI.Apply(robot_prim)
    material_api.BindMaterial("/Material/RobotMaterial")

# Example usage
configure_robot_collision("/World/Robot/HumanoidRobot")
```

### 1.2.2 Rigid-Body Dynamics

The rigid-body dynamics system in Isaac Sim handles the physics of humanoid robot limbs, ensuring realistic movement and interaction with the environment:

```python
# Example of configuring rigid-body dynamics
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.prims import get_prim_at_path
from pxr import Gf

def configure_rigid_body_dynamics(robot_path, link_name):
    # Get the specific link prim
    link_path = f"{robot_path}/{link_name}"
    link_prim = get_prim_at_path(link_path)

    # Apply rigid body API
    rigid_body_api = UsdPhysics.RigidBodyAPI.Apply(link_prim)
    rigid_body_api.CreateRigidBodyEnabledAttr().Set(True)

    # Configure mass properties
    mass_api = UsdPhysics.MassAPI.Apply(link_prim)
    mass_api.CreateMassAttr().Set(1.0)  # kg
    mass_api.CreateCenterOfMassAttr().Set(Gf.Vec3f(0, 0, 0))

    # Configure joint limits and constraints
    joint_path = f"{robot_path}/joints/{link_name}_joint"
    joint_prim = get_prim_at_path(joint_path)

    # Apply joint limits
    joint_api = UsdPhysics.JointAPI.Apply(joint_prim)
    joint_api.CreateLowerLimitAttr().Set(-1.57)  # -90 degrees
    joint_api.CreateUpperLimitAttr().Set(1.57)   # 90 degrees

# Example usage
configure_rigid_body_dynamics("/World/Robot/HumanoidRobot", "left_arm_link")
```

### 1.2.3 Physics Settings for Humanoid Robots

Humanoid robots require specific physics configurations to ensure stable simulation:

| Setting | Recommended Value | Rationale |
|---------|-------------------|-----------|
| Fixed Timestep | 1/60 seconds | Balance between stability and performance |
| Solver Iterations | 8-16 | Adequate for complex humanoid joint constraints |
| Gravity | [0, 0, -9.81] m/s² | Earth gravity simulation |
| Max Velocity | 10 m/s | Prevents numerical instability |
| Joint Damping | 0.1-0.5 | Provides realistic joint behavior |
| Collision Margin | 0.001 m | Ensures proper collision detection |

## 1.3 VSLAM (Visual Simultaneous Localization and Mapping)

### 1.3.1 Overview of VSLAM in Isaac Sim

Visual Simultaneous Localization and Mapping (VSLAM) combines visual input from cameras with motion data to simultaneously map the environment and determine the robot's position within it. Isaac Sim provides realistic camera simulation that enables effective VSLAM algorithm development and testing.

```python
# Example VSLAM sensor setup in Isaac Sim
import omni
from omni.isaac.core import World
from omni.isaac.sensor import Camera
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.core.utils.stage import add_reference_to_stage

def setup_vslam_sensors(robot_path):
    # Create stereo camera pair for VSLAM
    left_camera_path = f"{robot_path}/sensors/left_camera"
    right_camera_path = f"{robot_path}/sensors/right_camera"

    # Create left camera
    create_prim(
        prim_path=left_camera_path,
        prim_type="Camera",
        position=[0.1, -0.05, 0.1],  # Position relative to robot
        orientation=[0, 0, 0, 1]
    )

    # Create right camera
    create_prim(
        prim_path=right_camera_path,
        prim_type="Camera",
        position=[0.1, 0.05, 0.1],   # Position relative to robot
        orientation=[0, 0, 0, 1]
    )

    # Configure camera properties
    left_cam = Camera(
        prim_path=left_camera_path,
        frequency=30,  # Hz
        resolution=(640, 480)
    )

    right_cam = Camera(
        prim_path=right_camera_path,
        frequency=30,  # Hz
        resolution=(640, 480)
    )

    return left_cam, right_cam

# Example usage
world = World(stage_units_in_meters=1.0)
left_camera, right_camera = setup_vslam_sensors("/World/Robot/HumanoidRobot")
```

### 1.3.2 Camera Integration for VSLAM

Isaac Sim provides realistic camera simulation with proper optical properties that are essential for VSLAM algorithms:

```python
# Advanced camera configuration for VSLAM
import omni
from omni.isaac.sensor import Camera
from omni.replicator.core import random_colours
import numpy as np

def configure_vslam_camera(prim_path, focal_length=24.0, horizontal_aperture=20.955):
    # Create camera with VSLAM-specific properties
    camera = Camera(
        prim_path=prim_path,
        frequency=30,
        resolution=(1280, 720),
        position=[0.1, 0.0, 0.1]
    )

    # Configure camera intrinsics
    camera.prim.GetAttribute("focalLength").Set(focal_length)
    camera.prim.GetAttribute("horizontalAperture").Set(horizontal_aperture)

    # Enable various sensor outputs
    camera.add_raw_sensor_data_to_frame("rgb")
    camera.add_raw_sensor_data_to_frame("depth")
    camera.add_raw_sensor_data_to_frame("normals")
    camera.add_raw_sensor_data_to_frame("instance_segmentation")

    return camera

# Example of setting up a monocular camera for VSLAM
mono_camera = configure_vslam_camera("/World/Robot/HumanoidRobot/sensors/mono_camera")
```

### 1.3.3 LiDAR Integration with VSLAM

LiDAR sensors provide complementary data to visual sensors in VSLAM systems, offering precise distance measurements:

```python
# LiDAR sensor setup for VSLAM enhancement
import omni
from omni.isaac.range_sensor import LidarRtx
from omni.isaac.core.utils.prims import get_prim_at_path

def setup_lidar_for_vslam(robot_path):
    # Create LiDAR sensor
    lidar_path = f"{robot_path}/sensors/lidar"

    lidar = LidarRtx(
        prim_path=lidar_path,
        translation=[0.1, 0.0, 0.15],  # Position on robot
        orientation=[0, 0, 0, 1],
        config="VLP16",  # Velodyne VLP-16 configuration
        rotation_frequency=10,  # 10 Hz
        points_collection_frequency=1000000,  # 1M points per second
        horizontal_resolution=0.2,  # degrees
        vertical_resolution=2.0,    # degrees
        horizontal_lasers=16,
        vertical_lasers=16,
        upper_fov=15.0,
        lower_fov=-15.0,
        max_range=100.0,
        min_range=0.1
    )

    return lidar

# Example usage
lidar_sensor = setup_lidar_for_vslam("/World/Robot/HumanoidRobot")
```

## 1.4 Nav2 Navigation Stack in Isaac Sim

### 1.4.1 Introduction to Nav2 in Simulation

The Navigation2 (Nav2) stack is the next-generation navigation framework for ROS 2, providing a complete solution for robot navigation including path planning, obstacle avoidance, and localization. Isaac Sim provides excellent integration with Nav2, enabling comprehensive navigation testing.

```yaml
# Nav2 configuration for Isaac Sim (nav2_params.yaml)
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_link"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05

amcl_map_client:
  ros__parameters:
    use_sim_time: True

amcl_rclcpp_node:
  ros__parameters:
    use_sim_time: True

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: "map"
    robot_base_frame: "base_link"
    odom_topic: "/odom"
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    default_nav_through_poses_bt_xml: "nav2_bt_navigator/navigate_through_poses_w_replanning_and_recovery.xml"
    default_nav_to_pose_bt_xml: "nav2_bt_navigator/navigate_to_pose_w_replanning_and_recovery.xml"
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_smooth_path_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_time_expired_condition_bt_node
    - nav2_path_expiring_timer_condition
    - nav2_distance_traveled_condition_bt_node
    - nav2_single_trigger_bt_node
    - nav2_is_battery_low_condition_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_controller_cancel_bt_node
    - nav2_path_longer_on_approach_bt_node
    - nav2_wait_cancel_bt_node
    - nav2_spin_cancel_bt_node
    - nav2_back_up_cancel_bt_node
    - nav2_assisted_teleop_cancel_bt_node
    - nav2_drive_on_heading_cancel_bt_node
```

### 1.4.2 Path Planning and Obstacle Avoidance

Nav2 provides sophisticated path planning capabilities that work seamlessly with Isaac Sim's physics simulation:

```python
# Example Python script for Nav2 integration with Isaac Sim
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient

class IsaacSimNav2Interface(Node):
    def __init__(self):
        super().__init__('isaac_sim_nav2_interface')

        # Create action client for navigation
        self.nav_to_pose_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Wait for Nav2 server
        self.nav_to_pose_client.wait_for_server()

    def send_goal_pose(self, x, y, z, ox, oy, oz, ow):
        """Send a navigation goal to Nav2"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = z

        goal_msg.pose.pose.orientation.x = ox
        goal_msg.pose.pose.orientation.y = oy
        goal_msg.pose.pose.orientation.z = oz
        goal_msg.pose.pose.orientation.w = ow

        # Send goal
        self.nav_to_pose_client.send_goal_async(goal_msg)

    def send_navigation_goal(self, x, y):
        """Send a simple navigation goal"""
        self.send_goal_pose(x, y, 0.0, 0.0, 0.0, 0.0, 1.0)

def main():
    rclpy.init()
    nav_interface = IsaacSimNav2Interface()

    # Example: Navigate to a specific location in Isaac Sim
    nav_interface.send_navigation_goal(5.0, 3.0)

    rclpy.spin(nav_interface)
    nav_interface.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 1.4.3 Robot Localization in Simulation

Accurate localization is crucial for navigation, and Isaac Sim provides realistic sensor simulation for localization algorithms:

```python
# Example localization setup for Isaac Sim
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped
import tf2_ros

class IsaacSimLocalization(Node):
    def __init__(self):
        super().__init__('isaac_sim_localization')

        # Subscribers for sensor data
        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        # Publisher for initial pose
        self.initial_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            'initialpose',
            10
        )

        # TF buffer and listener
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

    def scan_callback(self, msg):
        """Process laser scan data from Isaac Sim"""
        # In simulation, we can use ground truth to initialize localization
        # or use the scan data for scan matching
        pass

    def imu_callback(self, msg):
        """Process IMU data from Isaac Sim"""
        # Use IMU data for orientation estimation
        pass

    def odom_callback(self, msg):
        """Process odometry data from Isaac Sim"""
        # Use odometry for position estimation
        pass

    def publish_initial_pose(self, x, y, z, ox, oy, oz, ow):
        """Publish initial pose for AMCL"""
        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header.frame_id = 'map'
        pose_msg.header.stamp = self.get_clock().now().to_msg()

        pose_msg.pose.pose.position.x = x
        pose_msg.pose.pose.position.y = y
        pose_msg.pose.pose.position.z = z

        pose_msg.pose.pose.orientation.x = ox
        pose_msg.pose.pose.orientation.y = oy
        pose_msg.pose.pose.orientation.z = oz
        pose_msg.pose.pose.orientation.w = ow

        # Set covariance (more confident in simulation)
        pose_msg.pose.covariance = [
            0.25, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.25, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0685
        ]

        self.initial_pose_pub.publish(pose_msg)

def main():
    rclpy.init()
    localization_node = IsaacSimLocalization()

    # Initialize with ground truth pose from Isaac Sim
    localization_node.publish_initial_pose(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0)

    rclpy.spin(localization_node)
    localization_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.5 Python API Integration with ROS 2

### 1.5.1 Isaac Sim Python API Basics

Isaac Sim provides a comprehensive Python API that enables programmatic control of the simulation environment and integration with ROS 2:

```python
# Isaac Sim Python API example
import omni
from omni.isaac.core import World, SimulationApp
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim, get_prim_at_path
from omni.isaac.core.robots import Robot
import carb

# Start simulation application
simulation_app = SimulationApp({"headless": False})

# Initialize world
world = World(stage_units_in_meters=1.0)

# Create a simple world with ground plane
add_reference_to_stage(
    usd_path="/Isaac/Environments/Simple_Room/simple_room.usd",
    prim_path="/World"
)

# Create a humanoid robot
add_reference_to_stage(
    usd_path="/Isaac/Robots/Humanoid/humanoid_instanceable.usd",
    prim_path="/World/Robot/HumanoidRobot"
)

# Add a ground plane
create_prim(
    prim_path="/World/GroundPlane",
    prim_type="Plane",
    position=[0, 0, 0],
    attributes={"size": 1000}
)

# Reset the world
world.reset()

# Run simulation
for i in range(1000):
    world.step(render=True)
    if i % 100 == 0:
        print(f"Simulation step: {i}")

simulation_app.close()
```

### 1.5.2 ROS 2 Bridge Integration

The ROS 2 bridge in Isaac Sim enables seamless communication between the simulation and external ROS 2 nodes:

```python
# Isaac Sim ROS 2 bridge example
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.core.robots import Robot
import carb
import rclpy
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist

def setup_ros_bridge():
    """Setup ROS 2 bridge in Isaac Sim"""
    # Enable ROS bridge extension
    ext_manager = omni.kit.app.get_app().get_extension_manager()
    ext_manager.set_enabled("omni.isaac.ros_bridge", True)

    # Initialize ROS 2 context
    rclpy.init()

def create_robot_with_ros_interfaces(robot_path):
    """Create robot with ROS 2 interfaces"""
    # Create robot prim
    robot = Robot(
        prim_path=robot_path,
        name="humanoid_robot",
        usd_path="/Isaac/Robots/Humanoid/humanoid_instanceable.usd"
    )

    # Configure ROS 2 publishers and subscribers
    # This would typically be done through Isaac Sim's ROS bridge extensions
    pass

def main():
    # Setup simulation
    world = World(stage_units_in_meters=1.0)

    # Add environment
    add_reference_to_stage(
        usd_path="/Isaac/Environments/Simple_Room/simple_room.usd",
        prim_path="/World"
    )

    # Create robot
    robot = Robot(
        prim_path="/World/Robot/HumanoidRobot",
        name="humanoid_robot",
        usd_path="/Isaac/Robots/Humanoid/humanoid_instanceable.usd"
    )

    # Reset simulation
    world.reset()

    # Run simulation with ROS 2 integration
    for i in range(1000):
        world.step(render=True)

        # At certain intervals, publish ROS 2 messages
        if i % 60 == 0:  # Publish every 60 steps (1 Hz if sim runs at 60 Hz)
            # This would publish sensor data, joint states, etc.
            print(f"Simulation step: {i}, publishing ROS data...")

    world.stop()

if __name__ == "__main__":
    main()
```

## 1.6 Hands-On Examples

### 1.6.1 Example 1: Launch a Humanoid Robot in Isaac Sim and Visualize Sensors

This example demonstrates how to launch a humanoid robot in Isaac Sim and set up its sensors:

```python
# Complete example: Launch humanoid robot with sensors in Isaac Sim
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.core.robots import Robot
from omni.isaac.sensor import Camera
from omni.isaac.range_sensor import LidarRtx
import numpy as np
import carb

# Initialize simulation
simulation_app = SimulationApp({"headless": False})
world = World(stage_units_in_meters=1.0)

# Set up the stage
stage = omni.usd.get_context().get_stage()
world.scene.add_default_ground_plane()

# Add a humanoid robot
humanoid_robot = Robot(
    prim_path="/World/Robot/HumanoidRobot",
    name="humanoid_robot",
    usd_path="/Isaac/Robots/Humanoid/humanoid_instanceable.usd",
    position=[0.0, 0.0, 0.5],
    orientation=[0.0, 0.0, 0.0, 1.0]
)

# Add sensors to the robot
# RGB camera
camera = Camera(
    prim_path="/World/Robot/HumanoidRobot/Camera",
    name="humanoid_camera",
    position=[0.1, 0.0, 0.1],
    frequency=30,
    resolution=(640, 480)
)

# LiDAR sensor
lidar = LidarRtx(
    prim_path="/World/Robot/HumanoidRobot/LiDAR",
    name="humanoid_lidar",
    translation=[0.1, 0.0, 0.15],
    config="VLP16",
    rotation_frequency=10,
    points_collection_frequency=1000000
)

# Reset the world
world.reset()

# Run simulation and collect sensor data
for i in range(1000):
    world.step(render=True)

    if i % 100 == 0:
        # Get camera data
        camera_data = camera.get_rgb()
        if camera_data is not None:
            print(f"Camera frame captured at step {i}")

        # Get LiDAR data
        lidar_data = lidar.get_linear_depth_data()
        if lidar_data is not None:
            print(f"LiDAR data collected at step {i}, points: {len(lidar_data)}")

simulation_app.close()
```

### 1.6.2 Example 2: Simulate a Robot Mapping a Room Using VSLAM

This example demonstrates VSLAM in Isaac Sim by creating a mapping scenario:

```python
# VSLAM mapping example in Isaac Sim
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.robots import Robot
from omni.isaac.sensor import Camera
import numpy as np
import cv2

def setup_vslam_environment():
    """Setup environment for VSLAM simulation"""
    simulation_app = SimulationApp({"headless": False})
    world = World(stage_units_in_meters=1.0)

    # Add a complex room environment for mapping
    add_reference_to_stage(
        usd_path="/Isaac/Environments/Simple_Room/simple_room.usd",
        prim_path="/World"
    )

    # Add additional objects to create features for VSLAM
    # (chairs, tables, etc. that provide visual landmarks)

    return simulation_app, world

def setup_vslam_robot():
    """Setup robot with VSLAM sensors"""
    robot = Robot(
        prim_path="/World/Robot/VSLAMRobot",
        name="vslam_robot",
        usd_path="/Isaac/Robots/Humanoid/humanoid_instanceable.usd",
        position=[0.0, 0.0, 0.5]
    )

    # Add stereo cameras for VSLAM
    left_camera = Camera(
        prim_path="/World/Robot/VSLAMRobot/LeftCamera",
        name="left_camera",
        position=[0.1, -0.05, 0.1],
        frequency=30,
        resolution=(640, 480)
    )

    right_camera = Camera(
        prim_path="/World/Robot/VSLAMRobot/RightCamera",
        name="right_camera",
        position=[0.1, 0.05, 0.1],
        frequency=30,
        resolution=(640, 480)
    )

    return robot, left_camera, right_camera

def simulate_vslam_mapping():
    """Simulate VSLAM mapping process"""
    simulation_app, world = setup_vslam_environment()

    robot, left_cam, right_cam = setup_vslam_robot()

    world.reset()

    # Simulate robot movement for mapping
    movement_sequence = [
        [1.0, 0.0, 0.5],    # Move forward
        [1.0, 1.0, 0.5],    # Move right
        [0.0, 1.0, 0.5],    # Move back
        [0.0, 0.0, 0.5]     # Return to start
    ]

    for step, target_pos in enumerate(movement_sequence):
        for i in range(300):  # 5 seconds per movement at 60 Hz
            world.step(render=True)

            # Move robot towards target position
            current_pos = robot.get_world_pose()[0]
            direction = np.array(target_pos[:2]) - np.array(current_pos[:2])
            distance = np.linalg.norm(direction)

            if distance > 0.1:  # If not close to target
                direction = direction / distance * 0.01  # Normalize and scale
                new_pos = [current_pos[0] + direction[0],
                          current_pos[1] + direction[1],
                          current_pos[2]]
                robot.set_world_pose(position=new_pos)

            # Capture stereo images for VSLAM
            if i % 10 == 0:  # Capture every 10 steps
                left_img = left_cam.get_rgb()
                right_img = right_cam.get_rgb()

                if left_img is not None and right_img is not None:
                    print(f"Captured stereo pair at step {step}, frame {i}")
                    # Here you would process the stereo images for mapping

    simulation_app.close()

# Run the VSLAM simulation
simulate_vslam_mapping()
```

### 1.6.3 Example 3: Integrate Nav2 to Navigate the Robot Autonomously

This example demonstrates Nav2 integration with Isaac Sim for autonomous navigation:

```python
# Nav2 autonomous navigation example
import rclpy
from rclpy.node import Node
from nav2_msgs.action import NavigateToPose
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
import time

class IsaacSimNav2Example(Node):
    def __init__(self):
        super().__init__('isaac_sim_nav2_example')

        # Create action client for navigation
        self.nav_to_pose_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Wait for Nav2 server to be available
        self.nav_to_pose_client.wait_for_server()

    def send_navigation_goals(self):
        """Send a sequence of navigation goals"""
        # Define a sequence of goals for the robot to navigate to
        goals = [
            {"x": 2.0, "y": 2.0, "theta": 0.0},
            {"x": 4.0, "y": 0.0, "theta": 1.57},
            {"x": 2.0, "y": -2.0, "theta": 3.14},
            {"x": 0.0, "y": 0.0, "theta": 0.0}
        ]

        for i, goal in enumerate(goals):
            self.get_logger().info(f"Sending goal {i+1}: ({goal['x']}, {goal['y']})")
            self.send_goal(goal['x'], goal['y'], goal['theta'])

            # Wait for completion before sending next goal
            time.sleep(10)  # Adjust based on expected navigation time

    def send_goal(self, x, y, theta):
        """Send a single navigation goal"""
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()

        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Convert theta to quaternion
        import math
        qw = math.cos(theta / 2.0)
        qz = math.sin(theta / 2.0)
        goal_msg.pose.pose.orientation.x = 0.0
        goal_msg.pose.pose.orientation.y = 0.0
        goal_msg.pose.pose.orientation.z = qz
        goal_msg.pose.pose.orientation.w = qw

        # Send goal
        future = self.nav_to_pose_client.send_goal_async(goal_msg)
        future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        """Handle result callback"""
        result = future.result().result
        self.get_logger().info(f'Result: {result}')

def main():
    rclpy.init()
    nav2_example = IsaacSimNav2Example()

    # Send navigation goals
    nav2_example.send_navigation_goals()

    rclpy.spin(nav2_example)
    nav2_example.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.7 Data Flow Diagrams

### 1.7.1 Isaac Sim ↔ ROS 2 ↔ Robot Data Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   ROS 2 Nodes   │◄──►│   Isaac Sim      │◄──►│   Robot Control │
│                 │    │   ROS Bridge     │    │   System        │
│ - Navigation    │    │ - Topic Mapping  │    │                 │
│ - Perception    │    │ - Message Conv   │    │ - Joint Control │
│ - Planning      │    │ - TF Broadcast   │    │ - Sensor Proc   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   External      │    │   Simulation     │    │   Physics &     │
│   Applications  │    │   Environment    │    │   Rendering     │
│                 │    │                  │    │                 │
│ - RViz          │    │ - USD Stage      │    │ - PhysX Engine │
│ - RQT Tools     │    │ - Robot Models   │    │ - Omniverse RT │
│ - Custom Nodes  │    │ - Sensors        │    │ - Materials     │
└─────────────────┘    └─────────────────┘     └─────────────────┘
```

### 1.7.2 Sensor Data Processing Pipeline in Simulation

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Isaac Sim     │    │   Sensor Data    │    │   ROS 2 Topics  │
│   Sensors       │───►│   Processing     │───►│   Publishing    │
│                 │    │                  │    │                 │
│ - Camera        │    │ - Noise Addition │    │ - /camera/image │
│ - LiDAR         │    │ - Data Filtering │    │ - /scan         │
│ - IMU           │    │ - Format Conv    │    │ - /imu/data     │
│ - Joint States  │    │ - Rate Control   │    │ - /joint_states │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Sensor    │    │   Filtered Data  │    │   Processed     │
│   Data          │    │   Pipeline       │    │   Messages      │
│                 │    │                  │    │                 │
│ - Depth Images  │    │ - Point Clouds   │    │ - Standardized  │
│ - Point Clouds  │    │ - Feature Maps   │    │   Format        │
│ - Joint Angles  │    │ - Odometry       │    │ - Synchronized  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 1.7.3 Nav2 Navigation Workflow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Goal          │    │   Path Planning  │    │   Local         │
│   Request       │───►│   (Global)       │───►│   Planning      │
│                 │    │                  │    │                 │
│ - PoseStamped   │    │ - A* Algorithm   │    │ - DWA/Teb       │
│ - Nav2 Action   │    │ - Costmap        │    │ - Local Costmap │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Global        │    │   Path Following │    │   Robot         │
│   Path          │───►│   Controller     │───►│   Execution     │
│                 │    │                  │    │                 │
│ - Waypoints     │    │ - Pure Pursuit   │    │ - Motor Control │
│ - Waypoint Nav  │    │ - PID Control    │    │ - Feedback      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                            Feedback Loop
```

## 1.8 Tables for Clarity

### 1.8.1 Common Isaac Sim Nodes and Python API Methods

| Node/Method | Purpose | Use Case | Example |
|-------------|---------|----------|---------|
| World | Simulation world management | Main simulation control | `world = World()` |
| Robot | Robot entity creation | Robot instantiation | `robot = Robot(prim_path, usd_path)` |
| Camera | Camera sensor creation | Visual sensing | `camera = Camera(prim_path, resolution)` |
| LidarRtx | LiDAR sensor creation | Range sensing | `lidar = LidarRtx(prim_path, config)` |
| SimulationApp | App lifecycle management | Simulation startup/shutdown | `app = SimulationApp()` |
| add_reference_to_stage | USD stage management | Adding assets to scene | `add_reference_to_stage(usd_path, prim_path)` |
| create_prim | Prim creation | Creating basic objects | `create_prim(prim_path, prim_type)` |

### 1.8.2 Recommended Simulation Physics Settings for Humanoid Robots

| Setting | Value | Reasoning |
|---------|-------|-----------|
| Fixed Timestep | 1/60 seconds | Balance between stability and performance |
| Solver Iterations | 8-16 | Adequate for complex joint constraints |
| Max Position Iterations | 8 | Stability for humanoid joints |
| Max Velocity Iterations | 1 | Velocity constraint solving |
| Joint Damping | 0.1-0.5 | Realistic joint behavior |
| Joint Friction | 0.01-0.1 | Prevents sliding and unrealistic motion |
| Collision Margin | 0.001 m | Proper collision detection |
| Max Velocity | 10 m/s | Prevents numerical instability |

### 1.8.3 Mapping Sensors to ROS 2 Topics

| Isaac Sim Sensor | ROS 2 Topic | Message Type | Purpose |
|------------------|-------------|--------------|---------|
| Camera | /camera/image | sensor_msgs/Image | Visual sensing |
| Camera | /camera/depth | sensor_msgs/Image | Depth sensing |
| LiDAR | /scan | sensor_msgs/LaserScan | Range sensing |
| IMU | /imu/data | sensor_msgs/Imu | Orientation sensing |
| Joint State | /joint_states | sensor_msgs/JointState | Joint position/velocity |
| Odometry | /odom | nav_msgs/Odometry | Robot pose estimation |
| Point Cloud | /point_cloud | sensor_msgs/PointCloud2 | 3D mapping |

## 1.9 Exercises

### 1.9.1 Exercise 1: Launch Isaac Sim with a Humanoid Robot
Launch Isaac Sim and import a humanoid robot model into the simulation environment. Configure the robot's basic properties and verify that it appears correctly in the scene.

### 1.9.2 Exercise 2: Configure VSLAM Sensors
Add stereo cameras to your humanoid robot in Isaac Sim and configure them for VSLAM applications. Verify that the cameras produce appropriate visual data.

### 1.9.3 Exercise 3: Run Nav2 Navigation Stack
Set up the Nav2 navigation stack to work with your Isaac Sim environment. Configure the necessary parameters for localization, mapping, and navigation.

### 1.9.4 Exercise 4: Integrate Python API Control
Use the Isaac Sim Python API to programmatically control your robot's movement and sensor data collection in the simulation.

### 1.9.5 Exercise 5: Test Navigation in Complex Environments
Create a complex environment with obstacles and test the Nav2 navigation stack's ability to plan and execute paths around them.

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Launch Isaac Sim with a Humanoid Robot</summary>

```bash
# Install Isaac Sim prerequisites and extensions
# First, install the necessary Isaac Sim extensions

# Create a launch script for Isaac Sim with humanoid robot
import omni
from pxr import Gf, UsdGeom, Sdf, Usd, PhysxSchema
import carb
import omni.usd
import omni.kit.commands
import omni.graph.core as og
import numpy as np

# Python script to load a humanoid robot in Isaac Sim
def load_humanoid_robot():
    # Get the USD stage
    stage = omni.usd.get_context().get_stage()

    # Create a new prim for the robot
    robot_path = "/World/HumanoidRobot"
    robot_prim = stage.DefinePrim(robot_path, "Xform")

    # Load humanoid robot USD from path (assuming you have a humanoid robot USD file)
    # For example, if you have a robot model at a specific path:
    humanoid_asset_path = "path/to/humanoid_robot.usd"  # Replace with actual path

    # Import the robot model
    omni.kit.commands.execute(
        "CreateReference prim",
        path=Sdf.Path(robot_path),
        asset_path=humanoid_asset_path
    )

    # Set initial position and orientation
    xform_api = UsdGeom.Xformable(robot_prim)
    xform_api.AddTranslateOp().Set(Gf.Vec3d(0, 0, 0.8))  # Raise robot to appropriate height
    xform_api.AddOrientOp().Set(Gf.Quath(1.0, Gf.Vec3h(0, 0, 0)))  # No rotation

    print(f"Humanoid robot loaded at {robot_path}")

# Alternative approach using Isaac Sim's robot loader
def setup_isaac_sim_environment():
    # Enable necessary extensions
    omni.kit.app.get_app().extension_manager.set_extension_enabled("omni.isaac.ros2_bridge", True)
    omni.kit.app.get_app().extension_manager.set_extension_enabled("omni.isaac.sensor", True)

    # Create ground plane
    ground_path = "/World/GroundPlane"
    omni.kit.commands.execute(
        "AddXformCommand",
        usd_path=ground_path,
        name="GroundPlane"
    )

    # Add rigid body and collision to ground
    omni.kit.commands.execute(
        "AddRigidBodyCommand",
        path=Sdf.Path(ground_path),
        approximation_shape="convexHull"
    )

    # Load the humanoid robot
    load_humanoid_robot()

    # Configure physics properties
    physics_settings = omni.physics.get_simulation_settings()
    physics_settings.enable_scene_query_support = True
    physics_settings.enable_gpu_physics = False  # Disable for stability if needed
    physics_settings.use_gpu_dynamic = False
    physics_settings.use_gpu_feedback = False
    omni.physics.configure_simulation(physics_settings)

# Run the setup
setup_isaac_sim_environment()
```

For launching Isaac Sim with a humanoid robot via command line:

```bash
# Launch Isaac Sim with a specific robot model
isaac-sim/python.sh -c "
import omni
from omni.isaac.kit import SimulationApp

# Initialize simulation app
config = {
    'headless': False,
    'window_width': 1280,
    'window_height': 720
}
simulation_app = SimulationApp(config)

# Load the humanoid robot
from omni.isaac.core import World
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage

world = World(stage_units_in_meters=1.0)

# Add robot to stage
robot_asset_path = get_assets_root_path() + '/Isaac/Robots/Humanoid/humanoid.usd'
add_reference_to_stage(usd_path=robot_asset_path, prim_path='/World/Humanoid')

# Reset the world
world.reset()

# Run simulation
for i in range(1000):
    world.step(render=True)

simulation_app.close()
"
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Configure VSLAM Sensors</summary>

```python
# configure_vsiam_sensors.py
import omni
from pxr import Gf, UsdGeom, Sdf, Usd, PhysxSchema
from omni.isaac.sensor import Camera
from omni.isaac.core.utils.stage import get_current_stage
from omni.isaac.core.utils.prims import get_prim_at_path
import numpy as np

def setup_vsiam_sensors(robot_path="/World/HumanoidRobot"):
    """
    Set up VSLAM sensors (stereo cameras) on the humanoid robot
    """
    stage = get_current_stage()

    # Create left camera
    left_camera_path = f"{robot_path}/LeftCamera"
    right_camera_path = f"{robot_path}/RightCamera"

    # Add camera prims to the robot
    left_camera_prim = stage.DefinePrim(left_camera_path, "Camera")
    right_camera_prim = stage.DefinePrim(right_camera_path, "Camera")

    # Configure left camera
    left_camera_xform = UsdGeom.Xformable(left_camera_prim)
    # Position left camera slightly to the left of the head
    left_camera_xform.AddTranslateOp().Set(Gf.Vec3d(0.05, 0.05, 0.1))  # x, y, z offset from head

    # Configure right camera (same height, different lateral position)
    right_camera_xform = UsdGeom.Xformable(right_camera_prim)
    right_camera_xform.AddTranslateOp().Set(Gf.Vec3d(0.05, -0.05, 0.1))  # x, y, z offset from head

    # Set camera properties for stereo vision
    left_camera_attr = left_camera_prim.GetAttribute("primvars:resolution")
    if not left_camera_attr.IsValid():
        # Create camera using Isaac Sim API
        from omni.isaac.core.prims import XFormPrim
        left_cam = Camera(
            prim_path=left_camera_path,
            frequency=30,  # 30Hz
            resolution=(640, 480),
            position=np.array([0.05, 0.05, 0.1]),
            orientation=np.array([0, 0, 0, 1])
        )

        right_cam = Camera(
            prim_path=right_camera_path,
            frequency=30,  # 30Hz
            resolution=(640, 480),
            position=np.array([0.05, -0.05, 0.1]),
            orientation=np.array([0, 0, 0, 1])
        )

        # Set camera intrinsics for stereo matching
        # Typical focal length for 640x480 image: ~320 pixels
        left_cam.focal_length = 320.0
        right_cam.focal_length = 320.0

        print("Stereo cameras configured for VSLAM")

def setup_vslam_with_ros_bridge():
    """
    Set up VSLAM with ROS 2 bridge for publishing camera data
    """
    # Enable ROS2 bridge
    import omni.isaac.ros2_bridge
    omni.kit.app.get_app().extension_manager.set_extension_enabled("omni.isaac.ros2_bridge", True)

    # Create ROS2 bridge node
    import rclpy
    from sensor_msgs.msg import Image, CameraInfo
    from geometry_msgs.msg import PointStamped
    from cv_bridge import CvBridge

    rclpy.init()
    node = rclpy.create_node('vsiam_sensor_node')

    # Publishers for left and right camera images
    left_img_pub = node.create_publisher(Image, '/humanoid/left_camera/image_raw', 10)
    right_img_pub = node.create_publisher(Image, '/humanoid/right_camera/image_raw', 10)
    left_info_pub = node.create_publisher(CameraInfo, '/humanoid/left_camera/camera_info', 10)
    right_info_pub = node.create_publisher(CameraInfo, '/humanoid/right_camera/camera_info', 10)

    bridge = CvBridge()

    # Timer to publish camera data periodically
    def publish_camera_data():
        # In Isaac Sim, this would be called when new camera data is available
        # For this example, we'll simulate the process

        # Publish camera info
        camera_info = CameraInfo()
        camera_info.width = 640
        camera_info.height = 480
        camera_info.k = [320.0, 0.0, 320.0, 0.0, 320.0, 240.0, 0.0, 0.0, 1.0]  # Intrinsics matrix
        camera_info.p = [320.0, 0.0, 320.0, 0.0, 0.0, 320.0, 240.0, 0.0, 0.0, 0.0, 1.0, 0.0]  # Projection matrix

        left_info_pub.publish(camera_info)
        right_info_pub.publish(camera_info)

        print("VSLAM camera data publishing configured")

    # Set up timer to publish data
    timer = node.create_timer(0.1, publish_camera_data)  # 10Hz

    # Run until shutdown
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

def main():
    # Set up VSLAM sensors
    setup_vsiam_sensors()
    setup_vslam_with_ros_bridge()

if __name__ == "__main__":
    main()
```

Configuration for VSLAM parameters in Isaac Sim:

```yaml
# config/vslam_config.yaml
humanoid_vslam:
  ros__parameters:
    # Camera parameters
    left_camera.resolution: [640, 480]
    left_camera.frequency: 30.0
    left_camera.field_of_view: 90.0
    right_camera.resolution: [640, 480]
    right_camera.frequency: 30.0
    right_camera.field_of_view: 90.0
    stereo_baseline: 0.1  # 10cm between cameras

    # VSLAM parameters
    vsiam_algorithm: "orb_slam"
    vsiam_map_size: 1000  # Maximum map size
    vsiam_keyframe_threshold: 0.1  # Minimum distance between keyframes
    vsiam_tracking_quality_threshold: 0.5  # Minimum tracking quality

    # ROS2 bridge settings
    ros2_namespace: "humanoid"
    camera_topic_prefix: "camera"
    image_transport_plugins: ["compressed", "theora"]
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Run Nav2 Navigation Stack</summary>

```python
# nav2_isaac_sim_integration.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped
from nav_msgs.msg import OccupancyGrid, Path
from std_msgs.msg import String
from builtin_interfaces.msg import Duration
import time

class Nav2IsaacSimIntegration(Node):
    def __init__(self):
        super().__init__('nav2_isaac_sim_integration')

        # Publishers
        self.initial_pose_pub = self.create_publisher(PoseWithCovarianceStamped, 'initialpose', 10)
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        self.status_pub = self.create_publisher(String, 'nav2_status', 10)

        # Subscribers
        self.map_sub = self.create_subscription(OccupancyGrid, 'map', self.map_callback, 10)
        self.path_sub = self.create_subscription(Path, 'plan', self.path_callback, 10)

        # Parameters for Nav2
        self.declare_parameter('planner_frequency', 5.0)
        self.declare_parameter('controller_frequency', 20.0)
        self.declare_parameter('costmap_resolution', 0.05)
        self.declare_parameter('robot_radius', 0.3)

        self.planner_frequency = self.get_parameter('planner_frequency').value
        self.controller_frequency = self.get_parameter('controller_frequency').value
        self.costmap_resolution = self.get_parameter('costmap_resolution').value
        self.robot_radius = self.get_parameter('robot_radius').value

        # Timer for navigation commands
        self.nav_timer = self.create_timer(2.0, self.send_navigation_commands)

        # Internal state
        self.current_map = None
        self.current_path = None
        self.navigation_active = False

        self.get_logger().info('Nav2-Isaac Sim integration node initialized')

    def map_callback(self, msg):
        """Handle map updates from SLAM or static map"""
        self.current_map = msg
        self.get_logger().info(f'Received map with resolution: {msg.info.resolution}')

    def path_callback(self, msg):
        """Handle path updates from global planner"""
        self.current_path = msg
        self.get_logger().info(f'Received path with {len(msg.poses)} waypoints')

    def send_initial_pose(self):
        """Send initial pose to Nav2 for localization"""
        initial_pose = PoseWithCovarianceStamped()
        initial_pose.header.stamp = self.get_clock().now().to_msg()
        initial_pose.header.frame_id = 'map'

        # Set robot's initial position in the simulation world
        initial_pose.pose.pose.position.x = 0.0
        initial_pose.pose.pose.position.y = 0.0
        initial_pose.pose.pose.position.z = 0.0

        # Set orientation (facing forward)
        initial_pose.pose.pose.orientation.z = 0.0
        initial_pose.pose.pose.orientation.w = 1.0

        # Set covariance (low uncertainty for simulation)
        initial_pose.pose.covariance = [
            0.1, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.1, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0, 0.0, 0.05
        ]

        self.initial_pose_pub.publish(initial_pose)
        self.get_logger().info('Initial pose published')

    def send_navigation_goal(self, x, y, theta=0.0):
        """Send navigation goal to Nav2"""
        goal = PoseStamped()
        goal.header.stamp = self.get_clock().now().to_msg()
        goal.header.frame_id = 'map'

        goal.pose.position.x = x
        goal.pose.position.y = y
        goal.pose.position.z = 0.0

        # Convert theta to quaternion
        import math
        goal.pose.orientation.z = math.sin(theta / 2.0)
        goal.pose.orientation.w = math.cos(theta / 2.0)

        self.goal_pub.publish(goal)
        self.get_logger().info(f'Navigation goal sent to ({x}, {y})')

    def send_navigation_commands(self):
        """Send navigation commands periodically"""
        if not self.navigation_active:
            # Send initial pose first
            self.send_initial_pose()
            self.navigation_active = True

            # Then send a goal after a short delay
            time.sleep(1.0)
            self.send_navigation_goal(2.0, 2.0, 0.0)  # Go to (2,2) facing forward
        else:
            # Send another goal to a different location
            self.send_navigation_goal(-1.0, 1.5, 1.57)  # Go to (-1, 1.5) facing left

def main(args=None):
    rclpy.init(args=args)
    node = Nav2IsaacSimIntegration()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Nav2 integration node stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Nav2 configuration file for Isaac Sim:

```yaml
# config/nav2_params.yaml
amcl:
  ros__parameters:
    use_sim_time: True
    alpha1: 0.2
    alpha2: 0.2
    alpha3: 0.2
    alpha4: 0.2
    alpha5: 0.2
    base_frame_id: "base_link"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    likelihood_max_dist: 2.0
    set_initial_pose: true
    initial_pose:
      x: 0.0
      y: 0.0
      z: 0.0
      yaw: 0.0
    tf_broadcast: true
    transform_tolerance: 1.0
    update_min_a: 0.2
    update_min_d: 0.25
    z_hit: 0.5
    z_max: 0.05
    z_rand: 0.5
    z_short: 0.05
    scan_topic: scan
    map_topic: map
    odom_topic: odom
    initial_pose_topic: initialpose
    robot_model_type: "nav2_amcl::DifferentialMotionModel"
    qos: 2
    scan_downsample_consider_n_inf: true
    scan_downsample_inf_epsilon: 0.1
    max_beams: 60
    sigma_hit: 0.2

bt_navigator:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1666
    groot_zmq_server_port: 1667
    default_nav_through_poses_bt_xml: "nav2_bt_xml_v0/navigate_w_replanning_and_recovery.xml"
    default_nav_to_pose_bt_xml: "nav2_bt_xml_v0/navigate_w_replanning_and_recovery.xml"
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_globally_consistent_condition_bt_node
    - nav2_is_path_valid_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_user_task_ready_condition_bt_node
    - nav2_battery_low_condition_bt_node
    - nav2_is_battery_charging_condition_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_recovered_condition_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_goal_node_bt_node
    - nav2_anchor_goal_node_bt_node

bt_navigator_navigate_through_poses:
  ros__parameters:
    use_sim_time: True
    global_frame: map
    robot_base_frame: base_link
    odom_topic: odom
    bt_loop_duration: 10
    default_server_timeout: 20
    enable_groot_monitoring: True
    groot_zmq_publisher_port: 1668
    groot_zmq_server_port: 1669
    plugin_lib_names:
    - nav2_compute_path_to_pose_action_bt_node
    - nav2_compute_path_through_poses_action_bt_node
    - nav2_follow_path_action_bt_node
    - nav2_spin_action_bt_node
    - nav2_wait_action_bt_node
    - nav2_assisted_teleop_action_bt_node
    - nav2_back_up_action_bt_node
    - nav2_drive_on_heading_bt_node
    - nav2_clear_costmap_service_bt_node
    - nav2_is_stuck_condition_bt_node
    - nav2_goal_reached_condition_bt_node
    - nav2_goal_updated_condition_bt_node
    - nav2_globally_consistent_condition_bt_node
    - nav2_is_path_valid_condition_bt_node
    - nav2_initial_pose_received_condition_bt_node
    - nav2_reinitialize_global_localization_service_bt_node
    - nav2_transform_available_condition_bt_node
    - nav2_user_task_ready_condition_bt_node
    - nav2_battery_low_condition_bt_node
    - nav2_is_battery_charging_condition_bt_node
    - nav2_navigate_to_pose_action_bt_node
    - nav2_navigate_through_poses_action_bt_node
    - nav2_remove_passed_goals_action_bt_node
    - nav2_planner_selector_bt_node
    - nav2_controller_selector_bt_node
    - nav2_goal_checker_selector_bt_node
    - nav2_recovered_condition_bt_node
    - nav2_rate_controller_bt_node
    - nav2_distance_controller_bt_node
    - nav2_speed_controller_bt_node
    - nav2_truncate_path_action_bt_node
    - nav2_truncate_path_local_action_bt_node
    - nav2_goal_updater_node_bt_node
    - nav2_recovery_node_bt_node
    - nav2_pipeline_sequence_bt_node
    - nav2_round_robin_node_bt_node
    - nav2_transform_goal_node_bt_node
    - nav2_anchor_goal_node_bt_node

controller_server:
  ros__parameters:
    use_sim_time: True
    controller_frequency: 20.0
    min_x_velocity_threshold: 0.001
    min_y_velocity_threshold: 0.5
    min_theta_velocity_threshold: 0.001
    progress_checker_plugin: "progress_checker"
    goal_checker_plugin: "goal_checker"
    controller_plugins: ["FollowPath"]

    # Progress checker parameters
    progress_checker:
      plugin: "nav2_controller::SimpleProgressChecker"
      required_movement_radius: 0.5
      movement_time_allowance: 10.0

    # Goal checker parameters
    goal_checker:
      plugin: "nav2_controller::SimpleGoalChecker"
      xy_goal_tolerance: 0.25
      yaw_goal_tolerance: 0.25
      stateful: True

    # DWB parameters
    FollowPath:
      plugin: "nav2_rotation_shim_controller::RotationShimController"
      primary_controller: "dwb_core::DWBLocalPlanner"
      rotation_shim:
        plugin: "nav2_controller::SimpleProgressChecker"
        required_movement_radius: 0.5
        movement_time_allowance: 10.0

      # DWB parameters
      dwb_local_planner:
        plugin: "dwb_core::DWBLocalPlanner"
        debug_trajectory_details: False
        min_vel_x: 0.0
        min_vel_y: 0.0
        max_vel_x: 0.5
        max_vel_y: 0.0
        max_vel_theta: 1.0
        min_speed_xy: 0.0
        max_speed_xy: 0.5
        min_speed_theta: 0.0
        acc_lim_x: 2.5
        acc_lim_y: 0.0
        acc_lim_theta: 3.2
        decel_lim_x: -2.5
        decel_lim_y: 0.0
        decel_lim_theta: -3.2
        vx_samples: 20
        vy_samples: 5
        vtheta_samples: 20
        sim_time: 1.7
        linear_granularity: 0.05
        angular_granularity: 0.025
        transform_tolerance: 0.2
        xy_goal_tolerance: 0.25
        yaw_goal_tolerance: 0.25
        rot_stopped_vel: 0.0025
        trans_stopped_vel: 0.01
        short_circuit_trajectory_evaluation: True
        stateful: True
        critics: ["RotateToGoal", "Oscillation", "BaseObstacle", "GoalAlign", "PathAlign", "PathDist", "GoalDist"]
        BaseObstacle.scale: 0.02
        PathAlign.scale: 32.0
        PathAlign.forward_point_distance: 0.1
        GoalAlign.scale: 24.0
        GoalAlign.forward_point_distance: 0.1
        PathDist.scale: 32.0
        GoalDist.scale: 24.0
        RotateToGoal.scale: 32.0
        RotateToGoal.slowing_factor: 5.0
        RotateToGoal.lookahead_time: -1.0
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: Integrate Python API Control</summary>

```python
# isaac_sim_python_api_control.py
import omni
from pxr import Gf, UsdGeom, Sdf, Usd, PhysxSchema
import carb
import omni.usd
import omni.kit.commands
import numpy as np
from omni.isaac.core import World
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.viewports import set_camera_view
from omni.isaac.core.articulations import ArticulationView
from omni.isaac.core.controllers import BaseController
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.utils.nucleus import get_assets_root_path
import asyncio

class HumanoidController(BaseController):
    def __init__(self, name: str = "humanoid_controller"):
        super().__init__(name=name)
        self.name = name
        self._num_dof = 24  # Assuming a humanoid with 24 DOF

    def forward(self, actions):
        """
        Forward pass of the controller
        """
        pos_targets = actions[:self._num_dof]
        vel_targets = actions[self._num_dof:]
        return {"joint_positions": pos_targets, "joint_velocities": vel_targets}

class IsaacSimPythonController:
    def __init__(self):
        self.world = None
        self.humanoid_robot = None
        self.controller = None

        # Initialize simulation
        self.setup_simulation()

    def setup_simulation(self):
        """Set up Isaac Sim environment with humanoid robot"""
        # Initialize the world
        self.world = World(stage_units_in_meters=1.0)

        # Get assets root path
        assets_root_path = get_assets_root_path()
        if assets_root_path is None:
            carb.log_error("Could not find Isaac Sim assets. Ensure nucleus server is running.")
            return False

        # Add humanoid robot to the stage
        # Using a generic humanoid for example
        humanoid_asset_path = assets_root_path + "/Isaac/Robots/Humanoid/humanoid_instanceable.usd"

        # Add robot to stage
        add_reference_to_stage(
            usd_path=humanoid_asset_path,
            prim_path="/World/Humanoid"
        )

        # Create articulation view for the robot
        self.humanoid_robot = self.world.scene.add(
            ArticulationView(prim_path="/World/Humanoid", name="humanoid_view")
        )

        # Set up camera view
        set_camera_view(eye=[2.0, 2.0, 1.5], target=[0.0, 0.0, 0.5])

        return True

    def initialize_robot(self):
        """Initialize robot positions and setup controller"""
        # Reset the world to initialize the robot
        self.world.reset()

        # Initialize joint positions to default home position
        default_positions = np.zeros(self.controller._num_dof)
        self.humanoid_robot.set_joint_positions(default_positions)

        print("Robot initialized with default positions")

    def control_robot_joints(self, joint_positions, joint_velocities=None):
        """Control robot joints using Python API"""
        if self.humanoid_robot is None:
            print("Robot not initialized, cannot control joints")
            return False

        # Apply joint positions
        self.humanoid_robot.set_joint_positions(joint_positions)

        # Optionally apply velocities if provided
        if joint_velocities is not None:
            self.humanoid_robot.set_joint_velocities(joint_velocities)

        print(f"Applied joint positions: {joint_positions[:6]}...")  # Show first 6 joints
        return True

    def get_robot_state(self):
        """Get current robot state"""
        if self.humanoid_robot is None:
            return None

        # Get joint positions
        joint_positions = self.humanoid_robot.get_joint_positions()

        # Get joint velocities
        joint_velocities = self.humanoid_robot.get_joint_velocities()

        # Get base position and orientation
        base_positions = self.humanoid_robot.get_world_poses()

        state = {
            'joint_positions': joint_positions,
            'joint_velocities': joint_velocities,
            'base_positions': base_positions[0],
            'base_orientations': base_positions[1]
        }

        return state

    def collect_sensor_data(self):
        """Collect sensor data from the simulation"""
        # In a real implementation, this would collect data from:
        # - IMU sensors
        # - Joint encoders
        # - Camera feeds
        # - LiDAR data
        # - Force/torque sensors

        # For this example, we'll simulate collecting data
        robot_state = self.get_robot_state()

        if robot_state is None:
            return None

        # Simulate sensor data
        sensor_data = {
            'imu': {
                'linear_acceleration': [0.1, 0.0, 9.8],  # Simulated gravity + small acceleration
                'angular_velocity': [0.0, 0.0, 0.0],     # No rotation initially
                'orientation': [0.0, 0.0, 0.0, 1.0]     # Identity quaternion
            },
            'joint_encoders': robot_state['joint_positions'].tolist(),
            'base_pose': {
                'position': robot_state['base_positions'].tolist(),
                'orientation': robot_state['base_orientations'].tolist()
            },
            'timestamp': carb.tokens.get_time()
        }

        return sensor_data

    def execute_control_loop(self):
        """Execute control loop to move the robot"""
        # Define a simple walking pattern (simplified for demonstration)
        walking_pattern = [
            [0.1, -0.1, 0.0, 0.0, 0.0, 0.0],  # First step
            [0.0, 0.0, 0.1, -0.1, 0.0, 0.0],  # Second step
            [-0.1, 0.1, 0.0, 0.0, 0.0, 0.0], # Return to center
            [0.0, 0.0, -0.1, 0.1, 0.0, 0.0]  # Return to center
        ]

        for step in walking_pattern:
            # Apply the control step
            # This is a simplified example - in reality, you'd calculate full joint positions
            current_positions = self.humanoid_robot.get_joint_positions()

            # Modify some key joints for walking simulation
            # For example, modify hip and knee joints for stepping motion
            new_positions = current_positions.copy()

            # Apply step pattern to leg joints (simplified)
            # This is a very basic example - real humanoid control is much more complex
            new_positions[2] += step[0]  # Left hip
            new_positions[3] += step[1]  # Left knee
            new_positions[8] += step[2]  # Right hip
            new_positions[9] += step[3]  # Right knee

            self.humanoid_robot.set_joint_positions(new_positions)

            # Step the world
            self.world.step(render=True)

            # Collect sensor data
            sensor_data = self.collect_sensor_data()
            print(f"Sensor data collected at step: {sensor_data['timestamp']}")

    def run_simulation(self, steps=1000):
        """Run the simulation for specified steps"""
        for i in range(steps):
            # Step the physics simulation
            self.world.step(render=True)

            # Occasionally collect sensor data and apply control
            if i % 10 == 0:
                sensor_data = self.collect_sensor_data()
                if sensor_data:
                    print(f"Step {i}: Collected sensor data")

            # Apply control commands periodically
            if i % 50 == 0 and i > 0:
                self.execute_control_loop()

def main():
    # Initialize Isaac Sim controller
    controller = IsaacSimPythonController()

    if controller.setup_simulation():
        # Initialize the robot
        controller.initialize_robot()

        # Run the simulation
        controller.run_simulation(steps=1000)

        print("Simulation completed")
    else:
        print("Failed to set up simulation")

if __name__ == "__main__":
    main()
```

For integration with ROS 2, you would use the ROS2 bridge extension:

```python
# ros2_integration_script.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
import time

class IsaacSimROS2Bridge(Node):
    def __init__(self):
        super().__init__('isaac_sim_ros2_bridge')

        # Publishers for sensor data
        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu/data', 10)

        # Subscriber for robot commands
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10
        )

        # Timer for publishing sensor data
        self.sensor_timer = self.create_timer(0.05, self.publish_sensor_data)  # 20Hz

        # Initialize Isaac Sim controller
        self.isaac_controller = IsaacSimPythonController()
        self.isaac_controller.setup_simulation()
        self.isaac_controller.initialize_robot()

        # Store command velocity
        self.linear_vel = 0.0
        self.angular_vel = 0.0

        self.get_logger().info('Isaac Sim ROS2 bridge initialized')

    def cmd_vel_callback(self, msg):
        """Handle velocity commands from ROS2"""
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

        # Apply the command to Isaac Sim (this would interface with the actual controller)
        self.apply_velocity_command(self.linear_vel, self.angular_vel)

    def apply_velocity_command(self, linear_x, angular_z):
        """Apply velocity command to Isaac Sim robot"""
        # In practice, this would translate the velocity command
        # to appropriate joint control commands for the humanoid
        print(f"Applying velocity command: linear={linear_x}, angular={angular_z}")

        # This is where you'd interface with Isaac Sim's Python API
        # to control the humanoid robot based on the velocity command
        pass

    def publish_sensor_data(self):
        """Publish sensor data from Isaac Sim to ROS2 topics"""
        # Get robot state from Isaac Sim
        robot_state = self.isaac_controller.get_robot_state()

        if robot_state:
            # Publish joint states
            joint_msg = JointState()
            joint_msg.header = Header()
            joint_msg.header.stamp = self.get_clock().now().to_msg()
            joint_msg.header.frame_id = 'base_link'

            # For this example, we'll use simulated joint names
            joint_names = [
                'left_hip', 'left_knee', 'left_ankle',
                'right_hip', 'right_knee', 'right_ankle',
                'left_shoulder', 'left_elbow', 'right_shoulder', 'right_elbow'
            ]

            joint_msg.name = joint_names
            joint_msg.position = robot_state['joint_positions'][:len(joint_names)]
            joint_msg.velocity = robot_state['joint_velocities'][:len(joint_names)]
            joint_msg.effort = [0.0] * len(joint_names)  # Placeholder

            self.joint_state_pub.publish(joint_msg)

            # Publish IMU data
            imu_msg = Imu()
            imu_msg.header = Header()
            imu_msg.header.stamp = self.get_clock().now().to_msg()
            imu_msg.header.frame_id = 'imu_link'

            # Set orientation (simplified)
            imu_msg.orientation.x = 0.0
            imu_msg.orientation.y = 0.0
            imu_msg.orientation.z = 0.0
            imu_msg.orientation.w = 1.0

            # Set angular velocity
            imu_msg.angular_velocity.x = 0.0
            imu_msg.angular_velocity.y = 0.0
            imu_msg.angular_velocity.z = self.angular_vel

            # Set linear acceleration
            imu_msg.linear_acceleration.x = self.linear_vel
            imu_msg.linear_acceleration.y = 0.0
            imu_msg.linear_acceleration.z = 9.81  # Gravity

            self.imu_pub.publish(imu_msg)

def main(args=None):
    rclpy.init(args=args)
    bridge = IsaacSimROS2Bridge()

    try:
        rclpy.spin(bridge)
    except KeyboardInterrupt:
        bridge.get_logger().info('Isaac Sim ROS2 bridge stopped by user')
    finally:
        bridge.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Test Navigation in Complex Environments</summary>

```python
# complex_navigation_test.py
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.msg import Path, OccupancyGrid
from visualization_msgs.msg import Marker, MarkerArray
from std_msgs.msg import ColorRGBA
import math
import numpy as np

class ComplexNavigationTester(Node):
    def __init__(self):
        super().__init__('complex_navigation_tester')

        # Publishers
        self.goal_pub = self.create_publisher(PoseStamped, 'goal_pose', 10)
        self.path_marker_pub = self.create_publisher(Marker, 'path_visualization', 10)
        self.obstacle_marker_pub = self.create_publisher(MarkerArray, 'obstacle_visualization', 10)

        # Subscribers
        self.path_sub = self.create_subscription(Path, 'plan', self.path_callback, 10)
        self.map_sub = self.create_subscription(OccupancyGrid, 'map', self.map_callback, 10)

        # Parameters
        self.declare_parameter('test_scenario', 'maze')
        self.declare_parameter('navigation_frequency', 1.0)
        self.declare_parameter('obstacle_density', 0.3)

        self.test_scenario = self.get_parameter('test_scenario').value
        nav_freq = self.get_parameter('navigation_frequency').value

        # Timer for sending navigation goals
        self.nav_timer = self.create_timer(1.0/nav_freq, self.send_navigation_goals)

        # Internal state
        self.paths_received = []
        self.current_map = None
        self.goal_count = 0
        self.max_goals = 5  # Number of goals to test

        # Define test environments
        self.test_environments = {
            'maze': self.create_maze_environment,
            'corridor': self.create_corridor_environment,
            'cluttered': self.create_cluttered_environment,
            'narrow_passage': self.create_narrow_passage_environment
        }

        self.get_logger().info('Complex navigation tester initialized')

    def map_callback(self, msg):
        """Handle map updates"""
        self.current_map = msg
        self.get_logger().info(f'Received map with resolution: {msg.info.resolution}')

    def path_callback(self, msg):
        """Handle path updates from Nav2"""
        self.paths_received.append(msg)
        path_length = self.calculate_path_length(msg)
        self.get_logger().info(f'Received path with {len(msg.poses)} waypoints, length: {path_length:.2f}m')

    def calculate_path_length(self, path_msg):
        """Calculate total path length"""
        if len(path_msg.poses) < 2:
            return 0.0

        total_length = 0.0
        for i in range(1, len(path_msg.poses)):
            prev_pose = path_msg.poses[i-1].pose.position
            curr_pose = path_msg.poses[i].pose.position

            dx = curr_pose.x - prev_pose.x
            dy = curr_pose.y - prev_pose.y
            dist = math.sqrt(dx*dx + dy*dy)
            total_length += dist

        return total_length

    def create_maze_environment(self):
        """Create maze-like obstacles"""
        # In a real implementation, this would modify the map or create obstacles in Isaac Sim
        # For this example, we'll define obstacle positions
        obstacles = []

        # Create maze walls
        for x in range(-5, 6):
            for y in [-4, -2, 0, 2, 4]:  # Horizontal walls
                obstacles.append(Point(x=x, y=y, z=0.0))

        for x in [-4, -2, 0, 2, 4]:
            for y in range(-5, 6):  # Vertical walls
                obstacles.append(Point(x=x, y=y, z=0.0))

        return obstacles

    def create_corridor_environment(self):
        """Create corridor environment with narrow passages"""
        obstacles = []

        # Create walls on both sides of a corridor
        for y in range(-10, 11):
            obstacles.append(Point(x=-3, y=y, z=0.0))
            obstacles.append(Point(x=3, y=y, z=0.0))

        # Add some obstacles in the corridor
        for x in [-2, 0, 2]:
            for y in range(-8, -5):
                obstacles.append(Point(x=x, y=y, z=0.0))

        return obstacles

    def create_cluttered_environment(self):
        """Create environment with scattered obstacles"""
        obstacles = []

        # Randomly scatter obstacles
        obstacle_density = self.get_parameter('obstacle_density').value
        for x in range(-10, 11):
            for y in range(-10, 11):
                if math.sqrt(x*x + y*y) > 2:  # Keep center clear
                    if np.random.random() < obstacle_density:
                        obstacles.append(Point(x=x, y=y, z=0.0))

        return obstacles

    def create_narrow_passage_environment(self):
        """Create environment with narrow passages to test navigation"""
        obstacles = []

        # Create walls with gaps
        for y in range(-10, 11):
            if abs(y) != 3:  # Leave gaps at y = -3 and y = 3
                obstacles.append(Point(x=-5, y=y, z=0.0))
                obstacles.append(Point(x=5, y=y, z=0.0))

        # Add vertical barriers with small gaps
        for x in range(-4, 5):
            if abs(x) > 2:  # Leave center gap
                obstacles.append(Point(x=x, y=-3, z=0.0))
                obstacles.append(Point(x=x, y=3, z=0.0))

        return obstacles

    def visualize_obstacles(self, obstacles):
        """Visualize obstacles in RViz"""
        marker_array = MarkerArray()

        for i, obstacle in enumerate(obstacles):
            marker = Marker()
            marker.header.frame_id = 'map'
            marker.header.stamp = self.get_clock().now().to_msg()
            marker.ns = 'obstacles'
            marker.id = i
            marker.type = Marker.CUBE
            marker.action = Marker.ADD

            marker.pose.position = obstacle
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.5
            marker.scale.y = 0.5
            marker.scale.z = 1.0
            marker.color.r = 0.8
            marker.color.g = 0.2
            marker.color.b = 0.2
            marker.color.a = 0.8

            marker_array.markers.append(marker)

        self.obstacle_marker_pub.publish(marker_array)

    def send_navigation_goals(self):
        """Send navigation goals for testing"""
        if self.goal_count >= self.max_goals:
            self.get_logger().info('Completed all navigation tests')
            return

        # Get current environment obstacles
        if self.test_scenario in self.test_environments:
            obstacles = self.test_environments[self.test_scenario]()
            self.visualize_obstacles(obstacles)

        # Define test goals based on scenario
        goals = {
            'maze': [(5.0, 5.0), (-5.0, -5.0), (0.0, 0.0)],
            'corridor': [(0.0, 8.0), (0.0, -8.0), (2.0, 6.0)],
            'cluttered': [(3.0, 4.0), (-2.0, 6.0), (5.0, -3.0)],
            'narrow_passage': [(0.0, 8.0), (0.0, -8.0), (4.0, 0.0)]
        }

        if self.test_scenario in goals and self.goal_count < len(goals[self.test_scenario]):
            goal_x, goal_y = goals[self.test_scenario][self.goal_count]

            goal_msg = PoseStamped()
            goal_msg.header.stamp = self.get_clock().now().to_msg()
            goal_msg.header.frame_id = 'map'
            goal_msg.pose.position.x = goal_x
            goal_msg.pose.position.y = goal_y
            goal_msg.pose.position.z = 0.0
            goal_msg.pose.orientation.w = 1.0

            self.goal_pub.publish(goal_msg)
            self.get_logger().info(f'Sent navigation goal #{self.goal_count + 1}: ({goal_x}, {goal_y})')

            self.goal_count += 1
        else:
            self.nav_timer.cancel()  # Stop sending goals
            self.evaluate_performance()

    def evaluate_performance(self):
        """Evaluate navigation performance"""
        if not self.paths_received:
            self.get_logger().warn('No paths received for evaluation')
            return

        # Calculate performance metrics
        total_paths = len(self.paths_received)
        total_length = sum(self.calculate_path_length(path) for path in self.paths_received)
        avg_length = total_length / total_paths if total_paths > 0 else 0.0

        self.get_logger().info(f'Navigation performance evaluation:')
        self.get_logger().info(f'  - Paths completed: {total_paths}')
        self.get_logger().info(f'  - Average path length: {avg_length:.2f}m')
        self.get_logger().info(f'  - Success rate: {total_paths}/{self.max_goals} goals')

        # In a real system, you would also measure:
        # - Time to compute path
        # - Execution time
        # - Deviation from planned path
        # - Collision avoidance effectiveness

def main(args=None):
    rclpy.init(args=args)
    tester = ComplexNavigationTester()

    try:
        rclpy.spin(tester)
    except KeyboardInterrupt:
        tester.get_logger().info('Complex navigation tester stopped by user')
    finally:
        tester.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

Launch file for the complete navigation test:

```python
# launch/navigation_test_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time if true'
    )

    test_scenario = DeclareLaunchArgument(
        'test_scenario',
        default_value='maze',
        description='Test scenario: maze, corridor, cluttered, or narrow_passage'
    )

    # Isaac Sim node (would be configured separately)
    isaac_sim_node = Node(
        package='my_humonoid_robot',
        executable='isaac_sim_bridge',
        name='isaac_sim_bridge',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'scenario': LaunchConfiguration('test_scenario')}
        ],
        output='screen'
    )

    # Complex navigation tester
    navigation_tester = Node(
        package='my_humonoid_robot',
        executable='complex_navigation_tester',
        name='complex_navigation_tester',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'test_scenario': LaunchConfiguration('test_scenario')}
        ],
        output='screen'
    )

    # RViz for visualization
    rviz_config = os.path.join(
        get_package_share_directory('my_humonoid_robot'),
        'rviz',
        'navigation_test.rviz'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output='screen'
    )

    return LaunchDescription([
        use_sim_time,
        test_scenario,
        isaac_sim_node,
        navigation_tester,
        rviz_node
    ])
```

</details>

## 1.10 Mini-Project: Simulate a Humanoid Robot Performing VSLAM with Autonomous Navigation

Create a complete simulation scenario where a humanoid robot performs VSLAM to map an unknown environment and then uses the Nav2 stack for autonomous navigation. The project should include:

1. A humanoid robot with appropriate VSLAM sensors (stereo cameras, LiDAR)
2. An unknown environment that the robot must map using VSLAM algorithms
3. Integration of the Nav2 navigation stack for autonomous path planning
4. Real-time visualization of the mapping process and navigation execution
5. Performance metrics for both VSLAM accuracy and navigation efficiency
6. Analysis of how well the robot can navigate in the mapped environment

The project should demonstrate the complete pipeline from sensor data acquisition through mapping to autonomous navigation, showcasing the power of Isaac Sim for developing complex robotic systems.

## 1.11 Summary

This chapter has introduced the fundamental concepts of NVIDIA Isaac Sim for humanoid robot simulation, with a focus on VSLAM and Nav2 integration. Isaac Sim provides a powerful platform for developing and testing complex robotic algorithms in a photorealistic, physics-accurate simulation environment.

Key concepts covered include:
- Isaac Sim setup and environment configuration for humanoid robots
- Physics simulation with proper collision detection and rigid-body dynamics
- VSLAM implementation using camera and LiDAR sensors in simulation
- Nav2 navigation stack integration for autonomous navigation
- Python API usage for simulation control and ROS 2 integration

The examples and exercises provided demonstrate practical applications of these concepts, preparing you to create sophisticated simulation environments for humanoid robot development and research. Isaac Sim's combination of realistic physics, high-quality rendering, and ROS 2 integration makes it an ideal platform for advancing humanoid robotics research and development.