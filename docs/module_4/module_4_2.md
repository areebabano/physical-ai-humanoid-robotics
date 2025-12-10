---
title: "Module 4.2 -  Chapter 2: Locomotion Control"
sidebar_position: 2
---

# Module 4.2 - Locomotion Control

## Overview

Locomotion control is a critical aspect of humanoid robotics that involves generating and executing walking patterns while maintaining balance and stability. This chapter explores various locomotion strategies, walking pattern generation, and control techniques for enabling humanoid robots to move effectively in diverse environments.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the principles of humanoid locomotion and walking patterns
- Implement walking pattern generators using various approaches
- Design controllers for stable walking and gait transitions
- Analyze and optimize walking parameters for different terrains
- Implement recovery strategies for walking disturbances
- Integrate locomotion with balance control systems

## Introduction to Humanoid Locomotion

Humanoid locomotion involves the complex task of generating stable walking patterns that enable the robot to move from one location to another while maintaining balance. Unlike wheeled robots, humanoid robots must manage the dynamic balance of an inverted pendulum system while executing alternating leg movements.

### Walking Phases

Humanoid walking consists of several distinct phases:

1. **Single Support Phase**: One foot is in contact with the ground
2. **Double Support Phase**: Both feet are in contact with the ground
3. **Swing Phase**: One foot is moving through the air
4. **Contact Phase**: Foot makes contact with the ground

### Key Locomotion Parameters

- **Step Length**: Distance between consecutive foot placements
- **Step Width**: Lateral distance between feet
- **Step Height**: Vertical clearance during swing phase
- **Walking Speed**: Average forward velocity
- **Step Frequency**: Steps per unit time
- **Support Duration**: Time spent in single/double support phases

## Walking Pattern Generation

### Preview Control Method

Preview control is a widely used approach for generating stable walking patterns by considering future reference trajectories.

```python
import numpy as np
from scipy.linalg import solve_continuous_are
import matplotlib.pyplot as plt

class PreviewController:
    """
    Preview controller for walking pattern generation based on ZMP reference.
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

        # Solve Riccati equation for LQR
        self.K = self.solve_lqr()

        # Preview gain calculation
        self.preview_gain = self.calculate_preview_gain()

    def solve_lqr(self):
        """
        Solve LQR problem to get feedback gain matrix.
        """
        # Continuous algebraic Riccati equation
        P = solve_continuous_are(self.A, self.B.reshape(-1, 1), self.Q, self.R)

        # Feedback gain
        K = (1/self.R) * self.B.T @ P
        return K

    def calculate_preview_gain(self):
        """
        Calculate preview gain for future reference tracking.
        """
        # This is a simplified preview gain calculation
        # In practice, this involves solving differential equations
        preview_steps = int(self.preview_window / self.sampling_time)
        preview_gain = np.zeros(preview_steps)

        # Exponential decay for preview weights
        for i in range(preview_steps):
            preview_gain[i] = np.exp(-0.1 * i)

        return preview_gain

    def generate_trajectory(self, zmp_reference, initial_state):
        """
        Generate CoM trajectory based on ZMP reference using preview control.
        """
        n_steps = len(zmp_reference)
        trajectory = np.zeros((n_steps, 3))  # [x, x_dot, x_ddot]
        state = initial_state.copy()

        for k in range(n_steps):
            # Current error
            zmp_ref = zmp_reference[k]
            com_pos = state[0]
            zmp_current = com_pos - state[2] / self.omega**2

            # Error calculation
            e = zmp_current - zmp_ref

            # Future preview contribution (simplified)
            preview_contribution = 0
            for j in range(min(len(self.preview_gain), n_steps - k)):
                preview_contribution += self.preview_gain[j] * (zmp_reference[k + j] - zmp_ref)

            # Control input
            u = -self.K @ state + preview_contribution

            # Update state
            state_dot = self.A @ state + self.B * u
            state = state + state_dot * self.sampling_time

            trajectory[k] = state

        return trajectory

class WalkingPatternGenerator:
    """
    Generator for complete walking patterns including CoM, foot positions, and ZMP.
    """

    def __init__(self, step_length=0.3, step_width=0.2, step_height=0.05,
                 com_height=0.8, walking_period=1.0):
        self.step_length = step_length
        self.step_width = step_width
        self.step_height = step_height
        self.com_height = com_height
        self.walking_period = walking_period

        # Initialize preview controller
        self.preview_controller = PreviewController(com_height=com_height)

    def generate_foot_trajectory(self, start_pos, n_steps, step_type='forward'):
        """
        Generate foot trajectory for walking.
        """
        # Foot positions
        left_foot_pos = []
        right_foot_pos = []

        # Generate for n_steps
        for i in range(n_steps):
            t = i * self.walking_period

            # Left foot trajectory
            if i % 2 == 0:  # Left foot support phase
                # During support phase, foot is stationary
                left_x = start_pos[0] + (i // 2) * self.step_length
                left_y = start_pos[1] + self.step_width / 2 * (-1) ** (i // 2)
                left_z = 0  # On ground
            else:  # Left foot swing phase
                # Generate swing trajectory
                phase = (i % 2) * 0.5  # 0.0 or 0.5
                left_x = start_pos[0] + (i // 2 + 1) * self.step_length
                left_y = start_pos[1] + self.step_width / 2 * (-1) ** (i // 2 + 1)
                left_z = self.step_height * np.sin(np.pi * phase)  # Swing height

            # Right foot trajectory (opposite phase)
            if i % 2 == 1:  # Right foot support phase
                right_x = start_pos[0] + (i // 2) * self.step_length
                right_y = start_pos[1] + self.step_width / 2 * (-1) ** (i // 2 + 1)
                right_z = 0  # On ground
            else:  # Right foot swing phase
                right_x = start_pos[0] + (i // 2 + 1) * self.step_length
                right_y = start_pos[1] + self.step_width / 2 * (-1) ** (i // 2)
                right_z = self.step_height * np.sin(np.pi * (1 - (i % 2) * 0.5))  # Swing height

            left_foot_pos.append([left_x, left_y, left_z])
            right_foot_pos.append([right_x, right_y, right_z])

        return np.array(left_foot_pos), np.array(right_foot_pos)

    def generate_zmp_reference(self, n_steps):
        """
        Generate ZMP reference trajectory for stable walking.
        """
        zmp_ref = []

        for i in range(n_steps):
            # Simple ZMP reference - between feet during double support
            # and under supporting foot during single support
            if i % 2 == 0:  # Left foot support
                zmp_x = i * self.step_length  # Approximate
                zmp_y = -self.step_width / 4  # Slightly toward left foot
            else:  # Right foot support
                zmp_x = i * self.step_length
                zmp_y = self.step_width / 4   # Slightly toward right foot

            zmp_ref.append([zmp_x, zmp_y])

        return np.array(zmp_ref)

    def generate_com_trajectory(self, zmp_reference, initial_com_pos):
        """
        Generate CoM trajectory based on ZMP reference.
        """
        # Prepare initial state [x, x_dot, x_ddot]
        initial_state_x = np.array([initial_com_pos[0], 0, 0])
        initial_state_y = np.array([initial_com_pos[1], 0, 0])

        # Generate trajectories for X and Y directions separately
        com_x_traj = self.preview_controller.generate_trajectory(
            zmp_reference[:, 0], initial_state_x
        )
        com_y_traj = self.preview_controller.generate_trajectory(
            zmp_reference[:, 1], initial_state_y
        )

        # Combine into full trajectory
        com_trajectory = np.column_stack([
            com_x_traj[:, 0],  # x position
            com_y_traj[:, 0],  # y position
            np.full(len(com_x_traj), self.com_height)  # z position (constant height)
        ])

        return com_trajectory

    def generate_complete_walking_pattern(self, n_steps, start_pos=[0, 0, 0]):
        """
        Generate complete walking pattern including CoM, feet, and ZMP.
        """
        # Generate foot trajectories
        left_foot, right_foot = self.generate_foot_trajectory(start_pos, n_steps)

        # Generate ZMP reference
        zmp_reference = self.generate_zmp_reference(n_steps)

        # Generate CoM trajectory
        com_trajectory = self.generate_com_trajectory(zmp_reference, start_pos)

        return {
            'com_trajectory': com_trajectory,
            'left_foot_trajectory': left_foot,
            'right_foot_trajectory': right_foot,
            'zmp_reference': zmp_reference,
            'n_steps': n_steps
        }

# Example usage
def example_preview_control():
    """
    Example of using preview control for walking pattern generation.
    """
    # Initialize walking pattern generator
    walker = WalkingPatternGenerator(
        step_length=0.3,
        step_width=0.2,
        step_height=0.05,
        com_height=0.8,
        walking_period=1.0
    )

    # Generate walking pattern
    pattern = walker.generate_complete_walking_pattern(n_steps=10)

    print("Walking pattern generated successfully!")
    print(f"CoM trajectory shape: {pattern['com_trajectory'].shape}")
    print(f"Left foot trajectory shape: {pattern['left_foot_trajectory'].shape}")
    print(f"ZMP reference shape: {pattern['zmp_reference'].shape}")

    return pattern
```

