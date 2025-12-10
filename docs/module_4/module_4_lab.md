---
id: module_4_lab
title: "Module 4 Lab - Humanoid Control Systems Lab"
sidebar_position: 6
---

# Module 4 Lab - Humanoid Control Systems Lab

## Overview

Welcome to the Humanoid Control Systems Lab! This hands-on lab integrates all the concepts learned in Module 4, including balance and posture control, locomotion control, whole-body control, and perception-action integration. You'll implement a complete humanoid control system that combines all these elements to create a functional humanoid robot that can maintain balance, walk, and interact with its environment.

## Learning Objectives

By the end of this lab, you will be able to:
- Integrate multiple control systems into a unified humanoid control architecture
- Implement a complete humanoid robot controller with balance, locomotion, and perception
- Create a perception-action loop that enables environmental interaction
- Debug and tune complex control systems for humanoid robots
- Evaluate the performance of integrated control systems

## Prerequisites

Before starting this lab, you should have:
- Completed all Module 4 chapters (4.0-4.4)
- Experience with ROS 2 development
- Understanding of Python and C++ for robotics
- Basic knowledge of control theory and state estimation
- Access to a humanoid robot simulation environment (Isaac Sim or Gazebo)

## Lab Structure

This lab is organized into 4 main sections:
1. **Integrated Control Architecture Setup** - Setting up the unified control system
2. **Balance and Locomotion Integration** - Combining balance and walking controllers
3. **Perception-Action Integration** - Adding environmental perception and interaction
4. **Performance Evaluation and Tuning** - Testing and optimizing the complete system

## Section 1: Integrated Control Architecture Setup

In this section, we'll set up the foundational architecture that will integrate all control systems. The key is to create a hierarchical control structure where different controllers can operate simultaneously without conflicts.

### 1.1 Control Architecture Design

The integrated control architecture follows a hierarchical structure:

```python
#!/usr/bin/env python3
"""
Integrated Humanoid Control System Architecture
"""

import rospy
import numpy as np
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Twist, PoseStamped
from std_msgs.msg import Float64MultiArray
from tf.transformations import quaternion_from_euler, euler_from_quaternion
import threading
import time

class IntegratedControlArchitecture:
    """
    Main control architecture that integrates all humanoid control systems.
    """

    def __init__(self):
        # Initialize ROS node
        rospy.init_node('integrated_humanoid_controller')

        # Control system components
        self.balance_controller = BalanceController()
        self.locomotion_controller = LocomotionController()
        self.whole_body_controller = WholeBodyController()
        self.perception_controller = PerceptionController()

        # State variables
        self.current_state = {
            'joint_positions': np.zeros(28),  # Example for 28 DOF humanoid
            'joint_velocities': np.zeros(28),
            'imu_data': None,
            'base_pose': None,
            'base_velocity': None,
            'contact_states': np.zeros(4)  # Foot contact states
        }

        # Control loop parameters
        self.control_rate = 100  # Hz
        self.rate = rospy.Rate(self.control_rate)

        # Publishers and subscribers
        self.joint_cmd_pub = rospy.Publisher('/joint_commands', JointState, queue_size=10)
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.joint_state_sub = rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)

        # Threading for different control loops
        self.control_lock = threading.Lock()
        self.running = True

        rospy.loginfo("Integrated Control Architecture initialized")

    def imu_callback(self, msg):
        """Handle IMU data updates."""
        with self.control_lock:
            self.current_state['imu_data'] = {
                'orientation': [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w],
                'angular_velocity': [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z],
                'linear_acceleration': [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z]
            }

    def joint_state_callback(self, msg):
        """Handle joint state updates."""
        with self.control_lock:
            # Update joint positions and velocities
            if len(msg.position) == len(self.current_state['joint_positions']):
                self.current_state['joint_positions'] = np.array(msg.position)
                self.current_state['joint_velocities'] = np.array(msg.velocity)

    def update_state_estimation(self):
        """Update state estimation using all available sensors."""
        # Integrate perception and sensor data for state estimation
        if self.current_state['imu_data'] is not None:
            # Update orientation and angular rates
            orientation = self.current_state['imu_data']['orientation']
            angular_vel = self.current_state['imu_data']['angular_velocity']

            # Update base pose using IMU and joint integration
            self.current_state['base_pose'] = self.estimate_base_pose(orientation)
            self.current_state['base_velocity'] = self.estimate_base_velocity(angular_vel)

    def estimate_base_pose(self, orientation):
        """Estimate base pose using IMU and forward kinematics."""
        # This would integrate IMU data with forward kinematics
        # For now, return a simple pose estimate
        return np.array([0.0, 0.0, 0.8, orientation[0], orientation[1], orientation[2], orientation[3]])

    def estimate_base_velocity(self, angular_vel):
        """Estimate base velocity from IMU and joint velocities."""
        # Integrate angular velocities and joint velocities
        return np.array([angular_vel[0], angular_vel[1], angular_vel[2], 0.0, 0.0, 0.0])

    def compute_control_commands(self):
        """Compute integrated control commands from all controllers."""
        with self.control_lock:
            # Update state estimation
            self.update_state_estimation()

            # Get commands from individual controllers
            balance_cmd = self.balance_controller.compute_command(self.current_state)
            locomotion_cmd = self.locomotion_controller.compute_command(self.current_state)
            whole_body_cmd = self.whole_body_controller.compute_command(self.current_state)

            # Integrate commands using task-priority framework
            integrated_cmd = self.integrate_commands(balance_cmd, locomotion_cmd, whole_body_cmd)

            return integrated_cmd

    def integrate_commands(self, balance_cmd, locomotion_cmd, whole_body_cmd):
        """
        Integrate commands from different controllers using task-priority framework.
        Balance has highest priority, followed by locomotion, then whole-body tasks.
        """
        # For this example, we'll use a simple weighted combination
        # In practice, this would use more sophisticated task-priority methods
        final_cmd = np.zeros_like(balance_cmd)

        # Apply balance corrections first (highest priority)
        final_cmd += 0.6 * balance_cmd

        # Apply locomotion commands (medium priority)
        final_cmd += 0.3 * locomotion_cmd

        # Apply whole-body commands (lower priority)
        final_cmd += 0.1 * whole_body_cmd

        return final_cmd

    def publish_commands(self, commands):
        """Publish joint commands to the robot."""
        msg = JointState()
        msg.header.stamp = rospy.Time.now()
        msg.position = commands.tolist()
        msg.velocity = [0.0] * len(commands)  # Set desired velocities
        msg.effort = [0.0] * len(commands)    # Set desired efforts

        self.joint_cmd_pub.publish(msg)

    def run_control_loop(self):
        """Main control loop that integrates all control systems."""
        rospy.loginfo("Starting integrated control loop")

        while not rospy.is_shutdown() and self.running:
            try:
                # Compute integrated control commands
                commands = self.compute_control_commands()

                # Publish commands to robot
                self.publish_commands(commands)

                # Sleep to maintain control rate
                self.rate.sleep()

            except Exception as e:
                rospy.logerr(f"Error in control loop: {e}")
                self.rate.sleep()

class BalanceController:
    """Balance controller component."""

    def __init__(self):
        # Initialize balance control parameters
        self.kp = 100.0
        self.ki = 10.0
        self.kd = 20.0
        self.error_integral = 0.0
        self.previous_error = 0.0

    def compute_command(self, state):
        """Compute balance correction commands."""
        # This would implement ZMP-based balance control
        # For this example, return a simple balance correction
        if state['imu_data'] is not None:
            orientation = state['imu_data']['orientation']
            roll, pitch, yaw = euler_from_quaternion(orientation)

            # Simple balance correction based on orientation
            balance_cmd = np.zeros(28)
            balance_cmd[0] = self.kp * pitch  # Ankle pitch for pitch balance
            balance_cmd[1] = self.kp * roll   # Ankle roll for roll balance

            return balance_cmd
        else:
            return np.zeros(28)

class LocomotionController:
    """Locomotion controller component."""

    def __init__(self):
        # Initialize locomotion control parameters
        self.step_length = 0.3
        self.step_height = 0.05
        self.step_period = 1.0
        self.phase = 0.0

    def compute_command(self, state):
        """Compute locomotion commands."""
        # This would implement walking pattern generation
        # For this example, return a simple walking command
        locomotion_cmd = np.zeros(28)

        # Simulate walking pattern
        self.phase += 2 * np.pi / (self.step_period * 100)  # Update phase based on control rate

        # Simple walking command (this would be much more complex in practice)
        locomotion_cmd[6] = self.step_length * np.sin(self.phase)  # Hip movement
        locomotion_cmd[7] = self.step_height * np.sin(self.phase)  # Knee movement

        return locomotion_cmd

class WholeBodyController:
    """Whole-body controller component."""

    def __init__(self):
        # Initialize whole-body control parameters
        self.task_weights = {}
        self.active_tasks = []

    def compute_command(self, state):
        """Compute whole-body control commands."""
        # This would implement task-priority framework
        # For this example, return a simple posture command
        whole_body_cmd = np.zeros(28)

        # Default standing posture
        default_posture = np.array([
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Lower body
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Upper body
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Arms
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # More joints
            0.0, 0.0, 0.0, 0.0              # Additional joints
        ])

        return default_posture

class PerceptionController:
    """Perception controller component."""

    def __init__(self):
        # Initialize perception parameters
        self.perception_active = True
        self.environment_map = None

    def compute_command(self, state):
        """Compute perception-based commands."""
        # This would implement perception-action integration
        # For this example, return zero command
        return np.zeros(28)

if __name__ == '__main__':
    try:
        # Initialize integrated control architecture
        controller = IntegratedControlArchitecture()

        # Start control loop in separate thread
        control_thread = threading.Thread(target=controller.run_control_loop)
        control_thread.start()

        # Keep main thread alive
        rospy.spin()

        # Stop controller when shutting down
        controller.running = False
        control_thread.join()

    except rospy.ROSInterruptException:
        rospy.loginfo("Control node interrupted")
    except Exception as e:
        rospy.logerr(f"Error running integrated controller: {e}")
```

