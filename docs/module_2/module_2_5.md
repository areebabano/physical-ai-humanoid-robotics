---
title: "Module 2.5 - Chapter 5: Simulation Integration with ROS 2"
sidebar_position: 5
---

# Module 2.5 - Simulation Integration with ROS 2

## Overview

This chapter covers the integration of Gazebo simulation with ROS 2, focusing on creating seamless workflows for humanoid robot development. We'll explore how to connect simulated robots to ROS 2, implement control interfaces, manage simulation states, and create effective development pipelines that bridge simulation and real hardware.

## Learning Objectives

By the end of this chapter, you will be able to:
- Integrate Gazebo simulation with ROS 2 using gazebo_ros2_control
- Implement proper control interfaces for humanoid robots in simulation
- Manage simulation states and transitions
- Create launch files for complex simulation scenarios
- Develop effective sim-to-real transfer strategies
- Debug and troubleshoot simulation-ROS 2 integration issues

## 5.1 Gazebo-ROS 2 Integration Architecture

### 5.1.1 Overview of Integration Components

The integration between Gazebo and ROS 2 involves several key components that work together:

```xml
<!-- Example of complete integration configuration in URDF -->
<?xml version="1.0" ?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Robot description -->
  <link name="base_link">
    <inertial>
      <mass value="10.0" />
      <origin xyz="0 0 0" rpy="0 0 0" />
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="0.3 0.2 0.5" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="0.3 0.2 0.5" />
      </geometry>
    </collision>
  </link>

  <!-- Example joint -->
  <joint name="hip_joint" type="revolute">
    <parent link="base_link" />
    <child link="thigh" />
    <origin xyz="0 0 -0.25" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1" />
  </joint>

  <link name="thigh">
    <inertial>
      <mass value="2.0" />
      <origin xyz="0 0 -0.2" rpy="0 0 0" />
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.02" />
    </inertial>
  </link>

  <!-- ROS2 Control interface -->
  <ros2_control name="GazeboSystem" type="system">
    <hardware>
      <plugin>gazebo_ros2_control/GazeboSystem</plugin>
    </hardware>
    <joint name="hip_joint">
      <command_interface name="position">
        <param name="min">-1.57</param>
        <param name="max">1.57</param>
      </command_interface>
      <command_interface name="velocity">
        <param name="min">-1.0</param>
        <param name="max">1.0</param>
      </command_interface>
      <command_interface name="effort">
        <param name="min">-100</param>
        <param name="max">100</param>
      </command_interface>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>
  </ros2_control>

  <!-- Gazebo plugin for ROS control -->
  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <parameters>$(find my_humanoid_package)/config/hardware_control.yaml</parameters>
      <ros>
        <namespace>/humanoid_robot</namespace>
      </ros>
    </plugin>
  </gazebo>
</robot>
```

### 5.1.2 Integration Architecture Components

```python
# Architecture overview as a Python class structure
class GazeboROS2Integration:
    """High-level overview of Gazebo-ROS 2 integration components"""

    def __init__(self):
        self.components = {
            'gazebo_ros2_control': {
                'description': 'Bridge between Gazebo and ROS 2 control',
                'function': 'Translates ROS 2 control commands to Gazebo physics'
            },
            'ros2_control': {
                'description': 'ROS 2 control framework',
                'function': 'Manages hardware interfaces and controllers'
            },
            'gazebo_ros_pkgs': {
                'description': 'ROS 2 interface to Gazebo',
                'function': 'Provides ROS 2 services for spawning, deleting models'
            },
            'controller_manager': {
                'description': 'Manages ROS 2 controllers',
                'function': 'Loads, starts, stops controllers'
            }
        }

    def get_integration_flow(self):
        """Return the data flow for integration"""
        return [
            "ROS 2 Controller sends commands",
            "Controller Manager routes commands",
            "ros2_control translates to hardware interface",
            "gazebo_ros2_control plugin applies to Gazebo physics",
            "Gazebo updates robot state",
            "State propagates back through the chain to ROS 2"
        ]

# Example usage
integration = GazeboROS2Integration()
print("Integration Components:", integration.components.keys())
print("Data Flow:", integration.get_integration_flow())
```

## 5.2 Setting Up the Integration

### 5.2.1 Installing Required Packages

```bash
# Install gazebo_ros2_control package
sudo apt update
sudo apt install ros-humble-gazebo-ros2-control
sudo apt install ros-humble-gazebo-ros2-control-plugins

# Install ros2_control related packages
sudo apt install ros-humble-ros2-control
sudo apt install ros-humble-ros2-controllers
sudo apt install ros-humble-controller-manager
sudo apt install ros-humble-joint-state-broadcaster
sudo apt install ros-humble-velocity-controllers
sudo apt install ros-humble-position-controllers
```

### 5.2.2 Hardware Control Configuration

Create `config/hardware_control.yaml`:

```yaml
# Controller manager configuration
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    # Joint State Broadcaster - essential for publishing joint states
    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    # Example controllers for humanoid robot
    left_leg_controller:
      type: position_controllers/JointGroupPositionController

    right_leg_controller:
      type: position_controllers/JointGroupPositionController

    left_arm_controller:
      type: position_controllers/JointGroupPositionController

    right_arm_controller:
      type: position_controllers/JointGroupPositionController

    head_controller:
      type: position_controllers/JointGroupPositionController

# Left leg controller configuration
left_leg_controller:
  ros__parameters:
    joints:
      - left_hip_joint
      - left_knee_joint
      - left_ankle_joint

# Right leg controller configuration
right_leg_controller:
  ros__parameters:
    joints:
      - right_hip_joint
      - right_knee_joint
      - right_ankle_joint

# Left arm controller configuration
left_arm_controller:
  ros__parameters:
    joints:
      - left_shoulder_pitch
      - left_shoulder_roll
      - left_elbow_joint

# Right arm controller configuration
right_arm_controller:
  ros__parameters:
    joints:
      - right_shoulder_pitch
      - right_shoulder_roll
      - right_elbow_joint

# Head controller configuration
head_controller:
  ros__parameters:
    joints:
      - neck_yaw
      - neck_pitch
```