### Inverted Pendulum Model for Walking

```python
class InvertedPendulumWalking:
    """
    Walking controller based on inverted pendulum model.
    """

    def __init__(self, com_height=0.8, gravity=9.81):
        self.com_height = com_height
        self.gravity = gravity
        self.omega = np.sqrt(gravity / com_height)

        # Walking parameters
        self.step_length = 0.3
        self.step_width = 0.2
        self.walking_period = 1.0

        # Support polygon
        self.support_polygon = {
            'x_min': -0.1,
            'x_max': 0.1,
            'y_min': -0.1,
            'y_max': 0.1
        }

    def compute_zmp_from_com(self, com_pos, com_acc):
        """
        Compute ZMP from CoM position and acceleration.
        """
        zmp_x = com_pos[0] - com_acc[0] / self.omega**2
        zmp_y = com_pos[1] - com_acc[1] / self.omega**2

        return np.array([zmp_x, zmp_y, 0])

    def plan_step_location(self, current_com, target_direction=[1, 0]):
        """
        Plan next step location based on current CoM and target direction.
        """
        # Calculate where to step to maintain balance
        # This is a simplified approach - in practice, use capture point
        step_x = current_com[0] + self.step_length * target_direction[0]
        step_y = current_com[1] + self.step_width * target_direction[1] * 0.5

        return np.array([step_x, step_y, 0])

    def generate_swing_foot_trajectory(self, start_pos, target_pos, step_height=0.05):
        """
        Generate smooth trajectory for swing foot motion.
        """
        # Number of trajectory points
        n_points = 50
        trajectory = []

        # Calculate trajectory using 5th order polynomial
        for i in range(n_points):
            t = i / (n_points - 1)  # Normalized time [0, 1]

            # 5th order polynomial coefficients for smooth motion
            poly = 6*t**5 - 15*t**4 + 10*t**3

            # Interpolate position
            pos_x = start_pos[0] + poly * (target_pos[0] - start_pos[0])
            pos_y = start_pos[1] + poly * (target_pos[1] - start_pos[1])

            # Add vertical motion for step clearance
            if 0.2 < t < 0.8:  # Mid-swing
                pos_z = start_pos[2] + step_height * np.sin(np.pi * (t - 0.2) / 0.6)
            else:
                pos_z = start_pos[2] + (target_pos[2] - start_pos[2]) * poly

            trajectory.append([pos_x, pos_y, pos_z])

        return np.array(trajectory)

    def compute_com_dynamics(self, zmp_ref, current_com, current_com_vel, dt=0.01):
        """
        Compute CoM dynamics based on ZMP reference.
        """
        # Inverted pendulum dynamics: COM_ddot = omega^2 * (COM - ZMP)
        com_acc_x = self.omega**2 * (current_com[0] - zmp_ref[0])
        com_acc_y = self.omega**2 * (current_com[1] - zmp_ref[1])

        # Update velocity and position
        new_com_vel = current_com_vel + np.array([com_acc_x, com_acc_y, 0]) * dt
        new_com_pos = current_com + new_com_vel * dt

        # Keep CoM at constant height
        new_com_pos[2] = self.com_height

        return new_com_pos, new_com_vel, np.array([com_acc_x, com_acc_y, 0])

class WalkingController:
    """
    Complete walking controller that integrates pattern generation and execution.
    """

    def __init__(self):
        self.inverted_pendulum = InvertedPendulumWalking()
        self.pattern_generator = WalkingPatternGenerator()

        # Walking state
        self.current_state = {
            'com_pos': np.array([0.0, 0.0, 0.8]),
            'com_vel': np.array([0.0, 0.0, 0.0]),
            'com_acc': np.array([0.0, 0.0, 0.0]),
            'left_foot_pos': np.array([0.0, 0.1, 0.0]),
            'right_foot_pos': np.array([0.0, -0.1, 0.0]),
            'current_step': 0,
            'walking_phase': 'double_support'  # double_support, left_support, right_support
        }

        # Walking parameters
        self.step_length = 0.3
        self.step_width = 0.2
        self.step_height = 0.05
        self.walking_speed = 0.3  # m/s

    def update_walking_phase(self):
        """
        Update walking phase based on step timing.
        """
        # This is a simplified phase update
        # In practice, use more sophisticated gait phase detection
        phase_duration = self.walking_period / 2  # Half cycle

        if self.current_state['current_step'] % 2 == 0:
            self.current_state['walking_phase'] = 'left_support'
        else:
            self.current_state['walking_phase'] = 'right_support'

    def compute_walking_control(self, target_velocity, dt=0.01):
        """
        Compute walking control commands based on target velocity.
        """
        # Calculate desired ZMP based on target velocity
        desired_zmp = self.calculate_desired_zmp(target_velocity)

        # Update CoM dynamics
        new_com_pos, new_com_vel, new_com_acc = self.inverted_pendulum.compute_com_dynamics(
            desired_zmp,
            self.current_state['com_pos'],
            self.current_state['com_vel'],
            dt
        )

        # Update walking phase
        self.update_walking_phase()

        # Plan next step if needed
        next_step_pos = self.plan_next_step()

        # Update state
        self.current_state['com_pos'] = new_com_pos
        self.current_state['com_vel'] = new_com_vel
        self.current_state['com_acc'] = new_com_acc

        return {
            'com_command': new_com_pos,
            'zmp_command': desired_zmp,
            'next_step_pos': next_step_pos,
            'walking_phase': self.current_state['walking_phase']
        }

    def calculate_desired_zmp(self, target_velocity):
        """
        Calculate desired ZMP based on target walking velocity.
        """
        # Simple ZMP planning based on velocity
        # In practice, use more sophisticated methods
        current_com = self.current_state['com_pos']

        # Lead the ZMP in the direction of movement
        zmp_offset_x = target_velocity[0] * 0.1  # Proportional to velocity
        zmp_offset_y = target_velocity[1] * 0.1

        desired_zmp = np.array([
            current_com[0] - zmp_offset_x,
            current_com[1] - zmp_offset_y,
            0
        ])

        return desired_zmp

    def plan_next_step(self):
        """
        Plan the location of the next step.
        """
        current_com = self.current_state['com_pos']

        # Simple step planning - place foot ahead in walking direction
        if self.current_state['walking_phase'] == 'left_support':
            # Right foot will swing next
            next_step_x = current_com[0] + self.step_length
            next_step_y = current_com[1] - self.step_width  # Alternate sides
        else:
            # Left foot will swing next
            next_step_x = current_com[0] + self.step_length
            next_step_y = current_com[1] + self.step_width

        return np.array([next_step_x, next_step_y, 0])

    def check_stability(self):
        """
        Check if current walking state is stable.
        """
        current_com = self.current_state['com_pos']
        current_com_acc = self.current_state['com_acc']

        # Calculate current ZMP
        current_zmp = self.inverted_pendulum.compute_zmp_from_com(
            current_com, current_com_acc
        )

        # Check if ZMP is within support polygon
        support_polygon = self.get_current_support_polygon()

        is_stable = (support_polygon['x_min'] <= current_zmp[0] <= support_polygon['x_max'] and
                     support_polygon['y_min'] <= current_zmp[1] <= support_polygon['y_max'])

        return is_stable, current_zmp

    def get_current_support_polygon(self):
        """
        Get the current support polygon based on foot positions.
        """
        if self.current_state['walking_phase'] == 'left_support':
            # Only left foot is supporting
            support_polygon = {
                'x_min': self.current_state['left_foot_pos'][0] - 0.05,
                'x_max': self.current_state['left_foot_pos'][0] + 0.05,
                'y_min': self.current_state['left_foot_pos'][1] - 0.1,
                'y_max': self.current_state['left_foot_pos'][1] + 0.1
            }
        elif self.current_state['walking_phase'] == 'right_support':
            # Only right foot is supporting
            support_polygon = {
                'x_min': self.current_state['right_foot_pos'][0] - 0.05,
                'x_max': self.current_state['right_foot_pos'][0] + 0.05,
                'y_min': self.current_state['right_foot_pos'][1] - 0.1,
                'y_max': self.current_state['right_foot_pos'][1] + 0.1
            }
        else:  # double_support
            # Both feet are supporting
            all_x = [self.current_state['left_foot_pos'][0], self.current_state['right_foot_pos'][0]]
            all_y = [self.current_state['left_foot_pos'][1], self.current_state['right_foot_pos'][1]]
            support_polygon = {
                'x_min': min(all_x) - 0.05,
                'x_max': max(all_x) + 0.05,
                'y_min': min(all_y) - 0.1,
                'y_max': max(all_y) + 0.1
            }

        return support_polygon
```