### 1.2 Testing the Architecture

Let's create a simple test script to verify the architecture is working:

```bash
#!/bin/bash
# test_control_architecture.sh

# Source ROS environment
source /opt/ros/humble/setup.bash
source install/setup.bash

# Launch the integrated controller
python3 integrated_humanoid_controller.py
```

## Section 2: Balance and Locomotion Integration

In this section, we'll implement the integration between balance and locomotion controllers, ensuring that the robot can maintain balance while walking.

### 2.1 ZMP-Based Walking with Balance Recovery

```python
#!/usr/bin/env python3
"""
ZMP-Based Walking with Balance Recovery Integration
"""

import rospy
import numpy as np
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Point, Vector3
from std_msgs.msg import Float64
import math

class ZMPWalkingController:
    """
    ZMP-based walking controller with integrated balance recovery.
    """

    def __init__(self):
        rospy.init_node('zmp_walking_controller')

        # Walking parameters
        self.step_length = 0.3  # meters
        self.step_width = 0.2   # meters
        self.step_height = 0.05 # meters
        self.step_period = 1.0  # seconds
        self.com_height = 0.8   # center of mass height

        # ZMP control parameters
        self.zmp_reference = np.zeros(2)  # [x, y]
        self.zmp_current = np.zeros(2)
        self.zmp_error = np.zeros(2)

        # Balance recovery parameters
        self.balance_threshold = 0.05  # meters
        self.recovery_active = False

        # Preview control parameters
        self.preview_window = 2.0  # seconds
        self.sampling_time = 0.01  # seconds
        self.omega = np.sqrt(9.81 / self.com_height)

        # State variables
        self.current_phase = 0.0
        self.support_foot = 'left'  # 'left' or 'right'
        self.swing_foot = 'right'   # 'left' or 'right'

        # Publishers and subscribers
        self.zmp_pub = rospy.Publisher('/zmp_reference', Point, queue_size=10)
        self.com_pub = rospy.Publisher('/com_reference', Point, queue_size=10)
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)

        # Initialize preview controller
        self.preview_controller = PreviewController(self.com_height)

        rospy.loginfo("ZMP Walking Controller initialized")

    def imu_callback(self, msg):
        """Process IMU data for balance monitoring."""
        # Extract orientation to calculate current ZMP
        orientation = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        # Calculate current ZMP based on orientation and contact forces
        self.update_current_zmp(orientation)

    def update_current_zmp(self, orientation):
        """Update current ZMP estimate based on sensor data."""
        # This would use actual force/torque sensors in practice
        # For simulation, estimate from IMU and kinematic data
        roll, pitch, yaw = self.orientation_to_rpy(orientation)

        # Simple ZMP estimation (in practice, use force plate or F/T sensors)
        self.zmp_current[0] = self.com_height * pitch / 9.81  # Simplified
        self.zmp_current[1] = self.com_height * roll / 9.81   # Simplified

    def orientation_to_rpy(self, orientation):
        """Convert quaternion to roll-pitch-yaw."""
        x, y, z, w = orientation

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

    def generate_footstep_pattern(self, num_steps=10):
        """Generate footstep pattern for walking."""
        footsteps = []

        for i in range(num_steps):
            # Calculate foot position based on step pattern
            if i % 2 == 0:  # Left foot step
                foot_x = (i // 2) * self.step_length
                foot_y = self.step_width / 2
                foot_type = 'left'
            else:  # Right foot step
                foot_x = ((i + 1) // 2) * self.step_length
                foot_y = -self.step_width / 2
                foot_type = 'right'

            # Add small variations for natural walking
            foot_x += np.random.normal(0, 0.01)
            foot_y += np.random.normal(0, 0.005)

            footsteps.append({
                'position': [foot_x, foot_y, 0.0],
                'type': foot_type,
                'time': i * self.step_period
            })

        return footsteps

    def compute_zmp_reference(self, phase, footsteps):
        """Compute ZMP reference trajectory for walking."""
        # This would implement the full ZMP reference generation
        # For this example, use simplified approach

        # Find current support phase based on phase
        step_index = int(phase / self.step_period)
        phase_in_step = phase % self.step_period

        if step_index < len(footsteps):
            current_support = footsteps[step_index]
            next_support = footsteps[step_index + 1] if step_index + 1 < len(footsteps) else current_support

            # Generate ZMP reference that moves from current support to next support
            alpha = phase_in_step / self.step_period
            self.zmp_reference[0] = current_support['position'][0] * (1 - alpha) + next_support['position'][0] * alpha
            self.zmp_reference[1] = current_support['position'][1] * (1 - alpha) + next_support['position'][1] * alpha

        return self.zmp_reference

    def balance_recovery_check(self):
        """Check if balance recovery is needed."""
        self.zmp_error = self.zmp_reference - self.zmp_current

        # Check if ZMP error exceeds threshold
        error_magnitude = np.linalg.norm(self.zmp_error)

        if error_magnitude > self.balance_threshold:
            self.recovery_active = True
            rospy.logwarn(f"Balance recovery activated: ZMP error = {error_magnitude:.3f}m")
            return True
        else:
            self.recovery_active = False
            return False

    def compute_balance_recovery(self):
        """Compute balance recovery commands."""
        # Use capture point concept for balance recovery
        com_pos = self.estimate_com_position()
        com_vel = self.estimate_com_velocity()

        # Calculate capture point
        capture_point = self.calculate_capture_point(com_pos, com_vel)

        # Generate recovery commands to move to capture point
        recovery_cmd = self.generate_recovery_commands(capture_point)

        return recovery_cmd

    def estimate_com_position(self):
        """Estimate center of mass position."""
        # In practice, this would use full kinematic model
        # For this example, return estimated CoM
        return np.array([0.0, 0.0, self.com_height])

    def estimate_com_velocity(self):
        """Estimate center of mass velocity."""
        # In practice, this would use full kinematic model
        # For this example, return estimated CoM velocity
        return np.array([0.0, 0.0, 0.0])

    def calculate_capture_point(self, com_pos, com_vel):
        """Calculate capture point for balance recovery."""
        # Capture point = CoM position + (CoM velocity / omega)
        capture_point = com_pos[:2] + com_vel[:2] / self.omega
        return capture_point

    def generate_recovery_commands(self, capture_point):
        """Generate commands to move to capture point."""
        # This would implement the actual recovery control
        # For this example, return simple recovery commands
        recovery_cmd = np.zeros(28)  # 28 DOF humanoid

        # Simple recovery based on capture point error
        cp_error = capture_point - self.zmp_current

        # Apply recovery commands to ankle joints for balance
        recovery_cmd[0] = 50.0 * cp_error[1]  # Ankle roll
        recovery_cmd[1] = 50.0 * cp_error[0]  # Ankle pitch

        return recovery_cmd

    def run_walking_control(self):
        """Main walking control loop."""
        rate = rospy.Rate(100)  # 100 Hz control rate

        # Generate footstep pattern
        footsteps = self.generate_footstep_pattern(20)

        rospy.loginfo("Starting ZMP-based walking control")

        while not rospy.is_shutdown():
            try:
                # Update current phase
                self.current_phase += 0.01  # 100Hz * 0.001s = 0.1s per step

                # Compute ZMP reference
                zmp_ref = self.compute_zmp_reference(self.current_phase, footsteps)

                # Check for balance recovery
                if self.balance_recovery_check():
                    # Apply balance recovery commands
                    recovery_cmd = self.compute_balance_recovery()
                    # Publish recovery commands
                    self.publish_recovery_commands(recovery_cmd)
                else:
                    # Continue normal walking
                    walking_cmd = self.compute_walking_commands()
                    # Publish walking commands
                    self.publish_walking_commands(walking_cmd)

                # Publish ZMP reference for monitoring
                zmp_msg = Point()
                zmp_msg.x = zmp_ref[0]
                zmp_msg.y = zmp_ref[1]
                zmp_msg.z = 0.0
                self.zmp_pub.publish(zmp_msg)

                rate.sleep()

            except Exception as e:
                rospy.logerr(f"Error in walking control: {e}")
                rate.sleep()

    def compute_walking_commands(self):
        """Compute walking commands for current phase."""
        # This would implement the full walking pattern generation
        # For this example, return simple walking commands
        walking_cmd = np.zeros(28)

        # Simple walking pattern based on current phase
        phase_norm = (self.current_phase % self.step_period) / self.step_period

        # Hip and knee movements for walking
        walking_cmd[6] = self.step_length * 0.5 * np.sin(2 * np.pi * phase_norm)  # Hip forward/back
        walking_cmd[7] = self.step_height * np.sin(2 * np.pi * phase_norm)        # Knee lift

        return walking_cmd

    def publish_recovery_commands(self, commands):
        """Publish balance recovery commands."""
        # This would publish to actual robot joints
        rospy.loginfo("Publishing balance recovery commands")

    def publish_walking_commands(self, commands):
        """Publish walking commands."""
        # This would publish to actual robot joints
        rospy.loginfo("Publishing walking commands")

class PreviewController:
    """
    Preview controller for ZMP-based walking.
    """

    def __init__(self, com_height=0.8, sampling_time=0.01, preview_window=2.0):
        self.com_height = com_height
        self.sampling_time = sampling_time
        self.preview_window = preview_window
        self.omega = np.sqrt(9.81 / com_height)

        # State space representation: x = [x, x_dot, x_ddot]^T
        self.A = np.array([
            [0, 1, 0],
            [0, 0, 1],
            [self.omega**2, 0, 0]
        ])

        self.B = np.array([0, 0, self.omega**2])

        # Q and R matrices for LQR design
        self.Q = np.diag([100, 1, 0.1])  # State weights
        self.R = 0.1  # Control weight

        # Calculate feedback gains using LQR
        self.K = self.calculate_lqr_gains()

        # Preview gains for future reference tracking
        self.preview_gains = self.calculate_preview_gains()

    def calculate_lqr_gains(self):
        """Calculate LQR feedback gains."""
        # Solve Riccati equation for LQR
        # This is a simplified implementation
        # In practice, use scipy.linalg.solve_continuous_are
        return np.array([10.0, 2.0, 1.0])  # Pre-calculated gains

    def calculate_preview_gains(self):
        """Calculate preview gains for reference tracking."""
        # Calculate preview gains for tracking future ZMP references
        num_preview_steps = int(self.preview_window / self.sampling_time)
        preview_gains = np.zeros(num_preview_steps)

        # Calculate gains using preview control theory
        for i in range(num_preview_steps):
            time_ahead = i * self.sampling_time
            preview_gains[i] = self.omega * np.exp(-self.omega * time_ahead)

        return preview_gains

if __name__ == '__main__':
    try:
        controller = ZMPWalkingController()
        controller.run_walking_control()
    except rospy.ROSInterruptException:
        rospy.loginfo("Walking controller interrupted")
    except Exception as e:
        rospy.logerr(f"Error running walking controller: {e}")
```

