---
id: module_1_lab
title: "Module 1 Lab - Hands-On ROS 2 for Humanoid Robotics"
sidebar_position: 7
---

# Module 1 Lab - Hands-On ROS 2 for Humanoid Robotics

## Lab Overview

This lab provides hands-on experience implementing the ROS 2 concepts learned in Module 1. You will create a complete ROS 2 package for a humanoid robot, implementing nodes, topics, services, and actions with practical applications.

## Learning Objectives

By completing this lab, you will:
- Create a complete ROS 2 package for humanoid robot control
- Implement publisher/subscriber communication for sensor data
- Design and implement custom services for humanoid control
- Create and use actions for complex humanoid behaviors
- Integrate all concepts into a cohesive system

## Prerequisites

- Completion of Module 1.1 through Module 1.6
- ROS 2 environment properly configured
- Python 3.8+ installed
- Basic understanding of humanoid robot kinematics

## Lab Duration

Estimated completion time: 4-6 hours

## Exercise 1: Creating the Humanoid Robot Package

First, create a new ROS 2 package for your humanoid robot:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python humanoid_robot_control
cd humanoid_robot_control
```

Create the package structure:

```
humanoid_robot_control/
├── humanoid_robot_control/
│   ├── __init__.py
│   ├── humanoid_node.py
│   ├── sensor_publisher.py
│   ├── joint_controller.py
│   └── behavior_actions.py
├── launch/
│   └── humanoid_system.launch.py
├── config/
│   └── humanoid_params.yaml
├── test/
│   └── test_copyright.py
├── package.xml
└── setup.py
```

### 1.1 Creating the Main Humanoid Node

Create `humanoid_robot_control/humanoid_node.py`:

```python
#!/usr/bin/env python3