## Gait Pattern Generation

### Footstep Planning

```python
class FootstepPlanner:
    """
    Planner for generating footstep sequences for humanoid walking.
    """

    def __init__(self, step_length=0.3, step_width=0.2, max_turn=np.pi/6):
        self.step_length = step_length
        self.step_width = step_width
        self.max_turn = max_turn

    def plan_footsteps(self, start_pos, goal_pos, start_orientation=0):
        """
        Plan sequence of footsteps from start to goal position.
        """
        footsteps = []

        # Calculate total distance and direction
        dx = goal_pos[0] - start_pos[0]
        dy = goal_pos[1] - start_pos[1]
        total_distance = np.sqrt(dx**2 + dy**2)
        direction_angle = np.arctan2(dy, dx)

        # Calculate number of steps needed
        n_steps = int(np.ceil(total_distance / self.step_length))

        # Generate footsteps
        current_pos = np.array(start_pos)
        current_orientation = start_orientation

        for i in range(n_steps + 1):  # +1 to include goal position
            # Calculate step position
            if i == 0:
                # Starting position
                step_pos = start_pos
            elif i == n_steps:
                # Final position
                step_pos = goal_pos
            else:
                # Intermediate step
                ratio = i / n_steps
                step_x = start_pos[0] + ratio * dx
                step_y = start_pos[1] + ratio * dy
                step_pos = [step_x, step_y, start_pos[2]]

            # Alternate feet
            foot_type = 'left' if i % 2 == 0 else 'right'

            # Add to footsteps
            footsteps.append({
                'position': step_pos,
                'foot_type': foot_type,
                'step_number': i
            })

        return footsteps

    def plan_terrain_adaptive_footsteps(self, path, terrain_map=None):
        """
        Plan footsteps adapted to terrain characteristics.
        """
        adaptive_footsteps = []

        for i, waypoint in enumerate(path):
            # Get terrain information at this point
            if terrain_map:
                terrain_info = self.analyze_terrain(waypoint, terrain_map)
            else:
                terrain_info = {'slope': 0, 'roughness': 0, 'obstacles': []}

            # Adjust step based on terrain
            adjusted_pos = self.adjust_step_for_terrain(waypoint, terrain_info)

            # Alternate feet
            foot_type = 'left' if i % 2 == 0 else 'right'

            adaptive_footsteps.append({
                'position': adjusted_pos,
                'foot_type': foot_type,
                'terrain_info': terrain_info,
                'step_number': i
            })

        return adaptive_footsteps

    def analyze_terrain(self, position, terrain_map):
        """
        Analyze terrain characteristics at given position.
        """
        # This would interface with actual terrain mapping
        # For simulation, return dummy values
        return {
            'slope': np.random.uniform(-0.1, 0.1),  # Random slope
            'roughness': np.random.uniform(0, 0.05),  # Surface roughness
            'obstacles': []  # No obstacles for now
        }

    def adjust_step_for_terrain(self, original_pos, terrain_info):
        """
        Adjust step position based on terrain characteristics.
        """
        adjusted_pos = list(original_pos)

        # Adjust for slope
        slope_adjustment = terrain_info['slope'] * 0.1  # Small adjustment
        adjusted_pos[2] += slope_adjustment  # Height adjustment

        # Adjust for roughness (wider steps on rough terrain)
        if terrain_info['roughness'] > 0.02:
            # Increase step width slightly
            pass  # In real implementation, adjust foot placement

        return adjusted_pos

class GaitPatternGenerator:
    """
    Generator for complete gait patterns including timing and coordination.
    """

    def __init__(self, walking_period=1.0, dsp_ratio=0.1):
        self.walking_period = walking_period
        self.dsp_ratio = dsp_ratio  # Double support phase ratio
        self.ssp_ratio = 1.0 - dsp_ratio  # Single support phase ratio

        # Phase durations
        self.dsp_duration = walking_period * dsp_ratio
        self.ssp_duration = walking_period * ssp_ratio / 2  # Per foot

    def generate_gait_timings(self, n_steps):
        """
        Generate timing information for gait phases.
        """
        timings = []

        for i in range(n_steps):
            # Calculate phase start times
            step_start = i * self.walking_period

            # Double support phase at beginning of step
            dsp_start = step_start
            dsp_end = dsp_start + self.dsp_duration

            # Single support phase for current support foot
            ssp_start = dsp_end
            ssp_end = ssp_start + self.ssp_duration

            # Double support phase at end of step
            dsp2_start = ssp_end
            dsp2_end = dsp2_start + self.dsp_duration

            # Next single support phase for other foot
            ssp2_start = dsp2_end
            ssp2_end = ssp2_start + self.ssp_duration

            timing_info = {
                'step_number': i,
                'step_start': step_start,
                'dsp1_start': dsp_start,
                'dsp1_end': dsp_end,
                'ssp1_start': ssp_start,
                'ssp1_end': ssp_end,
                'dsp2_start': dsp2_start,
                'dsp2_end': dsp2_end,
                'ssp2_start': ssp2_start,
                'ssp2_end': ssp2_end,
                'step_end': ssp2_end
            }

            timings.append(timing_info)

        return timings

    def generate_joint_trajectories(self, footsteps, gait_timings):
        """
        Generate joint trajectories for walking based on footsteps and timing.
        """
        # This would generate detailed joint angle trajectories
        # For now, return a simplified representation
        joint_trajectories = []

        for i, (footstep, timing) in enumerate(zip(footsteps, gait_timings)):
            # Generate joint trajectory for this step
            step_duration = timing['step_end'] - timing['step_start']
            n_points = int(step_duration / 0.01)  # 100Hz control

            # Simplified joint trajectory generation
            joint_step = {
                'step_number': i,
                'n_points': n_points,
                'duration': step_duration,
                'support_foot': 'left' if i % 2 == 0 else 'right',
                'swing_foot': 'right' if i % 2 == 0 else 'left'
            }

            joint_trajectories.append(joint_step)

        return joint_trajectories
```