### 2.2 Integration Test

Let's create a launch file to test the balance-locomotion integration:

```xml
<!-- launch/balance_locomotion_integration.launch.py -->
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='humanoid_control',
            executable='integrated_humanoid_controller',
            name='integrated_controller',
            output='screen'
        ),
        Node(
            package='humanoid_control',
            executable='zmp_walking_controller',
            name='zmp_walking_controller',
            output='screen'
        )
    ])
```

## Section 3: Perception-Action Integration

In this section, we'll add perception capabilities to enable the robot to interact with its environment based on sensor data.

### 3.1 Multi-Sensor State Estimation

```python
#!/usr/bin/env python3
"""
Multi-Sensor State Estimation with Perception-Action Integration
"""

import rospy
import numpy as np
from sensor_msgs.msg import JointState, Imu, LaserScan
from geometry_msgs.msg import Point, PoseStamped, Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Float64MultiArray
import tf
from tf.transformations import quaternion_from_euler, euler_from_quaternion
from scipy.spatial.transform import Rotation as R

class MultiSensorStateEstimator:
    """
    Multi-sensor state estimator for humanoid robot.
    Integrates IMU, joint encoders, vision, and other sensors.
    """

    def __init__(self):
        rospy.init_node('multi_sensor_state_estimator')

        # State dimensions
        self.state_dim = 13  # [x, y, z, vx, vy, vz, qx, qy, qz, qw, wx, wy, wz]
        self.state = np.zeros(self.state_dim)  # Current state estimate
        self.covariance = np.eye(self.state_dim) * 1.0  # State covariance

        # Sensor data storage
        self.imu_data = None
        self.joint_data = None
        self.vision_data = None
        self.odom_data = None

        # Extended Kalman Filter components
        self.ekf = ExtendedKalmanFilter(self.state_dim, control_dim=6, measurement_dim=12)

        # Publishers and subscribers
        self.state_pub = rospy.Publisher('/estimated_state', Float64MultiArray, queue_size=10)
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.joint_sub = rospy.Subscriber('/joint_states', JointState, self.joint_callback)
        self.odom_sub = rospy.Subscriber('/odom', Odometry, self.odom_callback)
        self.vision_sub = rospy.Subscriber('/vision_data', PoseStamped, self.vision_callback)

        # TF listener for additional pose information
        self.tf_listener = tf.TransformListener()

        # Control parameters
        self.update_rate = 100  # Hz
        self.rate = rospy.Rate(self.update_rate)

        rospy.loginfo("Multi-Sensor State Estimator initialized")

    def imu_callback(self, msg):
        """Handle IMU data updates."""
        self.imu_data = {
            'orientation': np.array([msg.orientation.x, msg.orientation.y,
                                   msg.orientation.z, msg.orientation.w]),
            'angular_velocity': np.array([msg.angular_velocity.x, msg.angular_velocity.y,
                                        msg.angular_velocity.z]),
            'linear_acceleration': np.array([msg.linear_acceleration.x, msg.linear_acceleration.y,
                                           msg.linear_acceleration.z])
        }

    def joint_callback(self, msg):
        """Handle joint state updates."""
        self.joint_data = {
            'positions': np.array(msg.position),
            'velocities': np.array(msg.velocity),
            'efforts': np.array(msg.effort)
        }

    def odom_callback(self, msg):
        """Handle odometry data updates."""
        self.odom_data = {
            'position': np.array([msg.pose.pose.position.x, msg.pose.pose.position.y,
                                msg.pose.pose.position.z]),
            'orientation': np.array([msg.pose.pose.orientation.x, msg.pose.pose.orientation.y,
                                   msg.pose.pose.orientation.z, msg.pose.pose.orientation.w]),
            'linear_velocity': np.array([msg.twist.twist.linear.x, msg.twist.twist.linear.y,
                                       msg.twist.twist.linear.z]),
            'angular_velocity': np.array([msg.twist.twist.angular.x, msg.twist.twist.angular.y,
                                        msg.twist.twist.angular.z])
        }

    def vision_callback(self, msg):
        """Handle vision data updates."""
        self.vision_data = {
            'position': np.array([msg.pose.position.x, msg.pose.position.y, msg.pose.position.z]),
            'orientation': np.array([msg.pose.orientation.x, msg.pose.orientation.y,
                                   msg.pose.orientation.z, msg.pose.orientation.w])
        }

    def predict_state(self, control_input, dt=0.01):
        """Predict state forward using IMU data and control input."""
        if self.imu_data is not None:
            # Use IMU acceleration and angular velocity for prediction
            linear_acc = self.imu_data['linear_acceleration']
            angular_vel = self.imu_data['angular_velocity']

            # Update state prediction based on IMU measurements
            # Position update: x_{k+1} = x_k + v_k * dt + 0.5 * a_k * dt^2
            self.state[0:3] += self.state[3:6] * dt + 0.5 * linear_acc * dt**2

            # Velocity update: v_{k+1} = v_k + a_k * dt
            self.state[3:6] += linear_acc * dt

            # Orientation update using angular velocity integration
            # This is a simplified approach; in practice, use quaternion integration
            delta_orientation = self.integrate_angular_velocity(angular_vel, dt)
            current_orientation = self.state[6:10]
            new_orientation = self.quaternion_multiply(current_orientation, delta_orientation)
            self.state[6:10] = new_orientation / np.linalg.norm(new_orientation)  # Normalize

            # Angular velocity remains (will be updated with measurement)
            self.state[10:13] = angular_vel

    def integrate_angular_velocity(self, angular_vel, dt):
        """Integrate angular velocity to get orientation change."""
        # Convert angular velocity to quaternion
        angle = np.linalg.norm(angular_vel) * dt
        if angle > 1e-6:  # Avoid division by zero
            axis = angular_vel / np.linalg.norm(angular_vel)
            # Create quaternion from axis-angle
            half_angle = angle / 2.0
            sin_half = np.sin(half_angle)
            cos_half = np.cos(half_angle)
            return np.array([cos_half, axis[0]*sin_half, axis[1]*sin_half, axis[2]*sin_half])
        else:
            return np.array([1.0, 0.0, 0.0, 0.0])  # No rotation

    def quaternion_multiply(self, q1, q2):
        """Multiply two quaternions."""
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2

        return np.array([w, x, y, z])

    def update_with_measurements(self):
        """Update state estimate with available measurements."""
        measurements = []
        measurement_indices = []

        # Add position measurements from odometry
        if self.odom_data is not None:
            measurements.extend(self.odom_data['position'])
            measurement_indices.extend([0, 1, 2])  # Position indices

        # Add orientation measurements from IMU
        if self.imu_data is not None:
            # Convert quaternion to Euler angles for easier handling
            euler = self.quaternion_to_euler(self.imu_data['orientation'])
            measurements.extend(euler)
            measurement_indices.extend([7, 8, 9])  # Euler angle indices (simplified)

        # Add angular velocity measurements from IMU
        if self.imu_data is not None:
            measurements.extend(self.imu_data['angular_velocity'])
            measurement_indices.extend([10, 11, 12])  # Angular velocity indices

        # Add vision-based position measurements if available
        if self.vision_data is not None:
            measurements.extend(self.vision_data['position'])
            measurement_indices.extend([0, 1, 2])  # Position indices

        # Perform EKF update with measurements
        if len(measurements) > 0:
            # Create measurement vector and indices
            z = np.array(measurements)
            # In practice, you'd create a proper measurement matrix H
            # For this example, we'll use a simplified approach
            self.update_ekf(z, measurement_indices)

    def quaternion_to_euler(self, quaternion):
        """Convert quaternion to Euler angles."""
        w, x, y, z = quaternion
        # Convert to scipy rotation object and then to Euler angles
        r = R.from_quat([x, y, z, w])
        euler = r.as_euler('xyz')
        return euler

    def update_ekf(self, measurements, indices):
        """Update EKF with measurements."""
        # This would perform the full EKF update
        # For this example, we'll use a simplified approach
        for i, idx in enumerate(indices):
            if idx < len(self.state):
                # Direct measurement update (simplified)
                self.state[idx] = measurements[i]

    def get_robot_state(self):
        """Get current estimated robot state."""
        return {
            'position': self.state[0:3],
            'velocity': self.state[3:6],
            'orientation': self.state[6:10],
            'angular_velocity': self.state[10:13]
        }

    def run_estimation_loop(self):
        """Main state estimation loop."""
        rospy.loginfo("Starting multi-sensor state estimation")

        while not rospy.is_shutdown():
            try:
                # Predict state forward
                control_input = np.zeros(6)  # Placeholder for control input
                self.predict_state(control_input, dt=1.0/self.update_rate)

                # Update with measurements
                self.update_with_measurements()

                # Publish estimated state
                self.publish_state_estimate()

                self.rate.sleep()

            except Exception as e:
                rospy.logerr(f"Error in state estimation: {e}")
                self.rate.sleep()

    def publish_state_estimate(self):
        """Publish the estimated state."""
        msg = Float64MultiArray()
        msg.data = self.state.tolist()
        self.state_pub.publish(msg)

class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for state estimation.
    """

    def __init__(self, state_dim, control_dim, measurement_dim):
        self.state_dim = state_dim
        self.control_dim = control_dim
        self.measurement_dim = measurement_dim

        # State vector: [x, y, z, vx, vy, vz, qx, qy, qz, qw, wx, wy, wz]
        # Position, velocity, orientation (quaternion), angular velocity
        self.state = np.zeros(state_dim)
        self.covariance = np.eye(state_dim) * 1.0

        # Process and measurement noise
        self.process_noise = np.eye(state_dim) * 0.1
        self.measurement_noise = np.eye(measurement_dim) * 0.1

        # Control input effect
        self.control_matrix = np.zeros((state_dim, control_dim))

    def predict(self, control_input, dt=0.01):
        """
        Prediction step: predict state forward in time.
        """
        # State transition model (simplified for humanoid)
        # x_{k+1} = f(x_k, u_k) + w_k
        predicted_state = self.state_transition(self.state, control_input, dt)

        # Linearize state transition model
        F = self.jacobian_state_transition(self.state, control_input, dt)

        # Predict covariance
        predicted_covariance = F @ self.covariance @ F.T + self.process_noise

        self.state = predicted_state
        self.covariance = predicted_covariance

        return self.state, self.covariance

    def state_transition(self, state, control, dt):
        """Nonlinear state transition function."""
        # Implement the nonlinear dynamics model
        new_state = state.copy()

        # Update position based on velocity
        new_state[0:3] += state[3:6] * dt

        # Update velocity based on acceleration (from control or IMU)
        # This would include the full dynamics model
        new_state[3:6] += control[0:3] * dt  # Linear acceleration from control

        # Update orientation based on angular velocity
        # This would require proper quaternion integration
        angular_vel = state[10:13]
        new_state[6:10] = self.integrate_quaternion(state[6:10], angular_vel, dt)

        # Update angular velocity based on control torques
        new_state[10:13] += control[3:6] * dt  # Angular acceleration from control

        return new_state

    def jacobian_state_transition(self, state, control, dt):
        """Jacobian of the state transition function."""
        # Calculate the Jacobian matrix F = ∂f/∂x
        F = np.eye(self.state_dim)

        # Simplified Jacobian - in practice, this would be calculated analytically
        # or using automatic differentiation
        F[0:3, 3:6] = np.eye(3) * dt  # Position-velocity relationship
        F[3:6, 10:13] = np.zeros((3, 3))  # Velocity-angular velocity (simplified)

        return F

    def integrate_quaternion(self, q, omega, dt):
        """Integrate quaternion with angular velocity."""
        # Convert angular velocity to quaternion
        omega_q = np.array([0, omega[0], omega[1], omega[2]])
        # Integrate: q_{k+1} = q_k + 0.5 * dt * (omega_q * q_k)
        dq = 0.5 * self.quaternion_multiply(omega_q, q) * dt
        new_q = q + dq
        # Normalize quaternion
        new_q = new_q / np.linalg.norm(new_q)
        return new_q

    def quaternion_multiply(self, q1, q2):
        """Multiply two quaternions."""
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2

        return np.array([w, x, y, z])

    def update(self, measurement):
        """
        Update step: incorporate measurement into state estimate.
        """
        # Measurement model: z = h(x) + v
        # Calculate measurement Jacobian H = ∂h/∂x
        H = self.jacobian_measurement()

        # Calculate innovation
        expected_measurement = self.measurement_model(self.state)
        innovation = measurement - expected_measurement

        # Calculate innovation covariance
        innovation_cov = H @ self.covariance @ H.T + self.measurement_noise

        # Calculate Kalman gain
        K = self.covariance @ H.T @ np.linalg.inv(innovation_cov)

        # Update state and covariance
        self.state = self.state + K @ innovation
        self.covariance = (np.eye(self.state_dim) - K @ H) @ self.covariance

        return self.state, self.covariance

    def measurement_model(self, state):
        """Nonlinear measurement model."""
        # Return expected measurement based on current state
        # This depends on what sensors are available
        return np.zeros(self.measurement_dim)

    def jacobian_measurement(self):
        """Jacobian of the measurement function."""
        # Calculate the Jacobian matrix H = ∂h/∂x
        return np.zeros((self.measurement_dim, self.state_dim))

if __name__ == '__main__':
    try:
        estimator = MultiSensorStateEstimator()
        estimator.run_estimation_loop()
    except rospy.ROSInterruptException:
        rospy.loginfo("State estimator interrupted")
    except Exception as e:
        rospy.logerr(f"Error running state estimator: {e}")
```