### 5.2.3 Robot State Publisher Configuration

Create `launch/simulation_with_control.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_name = LaunchConfiguration('world_name', default='humanoid_world')
    robot_name = LaunchConfiguration('robot_name', default='humanoid_robot')

    # Package locations
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    pkg_robot_description = FindPackageShare('my_humanoid_package')
    pkg_controller_manager = FindPackageShare('controller_manager')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([
                pkg_robot_description, 'worlds', world_name
            ]),
            'verbose': 'false',
        }.items()
    )

    # Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': PathJoinSubstitution([
                pkg_robot_description, 'urdf', 'humanoid.urdf'
            ])}
        ]
    )

    # Spawn entity in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', robot_name,
            '-x', '0',
            '-y', '0',
            '-z', '1.0',
            '-R', '0',
            '-P', '0',
            '-Y', '0'
        ],
        output='screen'
    )

    # Load controllers
    load_joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    load_left_leg_controller = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['left_leg_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    load_right_leg_controller = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['right_leg_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    load_left_arm_controller = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['left_arm_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    load_right_arm_controller = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['right_arm_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    load_head_controller = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['head_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    # Create launch description
    ld = LaunchDescription()

    # Add launch arguments
    ld.add_action(DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    ))

    ld.add_action(DeclareLaunchArgument(
        'world_name',
        default_value='empty_world.sdf',
        description='Choose one of the world files from `/my_humanoid_package/worlds`'
    ))

    ld.add_action(DeclareLaunchArgument(
        'robot_name',
        default_value='humanoid_robot',
        description='Name of the robot to spawn in Gazebo'
    ))

    # Add actions
    ld.add_action(gazebo)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_entity)

    # Load controllers after spawn
    ld.add_action(load_joint_state_broadcaster)
    ld.add_action(load_left_leg_controller)
    ld.add_action(load_right_leg_controller)
    ld.add_action(load_left_arm_controller)
    ld.add_action(load_right_arm_controller)
    ld.add_action(load_head_controller)

    return ld
```

## 5.3 Control Interface Implementation

### 5.3.1 Joint Control Implementation

Create `scripts/joint_control_node.py`:

```python
#!/usr/bin/env python3

"""
Joint control node for humanoid robot in simulation
Implements position, velocity, and effort control interfaces
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Header
from builtin_interfaces.msg import Duration
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from controller_manager_msgs.srv import SwitchController
import time
import math
from collections import deque


class HumanoidJointController(Node):
    def __init__(self):
        super().__init__('humanoid_joint_controller')

        # Publishers
        self.joint_trajectory_pub = self.create_publisher(
            JointTrajectory, '/left_leg_controller/joint_trajectory', 10
        )
        self.status_pub = self.create_publisher(
            JointTrajectoryControllerState, '/left_leg_controller/state', 10
        )

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )

        # Service clients
        self.controller_switch_client = self.create_client(
            SwitchController, '/controller_manager/switch_controller'
        )

        # Internal state
        self.joint_positions = {}
        self.joint_velocities = {}
        self.joint_efforts = {}
        self.command_history = deque(maxlen=100)  # For monitoring

        # Control parameters
        self.control_freq = 50  # Hz
        self.dt = 1.0 / self.control_freq

        # Control timer
        self.control_timer = self.create_timer(
            self.dt, self.control_loop
        )

        # Test sequence
        self.test_sequence = [
            self.test_standing_pose,
            self.test_simple_movement,
            self.test_trajectory_following
        ]
        self.current_test = 0
        self.test_start_time = time.time()

        self.get_logger().info('Humanoid joint controller initialized')

    def joint_state_callback(self, msg):
        """Update joint state information"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]
            if i < len(msg.velocity):
                self.joint_velocities[name] = msg.velocity[i]
            if i < len(msg.effort):
                self.joint_efforts[name] = msg.effort[i]

    def control_loop(self):
        """Main control loop"""
        # Execute current test
        if self.current_test < len(self.test_sequence):
            test_func = self.test_sequence[self.current_test]
            if test_func():
                self.current_test += 1
                self.test_start_time = time.time()
                self.get_logger().info(f'Test {self.current_test} completed')
        else:
            # All tests completed, can implement continuous behavior here
            self.execute_default_behavior()

    def test_standing_pose(self):
        """Test moving to standing pose"""
        t = time.time() - self.test_start_time
        if t > 5.0:  # 5 seconds
            return True  # Test completed

        # Define standing pose for left leg
        standing_pose = {
            'left_hip_joint': 0.0,
            'left_knee_joint': 0.0,
            'left_ankle_joint': 0.0
        }

        self.send_trajectory_command('left_leg_controller', standing_pose, duration=2.0)
        return False

    def test_simple_movement(self):
        """Test simple joint movements"""
        t = time.time() - self.test_start_time
        if t > 10.0:  # 10 seconds
            return True

        # Create oscillating movement
        hip_pos = math.sin(t * 0.5) * 0.2
        knee_pos = math.sin(t * 0.5 + math.pi/2) * 0.1
        ankle_pos = math.sin(t * 0.5 + math.pi) * 0.05

        joint_positions = {
            'left_hip_joint': hip_pos,
            'left_knee_joint': knee_pos,
            'left_ankle_joint': ankle_pos
        }

        self.send_trajectory_command('left_leg_controller', joint_positions, duration=0.5)
        return False

    def test_trajectory_following(self):
        """Test following a more complex trajectory"""
        t = time.time() - self.test_start_time
        if t > 15.0:  # 15 seconds
            return True

        # Create a circular trajectory in joint space
        phase = t * 0.3  # 0.3 Hz
        hip_pos = 0.2 * math.sin(phase)
        knee_pos = 0.1 * math.cos(phase * 1.5)  # Different frequency
        ankle_pos = 0.05 * math.sin(phase * 2)  # Even different frequency

        joint_positions = {
            'left_hip_joint': hip_pos,
            'left_knee_joint': knee_pos,
            'left_ankle_joint': ankle_pos
        }

        self.send_trajectory_command('left_leg_controller', joint_positions, duration=0.2)
        return False

    def execute_default_behavior(self):
        """Default behavior when tests are completed"""
        # For now, just maintain current position
        pass

    def send_trajectory_command(self, controller_name, joint_positions, duration=1.0):
        """Send a trajectory command to a specific controller"""
        msg = JointTrajectory()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = list(joint_positions.keys())

        point = JointTrajectoryPoint()
        point.positions = list(joint_positions.values())
        point.time_from_start = Duration(sec=int(duration), nanosec=int((duration % 1) * 1e9))

        msg.points = [point]

        # Publish to the appropriate controller topic
        if controller_name == 'left_leg_controller':
            self.joint_trajectory_pub.publish(msg)
        # Add other controllers as needed

        # Store command in history for monitoring
        self.command_history.append({
            'time': time.time(),
            'controller': controller_name,
            'positions': joint_positions
        })

    def get_controller_state(self):
        """Get current controller state for publishing"""
        state = JointTrajectoryControllerState()
        state.header.stamp = self.get_clock().now().to_msg()
        state.joint_names = list(self.joint_positions.keys())
        state.actual.positions = list(self.joint_positions.values())
        state.actual.velocities = list(self.joint_velocities.values())
        state.actual.accelerations = [0.0] * len(self.joint_positions)  # Simplified

        # For this example, desired = actual (no trajectory tracking)
        state.desired = state.actual
        state.error.positions = [0.0] * len(self.joint_positions)  # Simplified
        state.error.velocities = [0.0] * len(self.joint_positions)
        state.error.accelerations = [0.0] * len(self.joint_positions)

        return state

    def switch_controller(self, start_controllers, stop_controllers):
        """Switch controllers on/off"""
        if not self.controller_switch_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().error('Controller manager service not available')
            return

        request = SwitchController.Request()
        request.start_controllers = start_controllers
        request.stop_controllers = stop_controllers
        request.strictness = SwitchController.Request.BEST_EFFORT

        future = self.controller_switch_client.call_async(request)
        return future


def main(args=None):
    rclpy.init(args=args)

    node = HumanoidJointController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 5.3.2 Advanced Control Implementation

Create `scripts/advanced_control_node.py`:

```python
#!/usr/bin/env python3