## Walking Control Strategies

### Feedback Control for Walking

```python
class WalkingFeedbackController:
    """
    Feedback controller for stabilizing walking patterns.
    """

    def __init__(self, kp_com=100, ki_com=10, kd_com=20,
                 kp_foot=50, ki_foot=5, kd_foot=10):
        # CoM control gains
        self.kp_com = kp_com
        self.ki_com = ki_com
        self.kd_com = kd_com

        # Foot control gains
        self.kp_foot = kp_foot
        self.ki_foot = ki_foot
        self.kd_foot = kd_foot

        # Error integrals
        self.com_error_integral = np.zeros(3)
        self.foot_error_integral = np.zeros(3)

        # Previous errors
        self.previous_com_error = np.zeros(3)
        self.previous_foot_error = np.zeros(3)

        # Timing
        self.previous_time = 0

    def update_control(self, current_state, desired_state, dt=0.01):
        """
        Update feedback control based on current and desired states.
        """
        current_time = time.time()
        if self.previous_time == 0:
            dt = 0.01
        else:
            dt = current_time - self.previous_time

        # Calculate errors
        com_error = desired_state['com_pos'] - current_state['com_pos']
        foot_error = desired_state['foot_pos'] - current_state['foot_pos']

        # Update error integrals
        self.com_error_integral += com_error * dt
        self.foot_error_integral += foot_error * dt

        # Calculate derivatives
        com_error_derivative = (com_error - self.previous_com_error) / dt if dt > 0 else np.zeros(3)
        foot_error_derivative = (foot_error - self.previous_foot_error) / dt if dt > 0 else np.zeros(3)

        # PID control for CoM
        com_control = (self.kp_com * com_error +
                      self.ki_com * self.com_error_integral +
                      self.kd_com * com_error_derivative)

        # PID control for foot
        foot_control = (self.kp_foot * foot_error +
                       self.ki_foot * self.foot_error_integral +
                       self.kd_foot * foot_error_derivative)

        # Store for next iteration
        self.previous_com_error = com_error
        self.previous_foot_error = foot_error
        self.previous_time = current_time

        return {
            'com_control': com_control,
            'foot_control': foot_control,
            'dt': dt
        }

class WalkingStabilizer:
    """
    Advanced walking stabilizer that combines multiple control strategies.
    """

    def __init__(self):
        self.feedback_controller = WalkingFeedbackController()
        self.com_admittance_controller = ComAdmittanceController()
        self.foot_placement_controller = FootPlacementController()

        # Stability thresholds
        self.zmp_threshold = 0.05  # meters
        self.com_height_threshold = 0.02  # meters

    def stabilize_walking(self, sensor_data, reference_trajectory, dt=0.01):
        """
        Stabilize walking using multiple control strategies.
        """
        # Extract sensor data
        current_com = sensor_data['com_pos']
        current_com_vel = sensor_data['com_vel']
        current_com_acc = sensor_data['com_acc']
        current_foot_pos = sensor_data['foot_pos']
        current_imu = sensor_data['imu']

        # Calculate current ZMP
        current_zmp = self.calculate_current_zmp(current_com, current_com_acc)

        # Get reference values
        ref_com = reference_trajectory['com_pos']
        ref_foot = reference_trajectory['foot_pos']
        ref_zmp = reference_trajectory['zmp']

        # Check stability
        stability_metrics = self.evaluate_stability(
            current_com, ref_com, current_zmp, ref_zmp
        )

        # Generate control commands based on stability
        control_commands = {}

        if stability_metrics['is_stable']:
            # Normal walking control
            feedback_control = self.feedback_controller.update_control(
                {'com_pos': current_com, 'foot_pos': current_foot_pos},
                {'com_pos': ref_com, 'foot_pos': ref_foot},
                dt
            )

            control_commands.update(feedback_control)
        else:
            # Apply recovery control
            recovery_control = self.apply_recovery_control(
                sensor_data, reference_trajectory, stability_metrics
            )
            control_commands.update(recovery_control)

        return control_commands, stability_metrics

    def calculate_current_zmp(self, com_pos, com_acc):
        """
        Calculate current ZMP from CoM position and acceleration.
        """
        gravity = 9.81
        com_height = com_pos[2]
        omega = np.sqrt(gravity / com_height)

        zmp_x = com_pos[0] - com_acc[0] / omega**2
        zmp_y = com_pos[1] - com_acc[1] / omega**2

        return np.array([zmp_x, zmp_y, 0])

    def evaluate_stability(self, current_com, ref_com, current_zmp, ref_zmp):
        """
        Evaluate walking stability based on multiple metrics.
        """
        # ZMP error
        zmp_error = np.linalg.norm(current_zmp[:2] - ref_zmp[:2])

        # CoM tracking error
        com_error = np.linalg.norm(current_com - ref_com)

        # Check if within thresholds
        is_stable = (zmp_error < self.zmp_threshold and
                     com_error < 2 * self.zmp_threshold)  # More permissive for CoM

        stability_metrics = {
            'zmp_error': zmp_error,
            'com_error': com_error,
            'is_stable': is_stable,
            'zmp_threshold': self.zmp_threshold,
            'com_threshold': 2 * self.zmp_threshold
        }

        return stability_metrics

    def apply_recovery_control(self, sensor_data, reference_trajectory, stability_metrics):
        """
        Apply recovery control when walking becomes unstable.
        """
        # Recovery strategy based on type of instability
        if stability_metrics['zmp_error'] > self.zmp_threshold:
            # ZMP-based recovery
            recovery_commands = self.zmp_based_recovery(sensor_data)
        else:
            # General balance recovery
            recovery_commands = self.general_balance_recovery(sensor_data)

        return recovery_commands

    def zmp_based_recovery(self, sensor_data):
        """
        ZMP-based recovery control.
        """
        current_com = sensor_data['com_pos']
        current_com_vel = sensor_data['com_vel']

        # Calculate desired CoM adjustment to bring ZMP back to safe region
        desired_com_offset = self.calculate_zmp_recovery_com_offset(sensor_data)

        # Generate control to achieve desired CoM position
        recovery_control = {
            'com_adjustment': desired_com_offset,
            'zmp_recovery_active': True
        }

        return recovery_control

    def general_balance_recovery(self, sensor_data):
        """
        General balance recovery control.
        """
        # This would implement more general recovery strategies
        # like stepping, hip strategies, etc.
        recovery_control = {
            'balance_strategy': 'adjust_com',
            'recovery_active': True
        }

        return recovery_control

    def calculate_zmp_recovery_com_offset(self, sensor_data):
        """
        Calculate CoM offset needed to recover ZMP stability.
        """
        current_com = sensor_data['com_pos']
        current_com_acc = sensor_data['com_acc']

        # Simple proportional recovery
        gravity = 9.81
        com_height = current_com[2]
        omega = np.sqrt(gravity / com_height)

        # Calculate how much to adjust CoM to bring ZMP back to reference
        # ZMP = CoM - CoM_ddot/omega^2
        # So to achieve desired ZMP, CoM should be: ZMP + CoM_ddot/omega^2
        desired_zmp = np.array([current_com[0], current_com[1], 0])  # Target ZMP under CoM
        desired_com = desired_zmp + current_com_acc / omega**2

        com_offset = desired_com - current_com

        return com_offset

class ComAdmittanceController:
    """
    Admittance controller for CoM control during walking.
    """

    def __init__(self, admittance_matrix=None):
        if admittance_matrix is None:
            # Default admittance matrix (diagonal)
            self.admittance_matrix = np.diag([0.01, 0.01, 0.001])  # [x, y, z] admittance
        else:
            self.admittance_matrix = admittance_matrix

        # Damping and stiffness
        self.damping_ratio = 0.7
        self.natural_frequency = 2.0  # Hz

    def compute_com_adjustment(self, external_wrench, current_state):
        """
        Compute CoM adjustment based on external wrench using admittance control.
        """
        # External wrench typically includes forces and moments
        # For walking, we focus on forces that affect balance
        force_x, force_y, force_z = external_wrench[:3]

        # Apply admittance control: pos_change = admittance * force
        force_vector = np.array([force_x, force_y, force_z])
        pos_change = self.admittance_matrix @ force_vector

        return pos_change

class FootPlacementController:
    """
    Controller for dynamic foot placement during walking.
    """

    def __init__(self):
        # Capture point based foot placement
        self.com_height = 0.8
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / self.com_height)

        # Foot placement gains
        self.capture_point_gain = 0.8
        self.velocity_gain = 0.1

    def calculate_foot_placement(self, current_state, desired_velocity):
        """
        Calculate optimal foot placement based on current state.
        """
        current_com = current_state['com_pos']
        current_com_vel = current_state['com_vel']

        # Calculate capture point
        capture_point = self.calculate_capture_point(current_com, current_com_vel)

        # Calculate desired foot placement
        # Combine capture point with desired stepping direction
        desired_foot_x = (self.capture_point_gain * capture_point[0] +
                         self.velocity_gain * desired_velocity[0])
        desired_foot_y = (self.capture_point_gain * capture_point[1] +
                         self.velocity_gain * desired_velocity[1])

        # Add nominal step width alternation
        step_width = 0.2  # Nominal step width
        current_step_number = current_state.get('step_number', 0)
        if current_step_number % 2 == 0:
            desired_foot_y += step_width / 2  # Left foot
        else:
            desired_foot_y -= step_width / 2  # Right foot

        return np.array([desired_foot_x, desired_foot_y, 0])

    def calculate_capture_point(self, com_pos, com_vel):
        """
        Calculate the capture point for the current CoM state.
        """
        capture_point_x = com_pos[0] + com_vel[0] / self.omega
        capture_point_y = com_pos[1] + com_vel[1] / self.omega

        return np.array([capture_point_x, capture_point_y, 0])
```