"""
Main humanoid robot control node
Implements the core communication hub for the humanoid robot system
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float64MultiArray
from sensor_msgs.msg import JointState
from geometry_msgs.msg import Twist
from builtin_interfaces.msg import Duration
from humanoid_robot_control.srv import JointCommand
from humanoid_robot_control.action import WalkAction
from rclpy.action import ActionServer
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import threading
import time


class HumanoidNode(Node):
    def __init__(self):
        super().__init__('humanoid_robot_node')

        # Create callback groups for threading
        self.joint_callback_group = MutuallyExclusiveCallbackGroup()
        self.speech_callback_group = MutuallyExclusiveCallbackGroup()

        # Publishers
        self.joint_state_pub = self.create_publisher(
            JointState, 'joint_states', 10
        )
        self.speech_pub = self.create_publisher(
            String, 'robot_speech', 10
        )
        self.status_pub = self.create_publisher(
            String, 'robot_status', 10
        )

        # Subscribers
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10,
            callback_group=self.speech_callback_group
        )

        # Service server
        self.joint_cmd_srv = self.create_service(
            JointCommand,
            'joint_command',
            self.joint_command_callback
        )

        # Action server
        self._action_server = ActionServer(
            self,
            WalkAction,
            'walk_action',
            self.execute_walk_callback
        )

        # Robot state
        self.joint_positions = [0.0] * 28  # 28 DOF humanoid
        self.joint_velocities = [0.0] * 28
        self.joint_efforts = [0.0] * 28

        # Timer for joint state publishing
        self.joint_state_timer = self.create_timer(
            0.05,  # 20 Hz
            self.publish_joint_states,
            callback_group=self.joint_callback_group
        )

        self.get_logger().info('Humanoid robot node initialized')

    def cmd_vel_callback(self, msg):
        """Handle velocity commands"""
        self.get_logger().info(f'Received velocity command: {msg}')

        # Convert twist to speech feedback
        feedback_msg = String()
        if msg.linear.x > 0:
            feedback_msg.data = "Moving forward"
        elif msg.linear.x < 0:
            feedback_msg.data = "Moving backward"
        elif msg.angular.z > 0:
            feedback_msg.data = "Turning left"
        elif msg.angular.z < 0:
            feedback_msg.data = "Turning right"
        else:
            feedback_msg.data = "Stopping"

        self.speech_pub.publish(feedback_msg)

    def joint_command_callback(self, request, response):
        """Handle joint command service requests"""
        self.get_logger().info(f'Received joint command: {request}')

        try:
            joint_idx = request.joint_index
            if 0 <= joint_idx < len(self.joint_positions):
                self.joint_positions[joint_idx] = request.position
                self.joint_velocities[joint_idx] = request.velocity
                response.success = True
                response.message = f'Joint {joint_idx} updated successfully'
            else:
                response.success = False
                response.message = f'Invalid joint index: {joint_idx}'
        except Exception as e:
            response.success = False
            response.message = f'Error processing command: {str(e)}'

        return response

    def execute_walk_callback(self, goal_handle):
        """Execute walk action"""
        self.get_logger().info('Executing walk action...')

        feedback_msg = WalkAction.Feedback()
        result = WalkAction.Result()

        # Simulate walking
        for i in range(0, 101, 10):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                return result

            # Update feedback
            feedback_msg.progress = i
            goal_handle.publish_feedback(feedback_msg)

            # Simulate walking motion
            time.sleep(0.5)

            self.get_logger().info(f'Walk progress: {i}%')

        goal_handle.succeed()
        result.success = True
        result.message = 'Walk completed successfully'

        return result

    def publish_joint_states(self):
        """Publish joint state messages"""
        msg = JointState()
        msg.name = [f'joint_{i}' for i in range(28)]  # 28 DOF
        msg.position = self.joint_positions
        msg.velocity = self.joint_velocities
        msg.effort = self.joint_efforts
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        self.joint_state_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = HumanoidNode()

    # Use multi-threaded executor to handle callbacks properly
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### 1.2 Creating Service Definition

Create the service definition file at `srv/JointCommand.srv`:

```srv
# JointCommand.srv
int32 joint_index
float64 position
float64 velocity
---
bool success
string message
```

Create the action definition file at `action/WalkAction.action`:

```
# WalkAction.action
int32 steps
float64 speed
---
bool success
string message
---
int32 progress
```

### 1.3 Creating Setup Files

Update the `setup.py` file:

```python
from setuptools import find_packages, setup

package_name = 'humanoid_robot_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/humanoid_system.launch.py']),
        ('share/' + package_name + '/config', ['config/humanoid_params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Your Name',
    maintainer_email='your.email@example.com',
    description='ROS 2 package for humanoid robot control',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'humanoid_node = humanoid_robot_control.humanoid_node:main',
        ],
    },
)
```

### 1.4 Creating Launch File

Create `launch/humanoid_system.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    log_level = LaunchConfiguration('log_level', default='info')

    # Main humanoid node
    humanoid_node = Node(
        package='humanoid_robot_control',
        executable='humanoid_node',
        name='humanoid_robot_node',
        parameters=[
            {'use_sim_time': use_sim_time},
        ],
        arguments=['--log-level', log_level],
        output='screen'
    )

    # Additional nodes could be added here
    # For example, a sensor simulator or controller manager

    ld = LaunchDescription()

    # Add launch arguments
    ld.add_action(DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    ))

    ld.add_action(DeclareLaunchArgument(
        'log_level',
        default_value='info',
        description='Log level for the node'
    ))

    # Add nodes
    ld.add_action(humanoid_node)

    return ld
```

### 1.5 Creating Configuration File

Create `config/humanoid_params.yaml`:

```yaml
humanoid_robot_node:
  ros__parameters:
    use_sim_time: false
    joint_limits:
      min_position: -3.14
      max_position: 3.14
      max_velocity: 5.0
      max_effort: 100.0
    control_loop_frequency: 20.0
    safety_limits:
      max_joint_effort: 50.0
      emergency_stop_threshold: 100.0
    robot_description: "28 DOF humanoid robot"
    joint_names: [
      "left_hip_joint", "left_knee_joint", "left_ankle_joint",
      "right_hip_joint", "right_knee_joint", "right_ankle_joint",
      "left_shoulder_joint", "left_elbow_joint", "left_wrist_joint",
      "right_shoulder_joint", "right_elbow_joint", "right_wrist_joint",
      "waist_joint", "neck_joint", "head_joint"
      # Add remaining joint names as needed
    ]
```

## Exercise 2: Implementing a Sensor Publisher

Create `humanoid_robot_control/sensor_publisher.py`:

```python
#!/usr/bin/env python3

"""
Sensor publisher node for humanoid robot
Simulates various sensor data streams
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu, LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Header
import math
import random