### 3.2 Perception-Action Loop

```python
#!/usr/bin/env python3
"""
Perception-Action Integration Loop
"""

import rospy
import numpy as np
from sensor_msgs.msg import JointState, Imu, Image, PointCloud2
from geometry_msgs.msg import PoseStamped, Point, Vector3
from std_msgs.msg import String, Bool
from cv_bridge import CvBridge
import cv2
import threading
import time

class PerceptionActionLoop:
    """
    Main perception-action integration loop for humanoid robot.
    """

    def __init__(self):
        rospy.init_node('perception_action_loop')

        # Initialize components
        self.state_estimator = MultiSensorStateEstimator()
        self.controller = IntegratedControlArchitecture()
        self.perception_system = PerceptionSystem()

        # Performance monitoring
        self.loop_times = []
        self.last_loop_time = time.time()

        # Publishers and subscribers
        self.action_pub = rospy.Publisher('/action_commands', String, queue_size=10)
        self.debug_pub = rospy.Publisher('/perception_action_debug', String, queue_size=10)

        # Control parameters
        self.perception_rate = 30  # Hz for perception processing
        self.action_rate = 100     # Hz for action execution
        self.perception_period = 1.0 / self.perception_rate
        self.action_period = 1.0 / self.action_rate

        # Threading
        self.running = True
        self.perception_lock = threading.Lock()
        self.action_lock = threading.Lock()

        rospy.loginfo("Perception-Action Integration Loop initialized")

    def perception_step(self):
        """Perception processing step."""
        start_time = time.time()

        # Process sensor data to extract meaningful information
        perception_result = self.perception_system.process_sensors()

        # Update world model based on perception
        self.update_world_model(perception_result)

        # Plan actions based on perception and current goals
        action_plan = self.plan_actions(perception_result)

        # Publish planned actions
        self.publish_action_plan(action_plan)

        # Monitor performance
        loop_time = time.time() - start_time
        self.loop_times.append(loop_time)
        if len(self.loop_times) > 100:
            self.loop_times.pop(0)

        # Log performance if needed
        if loop_time > self.perception_period * 2:
            rospy.logwarn(f"Perception step took {loop_time:.3f}s, exceeding target {self.perception_period:.3f}s")

    def action_step(self):
        """Action execution step."""
        start_time = time.time()

        # Get current state from estimator
        current_state = self.state_estimator.get_robot_state()

        # Execute planned actions
        action_commands = self.execute_action_plan(current_state)

        # Send commands to robot
        self.send_action_commands(action_commands)

        # Monitor performance
        loop_time = time.time() - start_time
        if loop_time > self.action_period * 2:
            rospy.logwarn(f"Action step took {loop_time:.3f}s, exceeding target {self.action_period:.3f}s")

    def update_world_model(self, perception_result):
        """Update internal world model based on perception."""
        # This would update the robot's understanding of its environment
        # including object locations, obstacles, etc.
        pass

    def plan_actions(self, perception_result):
        """Plan actions based on perception and current goals."""
        # This would implement high-level action planning
        # based on perceived environment and task goals

        # For this example, return simple navigation or interaction commands
        if perception_result.get('obstacle_detected', False):
            return "avoid_obstacle"
        elif perception_result.get('target_object_detected', False):
            return "approach_object"
        else:
            return "continue_current_behavior"

    def execute_action_plan(self, current_state):
        """Execute the planned actions."""
        # This would convert high-level actions to low-level motor commands
        # For this example, return placeholder commands
        return np.zeros(28)  # 28 DOF humanoid

    def publish_action_plan(self, action_plan):
        """Publish the planned actions."""
        msg = String()
        msg.data = str(action_plan)
        self.action_pub.publish(msg)

    def send_action_commands(self, commands):
        """Send action commands to robot controllers."""
        # This would interface with the actual control system
        # For this example, just log the commands
        rospy.logdebug(f"Sending action commands: {commands[:5]}...")  # Log first 5 values

    def run_perception_action_loop(self):
        """Main perception-action integration loop."""
        rospy.loginfo("Starting perception-action integration loop")

        # Start perception and action threads
        perception_thread = threading.Thread(target=self.perception_loop)
        action_thread = threading.Thread(target=self.action_loop)

        perception_thread.start()
        action_thread.start()

        try:
            # Keep main thread alive
            rospy.spin()
        except KeyboardInterrupt:
            rospy.loginfo("Shutting down perception-action loop")
            self.running = False

        # Wait for threads to finish
        perception_thread.join()
        action_thread.join()

    def perception_loop(self):
        """Continuous perception processing loop."""
        rate = rospy.Rate(self.perception_rate)

        while not rospy.is_shutdown() and self.running:
            try:
                self.perception_step()
                rate.sleep()
            except Exception as e:
                rospy.logerr(f"Error in perception loop: {e}")
                rate.sleep()

    def action_loop(self):
        """Continuous action execution loop."""
        rate = rospy.Rate(self.action_rate)

        while not rospy.is_shutdown() and self.running:
            try:
                self.action_step()
                rate.sleep()
            except Exception as e:
                rospy.logerr(f"Error in action loop: {e}")
                rate.sleep()

class PerceptionSystem:
    """
    Perception system for environment understanding.
    """

    def __init__(self):
        # Initialize perception components
        self.cv_bridge = CvBridge()

        # Publishers and subscribers
        self.image_sub = rospy.Subscriber('/camera/rgb/image_raw', Image, self.image_callback)
        self.pointcloud_sub = rospy.Subscriber('/camera/depth/points', PointCloud2, self.pointcloud_callback)

        # Perception results
        self.latest_image = None
        self.latest_pointcloud = None
        self.object_detections = []

        rospy.loginfo("Perception System initialized")

    def image_callback(self, msg):
        """Handle image data."""
        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")
            self.latest_image = cv_image
        except Exception as e:
            rospy.logerr(f"Error converting image: {e}")

    def pointcloud_callback(self, msg):
        """Handle point cloud data."""
        self.latest_pointcloud = msg
        # Process point cloud for obstacle detection, etc.

    def process_sensors(self):
        """Process all sensor data for environment understanding."""
        result = {
            'obstacle_detected': False,
            'target_object_detected': False,
            'environment_map': None,
            'object_poses': [],
            'free_space': []
        }

        # Process image data for object detection
        if self.latest_image is not None:
            image_result = self.process_image(self.latest_image)
            result.update(image_result)

        # Process point cloud data for obstacle detection
        if self.latest_pointcloud is not None:
            pc_result = self.process_pointcloud(self.latest_pointcloud)
            result.update(pc_result)

        return result

    def process_image(self, image):
        """Process image for object detection and recognition."""
        result = {
            'obstacle_detected': False,
            'target_object_detected': False,
            'object_poses': []
        }

        # Simple color-based object detection (example)
        # In practice, use deep learning models or other advanced methods
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Define color ranges for target objects
        lower_red = np.array([0, 120, 70])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Filter small detections
                # Calculate object center
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Convert to 3D if depth information is available
                    # For now, just store 2D position
                    result['target_object_detected'] = True
                    result['object_poses'].append({'x': cx, 'y': cy, 'z': 0.0})

        return result

    def process_pointcloud(self, pointcloud):
        """Process point cloud for obstacle detection."""
        result = {
            'obstacle_detected': False,
            'free_space': []
        }

        # Simple obstacle detection based on distance
        # In practice, use more sophisticated methods
        # This is a placeholder - actual point cloud processing would be more complex

        # For this example, assume obstacles are detected within 1 meter
        result['obstacle_detected'] = True  # Placeholder

        return result

if __name__ == '__main__':
    try:
        loop = PerceptionActionLoop()
        loop.run_perception_action_loop()
    except rospy.ROSInterruptException:
        rospy.loginfo("Perception-action loop interrupted")
    except Exception as e:
        rospy.logerr(f"Error running perception-action loop: {e}")
```