## Terrain Adaptive Walking

### Adaptive Control for Different Terrains

```python
class TerrainAdaptiveWalker:
    """
    Walking controller that adapts to different terrain conditions.
    """

    def __init__(self):
        self.terrain_classifier = TerrainClassifier()
        self.adaptive_controller = AdaptiveWalkingController()
        self.footstep_adjuster = FootstepAdjuster()

    def walk_on_terrain(self, sensor_data, target_velocity, terrain_map=None):
        """
        Walk adaptively based on terrain conditions.
        """
        # Classify current terrain
        terrain_type = self.terrain_classifier.classify_terrain(sensor_data, terrain_map)

        # Get terrain-specific parameters
        terrain_params = self.get_terrain_parameters(terrain_type)

        # Adjust walking pattern based on terrain
        adjusted_commands = self.adaptive_controller.generate_adaptive_commands(
            sensor_data, target_velocity, terrain_params
        )

        return adjusted_commands, terrain_type

    def get_terrain_parameters(self, terrain_type):
        """
        Get walking parameters for specific terrain type.
        """
        terrain_params = {
            'flat': {
                'step_length': 0.3,
                'step_height': 0.05,
                'step_width': 0.2,
                'walking_period': 1.0,
                'dsp_ratio': 0.1,
                'max_angular_velocity': 0.5
            },
            'uneven': {
                'step_length': 0.2,
                'step_height': 0.1,
                'step_width': 0.25,
                'walking_period': 1.2,
                'dsp_ratio': 0.15,
                'max_angular_velocity': 0.3
            },
            'slippery': {
                'step_length': 0.15,
                'step_height': 0.02,
                'step_width': 0.2,
                'walking_period': 1.5,
                'dsp_ratio': 0.2,
                'max_angular_velocity': 0.2
            },
            'stairs': {
                'step_length': 0.25,
                'step_height': 0.15,
                'step_width': 0.2,
                'walking_period': 1.3,
                'dsp_ratio': 0.12,
                'max_angular_velocity': 0.3
            }
        }

        return terrain_params.get(terrain_type, terrain_params['flat'])

class TerrainClassifier:
    """
    Classify terrain types based on sensor data.
    """

    def classify_terrain(self, sensor_data, terrain_map=None):
        """
        Classify terrain based on available sensor data.
        """
        # This would typically use multiple sensors:
        # - Vision for surface texture/color
        # - Force/torque sensors for compliance
        # - IMU for vibrations
        # - Range sensors for roughness

        if terrain_map:
            # Use pre-mapped terrain information
            current_pos = sensor_data.get('position', [0, 0, 0])
            terrain_type = self.get_terrain_from_map(current_pos, terrain_map)
        else:
            # Use sensor-based classification
            terrain_type = self.classify_from_sensors(sensor_data)

        return terrain_type

    def get_terrain_from_map(self, position, terrain_map):
        """
        Get terrain type from pre-built terrain map.
        """
        # Simplified - in practice, this would look up the map
        return 'flat'  # Default

    def classify_from_sensors(self, sensor_data):
        """
        Classify terrain based on sensor readings.
        """
        # Example classification based on IMU data
        imu_data = sensor_data.get('imu', {})
        angular_velocity = imu_data.get('angular_velocity', [0, 0, 0])
        linear_acceleration = imu_data.get('linear_acceleration', [0, 0, 0])

        # Calculate vibration metrics
        vibration_magnitude = np.linalg.norm(angular_velocity)
        acceleration_magnitude = np.linalg.norm(linear_acceleration)

        # Simple classification logic
        if vibration_magnitude > 0.5 or acceleration_magnitude > 12:  # High vibration/acceleration
            return 'uneven'
        elif acceleration_magnitude < 8:  # Low normal force (possible slip)
            return 'slippery'
        else:
            return 'flat'

class AdaptiveWalkingController:
    """
    Controller that adapts walking parameters based on terrain.
    """

    def __init__(self):
        self.base_controller = WalkingController()
        self.terrain_params = {}

    def generate_adaptive_commands(self, sensor_data, target_velocity, terrain_params):
        """
        Generate walking commands adapted to terrain parameters.
        """
        # Update controller with terrain-specific parameters
        self.update_terrain_parameters(terrain_params)

        # Generate base walking commands
        base_commands = self.base_controller.compute_walking_control(target_velocity)

        # Apply terrain-specific adaptations
        adaptive_commands = self.apply_terrain_adaptations(
            base_commands, sensor_data, terrain_params
        )

        return adaptive_commands

    def update_terrain_parameters(self, terrain_params):
        """
        Update controller with terrain-specific parameters.
        """
        self.terrain_params = terrain_params

        # Update base controller parameters
        self.base_controller.step_length = terrain_params['step_length']
        self.base_controller.step_width = terrain_params['step_width']
        self.base_controller.step_height = terrain_params['step_height']
        self.base_controller.walking_speed = terrain_params['step_length'] / terrain_params['walking_period']

    def apply_terrain_adaptations(self, base_commands, sensor_data, terrain_params):
        """
        Apply terrain-specific adaptations to base commands.
        """
        adaptive_commands = base_commands.copy()

        # Adjust for terrain roughness (if applicable)
        if terrain_params.get('roughness', 0) > 0.05:
            # Increase step height for rough terrain
            adaptive_commands['step_height'] = terrain_params['step_height'] * 1.5

        # Adjust timing for slippery surfaces
        if 'slippery' in str(terrain_params):
            # Increase DSP ratio for more stability
            adaptive_commands['dsp_ratio'] = min(0.3, terrain_params['dsp_ratio'] * 1.5)

        # Limit angular velocity on unstable terrain
        max_ang_vel = terrain_params.get('max_angular_velocity', 0.5)
        if 'angular_velocity' in sensor_data:
            current_ang_vel = np.linalg.norm(sensor_data['angular_velocity'])
            if current_ang_vel > max_ang_vel * 0.8:  # 80% threshold
                # Reduce walking speed
                adaptive_commands['walking_speed'] *= 0.7

        return adaptive_commands

class FootstepAdjuster:
    """
    Adjust footstep placement based on terrain and stability.
    """

    def __init__(self):
        self.safety_margin = 0.05  # 5cm safety margin

    def adjust_footsteps(self, planned_footsteps, terrain_info, stability_data):
        """
        Adjust planned footsteps based on terrain and stability information.
        """
        adjusted_footsteps = []

        for i, footstep in enumerate(planned_footsteps):
            original_pos = footstep['position']

            # Get terrain information for this step location
            terrain_at_step = self.get_terrain_info_at_location(original_pos, terrain_info)

            # Adjust for terrain characteristics
            adjusted_pos = self.adjust_for_terrain(original_pos, terrain_at_step)

            # Adjust for stability requirements
            if stability_data.get('is_unstable', False):
                adjusted_pos = self.adjust_for_stability(adjusted_pos, stability_data)

            adjusted_footstep = footstep.copy()
            adjusted_footstep['position'] = adjusted_pos
            adjusted_footstep['original_position'] = original_pos

            adjusted_footsteps.append(adjusted_footstep)

        return adjusted_footsteps

    def adjust_for_terrain(self, original_pos, terrain_info):
        """
        Adjust footstep for terrain characteristics.
        """
        adjusted_pos = list(original_pos)

        # Adjust for slope
        slope = terrain_info.get('slope', 0)
        if abs(slope) > 0.1:  # Significant slope
            # Adjust foot orientation and position
            adjusted_pos[2] += slope * 0.1  # Height adjustment

        # Adjust for obstacles
        obstacles = terrain_info.get('obstacles', [])
        if obstacles:
            # Find safe placement avoiding obstacles
            adjusted_pos = self.avoid_obstacles(adjusted_pos, obstacles)

        return adjusted_pos

    def adjust_for_stability(self, original_pos, stability_data):
        """
        Adjust footstep for stability requirements.
        """
        # This would implement stability-based adjustments
        # like wider steps when unstable
        return original_pos

    def avoid_obstacles(self, original_pos, obstacles):
        """
        Adjust footstep to avoid obstacles.
        """
        adjusted_pos = list(original_pos)

        # Simple obstacle avoidance - move laterally if obstacle detected
        for obstacle in obstacles:
            obs_pos = obstacle['position']
            obs_size = obstacle.get('size', 0.1)

            # Check if footstep collides with obstacle
            distance = np.linalg.norm(np.array(original_pos[:2]) - np.array(obs_pos[:2]))
            if distance < obs_size + self.safety_margin:
                # Adjust laterally to avoid obstacle
                angle_to_obstacle = np.arctan2(
                    obs_pos[1] - original_pos[1],
                    obs_pos[0] - original_pos[0]
                )
                # Move perpendicular to the obstacle
                adjust_angle = angle_to_obstacle + np.pi/2
                adjusted_pos[0] += self.safety_margin * np.cos(adjust_angle)
                adjusted_pos[1] += self.safety_margin * np.sin(adjust_angle)

        return adjusted_pos

    def get_terrain_info_at_location(self, position, terrain_info):
        """
        Get terrain information at specific location.
        """
        # This would look up terrain map or sensor data
        # For simulation, return default values
        return {
            'slope': 0,
            'roughness': 0,
            'friction': 0.8,
            'obstacles': []
        }
```