class SensorPublisherNode(Node):
    def __init__(self):
        super().__init__('sensor_publisher_node')

        # Publishers
        self.joint_pub = self.create_publisher(JointState, 'sim_joint_states', 10)
        self.imu_pub = self.create_publisher(Imu, 'imu/data', 10)
        self.scan_pub = self.create_publisher(LaserScan, 'scan', 10)

        # Timer for publishing sensor data
        self.timer = self.create_timer(0.05, self.publish_sensors)  # 20 Hz

        # Initialize joint positions
        self.joint_positions = [0.0] * 28
        self.joint_velocities = [0.0] * 28
        self.joint_efforts = [0.0] * 28

        self.get_logger().info('Sensor publisher node initialized')

    def publish_sensors(self):
        """Publish all sensor data"""
        self.publish_joint_states()
        self.publish_imu_data()
        self.publish_laser_scan()

    def publish_joint_states(self):
        """Publish joint state data"""
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        # Generate simulated joint positions with small random movements
        for i in range(28):
            self.joint_positions[i] += random.uniform(-0.01, 0.01)
            self.joint_velocities[i] = random.uniform(-0.1, 0.1)
            self.joint_efforts[i] = random.uniform(-1.0, 1.0)

        msg.name = [f'joint_{i}' for i in range(28)]
        msg.position = self.joint_positions.copy()
        msg.velocity = self.joint_velocities.copy()
        msg.effort = self.joint_efforts.copy()

        self.joint_pub.publish(msg)

    def publish_imu_data(self):
        """Publish IMU data"""
        msg = Imu()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        # Simulate orientation (slightly off vertical)
        roll = random.gauss(0.0, 0.05)
        pitch = random.gauss(0.0, 0.05)
        yaw = random.gauss(0.0, 0.1)

        # Convert roll, pitch, yaw to quaternion
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)

        msg.orientation.w = cr * cp * cy + sr * sp * sy
        msg.orientation.x = sr * cp * cy - cr * sp * sy
        msg.orientation.y = cr * sp * cy + sr * cp * sy
        msg.orientation.z = cr * cp * sy - sr * sp * cy

        # Simulate angular velocity
        msg.angular_velocity.x = random.gauss(0.0, 0.1)
        msg.angular_velocity.y = random.gauss(0.0, 0.1)
        msg.angular_velocity.z = random.gauss(0.0, 0.1)

        # Simulate linear acceleration
        msg.linear_acceleration.x = random.gauss(0.0, 0.5)
        msg.linear_acceleration.y = random.gauss(0.0, 0.5)
        msg.linear_acceleration.z = random.gauss(9.81, 0.1)  # Gravity

        self.imu_pub.publish(msg)

    def publish_laser_scan(self):
        """Publish laser scan data"""
        msg = LaserScan()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_link'

        msg.angle_min = -math.pi / 2  # -90 degrees
        msg.angle_max = math.pi / 2    # 90 degrees
        msg.angle_increment = math.pi / 180  # 1 degree
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.1
        msg.range_max = 10.0

        # Generate ranges with some obstacles
        num_ranges = int((msg.angle_max - msg.angle_min) / msg.angle_increment) + 1
        ranges = []

        for i in range(num_ranges):
            angle = msg.angle_min + i * msg.angle_increment

            # Create some obstacles in the environment
            distance = 5.0  # Default distance

            # Add some obstacles
            if -0.5 < angle < 0.5:  # Front area
                distance = random.uniform(1.0, 3.0)  # Obstacle in front
            else:
                distance = random.uniform(3.0, 8.0)  # Clear space

            ranges.append(distance)

        msg.ranges = ranges
        msg.intensities = [100.0] * len(ranges)  # Constant intensity

        self.scan_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = SensorPublisherNode()

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