### 3.3 Integration Launch File

```xml
<!-- launch/perception_action_integration.launch.py -->
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='humanoid_control',
            executable='multi_sensor_state_estimator',
            name='state_estimator',
            output='screen'
        ),
        Node(
            package='humanoid_control',
            executable='perception_action_loop',
            name='perception_action_loop',
            output='screen'
        ),
        Node(
            package='humanoid_control',
            executable='integrated_humanoid_controller',
            name='integrated_controller',
            output='screen'
        )
    ])
```

## Section 4: Performance Evaluation and Tuning

In this final section, we'll implement tools to evaluate and tune the integrated control system.

### 4.1 Performance Metrics and Evaluation

```python
#!/usr/bin/env python3
"""
Performance Evaluation and Tuning for Integrated Humanoid Control System
"""

import rospy
import numpy as np
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import PoseStamped, Twist
from sensor_msgs.msg import JointState, Imu
import matplotlib.pyplot as plt
import time
import json

class PerformanceEvaluator:
    """
    Performance evaluation system for integrated humanoid control.
    """

    def __init__(self):
        rospy.init_node('performance_evaluator')

        # Performance metrics storage
        self.metrics = {
            'balance_stability': [],
            'walking_efficiency': [],
            'control_accuracy': [],
            'computation_time': [],
            'energy_consumption': [],
            'task_success_rate': []
        }

        # Reference trajectories for comparison
        self.reference_trajectories = {}

        # Publishers and subscribers
        self.state_sub = rospy.Subscriber('/estimated_state', Float64MultiArray, self.state_callback)
        self.joint_sub = rospy.Subscriber('/joint_states', JointState, self.joint_callback)
        self.imu_sub = rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        self.performance_pub = rospy.Publisher('/performance_metrics', Float64MultiArray, queue_size=10)

        # Timing for performance measurement
        self.start_time = time.time()

        # Evaluation parameters
        self.evaluation_window = 10.0  # seconds
        self.evaluation_start = time.time()

        rospy.loginfo("Performance Evaluator initialized")

    def state_callback(self, msg):
        """Handle state estimation updates."""
        state = np.array(msg.data)

        # Calculate balance stability metric
        balance_metric = self.calculate_balance_stability(state)
        self.metrics['balance_stability'].append(balance_metric)

        # Calculate control accuracy metric
        accuracy_metric = self.calculate_control_accuracy(state)
        self.metrics['control_accuracy'].append(accuracy_metric)

    def joint_callback(self, msg):
        """Handle joint state updates."""
        # Calculate energy consumption based on joint efforts
        if len(msg.effort) > 0:
            energy = np.sum(np.abs(msg.effort))  # Simplified energy calculation
            self.metrics['energy_consumption'].append(energy)

    def imu_callback(self, msg):
        """Handle IMU data for stability assessment."""
        # Extract orientation for balance assessment
        orientation = [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w]
        roll, pitch, yaw = self.orientation_to_rpy(orientation)

        # Stability based on orientation deviation from upright
        stability = np.sqrt(roll**2 + pitch**2)
        # Lower values indicate better stability
        self.metrics['balance_stability'].append(1.0 - stability)  # Normalize to 0-1 scale

    def orientation_to_rpy(self, orientation):
        """Convert quaternion to roll-pitch-yaw."""
        x, y, z, w = orientation

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = np.copysign(np.pi / 2, sinp)  # Use 90 degrees if out of range
        else:
            pitch = np.arcsin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = np.arctan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

    def calculate_balance_stability(self, state):
        """Calculate balance stability metric."""
        # State includes [x, y, z, vx, vy, vz, qx, qy, qz, qw, wx, wy, wz]
        # For balance, focus on orientation (quaternion) and angular velocity
        orientation = state[6:10]
        angular_vel = state[10:13]

        # Convert quaternion to roll/pitch angles
        r = np.arctan2(2*(orientation[3]*orientation[0] + orientation[1]*orientation[2]),
                       1 - 2*(orientation[0]**2 + orientation[1]**2))
        p = np.arcsin(2*(orientation[3]*orientation[1] - orientation[2]*orientation[0]))

        # Combine orientation and angular velocity for stability score
        orientation_deviation = np.sqrt(r**2 + p**2)
        angular_velocity_magnitude = np.linalg.norm(angular_vel)

        # Stability score: 0 = unstable, 1 = perfectly stable
        stability_score = np.exp(-(orientation_deviation + 0.1 * angular_velocity_magnitude))

        return stability_score

    def calculate_control_accuracy(self, state):
        """Calculate control accuracy metric."""
        # This would compare actual state to desired state
        # For this example, use a simplified approach
        position_error = np.linalg.norm(state[0:3])  # Distance from origin
        velocity_error = np.linalg.norm(state[3:6])  # Velocity magnitude

        # Accuracy score: 1 = perfect accuracy, 0 = no accuracy
        accuracy_score = np.exp(-(position_error + 0.1 * velocity_error))

        return accuracy_score

    def calculate_walking_efficiency(self):
        """Calculate walking efficiency metric."""
        # This would require reference walking trajectories
        # For this example, return a placeholder
        if len(self.metrics['energy_consumption']) > 0:
            avg_energy = np.mean(self.metrics['energy_consumption'][-100:])  # Last 100 samples
            # Efficiency: lower energy = higher efficiency
            efficiency = 1.0 / (1.0 + avg_energy)  # Normalize to 0-1 scale
            return efficiency
        else:
            return 0.5  # Default value

    def calculate_task_success_rate(self):
        """Calculate task success rate."""
        # This would track completed tasks vs attempted tasks
        # For this example, return a placeholder
        return 0.85  # 85% success rate

    def get_current_performance(self):
        """Get current performance metrics."""
        current_metrics = {}

        for metric_name, values in self.metrics.items():
            if len(values) > 0:
                current_metrics[metric_name] = float(np.mean(values[-10:]))  # Last 10 values
            else:
                current_metrics[metric_name] = 0.0

        # Add efficiency and success rate
        current_metrics['walking_efficiency'] = self.calculate_walking_efficiency()
        current_metrics['task_success_rate'] = self.calculate_task_success_rate()

        return current_metrics

    def evaluate_performance(self):
        """Perform comprehensive performance evaluation."""
        current_metrics = self.get_current_performance()

        rospy.loginfo("=== Performance Evaluation Report ===")
        for metric, value in current_metrics.items():
            rospy.loginfo(f"{metric}: {value:.3f}")

        # Calculate overall performance score
        overall_score = np.mean(list(current_metrics.values()))
        rospy.loginfo(f"Overall Performance Score: {overall_score:.3f}")

        # Check for performance issues
        if current_metrics.get('balance_stability', 1.0) < 0.7:
            rospy.logwarn("Balance stability below threshold, consider tuning balance controller")
        if current_metrics.get('control_accuracy', 1.0) < 0.8:
            rospy.logwarn("Control accuracy below threshold, consider tuning control gains")

        return current_metrics

    def run_evaluation_loop(self):
        """Main evaluation loop."""
        rate = rospy.Rate(1)  # Evaluate once per second

        rospy.loginfo("Starting performance evaluation loop")

        while not rospy.is_shutdown():
            try:
                # Evaluate performance
                metrics = self.evaluate_performance()

                # Publish performance metrics
                self.publish_performance_metrics(metrics)

                rate.sleep()

            except Exception as e:
                rospy.logerr(f"Error in evaluation loop: {e}")
                rate.sleep()

    def publish_performance_metrics(self, metrics):
        """Publish performance metrics."""
        msg = Float64MultiArray()
        msg.data = [metrics.get(key, 0.0) for key in self.metrics.keys()]
        self.performance_pub.publish(msg)

class ParameterTuner:
    """
    Automatic parameter tuning for humanoid control systems.
    """

    def __init__(self):
        rospy.init_node('parameter_tuner')

        # Control parameters to tune
        self.parameters = {
            'balance_kp': 100.0,
            'balance_ki': 10.0,
            'balance_kd': 20.0,
            'walking_step_length': 0.3,
            'walking_step_period': 1.0,
            'zmp_preview_window': 2.0,
            'control_rate': 100.0
        }

        # Performance evaluator interface
        self.performance_evaluator = PerformanceEvaluator()

        # Tuning parameters
        self.tuning_active = False
        self.tuning_method = 'grid_search'  # or 'gradient_descent', 'genetic_algorithm'
        self.current_best_score = 0.0
        self.best_parameters = self.parameters.copy()

        rospy.loginfo("Parameter Tuner initialized")

    def tune_parameters(self):
        """Start parameter tuning process."""
        rospy.loginfo("Starting parameter tuning...")
        self.tuning_active = True

        if self.tuning_method == 'grid_search':
            self.grid_search_tuning()
        elif self.tuning_method == 'gradient_descent':
            self.gradient_descent_tuning()
        elif self.tuning_method == 'genetic_algorithm':
            self.genetic_algorithm_tuning()

        self.tuning_active = False
        rospy.loginfo("Parameter tuning completed")
        rospy.loginfo(f"Best parameters found: {self.best_parameters}")
        rospy.loginfo(f"Best performance score: {self.current_best_score:.3f}")

    def grid_search_tuning(self):
        """Perform grid search parameter tuning."""
        # Define parameter ranges to search
        param_ranges = {
            'balance_kp': np.linspace(50, 200, 4),
            'balance_ki': np.linspace(5, 25, 4),
            'balance_kd': np.linspace(10, 50, 4),
            'walking_step_length': np.linspace(0.2, 0.4, 3)
        }

        # Try all combinations
        best_score = 0.0
        best_params = self.parameters.copy()

        # This is a simplified grid search
        # In practice, use more sophisticated optimization
        for kp in param_ranges['balance_kp']:
            for ki in param_ranges['balance_ki']:
                for kd in param_ranges['balance_kd']:
                    for step_len in param_ranges['walking_step_length']:
                        # Update parameters
                        self.parameters['balance_kp'] = kp
                        self.parameters['balance_ki'] = ki
                        self.parameters['balance_kd'] = kd
                        self.parameters['walking_step_length'] = step_len

                        # Test performance with these parameters
                        score = self.test_parameters()

                        if score > best_score:
                            best_score = score
                            best_params = self.parameters.copy()
                            rospy.loginfo(f"New best score: {score:.3f} with params: {best_params}")

        # Apply best parameters
        self.parameters = best_params
        self.current_best_score = best_score
        self.best_parameters = best_params

    def test_parameters(self):
        """Test current parameters and return performance score."""
        # This would run a short test with current parameters
        # For this example, return a placeholder score based on parameter values
        # In practice, this would run actual robot tests and measure performance

        # Simple scoring function (in practice, run actual tests)
        kp = self.parameters['balance_kp']
        ki = self.parameters['balance_ki']
        kd = self.parameters['balance_kd']

        # Higher KP might improve stability but cause oscillation
        # Find balance between stability and smoothness
        stability_score = min(kp / 200.0, 1.0)  # Higher KP = more stability
        smoothness_score = 1.0 / (1.0 + ki/10.0 + kd/20.0)  # Lower integral/derivative = smoother

        # Combine scores
        score = 0.6 * stability_score + 0.4 * smoothness_score

        # Add some random variation to simulate real testing
        score += np.random.normal(0, 0.05)

        return max(0.0, min(1.0, score))  # Clamp to [0, 1]

    def apply_parameters(self):
        """Apply tuned parameters to control system."""
        # This would send parameters to the actual control system
        # For this example, just log the parameters
        rospy.loginfo(f"Applying tuned parameters: {self.parameters}")

        # In practice, use ROS parameters or service calls
        for param_name, param_value in self.parameters.items():
            rospy.set_param(f'/{param_name}', param_value)

if __name__ == '__main__':
    try:
        # Run performance evaluation
        evaluator = PerformanceEvaluator()

        # For this lab, we'll run a simple evaluation
        rospy.sleep(5.0)  # Let system run for a bit

        # Evaluate performance
        final_metrics = evaluator.evaluate_performance()

        # Save evaluation results
        with open('/tmp/humanoid_performance_evaluation.json', 'w') as f:
            json.dump(final_metrics, f, indent=2)

        rospy.loginfo("Performance evaluation completed. Results saved to /tmp/humanoid_performance_evaluation.json")

    except rospy.ROSInterruptException:
        rospy.loginfo("Performance evaluation interrupted")
    except Exception as e:
        rospy.logerr(f"Error in performance evaluation: {e}")
```