## Implementation Example: Complete Walking Controller

```python
#!/usr/bin/env python3
"""
Complete implementation of a walking controller for humanoid robots.
"""

import rospy
import numpy as np
from sensor_msgs.msg import Imu, JointState
from geometry_msgs.msg import Vector3, Point
from std_msgs.msg import Float64MultiArray
import time

class HumanoidWalkingNode:
    """
    ROS node for humanoid walking control.
    """

    def __init__(self):
        rospy.init_node('humanoid_walking_controller')

        # Initialize controllers
        self.walking_controller = WalkingController()
        self.stabilizer = WalkingStabilizer()
        self.terrain_adaptive_walker = TerrainAdaptiveWalker()

        # State variables
        self.current_com = np.array([0.0, 0.0, 0.8])
        self.current_com_vel = np.array([0.0, 0.0, 0.0])
        self.current_com_acc = np.array([0.0, 0.0, 0.0])
        self.current_joint_positions = np.zeros(28)  # Example: 28 DOF humanoid
        self.current_joint_velocities = np.zeros(28)
        self.current_imu = Vector3(0, 0, 0)

        # Publishers and subscribers
        self.joint_command_pub = rospy.Publisher(
            '/joint_group_position_controller/command',
            Float64MultiArray,
            queue_size=10
        )

        rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)

        # Walking command subscriber
        rospy.Subscriber('/walking_command', Vector3, self.walking_command_callback)

        # Walking status publisher
        self.status_pub = rospy.Publisher('/walking_status', Vector3, queue_size=10)

        # Control parameters
        self.control_rate = 100  # 100 Hz
        self.rate = rospy.Rate(self.control_rate)

        # Walking state
        self.is_walking = False
        self.target_velocity = np.array([0.0, 0.0, 0.0])

        print("Humanoid Walking Controller initialized")

    def imu_callback(self, msg):
        """
        Handle IMU data for walking control.
        """
        self.current_imu.x = msg.linear_acceleration.x
        self.current_imu.y = msg.linear_acceleration.y
        self.current_imu.z = msg.linear_acceleration.z

    def joint_state_callback(self, msg):
        """
        Handle joint state data.
        """
        if len(msg.position) == len(self.current_joint_positions):
            self.current_joint_positions = np.array(msg.position)
            self.current_joint_velocities = np.array(msg.velocity)

    def walking_command_callback(self, msg):
        """
        Handle walking velocity commands.
        """
        self.target_velocity[0] = msg.x  # Forward velocity
        self.target_velocity[1] = msg.y  # Lateral velocity
        self.target_velocity[2] = msg.z  # Turning velocity

        # Start walking if not already
        if not self.is_walking and np.linalg.norm(self.target_velocity) > 0.01:
            self.is_walking = True
            print(f"Starting walk with velocity: {self.target_velocity}")

    def compute_walking_control(self):
        """
        Main walking control computation.
        """
        if not self.is_walking:
            # Send zero commands when not walking
            return np.zeros(len(self.current_joint_positions))

        # Create sensor data dictionary
        sensor_data = {
            'com_pos': self.current_com,
            'com_vel': self.current_com_vel,
            'com_acc': self.current_com_acc,
            'imu': {
                'linear_acceleration': [self.current_imu.x, self.current_imu.y, self.current_imu.z],
                'angular_velocity': [0, 0, 0]  # Would get from IMU if available
            },
            'joint_positions': self.current_joint_positions,
            'joint_velocities': self.current_joint_velocities
        }

        # Create reference trajectory
        reference_trajectory = {
            'com_pos': self.current_com,
            'foot_pos': np.array([0, 0, 0]),  # Would be calculated
            'zmp': np.array([0, 0, 0])  # Would be calculated
        }

        # Compute basic walking control
        walking_output = self.walking_controller.compute_walking_control(
            self.target_velocity
        )

        # Apply stabilization
        control_commands, stability_metrics = self.stabilizer.stabilize_walking(
            sensor_data, reference_trajectory
        )

        # Check if stable
        if not stability_metrics['is_stable']:
            print(f"Instability detected! ZMP error: {stability_metrics['zmp_error']:.3f}")

        # For this example, return simple joint commands
        # In practice, this would convert to actual joint trajectories
        joint_commands = self.generate_joint_commands(walking_output, control_commands)

        return joint_commands

    def generate_joint_commands(self, walking_output, control_commands):
        """
        Generate joint commands from walking output and control commands.
        """
        # This would typically involve:
        # 1. Inverse kinematics to convert foot positions to joint angles
        # 2. Inverse dynamics to compute required joint torques
        # 3. Applying feedback control corrections

        # For simulation, return simple proportional commands
        n_joints = len(self.current_joint_positions)
        commands = np.zeros(n_joints)

        # Add some basic walking pattern
        time_now = rospy.Time.now().to_sec()
        for i in range(n_joints):
            # Simple oscillating pattern for walking
            commands[i] = 0.1 * np.sin(2 * np.pi * 0.5 * time_now + i * 0.1)

        return commands

    def run(self):
        """
        Main control loop.
        """
        print("Starting walking control loop...")

        loop_count = 0
        while not rospy.is_shutdown():
            try:
                # Compute walking control
                joint_commands = self.compute_walking_control()

                # Publish joint commands
                cmd_msg = Float64MultiArray()
                cmd_msg.data = joint_commands.tolist()
                self.joint_command_pub.publish(cmd_msg)

                # Publish walking status periodically
                if loop_count % 10 == 0:  # Every 100ms
                    status_msg = Vector3()
                    status_msg.x = float(self.is_walking)
                    status_msg.y = self.target_velocity[0]  # Forward velocity
                    status_msg.z = self.target_velocity[1]  # Lateral velocity
                    self.status_pub.publish(status_msg)

                # Sleep to maintain control rate
                self.rate.sleep()
                loop_count += 1

            except rospy.ROSInterruptException:
                print("Walking controller interrupted")
                break
            except Exception as e:
                print(f"Error in walking control: {e}")
                rospy.sleep(0.1)  # Brief pause before continuing

def main():
    """
    Main function to start the walking controller.
    """
    try:
        walking_node = HumanoidWalkingNode()
        walking_node.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("Walking controller stopped by user")

if __name__ == '__main__':
    main()
```