"""
Advanced control node for humanoid robot simulation
Implements model predictive control, balance control, and gait generation
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Float32, Bool
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import numpy as np
import math
import time
from collections import deque


class AdvancedHumanoidController(Node):
    def __init__(self):
        super().__init__('advanced_humanoid_controller')

        # Publishers
        self.left_leg_pub = self.create_publisher(
            JointTrajectory, '/left_leg_controller/joint_trajectory', 10
        )
        self.right_leg_pub = self.create_publisher(
            JointTrajectory, '/right_leg_controller/joint_trajectory', 10
        )
        self.left_arm_pub = self.create_publisher(
            JointTrajectory, '/left_arm_controller/joint_trajectory', 10
        )
        self.right_arm_pub = self.create_publisher(
            JointTrajectory, '/right_arm_controller/joint_trajectory', 10
        )
        self.head_pub = self.create_publisher(
            JointTrajectory, '/head_controller/joint_trajectory', 10
        )
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.balance_pub = self.create_publisher(Float32, '/balance_score', 10)

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )
        self.imu_sub = self.create_subscription(
            Imu, '/imu/data', self.imu_callback, 10
        )
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel_input', self.cmd_vel_input_callback, 10
        )

        # Internal state
        self.joint_positions = {}
        self.joint_velocities = {}
        self.orientation = None
        self.angular_velocity = None
        self.linear_acceleration = None
        self.desired_velocity = Twist()

        # Control parameters
        self.control_freq = 100  # Hz
        self.dt = 1.0 / self.control_freq
        self.balance_threshold = 0.3  # Radians

        # Walking gait parameters
        self.step_height = 0.05  # meters
        self.step_length = 0.3   # meters
        self.step_duration = 1.0 # seconds
        self.gait_phase = 0.0

        # Balance control parameters
        self.balance_kp = 5.0
        self.balance_kd = 1.0

        # Control timer
        self.control_timer = self.create_timer(
            self.dt, self.control_loop
        )

        # Data history for control algorithms
        self.orientation_history = deque(maxlen=50)
        self.position_history = deque(maxlen=50)

        self.get_logger().info('Advanced humanoid controller initialized')

    def joint_state_callback(self, msg):
        """Update joint state information"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]
            if i < len(msg.velocity):
                self.joint_velocities[name] = msg.velocity[i]

    def imu_callback(self, msg):
        """Update IMU information"""
        self.orientation = [
            msg.orientation.w,
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z
        ]
        self.angular_velocity = [
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ]
        self.linear_acceleration = [
            msg.linear_acceleration.x,
            msg.linear_acceleration.y,
            msg.linear_acceleration.z
        ]

        # Store in history for filtering
        if self.orientation:
            self.orientation_history.append(self.orientation.copy())

    def cmd_vel_input_callback(self, msg):
        """Update desired velocity"""
        self.desired_velocity = msg

    def control_loop(self):
        """Main control loop with multiple control layers"""
        # Calculate balance metrics
        balance_score = self.calculate_balance_score()
        self.balance_pub.publish(Float32(data=balance_score))

        # Emergency balance correction if robot is falling
        if balance_score > self.balance_threshold:
            self.emergency_balance_correction()
            return

        # Normal control modes
        if abs(self.desired_velocity.linear.x) > 0.01 or abs(self.desired_velocity.angular.z) > 0.01:
            # Walking mode
            self.execute_walking_gait()
        else:
            # Standing mode
            self.execute_standing_control()

        # Arm control (simple default positions)
        self.execute_arm_control()

        # Head control (look forward)
        self.execute_head_control()

    def calculate_balance_score(self):
        """Calculate balance score from IMU data"""
        if not self.orientation:
            return 0.0

        # Convert quaternion to roll and pitch
        w, x, y, z = self.orientation

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        pitch = math.asin(sinp)

        # Balance score is the magnitude of tilt
        balance_score = abs(roll) + abs(pitch)
        return balance_score

    def emergency_balance_correction(self):
        """Emergency control to prevent falling"""
        self.get_logger().warn('Emergency balance correction activated!')

        # Move to safe standing position
        left_leg_pos = {
            'left_hip_joint': 0.0,
            'left_knee_joint': 0.0,
            'left_ankle_joint': 0.0
        }
        right_leg_pos = {
            'right_hip_joint': 0.0,
            'right_knee_joint': 0.0,
            'right_ankle_joint': 0.0
        }

        self.send_leg_trajectory('left', left_leg_pos, duration=0.5)
        self.send_leg_trajectory('right', right_leg_pos, duration=0.5)

    def execute_walking_gait(self):
        """Execute walking gait based on desired velocity"""
        current_time = time.time()
        self.gait_phase = (current_time / self.step_duration) % 2.0

        # Calculate step parameters based on desired velocity
        speed_factor = min(abs(self.desired_velocity.linear.x) / 0.5, 1.0)  # Normalize to 0-1
        step_length = self.step_length * speed_factor
        step_height = self.step_height * speed_factor

        # Generate walking pattern
        left_foot_pos, right_foot_pos = self.generate_step_pattern(
            self.gait_phase, step_length, step_height
        )

        # Convert foot positions to joint angles (simplified inverse kinematics)
        left_leg_angles = self.inverse_kinematics_leg(left_foot_pos)
        right_leg_angles = self.inverse_kinematics_leg(right_foot_pos)

        # Add balance corrections
        balance_correction = self.calculate_balance_correction()
        left_leg_angles = self.apply_balance_correction(left_leg_angles, balance_correction)
        right_leg_angles = self.apply_balance_correction(right_leg_angles, balance_correction)

        # Publish trajectories
        self.send_leg_trajectory('left', left_leg_angles, duration=0.1)
        self.send_leg_trajectory('right', right_leg_angles, duration=0.1)

    def generate_step_pattern(self, phase, step_length, step_height):
        """Generate foot step pattern based on gait phase"""
        # Phase 0-1: Left foot swings forward, right foot supports
        # Phase 1-2: Right foot swings forward, left foot supports

        if phase < 1.0:  # Left swing phase
            # Left foot trajectory
            left_x = step_length * math.sin(phase * math.pi) / 2
            left_z = step_height * math.sin(phase * math.pi) if phase < 0.5 else 0
            left_foot_pos = [left_x, 0, left_z]

            # Right foot stays in place
            right_foot_pos = [0, 0, 0]
        else:  # Right swing phase
            # Right foot trajectory
            right_x = step_length * math.sin((phase - 1) * math.pi) / 2
            right_z = step_height * math.sin((phase - 1) * math.pi) if phase < 1.5 else 0
            right_foot_pos = [right_x, 0, right_z]

            # Left foot stays in place
            left_foot_pos = [0, 0, 0]

        return left_foot_pos, right_foot_pos

    def inverse_kinematics_leg(self, foot_position):
        """Simple inverse kinematics for 3-DOF leg"""
        x, y, z = foot_position

        # Simplified 3-DOF inverse kinematics
        # Leg length calculation
        target_dist = math.sqrt(x*x + z*z)
        leg_length = 0.4  # Sum of thigh and shin lengths

        # Check if target is reachable
        if target_dist > leg_length * 0.9:  # 90% of max reach
            target_dist = leg_length * 0.9

        # Hip angle (assuming 2D movement in x-z plane)
        hip_angle = math.atan2(x, z) if z != 0 else 0

        # Knee angle using law of cosines
        cos_knee = (target_dist**2 - leg_length**2) / (2 * leg_length**2)
        cos_knee = max(-1, min(1, cos_knee))  # Clamp to valid range
        knee_angle = math.acos(cos_knee)

        # Ankle angle to maintain foot orientation
        ankle_angle = -hip_angle - knee_angle

        return {
            'hip_joint': hip_angle,
            'knee_joint': knee_angle,
            'ankle_joint': ankle_angle
        }

    def calculate_balance_correction(self):
        """Calculate balance correction based on IMU data"""
        if not self.orientation:
            return {'roll': 0.0, 'pitch': 0.0}

        w, x, y, z = self.orientation

        # Calculate roll and pitch
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        sinp = 2 * (w * y - z * x)
        pitch = math.asin(sinp)

        # Calculate correction based on PD control
        roll_correction = -self.balance_kp * roll
        pitch_correction = -self.balance_kp * pitch

        return {'roll': roll_correction, 'pitch': pitch_correction}

    def apply_balance_correction(self, joint_angles, correction):
        """Apply balance correction to joint angles"""
        corrected_angles = joint_angles.copy()

        # Apply corrections based on the joint type
        # This is a simplified example - real implementation would be more complex
        if 'hip_joint' in corrected_angles:
            corrected_angles['hip_joint'] += correction['pitch'] * 0.5
        if 'ankle_joint' in corrected_angles:
            corrected_angles['ankle_joint'] += correction['pitch'] * 0.3

        return corrected_angles

    def execute_standing_control(self):
        """Execute standing balance control"""
        # Calculate balance corrections
        balance_correction = self.calculate_balance_correction()

        # Default standing position with balance corrections
        standing_pos = {
            'hip_joint': balance_correction['pitch'] * 0.1,
            'knee_joint': 0.0,
            'ankle_joint': balance_correction['pitch'] * 0.1
        }

        # Apply to both legs
        self.send_leg_trajectory('left', standing_pos, duration=0.1)
        self.send_leg_trajectory('right', standing_pos, duration=0.1)

    def execute_arm_control(self):
        """Execute arm control - maintain default positions"""
        left_arm_pos = {
            'left_shoulder_pitch': 0.0,
            'left_shoulder_roll': 0.0,
            'left_elbow_joint': 0.0
        }
        right_arm_pos = {
            'right_shoulder_pitch': 0.0,
            'right_shoulder_roll': 0.0,
            'right_elbow_joint': 0.0
        }

        self.send_arm_trajectory('left', left_arm_pos, duration=0.5)
        self.send_arm_trajectory('right', right_arm_pos, duration=0.5)

    def execute_head_control(self):
        """Execute head control - look forward"""
        head_pos = {
            'neck_yaw': 0.0,
            'neck_pitch': 0.0
        }
        self.send_head_trajectory(head_pos, duration=0.5)

    def send_leg_trajectory(self, side, joint_positions, duration=1.0):
        """Send trajectory command to leg controller"""
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = [f"{side}_{joint}" for joint in joint_positions.keys()]

        point = JointTrajectoryPoint()
        point.positions = list(joint_positions.values())
        point.time_from_start = Duration(
            sec=int(duration),
            nanosec=int((duration % 1) * 1e9)
        )

        msg.points = [point]

        if side == 'left':
            self.left_leg_pub.publish(msg)
        else:
            self.right_leg_pub.publish(msg)

    def send_arm_trajectory(self, side, joint_positions, duration=1.0):
        """Send trajectory command to arm controller"""
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = [f"{side}_{joint}" for joint in joint_positions.keys()]

        point = JointTrajectoryPoint()
        point.positions = list(joint_positions.values())
        point.time_from_start = Duration(
            sec=int(duration),
            nanosec=int((duration % 1) * 1e9)
        )

        msg.points = [point]

        if side == 'left':
            self.left_arm_pub.publish(msg)
        else:
            self.right_arm_pub.publish(msg)

    def send_head_trajectory(self, joint_positions, duration=1.0):
        """Send trajectory command to head controller"""
        msg = JointTrajectory()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.joint_names = list(joint_positions.keys())

        point = JointTrajectoryPoint()
        point.positions = list(joint_positions.values())
        point.time_from_start = Duration(
            sec=int(duration),
            nanosec=int((duration % 1) * 1e9)
        )

        msg.points = [point]

        self.head_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = AdvancedHumanoidController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 5.4 Simulation State Management