### 4.2 Comprehensive Test Script

```bash
#!/bin/bash
# run_module4_lab.sh

# Source ROS environment
source /opt/ros/humble/setup.bash
source install/setup.bash

echo "Starting Module 4 Lab - Humanoid Control Systems Integration"

# Create results directory
mkdir -p ~/humanoid_lab_results

# Launch the integrated system
echo "Launching integrated humanoid control system..."
ros2 launch humanoid_control integrated_system.launch.py &

# Wait for system to initialize
sleep 10

# Start performance evaluation
echo "Starting performance evaluation..."
ros2 run humanoid_control performance_evaluator &
PERFORMANCE_PID=$!

# Run perception-action integration
echo "Starting perception-action loop..."
ros2 run humanoid_control perception_action_loop &
PERCEPTION_PID=$!

# Wait for some time to collect data
sleep 30

# Evaluate performance
echo "Evaluating system performance..."
ros2 run humanoid_control performance_evaluator --eval

# Stop all processes
kill $PERFORMANCE_PID $PERCEPTION_PID 2>/dev/null

echo "Module 4 Lab completed. Results saved to ~/humanoid_lab_results/"
```

## Lab Exercises

### Exercise 1: Control System Integration
**Objective**: Integrate balance and locomotion controllers to create stable walking.