## Exercise 3: Creating a Joint Controller Node

Create `humanoid_robot_control/joint_controller.py`:

```python
#!/usr/bin/env python3

"""
Joint controller for humanoid robot
Implements PD control for humanoid joints
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray
import numpy as np
import math


class JointControllerNode(Node):
    def __init__(self):
        super().__init__('joint_controller_node')

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_state_callback, 10
        )
        self.joint_cmd_sub = self.create_subscription(
            Float64MultiArray, 'joint_commands', self.joint_command_callback, 10
        )

        # Publishers
        self.joint_cmd_pub = self.create_publisher(
            Float64MultiArray, 'joint_effort_commands', 10
        )

        # Controller parameters
        self.kp = 100.0  # Proportional gain
        self.kd = 10.0   # Derivative gain
        self.control_freq = 100  # Hz
        self.dt = 1.0 / self.control_freq

        # Robot state
        self.current_positions = np.zeros(28)
        self.current_velocities = np.zeros(28)
        self.current_efforts = np.zeros(28)
        self.desired_positions = np.zeros(28)
        self.desired_velocities = np.zeros(28)

        # Timer for control loop
        self.control_timer = self.create_timer(
            self.dt, self.control_loop
        )

        self.get_logger().info('Joint controller node initialized')

    def joint_state_callback(self, msg):
        """Update current joint state"""
        for i, name in enumerate(msg.name):
            if i < len(self.current_positions):
                try:
                    idx = int(name.split('_')[-1])  # Extract joint index from name
                    self.current_positions[idx] = msg.position[i]
                    if i < len(msg.velocity):
                        self.current_velocities[idx] = msg.velocity[i]
                    if i < len(msg.effort):
                        self.current_efforts[idx] = msg.effort[i]
                except (ValueError, IndexError):
                    # If we can't parse the joint name, use index directly
                    if i < len(self.current_positions):
                        self.current_positions[i] = msg.position[i]
                        if i < len(msg.velocity):
                            self.current_velocities[i] = msg.velocity[i]
                        if i < len(msg.effort):
                            self.current_efforts[i] = msg.effort[i]

    def joint_command_callback(self, msg):
        """Update desired joint positions"""
        for i, pos in enumerate(msg.data):
            if i < len(self.desired_positions):
                self.desired_positions[i] = pos

    def control_loop(self):
        """Main control loop implementing PD control"""
        # Calculate errors
        position_error = self.desired_positions - self.current_positions
        velocity_error = self.desired_velocities - self.current_velocities

        # PD control law
        efforts = self.kp * position_error + self.kd * velocity_error

        # Saturate efforts to prevent excessive forces
        efforts = np.clip(efforts, -50.0, 50.0)

        # Publish efforts
        effort_msg = Float64MultiArray()
        effort_msg.data = efforts.tolist()
        self.joint_cmd_pub.publish(effort_msg)


def main(args=None):
    rclpy.init(args=args)

    node = JointControllerNode()

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

## Exercise 4: Testing the System

Add the joint controller to the launch file and test the system:

Update the launch file to include the joint controller:

```python
# Add to the launch file after the humanoid_node definition
joint_controller_node = Node(
    package='humanoid_robot_control',
    executable='joint_controller',
    name='joint_controller',
    parameters=[
        {'use_sim_time': use_sim_time},
    ],
    arguments=['--log-level', log_level],
    output='screen'
)

# Add the joint controller node to the launch description
ld.add_action(joint_controller_node)
```

### 4.1 Testing Commands

After building and sourcing your package, test the system:

```bash
# Build the package
cd ~/ros2_ws
colcon build --packages-select humanoid_robot_control