### 5.4.1 Simulation State Control

Create `scripts/simulation_state_manager.py`:

```python
#!/usr/bin/env python3

"""
Simulation state manager for humanoid robot
Manages simulation reset, pause, unpause, and state saving/restoring
"""

import rclpy
from rclpy.node import Node
from std_srvs.srv import Empty, SetBool
from std_msgs.msg import Bool, String
from builtin_interfaces.msg import Time
from gazebo_msgs.srv import (
    SetEntityState, GetEntityState,
    SetModelConfiguration, GetModelConfiguration,
    ResetSimulation, ResetWorld,
    GetWorldProperties
)
from gazebo_msgs.msg import ModelState
import time


class SimulationStateManager(Node):
    def __init__(self):
        super().__init__('simulation_state_manager')

        # Publishers
        self.state_status_pub = self.create_publisher(Bool, '/simulation_running', 10)
        self.state_event_pub = self.create_publisher(String, '/simulation_events', 10)

        # Service clients
        self.reset_simulation_client = self.create_client(
            ResetSimulation, '/reset_simulation'
        )
        self.reset_world_client = self.create_client(
            ResetWorld, '/reset_world'
        )
        self.get_world_properties_client = self.create_client(
            GetWorldProperties, '/get_world_properties'
        )
        self.set_entity_state_client = self.create_client(
            SetEntityState, '/set_entity_state'
        )
        self.get_entity_state_client = self.create_client(
            GetEntityState, '/get_entity_state'
        )

        # Service servers
        self.reset_service = self.create_service(
            Empty, '/humanoid/reset_simulation', self.reset_simulation_callback
        )
        self.pause_service = self.create_service(
            SetBool, '/humanoid/pause_simulation', self.pause_simulation_callback
        )
        self.save_state_service = self.create_service(
            Empty, '/humanoid/save_state', self.save_state_callback
        )
        self.restore_state_service = self.create_service(
            Empty, '/humanoid/restore_state', self.restore_state_callback
        )

        # Internal state
        self.is_simulation_running = True
        self.saved_states = {}
        self.robot_name = 'humanoid_robot'

        # Timer for monitoring simulation state
        self.monitor_timer = self.create_timer(1.0, self.monitor_simulation_state)

        self.get_logger().info('Simulation state manager initialized')

    def reset_simulation_callback(self, request, response):
        """Reset the entire simulation"""
        self.get_logger().info('Resetting simulation...')

        if self.reset_simulation_client.wait_for_service(timeout_sec=1.0):
            reset_request = ResetSimulation.Request()
            future = self.reset_simulation_client.call_async(reset_request)

            # Wait for response
            rclpy.spin_until_future_complete(self, future)

            self.get_logger().info('Simulation reset completed')
            self.publish_event('simulation_reset')
        else:
            self.get_logger().error('Reset simulation service not available')

        return response

    def pause_simulation_callback(self, request, response):
        """Pause or unpause the simulation"""
        pause = request.data
        action = "Pausing" if pause else "Unpausing"
        self.get_logger().info(f'{action} simulation...')

        # For this example, we'll just log the action
        # In a real implementation, you would call the appropriate Gazebo services
        if pause:
            self.is_simulation_running = False
            self.get_logger().info('Simulation paused')
        else:
            self.is_simulation_running = True
            self.get_logger().info('Simulation unpaused')

        response.success = True
        response.message = f'Simulation {"paused" if pause else "unpaused"}'

        self.state_status_pub.publish(Bool(data=not pause))
        self.publish_event(f'simulation_{"paused" if pause else "resumed"}')

        return response

    def save_state_callback(self, request, response):
        """Save the current simulation state"""
        self.get_logger().info('Saving simulation state...')

        # Get current robot state
        if self.get_entity_state_client.wait_for_service(timeout_sec=1.0):
            state_request = GetEntityState.Request()
            state_request.name = self.robot_name

            future = self.get_entity_state_client.call_async(state_request)
            rclpy.spin_until_future_complete(self, future)

            if future.result() is not None:
                entity_state = future.result().state
                timestamp = self.get_clock().now().seconds_nanoseconds()

                # Save state with timestamp
                state_key = f"state_{timestamp[0]}_{timestamp[1]}"
                self.saved_states[state_key] = entity_state

                self.get_logger().info(f'State saved with key: {state_key}')
                self.publish_event(f'state_saved_{state_key}')
            else:
                self.get_logger().error('Failed to get entity state')
        else:
            self.get_logger().error('Get entity state service not available')

        return response

    def restore_state_callback(self, request, response):
        """Restore a previously saved simulation state"""
        if not self.saved_states:
            self.get_logger().warn('No saved states available')
            response.success = False
            response.message = 'No saved states available'
            return response

        # Get the most recent state
        latest_state_key = sorted(self.saved_states.keys())[-1]
        state_to_restore = self.saved_states[latest_state_key]

        self.get_logger().info(f'Restoring state: {latest_state_key}')

        if self.set_entity_state_client.wait_for_service(timeout_sec=1.0):
            state_request = SetEntityState.Request()
            state_request.state = state_to_restore

            future = self.set_entity_state_client.call_async(state_request)
            rclpy.spin_until_future_complete(self, future)

            if future.result() is not None:
                self.get_logger().info('State restored successfully')
                self.publish_event(f'state_restored_{latest_state_key}')
                response.success = True
                response.message = f'State {latest_state_key} restored'
            else:
                self.get_logger().error('Failed to restore state')
                response.success = False
                response.message = 'Failed to restore state'
        else:
            self.get_logger().error('Set entity state service not available')
            response.success = False
            response.message = 'Service not available'

        return response

    def monitor_simulation_state(self):
        """Monitor simulation state and publish updates"""
        running_msg = Bool()
        running_msg.data = self.is_simulation_running
        self.state_status_pub.publish(running_msg)

    def publish_event(self, event_name):
        """Publish a simulation event"""
        event_msg = String()
        event_msg.data = event_name
        self.state_event_pub.publish(event_msg)

    def get_simulation_time(self):
        """Get current simulation time"""
        # In simulation, ROS time equals simulation time when use_sim_time is true
        return self.get_clock().now()

    def wait_for_services(self):
        """Wait for required services to be available"""
        services = [
            self.reset_simulation_client,
            self.reset_world_client,
            self.get_world_properties_client,
            self.set_entity_state_client,
            self.get_entity_state_client
        ]

        for service in services:
            while not service.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'Waiting for {service.srv_name} service...')


def main(args=None):
    rclpy.init(args=args)

    node = SimulationStateManager()

    # Wait for services before starting
    node.wait_for_services()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 5.5 Debugging and Troubleshooting

### 5.5.1 Common Integration Issues and Solutions

```python
class SimulationDebuggingTools:
    """Tools and utilities for debugging Gazebo-ROS 2 integration"""

    @staticmethod
    def check_ros_control_setup():
        """Check if ros_control is properly set up"""
        import subprocess
        import yaml

        # Check if required packages are installed
        required_packages = [
            'ros-humble-ros2-control',
            'ros-humble-ros2-controllers',
            'ros-humble-gazebo-ros2-control'
        ]

        print("Checking required packages...")
        for pkg in required_packages:
            try:
                result = subprocess.run(['dpkg', '-l', pkg],
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"✓ {pkg} is installed")
                else:
                    print(f"✗ {pkg} is NOT installed")
            except Exception as e:
                print(f"Error checking {pkg}: {e}")

    @staticmethod
    def validate_urdf_with_ros2_control(urdf_content):
        """Validate URDF contains proper ros2_control configuration"""
        import xml.etree.ElementTree as ET

        try:
            root = ET.fromstring(urdf_content)

            # Check for ros2_control element
            ros2_control_elem = root.find('.//ros2_control')
            if ros2_control_elem is None:
                print("✗ No ros2_control element found in URDF")
                return False

            print("✓ ros2_control element found")

            # Check hardware interface
            hardware_elem = ros2_control_elem.find('hardware')
            if hardware_elem is None:
                print("✗ No hardware element found in ros2_control")
                return False

            plugin_elem = hardware_elem.find('plugin')
            if plugin_elem is None or plugin_elem.text != 'gazebo_ros2_control/GazeboSystem':
                print(f"✗ Wrong or missing plugin: {plugin_elem.text if plugin_elem is not None else 'None'}")
                return False

            print("✓ Correct Gazebo plugin found")

            # Check for command and state interfaces
            for joint_elem in ros2_control_elem.findall('.//joint'):
                joint_name = joint_elem.get('name')
                command_interfaces = joint_elem.findall('command_interface')
                state_interfaces = joint_elem.findall('state_interface')

                if not command_interfaces:
                    print(f"✗ Joint {joint_name} has no command interfaces")
                    return False
                if not state_interfaces:
                    print(f"✗ Joint {joint_name} has no state interfaces")
                    return False

            print("✓ All joints have proper interfaces")
            return True

        except ET.ParseError as e:
            print(f"✗ Invalid URDF XML: {e}")
            return False
        except Exception as e:
            print(f"✗ Error validating URDF: {e}")
            return False

    @staticmethod
    def check_controller_manager_status():
        """Check controller manager status"""
        import subprocess

        try:
            # List controllers
            result = subprocess.run([
                'ros2', 'control', 'list_controllers'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                print("Current controller status:")
                print(result.stdout)
                return True
            else:
                print(f"Error listing controllers: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error checking controller status: {e}")
            return False

    @staticmethod
    def print_debugging_guide():
        """Print common debugging steps"""
        guide = """
        Gazebo-ROS 2 Integration Debugging Guide:

        1. Check if Gazebo is running:
           - Run: gazebo
           - Check if GUI appears

        2. Verify ROS 2 network:
           - Run: ros2 topic list
           - Look for /clock, /tf, /joint_states topics

        3. Check controller status:
           - Run: ros2 control list_controllers
           - All controllers should be 'active'

        4. Verify joint state publication:
           - Run: ros2 topic echo /joint_states
           - Should show joint positions changing

        5. Check robot description:
           - Run: ros2 param get /robot_state_publisher robot_description
           - Should contain valid URDF

        6. Test controller switching:
           - Run: ros2 control switch_controllers --start <controller_name>

        7. Check for error messages:
           - Look for errors in Gazebo terminal
           - Check ROS 2 node outputs
        """
        print(guide)


# Example usage
debugger = SimulationDebuggingTools()
debugger.print_debugging_guide()
```

### 5.5.2 Performance Monitoring

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String
from sensor_msgs.msg import JointState
from control_msgs.msg import JointTrajectoryControllerState
import time
import psutil
import numpy as np


class SimulationPerformanceMonitor(Node):
    """Monitor performance of simulation-ROS 2 integration"""

    def __init__(self):
        super().__init__('simulation_performance_monitor')

        # Publishers
        self.cpu_pub = self.create_publisher(Float32, '/performance/cpu_percent', 10)
        self.memory_pub = self.create_publisher(Float32, '/performance/memory_percent', 10)
        self.control_rate_pub = self.create_publisher(Float32, '/performance/control_rate', 10)
        self.status_pub = self.create_publisher(String, '/performance/status', 10)

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )
        self.controller_state_sub = self.create_subscription(
            JointTrajectoryControllerState, '/left_leg_controller/state',
            self.controller_state_callback, 10
        )

        # Internal state
        self.joint_state_times = []
        self.control_state_times = []
        self.last_joint_time = None
        self.last_control_time = None

        # Performance timer
        self.performance_timer = self.create_timer(1.0, self.publish_performance_metrics)

        self.get_logger().info('Simulation performance monitor initialized')

    def joint_state_callback(self, msg):
        """Track joint state message timing"""
        current_time = time.time()

        if self.last_joint_time is not None:
            dt = current_time - self.last_joint_time
            self.joint_state_times.append(dt)

            # Keep only last 100 measurements
            if len(self.joint_state_times) > 100:
                self.joint_state_times.pop(0)

        self.last_joint_time = current_time

    def controller_state_callback(self, msg):
        """Track controller state message timing"""
        current_time = time.time()

        if self.last_control_time is not None:
            dt = current_time - self.last_control_time
            self.control_state_times.append(dt)

            if len(self.control_state_times) > 100:
                self.control_state_times.pop(0)

        self.last_control_time = current_time

    def publish_performance_metrics(self):
        """Publish performance metrics"""
        # CPU usage
        cpu_percent = Float32()
        cpu_percent.data = psutil.cpu_percent()
        self.cpu_pub.publish(cpu_percent)

        # Memory usage
        memory_percent = Float32()
        memory_percent.data = psutil.virtual_memory().percent
        self.memory_pub.publish(memory_percent)

        # Control rate (calculate from joint state timing)
        if len(self.joint_state_times) > 0:
            avg_dt = np.mean(self.joint_state_times)
            control_rate = Float32()
            control_rate.data = 1.0 / avg_dt if avg_dt > 0 else 0.0
            self.control_rate_pub.publish(control_rate)

            # Status message
            status_msg = String()
            status_msg.data = f"Control Rate: {control_rate.data:.1f} Hz, CPU: {cpu_percent.data:.1f}%, Mem: {memory_percent.data:.1f}%"
            self.status_pub.publish(status_msg)

            self.get_logger().info(status_msg.data)


def main(args=None):
    rclpy.init(args=args)

    node = SimulationPerformanceMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 5.6 Data Flow Diagrams

### 5.6.1 Gazebo-ROS 2 Integration Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Gazebo       │    │   gazebo_ros2_   │    │   ROS 2         │
│   Physics      │◄───┤   control        │◄───│   Controllers   │
│   Engine       │    │   Plugin         │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         │              ┌──────────────────┐             │
         │              │   ros2_control   │             │
         │              │   Framework      │             │
         │              └──────────────────┘             │
         │                       ▲                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   Hardware       │
                    │   Interface      │
                    │   Abstraction    │
                    └──────────────────┘
                                 │
                    ┌──────────────────┐
                    │   Joint State    │
                    │   Broadcaster    │
                    └──────────────────┘
                                 │
                    ┌──────────────────┐
                    │   Controller     │
                    │   Manager        │
                    └──────────────────┘
```

### 5.6.2 Control Command Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   High-Level    │    │   Controller     │    │   ros2_control  │
│   Commands      │───►│   (e.g., walking │───►│   Hardware      │
│   (Twist,       │    │   controller)    │    │   Interface     │
│   trajectory)   │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Controller    │    │   Command        │    │   Gazebo        │
│   Manager       │───►│   Processing     │───►│   Physics       │
│   (spawner,     │    │   (trajectory    │    │   Update        │
│   switcher)     │    │   generation)    │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌──────────────────┐
                    │   Feedback       │
                    │   Loop (joint    │
                    │   states, etc.)  │
                    └──────────────────┘
                                 │
                    ┌──────────────────┐
                    │   State          │
                    │   Estimation     │
                    └──────────────────┘
```

## 5.7 Tables for Clarity

### 5.7.1 Integration Components Comparison Table

| Component | Purpose | Configuration | Performance Impact |
|-----------|---------|---------------|-------------------|
| gazebo_ros2_control | Gazebo-ROS 2 bridge | URDF plugin tag | Medium (plugin overhead) |
| ros2_control | Control framework | YAML config files | Low (real-time capable) |
| controller_manager | Controller lifecycle | ROS 2 services | Very Low |
| joint_state_broadcaster | Publish joint states | Controller config | Low |
| hardware_interface | Abstract hardware | URDF ros2_control | None (abstraction) |

### 5.7.2 Controller Types and Use Cases Table

| Controller Type | Use Case | Update Rate | Complexity |
|-----------------|----------|-------------|------------|
| JointPositionController | Precise position control | 100-1000 Hz | Low |
| JointVelocityController | Velocity control | 100-1000 Hz | Low |
| JointEffortController | Force control | 100-1000 Hz | Medium |
| JointTrajectoryController | Smooth trajectory following | 50-200 Hz | Medium |
| ForwardCommandController | Direct command passing | As needed | Very Low |
| imu_sensor_broadcaster | IMU data publishing | 100-500 Hz | Low |

## 5.8 Exercises

### Exercise 1: Basic Integration
Set up a simple robot model with ros2_control integration in Gazebo. Verify that joint state publishing and basic position control work correctly.

### Exercise 2: Controller Configuration
Configure multiple controllers (position, velocity, trajectory) for different parts of a humanoid robot and test their functionality.

### Exercise 3: Advanced Control
Implement a walking gait controller that uses feedback from IMU and joint sensors to maintain balance while walking.

### Exercise 4: Performance Testing
Test the performance of your simulation setup under different loads and identify bottlenecks in the system.

### Exercise 5: Debugging Challenge
Introduce common configuration errors and practice identifying and fixing them using the debugging techniques covered.

## 5.9 Mini-Project: Complete Simulation Integration

Implement a complete simulation integration for a humanoid robot that includes:
1. Full ros2_control configuration with multiple controllers
2. Advanced control algorithms (balance, walking)
3. Simulation state management
4. Performance monitoring and optimization
5. Comprehensive testing and validation framework

## 5.10 Summary

This chapter has covered the essential aspects of integrating Gazebo simulation with ROS 2 for humanoid robotics development. The integration enables:

- Seamless development workflows between simulation and real hardware
- Advanced control algorithm development and testing
- Safe and cost-effective robot development
- Effective sim-to-real transfer strategies

Key takeaways include:
- Proper URDF configuration with ros2_control elements
- Controller manager setup and configuration
- Real-time performance considerations
- Debugging and troubleshooting techniques
- State management for simulation environments

The successful integration of Gazebo with ROS 2 forms the foundation for effective humanoid robot development, allowing complex algorithms to be tested and validated in a safe virtual environment before deployment on physical hardware.