1. Implement the `integrate_commands` function in the `IntegratedControlArchitecture` class to properly combine commands from different controllers using a task-priority framework.
2. Test the integrated system in simulation and observe how balance and locomotion interact.
3. Adjust the weighting parameters to achieve stable walking while maintaining balance.

**Solution**:
```python
def integrate_commands(self, balance_cmd, locomotion_cmd, whole_body_cmd):
    """
    Integrate commands from different controllers using task-priority framework.
    Balance has highest priority, followed by locomotion, then whole-body tasks.
    """
    # Initialize final command
    final_cmd = np.zeros_like(balance_cmd)

    # Define task priorities and weights
    balance_weight = 0.7    # High priority for balance
    locomotion_weight = 0.2 # Medium priority for locomotion
    whole_body_weight = 0.1 # Lower priority for whole-body tasks

    # Apply null-space projection to ensure higher-priority tasks aren't compromised
    # For balance (highest priority), apply directly
    final_cmd = balance_cmd * balance_weight

    # For locomotion, project onto null space of balance task
    # This is a simplified version - in practice, use full null-space projection
    locomotion_in_nullspace = locomotion_cmd * locomotion_weight
    final_cmd += locomotion_in_nullspace

    # For whole-body tasks, project onto null space of both balance and locomotion
    whole_body_in_nullspace = whole_body_cmd * whole_body_weight
    final_cmd += whole_body_in_nullspace

    # Normalize if needed to prevent command saturation
    max_cmd = np.max(np.abs(final_cmd))
    if max_cmd > 1.0:
        final_cmd = final_cmd / max_cmd

    return final_cmd
```