## Exercises

### Exercise 1: Walking Pattern Optimization
Implement a walking pattern generator that optimizes step parameters (length, width, height) for energy efficiency while maintaining stability. Test different parameter combinations and measure the energy consumption of the walking motion.

### Exercise 2: Terrain Adaptation
Create a terrain classification system that can identify different ground types (flat, uneven, slippery) using IMU and force sensor data. Implement adaptive walking control that modifies gait parameters based on the detected terrain.

### Exercise 3: ZMP-Based Walking Control
Implement a complete ZMP-based walking controller that generates stable walking patterns and maintains the ZMP within the support polygon during locomotion. Test the controller with different walking speeds and turning motions.

### Exercise 4: Balance Recovery Integration
Integrate the walking controller with the balance recovery system from the previous chapter. Test the system's ability to maintain walking when subjected to external disturbances and recover to stable walking.

## Summary

This chapter covered the fundamental concepts of humanoid locomotion control, including walking pattern generation, gait control strategies, and terrain adaptation. We explored preview control methods, inverted pendulum models, and feedback control techniques for stable walking. The implementation examples provide practical insights into developing walking controllers for real humanoid robots.

The key takeaways include:
- Walking pattern generation requires careful coordination of CoM and foot trajectories
- Preview control helps maintain stable ZMP tracking during walking
- Feedback control is essential for handling disturbances and terrain variations
- Terrain adaptation improves walking performance on different surfaces
- Integration with balance control ensures stable locomotion

In the next chapter, we'll explore whole-body control strategies that coordinate locomotion with upper body movements for complex humanoid tasks.