# Source the workspace
source install/setup.bash

# Launch the system
ros2 launch humanoid_robot_control humanoid_system.launch.py

# In another terminal, test the service
ros2 service call /joint_command humanoid_robot_control/srv/JointCommand "{
  joint_index: 0,
  position: 1.57,
  velocity: 0.0
}"

# Test the action
ros2 action send_goal /walk_action humanoid_robot_control/action/WalkAction "{
  steps: 10,
  speed: 0.5
}"
```

## Exercise 5: Creating a Behavior Actions Module

Create `humanoid_robot_control/behavior_actions.py`:

```python
#!/usr/bin/env python3

"""
Behavior actions for humanoid robot
Implements complex behaviors using action servers
"""

import rclpy
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
import time
import math

from humanoid_robot_control.action import WalkAction, GestureAction
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState


class BehaviorActionsNode(Node):
    def __init__(self):
        super().__init__('behavior_actions_node')

        # Create callback group for actions
        callback_group = ReentrantCallbackGroup()

        # Action servers
        self.walk_action_server = ActionServer(
            self,
            WalkAction,
            'walk_action',
            self.execute_walk,
            callback_group=callback_group,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.gesture_action_server = ActionServer(
            self,
            GestureAction,
            'gesture_action',
            self.execute_gesture,
            callback_group=callback_group,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        # Publishers for robot commands
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.joint_cmd_pub = self.create_publisher(JointState, 'joint_commands', 10)
        self.status_pub = self.create_publisher(String, 'robot_status', 10)

        # Robot state
        self.is_moving = False
        self.current_behavior = None

        self.get_logger().info('Behavior actions node initialized')

    def goal_callback(self, goal_request):
        """Accept or reject goal requests"""
        self.get_logger().info(f'Received goal request: {goal_request}')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject cancel requests"""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_walk(self, goal_handle):
        """Execute walking behavior"""
        self.get_logger().info('Executing walk behavior')

        feedback_msg = WalkAction.Feedback()
        result_msg = WalkAction.Result()

        # Get goal parameters
        steps = goal_handle.request.steps
        speed = goal_handle.request.speed

        self.current_behavior = 'walking'
        self.is_moving = True

        # Publish status
        status_msg = String()
        status_msg.data = f'Walking: {steps} steps at speed {speed}'
        self.status_pub.publish(status_msg)

        # Execute walk
        for step in range(steps):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result_msg.success = False
                result_msg.message = 'Walk cancelled'
                self.is_moving = False
                self.current_behavior = None
                return result_msg

            # Publish velocity command for walking
            cmd_msg = Twist()
            cmd_msg.linear.x = speed
            cmd_msg.angular.z = 0.0  # No turning for now
            self.cmd_vel_pub.publish(cmd_msg)

            # Update feedback
            feedback_msg.progress = int((step + 1) / steps * 100)
            goal_handle.publish_feedback(feedback_msg)

            # Sleep for step duration
            time.sleep(1.0 / speed if speed > 0 else 1.0)

        # Stop movement
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)

        self.is_moving = False
        self.current_behavior = None

        goal_handle.succeed()
        result_msg.success = True
        result_msg.message = f'Completed {steps} steps successfully'

        return result_msg

    def execute_gesture(self, goal_handle):
        """Execute gesture behavior"""
        self.get_logger().info(f'Executing gesture: {goal_handle.request.gesture_name}')

        feedback_msg = GestureAction.Feedback()
        result_msg = GestureAction.Result()

        gesture_name = goal_handle.request.gesture_name
        duration = goal_handle.request.duration

        self.current_behavior = 'gesturing'

        # Publish status
        status_msg = String()
        status_msg.data = f'Performing gesture: {gesture_name}'
        self.status_pub.publish(status_msg)

        # Execute different gestures based on name
        if gesture_name.lower() == 'wave':
            self.execute_wave_gesture(goal_handle, duration, feedback_msg)
        elif gesture_name.lower() == 'nod':
            self.execute_nod_gesture(goal_handle, duration, feedback_msg)
        elif gesture_name.lower() == 'point':
            self.execute_point_gesture(goal_handle, duration, feedback_msg)
        else:
            # Default to waving if unknown gesture
            self.execute_wave_gesture(goal_handle, duration, feedback_msg)

        goal_handle.succeed()
        result_msg.success = True
        result_msg.message = f'Gesture {gesture_name} completed successfully'

        self.current_behavior = None

        return result_msg

    def execute_wave_gesture(self, goal_handle, duration, feedback_msg):
        """Execute waving gesture"""
        start_time = time.time()

        # Simulate waving motion with joint commands
        while time.time() - start_time < duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return

            # Create waving motion pattern
            elapsed = time.time() - start_time
            angle = math.sin(elapsed * 4) * 0.5  # Oscillate at 2 Hz

            # Create joint state message for waving
            joint_msg = JointState()
            joint_msg.name = ['right_shoulder_pitch', 'right_elbow_yaw']
            joint_msg.position = [angle, -angle * 0.7]  # Coordinated movement

            self.joint_cmd_pub.publish(joint_msg)

            # Update feedback
            progress = int((elapsed / duration) * 100)
            feedback_msg.progress = progress
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(0.05)  # 20 Hz update rate

    def execute_nod_gesture(self, goal_handle, duration, feedback_msg):
        """Execute nodding gesture"""
        start_time = time.time()

        while time.time() - start_time < duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return

            # Create nodding motion pattern
            elapsed = time.time() - start_time
            angle = math.sin(elapsed * 3) * 0.3  # Oscillate at 1.5 Hz

            # Create joint state message for nodding
            joint_msg = JointState()
            joint_msg.name = ['neck_pitch']
            joint_msg.position = [angle]

            self.joint_cmd_pub.publish(joint_msg)

            # Update feedback
            progress = int((elapsed / duration) * 100)
            feedback_msg.progress = progress
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(0.05)

    def execute_point_gesture(self, goal_handle, duration, feedback_msg):
        """Execute pointing gesture"""
        start_time = time.time()

        while time.time() - start_time < duration:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                return

            # Create pointing motion - extend arm forward
            joint_msg = JointState()
            joint_msg.name = ['right_shoulder_pitch', 'right_elbow_yaw']
            joint_msg.position = [0.5, -1.0]  # Pointing position

            self.joint_cmd_pub.publish(joint_msg)

            # Update feedback
            progress = int((elapsed / duration) * 100)
            feedback_msg.progress = progress
            goal_handle.publish_feedback(feedback_msg)

            time.sleep(0.05)


def main(args=None):
    rclpy.init(args=args)

    node = BehaviorActionsNode()

    # Use multi-threaded executor to handle multiple action servers
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## Exercise 6: Integration and Testing

Add the behavior actions node to your launch file and create a test script:

Create `test/test_integration.py`:

```python
#!/usr/bin/env python3

"""
Integration test for humanoid robot system
Tests the interaction between all components
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String, Float64MultiArray
from geometry_msgs.msg import Twist
from humanoid_robot_control.action import WalkAction, GestureAction
from humanoid_robot_control.srv import JointCommand
import time


class IntegrationTestNode(Node):
    def __init__(self):
        super().__init__('integration_test_node')

        # Publishers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.speech_pub = self.create_publisher(String, 'robot_speech', 10)

        # Service client
        self.joint_cmd_client = self.create_client(
            JointCommand, 'joint_command'
        )

        # Action clients
        self.walk_action_client = ActionClient(
            self, WalkAction, 'walk_action'
        )
        self.gesture_action_client = ActionClient(
            self, GestureAction, 'gesture_action'
        )

        # Wait for services and actions
        self.get_logger().info('Waiting for services and actions...')
        self.joint_cmd_client.wait_for_service()
        self.walk_action_client.wait_for_server()
        self.gesture_action_client.wait_for_server()

        self.get_logger().info('All services and actions available')

        # Timer to run tests
        self.test_timer = self.create_timer(1.0, self.run_tests)
        self.test_step = 0

        self.get_logger().info('Integration test node initialized')

    def run_tests(self):
        """Run a sequence of integration tests"""
        if self.test_step == 0:
            self.test_speech()
        elif self.test_step == 1:
            self.test_joint_command()
        elif self.test_step == 2:
            self.test_walk_action()
        elif self.test_step == 3:
            self.test_gesture_action()
        elif self.test_step == 4:
            self.test_velocity_command()
        else:
            self.test_timer.cancel()
            self.get_logger().info('All integration tests completed')
            return

        self.test_step += 1

    def test_speech(self):
        """Test speech publishing"""
        self.get_logger().info('Test 1: Testing speech publishing')
        msg = String()
        msg.data = "Hello, this is a speech test"
        self.speech_pub.publish(msg)

    def test_joint_command(self):
        """Test joint command service"""
        self.get_logger().info('Test 2: Testing joint command service')

        request = JointCommand.Request()
        request.joint_index = 0
        request.position = 1.57
        request.velocity = 0.0

        future = self.joint_cmd_client.call_async(request)
        future.add_done_callback(self.joint_command_callback)

    def joint_command_callback(self, future):
        """Handle joint command response"""
        try:
            response = future.result()
            self.get_logger().info(f'Joint command response: {response.message}')
        except Exception as e:
            self.get_logger().error(f'Joint command service call failed: {e}')

    def test_walk_action(self):
        """Test walk action"""
        self.get_logger().info('Test 3: Testing walk action')

        goal_msg = WalkAction.Goal()
        goal_msg.steps = 5
        goal_msg.speed = 0.5

        self.walk_action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.walk_feedback_callback
        ).add_done_callback(self.walk_goal_callback)

    def walk_feedback_callback(self, feedback_msg):
        """Handle walk action feedback"""
        self.get_logger().info(f'Walk progress: {feedback_msg.feedback.progress}%')

    def walk_goal_callback(self, future):
        """Handle walk goal response"""
        goal_handle = future.result()
        self.get_logger().info(f'Walk goal accepted: {goal_handle.accepted}')

    def test_gesture_action(self):
        """Test gesture action"""
        self.get_logger().info('Test 4: Testing gesture action')

        goal_msg = GestureAction.Goal()
        goal_msg.gesture_name = 'wave'
        goal_msg.duration = 3.0

        self.gesture_action_client.send_goal_async(goal_msg)

    def test_velocity_command(self):
        """Test velocity command"""
        self.get_logger().info('Test 5: Testing velocity command')

        msg = Twist()
        msg.linear.x = 0.5
        msg.angular.z = 0.2
        self.cmd_vel_pub.publish(msg)

        # Stop after 2 seconds
        self.create_timer(2.0, self.stop_robot)

    def stop_robot(self):
        """Stop robot movement"""
        msg = Twist()
        self.cmd_vel_pub.publish(msg)
        self.get_logger().info('Robot stopped')


def main(args=None):
    rclpy.init(args=args)

    node = IntegrationTestNode()

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

## Lab Report Requirements

After completing all exercises, prepare a lab report that includes:

1. **System Architecture**: Document your overall system design
2. **Code Documentation**: Commented code for each component
3. **Testing Results**: Output from your integration tests
4. **Challenges Faced**: Any issues encountered and how you resolved them
5. **Lessons Learned**: Key insights from implementing the system

## Assessment Criteria

Your lab will be assessed based on:
- Correct implementation of ROS 2 concepts
- Proper use of nodes, topics, services, and actions
- Code quality and documentation
- Successful integration of all components
- Test results and system behavior

## Next Steps

Upon successful completion of this lab, you should have a working ROS 2 package that demonstrates all the concepts covered in Module 1. This foundation will be essential as you progress through the subsequent modules, where you'll build upon these concepts to create increasingly sophisticated humanoid robot systems.