### Exercise 2: ZMP-Based Walking
**Objective**: Implement a complete ZMP-based walking controller with balance recovery.

1. Complete the `ZMPWalkingController` class to generate stable walking patterns.
2. Implement the balance recovery mechanism using capture point theory.
3. Test the walking controller in simulation and tune parameters for stable locomotion.

**Solution**:
```python
def compute_zmp_reference(self, phase, footsteps):
    """Compute ZMP reference trajectory for walking."""
    # Calculate current step and phase within step
    step_index = int(phase / self.step_period)
    phase_in_step = phase % self.step_period

    if step_index < len(footsteps):
        current_support = footsteps[step_index]
        next_support = footsteps[min(step_index + 1, len(footsteps) - 1)]

        # Use 5th order polynomial for smooth ZMP transition
        alpha = phase_in_step / self.step_period
        # 5th order polynomial for smooth transition
        smooth_alpha = 10 * alpha**3 - 15 * alpha**4 + 6 * alpha**5

        # Interpolate between current and next support foot positions
        zmp_x = current_support['position'][0] * (1 - smooth_alpha) + next_support['position'][0] * smooth_alpha
        zmp_y = current_support['position'][1] * (1 - smooth_alpha) + next_support['position'][1] * smooth_alpha

        self.zmp_reference = np.array([zmp_x, zmp_y])

    return self.zmp_reference

def generate_recovery_commands(self, capture_point):
    """Generate commands to move to capture point."""
    # Calculate desired CoM position to achieve capture point
    desired_com_x = capture_point[0]
    desired_com_y = capture_point[1]

    # Get current CoM estimate from state estimator
    current_com = self.estimate_com_position()

    # Calculate CoM position error
    com_error = np.array([desired_com_x, desired_com_y]) - current_com[:2]

    # Generate recovery commands based on CoM error
    recovery_cmd = np.zeros(28)

    # Apply recovery to ankle joints for balance
    # Use PD control for CoM position tracking
    kp_com = 50.0
    kd_com = 10.0

    # Estimate CoM velocity for derivative term
    current_com_vel = self.estimate_com_velocity()
    com_vel_error = -current_com_vel[:2]  # Drive velocity to zero

    # Calculate ankle joint commands
    ankle_cmd_x = kp_com * com_error[0] + kd_com * com_vel_error[0]
    ankle_cmd_y = kp_com * com_error[1] + kd_com * com_vel_error[1]

    # Map to ankle joint indices (assuming ankle joints are at indices 0 and 1)
    recovery_cmd[0] = ankle_cmd_y  # Ankle roll
    recovery_cmd[1] = ankle_cmd_x  # Ankle pitch

    return recovery_cmd
```

### Exercise 3: Perception-Action Integration
**Objective**: Create a perception-action loop that allows the robot to respond to environmental changes.

1. Implement the `process_image` function to detect objects and obstacles.
2. Create a simple navigation planner that generates paths around obstacles.
3. Integrate the perception system with the walking controller to avoid obstacles.

**Solution**:
```python
def process_image(self, image):
    """Process image for object detection and obstacle avoidance."""
    result = {
        'obstacle_detected': False,
        'target_object_detected': False,
        'object_poses': [],
        'obstacle_positions': [],
        'free_space': []
    }

    # Convert to grayscale for edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection
    edges = cv2.Canny(blurred, 50, 150)

    # Find contours (potential obstacles/objects)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Filter small contours
            # Calculate bounding rectangle
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate center of object in image coordinates
            center_x = x + w // 2
            center_y = y + h // 2

            # Determine if this is an obstacle or target based on size/location
            if w * h > 5000:  # Large object - likely an obstacle
                result['obstacle_detected'] = True
                # Convert image coordinates to relative positions
                # This would require camera calibration in practice
                relative_x = (center_x - image.shape[1] // 2) / image.shape[1]  # Normalize to [-0.5, 0.5]
                relative_y = (center_y - image.shape[0] // 2) / image.shape[0]  # Normalize to [-0.5, 0.5]

                result['obstacle_positions'].append({
                    'x': relative_x,
                    'y': relative_y,
                    'distance_estimate': self.estimate_distance(w, h)
                })
            else:
                # Smaller object - could be target
                result['target_object_detected'] = True
                result['object_poses'].append({
                    'x': center_x,
                    'y': center_y,
                    'width': w,
                    'height': h
                })

    return result

def estimate_distance(self, pixel_width, pixel_height):
    """Estimate distance to object based on pixel size."""
    # This is a simplified distance estimation
    # In practice, use calibrated camera parameters
    # and known object size for accurate distance estimation

    # Assume known object size (e.g., 0.1m x 0.1m)
    known_width_m = 0.1
    focal_length_pixels = 500  # Approximate focal length

    # Distance = (known_width * focal_length) / pixel_width
    distance = (known_width_m * focal_length_pixels) / max(pixel_width, pixel_height)
    return min(distance, 5.0)  # Cap at 5m
```

## Summary

This lab has provided hands-on experience with integrating all major components of humanoid control systems:

1. **Integrated Control Architecture**: You learned to combine multiple control systems (balance, locomotion, whole-body) into a unified framework using task-priority approaches.

2. **Balance and Locomotion Integration**: You implemented ZMP-based walking with balance recovery mechanisms, learning how to maintain stability during locomotion.

3. **Perception-Action Integration**: You created perception systems that process sensor data and generate appropriate actions, enabling environmental interaction.

4. **Performance Evaluation**: You developed tools to measure and tune system performance, ensuring optimal behavior.

The complete integrated system demonstrates how modern humanoid robots combine multiple sophisticated control techniques to achieve complex behaviors like walking, balancing, and environmental interaction. This forms the foundation for advanced humanoid robotics applications.

## Next Steps

After completing this lab, you should be able to:
- Design and implement integrated control architectures for humanoid robots
- Combine different control strategies while maintaining system stability
- Integrate perception systems with control systems for environmental interaction
- Evaluate and tune complex robotic systems for optimal performance

Continue to experiment with different parameter settings, control strategies, and perception algorithms to deepen your understanding of humanoid control systems.