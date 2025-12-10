---
title: "Module 4.1 - Chapter 1: Balance and Posture Control"
sidebar_position: 1
---

# Module 4.1 - Balance and Posture Control

## Overview

Balance and posture control are fundamental challenges in humanoid robotics. Unlike wheeled or tracked robots, humanoid robots must maintain dynamic balance while performing tasks. This chapter explores the principles of balance control, various control strategies, and implementation techniques for maintaining stable posture in humanoid robots.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the physics of balance in bipedal systems
- Implement Zero Moment Point (ZMP) based balance controllers
- Design Center of Mass (CoM) control strategies
- Apply inverted pendulum models for balance control
- Implement feedback control for posture stabilization
- Analyze stability margins and balance recovery strategies

## Introduction to Humanoid Balance

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/humanoid_balance_concepts_dark.svg' : '/img/module_4/humanoid_balance_concepts_light.svg'}
        alt="Humanoid Balance Concepts: Static vs Dynamic Stability"
        style={{width: '100%', maxWidth: '700px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

Humanoid balance control addresses the challenge of maintaining stability while the robot is statically unstable. Unlike a table that is stable in its resting position, a humanoid robot must actively control its balance through coordinated joint movements.

### Static vs. Dynamic Stability

- **Static Stability**: Center of Mass (CoM) remains within the support polygon
- **Dynamic Stability**: Balance maintained through controlled motion and momentum

For humanoid robots, dynamic stability is essential as the support polygon (feet) is typically smaller than the robot's base.

## Zero Moment Point (ZMP) Theory

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/zmp_theory_illustration_dark.svg' : '/img/module_4/zmp_theory_illustration_light.svg'}
        alt="Zero Moment Point (ZMP) Theory for Humanoid Balance"
        style={{width: '100%', maxWidth: '700px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

The Zero Moment Point is a critical concept in humanoid balance control. It represents the point on the ground where the net moment of the ground reaction forces is zero.

### Mathematical Foundation

The ZMP is calculated as:
```
ZMP_x = (Mg * x_CoM - I * θ̈) / (Mg - Mz̈)
ZMP_y = (Mg * y_CoM - I * θ̈) / (Mg - Mz̈)
```

Where:
- M: Robot mass
- g: Gravitational acceleration
- x_CoM, y_CoM: Center of Mass coordinates
- I: Moment of inertia
- θ̈: Angular acceleration
- z̈: Vertical acceleration

### ZMP Stability Condition

For stable walking, the ZMP must remain within the support polygon defined by the feet:
```
x_support_min ≤ ZMP_x ≤ x_support_max
y_support_min ≤ ZMP_y ≤ y_support_max
```

## Inverted Pendulum Models

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/inverted_pendulum_models_dark.svg' : '/img/module_4/inverted_pendulum_models_light.svg'}
        alt="Inverted Pendulum Models for Humanoid Balance Control"
        style={{width: '100%', maxWidth: '700px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

### Linear Inverted Pendulum Model (LIPM)

The Linear Inverted Pendulum Model simplifies the balance problem by assuming constant height:
```
ẍ_CoM = ω²(x_CoM - x_ZMP)
```

Where ω² = g/h and h is the constant CoM height.

The solution for the CoM trajectory is:
```
x_CoM(t) = x_ZMP + A * e^(ωt) + B * e^(-ωt)
```

### Capture Point Concept

The Capture Point is the location where the robot must step to come to a complete stop:
```
Capture_Point = CoM_Position + CoM_Velocity/ω
```

## Balance Control Strategies

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/balance_control_strategies_dark.svg' : '/img/module_4/balance_control_strategies_light.svg'}
        alt="Balance Control Strategies for Humanoid Robots"
        style={{width: '100%', maxWidth: '800px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

### Feedback Control Approaches

```python
import numpy as np
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3

class BalanceController:
    """
    Balance controller using PID feedback control.
    """

    def __init__(self):
        # Control parameters
        self.kp = 100.0   # Proportional gain
        self.ki = 10.0    # Integral gain
        self.kd = 20.0    # Derivative gain

        # State variables
        self.error_integral = 0.0
        self.previous_error = 0.0
        self.previous_time = rospy.Time.now().to_sec()

        # Balance targets
        self.target_roll = 0.0
        self.target_pitch = 0.0
        self.target_yaw = 0.0

        # Publishers for joint control
        self.joint_publishers = {}

    def update_balance(self, current_orientation, current_angular_velocity):
        """
        Update balance control based on current state.
        """
        current_time = rospy.Time.now().to_sec()
        dt = current_time - self.previous_time

        if dt <= 0:
            return np.zeros(3)  # Return zero torques if dt is invalid

        # Calculate errors
        roll_error = self.target_roll - current_orientation.x
        pitch_error = self.target_pitch - current_orientation.y
        yaw_error = self.target_yaw - current_orientation.z

        # Update integral terms
        self.error_integral += np.array([roll_error, pitch_error, yaw_error]) * dt

        # Calculate derivatives
        error_derivative = (np.array([roll_error, pitch_error, yaw_error]) -
                           np.array([self.previous_error[0], self.previous_error[1], self.previous_error[2]])) / dt

        # Store current errors for next iteration
        self.previous_error = [roll_error, pitch_error, yaw_error]

        # PID control
        control_output = (self.kp * np.array([roll_error, pitch_error, yaw_error]) +
                         self.ki * self.error_integral +
                         self.kd * error_derivative)

        self.previous_time = current_time

        return control_output

class ZMPController:
    """
    Zero Moment Point controller for balance control.
    """

    def __init__(self, robot_mass, gravity=9.81):
        self.mass = robot_mass
        self.gravity = gravity
        self.height = 0.8  # Assumed CoM height
        self.omega = np.sqrt(self.gravity / self.height)

        # Support polygon parameters
        self.support_polygon = {
            'x_min': -0.1,  # 10cm behind ankle
            'x_max': 0.1,   # 10cm in front of ankle
            'y_min': -0.05, # 5cm to the side
            'y_max': 0.05   # 5cm to the side
        }

    def calculate_zmp(self, com_position, com_acceleration):
        """
        Calculate ZMP from CoM position and acceleration.
        """
        zmp_x = com_position[0] - com_acceleration[0] / self.omega**2
        zmp_y = com_position[1] - com_acceleration[1] / self.omega**2

        return np.array([zmp_x, zmp_y])

    def is_stable(self, zmp):
        """
        Check if ZMP is within support polygon.
        """
        x, y = zmp
        return (self.support_polygon['x_min'] <= x <= self.support_polygon['x_max'] and
                self.support_polygon['y_min'] <= y <= self.support_polygon['y_max'])

    def compute_com_trajectory(self, initial_com, target_com, duration, dt=0.01):
        """
        Compute CoM trajectory to achieve target ZMP.
        """
        t = np.arange(0, duration, dt)
        trajectory = []

        for ti in t:
            # Use 5th order polynomial interpolation
            ratio = ti / duration if duration > 0 else 1.0

            if ratio >= 1.0:
                trajectory.append(target_com)
            else:
                # 5th order polynomial for smooth transition
                h = 6 * ratio**5 - 15 * ratio**4 + 10 * ratio**3
                current_pos = initial_com + h * (target_com - initial_com)
                trajectory.append(current_pos)

        return np.array(trajectory)

    def generate_balance_correction(self, current_zmp, desired_zmp):
        """
        Generate balance correction based on ZMP error.
        """
        zmp_error = desired_zmp - current_zmp

        # Use feedback control to determine CoM adjustment
        # This is a simplified model - in practice, more complex inverse kinematics is needed
        com_correction = zmp_error * 0.1  # Scaling factor

        return com_correction

class CapturePointController:
    """
    Capture Point based balance controller.
    """

    def __init__(self, com_height, gravity=9.81):
        self.height = com_height
        self.gravity = gravity
        self.omega = np.sqrt(self.gravity / self.height)

    def calculate_capture_point(self, com_position, com_velocity):
        """
        Calculate the capture point based on current CoM state.
        """
        capture_point = com_position + com_velocity / self.omega
        return capture_point

    def should_step(self, current_capture_point, foot_positions):
        """
        Determine if a step is needed based on capture point.
        """
        # Check if capture point is outside support polygon
        # Simplified for 2D case (x-y plane)
        support_polygon = self.calculate_support_polygon(foot_positions)

        # Check if capture point is within support polygon
        x, y = current_capture_point[:2]

        return not (support_polygon['x_min'] <= x <= support_polygon['x_max'] and
                   support_polygon['y_min'] <= y <= support_polygon['y_max'])

    def calculate_support_polygon(self, foot_positions):
        """
        Calculate the support polygon based on foot positions.
        """
        if len(foot_positions) == 0:
            return {'x_min': 0, 'x_max': 0, 'y_min': 0, 'y_max': 0}

        x_coords = [pos[0] for pos in foot_positions]
        y_coords = [pos[1] for pos in foot_positions]

        return {
            'x_min': min(x_coords) - 0.05,  # Add margin
            'x_max': max(x_coords) + 0.05,
            'y_min': min(y_coords) - 0.1,
            'y_max': max(y_coords) + 0.1
        }

    def plan_step_location(self, current_capture_point, foot_positions):
        """
        Plan where to step to recover balance.
        """
        # Simple strategy: step toward capture point
        # In practice, this would involve more sophisticated planning

        # Calculate where capture point needs to be to be stable
        if len(foot_positions) == 0:
            # No feet down, need to step somewhere
            return current_capture_point[:2]

        # Find closest foot to move
        target_location = current_capture_point[:2]

        return target_location
```

## Whole-Body Balance Control

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/whole_body_balance_control_dark.svg' : '/img/module_4/whole_body_balance_control_light.svg'}
        alt="Whole-Body Balance Control for Humanoid Robots"
        style={{width: '100%', maxWidth: '800px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

### Center of Mass Control

```python
class CoMController:
    """
    Center of Mass controller for whole-body balance.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.target_com = np.zeros(3)  # Default target CoM
        self.current_com = np.zeros(3)

        # Control parameters
        self.com_kp = 50.0
        self.com_kd = 10.0

    def update_com_target(self, new_target):
        """
        Update the target CoM position.
        """
        self.target_com = new_target

    def compute_com_control(self, current_com, current_com_velocity):
        """
        Compute control output for CoM stabilization.
        """
        com_error = self.target_com - current_com
        com_control = (self.com_kp * com_error -
                      self.com_kd * current_com_velocity)

        return com_control

    def compute_joint_torques(self, com_control, current_joint_positions,
                             current_joint_velocities):
        """
        Convert CoM control to joint torques using inverse dynamics.
        """
        # This would typically use inverse kinematics and dynamics
        # For simplicity, we'll use a basic mapping
        jacobian = self.robot_model.get_com_jacobian()

        # Pseudo-inverse of Jacobian
        jacobian_inv = np.linalg.pinv(jacobian)

        # Compute required joint torques
        joint_torques = jacobian_inv.T @ com_control

        return joint_torques

class WholeBodyController:
    """
    Integrated whole-body controller combining multiple control objectives.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.com_controller = CoMController(robot_model)
        self.zmp_controller = ZMPController(robot_model.mass)
        self.balance_controller = BalanceController()

        # Task priorities
        self.task_weights = {
            'balance': 1.0,
            'posture': 0.3,
            'end_effector': 0.5
        }

    def compute_control(self, sensor_data):
        """
        Compute integrated control for whole-body balance.
        """
        # Extract sensor data
        current_orientation = sensor_data['orientation']
        current_angular_velocity = sensor_data['angular_velocity']
        current_com = sensor_data['com_position']
        current_com_velocity = sensor_data['com_velocity']
        current_joint_positions = sensor_data['joint_positions']
        current_joint_velocities = sensor_data['joint_velocities']

        # Compute individual control components
        balance_torques = self.balance_controller.update_balance(
            current_orientation, current_angular_velocity)

        com_control = self.com_controller.compute_com_control(
            current_com, current_com_velocity)

        # Convert CoM control to joint torques
        com_torques = self.com_controller.compute_joint_torques(
            com_control, current_joint_positions, current_joint_velocities)

        # Combine control objectives with priorities
        total_torques = (self.task_weights['balance'] * balance_torques +
                        self.task_weights['posture'] * com_torques)

        return total_torques

    def update_target_posture(self, target_posture):
        """
        Update target posture for the robot.
        """
        self.com_controller.update_com_target(target_posture)
```

## Balance Recovery Strategies

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/balance_recovery_strategies_dark.svg' : '/img/module_4/balance_recovery_strategies_light.svg'}
        alt="Balance Recovery Strategies for Humanoid Robots"
        style={{width: '100%', maxWidth: '800px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

### Fall Prevention and Recovery

```python
class BalanceRecoveryController:
    """
    Balance recovery controller for handling large disturbances.
    """

    def __init__(self):
        self.recovery_mode = False
        self.step_planner = CapturePointController(com_height=0.8)
        self.swing_leg_controller = SwingLegController()

        # Recovery thresholds
        self.tilt_threshold = np.radians(15)  # 15 degrees
        self.angular_velocity_threshold = np.radians(2)  # 2 rad/s
        self.com_drift_threshold = 0.1  # 10 cm

    def evaluate_stability(self, sensor_data):
        """
        Evaluate current stability and determine if recovery is needed.
        """
        orientation = sensor_data['orientation']
        angular_velocity = sensor_data['angular_velocity']
        com_position = sensor_data['com_position']
        com_velocity = sensor_data['com_velocity']

        # Check tilt angle
        tilt_angle = np.sqrt(orientation.x**2 + orientation.y**2)

        # Check angular velocity
        angular_speed = np.sqrt(angular_velocity.x**2 + angular_velocity.y**2)

        # Check CoM drift
        com_drift = np.sqrt(com_velocity[0]**2 + com_velocity[1]**2)

        # Determine if recovery is needed
        needs_recovery = (tilt_angle > self.tilt_threshold or
                         angular_speed > self.angular_velocity_threshold or
                         com_drift > self.com_drift_threshold)

        return needs_recovery, tilt_angle, angular_speed, com_drift

    def execute_recovery_step(self, current_state):
        """
        Execute a recovery step to regain balance.
        """
        # Calculate capture point
        capture_point = self.step_planner.calculate_capture_point(
            current_state['com_position'],
            current_state['com_velocity']
        )

        # Determine if step is needed
        foot_positions = current_state.get('foot_positions', [])
        should_step = self.step_planner.should_step(capture_point, foot_positions)

        if should_step:
            # Plan step location
            step_location = self.step_planner.plan_step_location(
                capture_point, foot_positions
            )

            # Execute step
            step_result = self.swing_leg_controller.execute_step(
                step_location, current_state
            )

            return step_result

        return False  # No step needed

    def adjust_posture(self, current_state):
        """
        Adjust posture to improve balance without stepping.
        """
        # This would involve adjusting joint angles to move CoM back to safe region
        # For example, bending knees, adjusting hip position, etc.

        posture_adjustment = np.zeros(len(current_state['joint_positions']))

        # Example: If tilted forward, adjust hip and ankle
        orientation = current_state['orientation']
        if orientation.y > 0.1:  # Tilted forward
            # Adjust hip pitch to move CoM back
            posture_adjustment[0] = -0.1  # Hip pitch adjustment
            posture_adjustment[1] = 0.05  # Ankle pitch adjustment

        return posture_adjustment

class SwingLegController:
    """
    Controller for swing leg motion during stepping.
    """

    def __init__(self):
        self.step_height = 0.1  # 10cm step height
        self.step_duration = 0.8  # 800ms step duration

    def plan_step_trajectory(self, start_pos, target_pos):
        """
        Plan a trajectory for the swing foot.
        """
        # Use 5th order polynomial for smooth motion
        duration = self.step_duration
        dt = 0.01  # 10ms control steps

        t = np.arange(0, duration, dt)
        trajectory = []

        # Calculate 3D trajectory
        for ti in t:
            ratio = ti / duration
            if ratio > 1.0:
                ratio = 1.0

            # 5th order polynomial for smooth interpolation
            h = 6 * ratio**5 - 15 * ratio**4 + 10 * ratio**3

            # Calculate position
            pos = start_pos + h * (target_pos - start_pos)

            # Add step height for clearance
            if 0.2 < ratio < 0.8:  # Mid-swing
                pos[2] += self.step_height * np.sin(np.pi * (ratio - 0.2) / 0.6)

            trajectory.append(pos)

        return np.array(trajectory)

    def execute_step(self, target_location, current_state):
        """
        Execute a step to the target location.
        """
        # Get current swing foot position
        swing_foot_pos = current_state.get('swing_foot_position',
                                         np.array([0.0, 0.0, 0.0]))

        # Plan trajectory
        target_pos = np.array([target_location[0], target_location[1], 0.0])
        trajectory = self.plan_step_trajectory(swing_foot_pos, target_pos)

        # Execute trajectory (in simulation, this would send commands to actuators)
        for i, pos in enumerate(trajectory):
            # Convert position to joint angles using inverse kinematics
            joint_angles = self.inverse_kinematics(pos)

            # Send joint commands
            self.send_joint_commands(joint_angles)

            # Sleep for control rate
            rospy.sleep(0.01)

        return True

    def inverse_kinematics(self, target_pos):
        """
        Simplified inverse kinematics for leg.
        """
        # This would be a full IK solver in practice
        # For now, return placeholder joint angles
        return np.zeros(6)  # 6 DOF leg

    def send_joint_commands(self, joint_angles):
        """
        Send joint angle commands to the robot.
        """
        # This would interface with the actual robot hardware
        pass
```

## Implementation Example: Simple Balance Controller

```python
#!/usr/bin/env python3
"""
Complete implementation of a balance controller for a simulated humanoid robot.
"""

import rospy
import numpy as np
from sensor_msgs.msg import Imu, JointState
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Vector3
import time

class HumanoidBalanceNode:
    """
    ROS node for humanoid balance control.
    """

    def __init__(self):
        rospy.init_node('humanoid_balance_controller')

        # Initialize controllers
        self.balance_controller = BalanceController()
        self.zmp_controller = ZMPController(robot_mass=60.0)
        self.recovery_controller = BalanceRecoveryController()

        # State variables
        self.current_orientation = Vector3(0, 0, 0)
        self.current_angular_velocity = Vector3(0, 0, 0)
        self.current_joint_positions = np.zeros(28)  # Example: 28 DOF humanoid
        self.current_joint_velocities = np.zeros(28)

        # Publishers and subscribers
        self.joint_command_pub = rospy.Publisher(
            '/joint_group_position_controller/command',
            Float64MultiArray,
            queue_size=10
        )

        rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)

        # Control parameters
        self.control_rate = 100  # 100 Hz
        self.rate = rospy.Rate(self.control_rate)

        print("Humanoid Balance Controller initialized")

    def imu_callback(self, msg):
        """
        Handle IMU data for balance control.
        """
        # Extract orientation (simplified - would need proper quaternion conversion)
        self.current_orientation.x = msg.orientation.x
        self.current_orientation.y = msg.orientation.y
        self.current_orientation.z = msg.orientation.z

        # Extract angular velocity
        self.current_angular_velocity = msg.angular_velocity

    def joint_state_callback(self, msg):
        """
        Handle joint state data.
        """
        if len(msg.position) == len(self.current_joint_positions):
            self.current_joint_positions = np.array(msg.position)
            self.current_joint_velocities = np.array(msg.velocity)

    def compute_balance_control(self):
        """
        Main balance control computation.
        """
        # Check for balance recovery
        sensor_data = {
            'orientation': self.current_orientation,
            'angular_velocity': self.current_angular_velocity,
            'joint_positions': self.current_joint_positions,
            'joint_velocities': self.current_joint_velocities
        }

        needs_recovery, tilt, ang_vel, com_drift = self.recovery_controller.evaluate_stability(sensor_data)

        if needs_recovery:
            print(f"Balance recovery needed: tilt={np.degrees(tilt):.1f}°, ang_vel={ang_vel:.2f} rad/s")
            recovery_result = self.recovery_controller.execute_recovery_step(sensor_data)

            if not recovery_result:
                # If step didn't help, try posture adjustment
                posture_adjustment = self.recovery_controller.adjust_posture(sensor_data)
                return posture_adjustment
        else:
            # Normal balance control
            control_output = self.balance_controller.update_balance(
                self.current_orientation,
                self.current_angular_velocity
            )

            return control_output

    def run(self):
        """
        Main control loop.
        """
        print("Starting balance control loop...")

        while not rospy.is_shutdown():
            try:
                # Compute balance control
                control_commands = self.compute_balance_control()

                # Publish joint commands
                cmd_msg = Float64MultiArray()
                cmd_msg.data = control_commands.tolist()
                self.joint_command_pub.publish(cmd_msg)

                # Sleep to maintain control rate
                self.rate.sleep()

            except rospy.ROSInterruptException:
                print("Balance controller interrupted")
                break
            except Exception as e:
                print(f"Error in balance control: {e}")
                rospy.sleep(0.1)  # Brief pause before continuing

def main():
    """
    Main function to start the balance controller.
    """
    try:
        balance_node = HumanoidBalanceNode()
        balance_node.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("Balance controller stopped by user")

if __name__ == '__main__':
    main()
```

## Advanced Balance Control Techniques

<BrowserOnly>
  {() => {
    const { theme } = useDocusaurusContext();
    const isDarkMode = theme?.appearance?.darkMode ?? false;
    return (
      <img
        src={isDarkMode ? '/img/module_4/advanced_balance_control_techniques_dark.svg' : '/img/module_4/advanced_balance_control_techniques_light.svg'}
        alt="Advanced Balance Control Techniques for Humanoid Robots"
        style={{width: '100%', maxWidth: '800px', margin: '20px auto', display: 'block'}}
      />
    );
  }}
</BrowserOnly>

### Model Predictive Control for Balance

```python
import cvxpy as cp

class ModelPredictiveBalanceController:
    """
    Model Predictive Control for humanoid balance.
    """

    def __init__(self, prediction_horizon=20, dt=0.01):
        self.N = prediction_horizon  # Prediction horizon
        self.dt = dt  # Time step
        self.n_states = 4  # [x, x_dot, y, y_dot] for simplified model
        self.n_controls = 2  # [F_x, F_y] forces

        # System matrices for LIPM
        self.A = np.array([
            [1, self.dt, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, self.dt],
            [0, 0, 0, 1]
        ])

        self.B = np.array([
            [self.dt**2 / 2, 0],
            [self.dt, 0],
            [0, self.dt**2 / 2],
            [0, self.dt]
        ])

        # Cost matrices
        self.Q = np.eye(self.n_states) * 10  # State cost
        self.R = np.eye(self.n_controls) * 0.1  # Control cost
        self.Qf = np.eye(self.n_states) * 50  # Terminal cost

    def solve_mpc(self, current_state, reference_trajectory):
        """
        Solve the MPC optimization problem.
        """
        # Decision variables
        X = cp.Variable((self.n_states, self.N + 1))
        U = cp.Variable((self.n_controls, self.N))

        # Objective function
        objective = 0

        # Running costs
        for k in range(self.N):
            state_error = X[:, k] - reference_trajectory[k]
            objective += cp.quad_form(state_error, self.Q)
            objective += cp.quad_form(U[:, k], self.R)

        # Terminal cost
        final_error = X[:, self.N] - reference_trajectory[self.N]
        objective += cp.quad_form(final_error, self.Qf)

        # Constraints
        constraints = []

        # Initial state
        constraints.append(X[:, 0] == current_state)

        # System dynamics
        for k in range(self.N):
            constraints.append(X[:, k+1] == self.A @ X[:, k] + self.B @ U[:, k])

        # Control limits (example: ±500N forces)
        for k in range(self.N):
            constraints.append(cp.norm(U[:, k], 2) <= 500)

        # ZMP constraints (simplified)
        for k in range(self.N):
            # ZMP = CoM - CoM_ddot / omega^2
            # For LIPM: ZMP_x = x - z_ddot/omega^2 (assuming constant height)
            # Simplified constraint on CoM position
            constraints.append(X[0, k] <= 0.1)  # x position limit
            constraints.append(X[0, k] >= -0.1)
            constraints.append(X[2, k] <= 0.05)  # y position limit
            constraints.append(X[2, k] >= -0.05)

        # Solve the problem
        problem = cp.Problem(cp.Minimize(objective), constraints)
        problem.solve(solver=cp.ECOS)

        if problem.status not in ["infeasible", "unbounded"]:
            # Return the first control input
            return U[:, 0].value
        else:
            # Return zero control if infeasible
            return np.zeros(self.n_controls)

    def update_reference(self, desired_com_position, current_time):
        """
        Update reference trajectory based on desired CoM position.
        """
        reference_trajectory = []

        for k in range(self.N + 1):
            t_k = current_time + k * self.dt
            # Simple reference: go to desired position
            ref_state = np.array([
                desired_com_position[0],
                0,  # desired velocity
                desired_com_position[1],
                0   # desired velocity
            ])
            reference_trajectory.append(ref_state)

        return reference_trajectory
```

## Exercises

### Exercise 1: ZMP Stability Analysis
Implement a ZMP calculator for a simulated humanoid robot and analyze the stability margins for different walking speeds. Calculate the maximum perturbation the robot can handle while maintaining balance.

### Exercise 2: PID Controller Tuning
Tune the PID parameters for the balance controller to achieve critical damping. Test the controller's response to impulse disturbances and measure the settling time and overshoot.

### Exercise 3: Capture Point Validation
Implement the capture point calculation and validate it against simulated robot dynamics. Compare the predicted capture point with the actual point where the robot needs to step to stop.

### Exercise 4: MPC vs PID Comparison
Compare the performance of Model Predictive Control and PID control for balance recovery. Measure stability margins, control effort, and response time for both approaches.

## Summary

This chapter covered the fundamental concepts of balance and posture control in humanoid robots. We explored the Zero Moment Point theory, inverted pendulum models, and various control strategies including PID control, ZMP-based control, and Model Predictive Control. The implementation examples provide practical insights into developing balance controllers for real humanoid robots.

The key takeaways include:
- Balance control requires continuous adjustment of the Center of Mass
- ZMP is a critical metric for determining stability
- Multiple control strategies can be combined for robust balance
- Recovery strategies are essential for handling large disturbances
- Real-time performance is crucial for effective balance control

In the next chapter, we'll explore locomotion control and walking pattern generation for humanoid robots.