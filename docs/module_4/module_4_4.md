---
id: module_4_4
title: "Module 4.4 - Chapter 4: Perception-Action Integration"
sidebar_position: 4
---

# Module 4.4 - Perception-Action Integration

## Overview

Perception-action integration is a critical component of humanoid robotics that bridges sensory input with motor output, enabling robots to interact intelligently with their environment. This chapter explores the integration of perception systems with control and action execution, covering sensor fusion, state estimation, and closed-loop control for autonomous humanoid behavior.

## Learning Objectives

By the end of this chapter, you will be able to:
- Implement sensor fusion techniques for robust state estimation
- Design closed-loop control systems that integrate perception and action
- Apply state estimation methods for humanoid robots
- Integrate perception outputs with whole-body control systems
- Implement adaptive control strategies based on perceptual feedback
- Design robust perception-action loops for uncertain environments

## Introduction to Perception-Action Integration

Perception-action integration creates a closed-loop system where sensory information drives motor actions, which in turn affect the sensory input. This feedback loop is fundamental to autonomous robot behavior, enabling robots to respond intelligently to their environment.

### The Perception-Action Loop

The perception-action loop consists of several key components:

```
Sensors → Perception → State Estimation → Planning → Control → Actuators
    ↑_______________________________________________________↓
```

### Key Integration Challenges

1. **Latency**: Sensor processing and action execution delays
2. **Uncertainty**: Noisy sensor data and model inaccuracies
3. **Synchronization**: Coordinating multiple sensor streams
4. **Real-time Performance**: Meeting strict timing constraints
5. **Robustness**: Handling sensor failures and environmental changes

## Sensor Fusion Techniques

### Kalman Filter Approaches

```python
import numpy as np
from scipy.linalg import block_diag
import matplotlib.pyplot as plt

class ExtendedKalmanFilter:
    """
    Extended Kalman Filter for humanoid state estimation.
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

    def update(self, measurement):
        """
        Update step: incorporate measurement into state estimate.
        """
        # Measurement model: z = h(x) + v
        expected_measurement = self.measurement_model(self.state)

        # Linearize measurement model
        H = self.jacobian_measurement(self.state)

        # Innovation (measurement residual)
        innovation = measurement - expected_measurement

        # Innovation covariance
        innovation_covariance = H @ self.covariance @ H.T + self.measurement_noise

        # Kalman gain
        kalman_gain = self.covariance @ H.T @ np.linalg.inv(innovation_covariance)

        # Update state estimate
        self.state = self.state + kalman_gain @ innovation

        # Update covariance
        I = np.eye(self.state_dim)
        self.covariance = (I - kalman_gain @ H) @ self.covariance

        return self.state, self.covariance

    def state_transition(self, state, control_input, dt):
        """
        Nonlinear state transition function for humanoid robot.
        """
        # Extract state components
        pos = state[:3]
        vel = state[3:6]
        quat = state[6:10]  # Orientation quaternion
        omega = state[10:13]  # Angular velocity

        # Update position based on velocity
        new_pos = pos + vel * dt

        # Update velocity based on acceleration (from control input)
        new_vel = vel + control_input[:3] * dt  # Assuming first 3 control inputs are forces

        # Update orientation using quaternion integration
        new_quat = self.integrate_quaternion(quat, omega, dt)

        # Update angular velocity (simplified)
        new_omega = omega + control_input[3:6] * dt  # Assuming next 3 are torques

        # Combine into new state vector
        new_state = np.concatenate([new_pos, new_vel, new_quat, new_omega])

        return new_state

    def integrate_quaternion(self, quat, omega, dt):
        """
        Integrate quaternion using angular velocity.
        """
        # Convert angular velocity to quaternion derivative
        omega_skew = np.array([
            [0, -omega[2], omega[1]],
            [omega[2], 0, -omega[0]],
            [-omega[1], omega[0], 0]
        ])

        # Quaternion derivative
        q_dot = 0.5 * omega_skew @ quat[:3]

        # Update quaternion
        new_quat = quat.copy()
        new_quat[:3] += q_dot * dt
        new_quat[3] += 0.5 * (omega @ quat[:3]) * dt  # qw component

        # Normalize quaternion
        new_quat = new_quat / np.linalg.norm(new_quat)

        return new_quat

    def jacobian_state_transition(self, state, control_input, dt):
        """
        Jacobian of state transition function.
        """
        F = np.eye(self.state_dim)

        # Partial derivatives of position with respect to velocity
        F[0:3, 3:6] = np.eye(3) * dt

        # Partial derivatives of velocity (simplified)
        # F[3:6, 3:6] = eye(3)  # Velocity remains roughly constant

        # Partial derivatives of quaternion (complex, simplified)
        # For now, assume minimal change in orientation model

        return F

    def measurement_model(self, state):
        """
        Nonlinear measurement model.
        """
        # Measurements: position, orientation, possibly velocity
        pos = state[:3]
        quat = state[6:10]

        # For this example, return position and orientation
        measurement = np.concatenate([pos, quat])

        return measurement[:self.measurement_dim]  # Truncate to measurement dimension

    def jacobian_measurement(self, state):
        """
        Jacobian of measurement function.
        """
        H = np.zeros((self.measurement_dim, self.state_dim))

        # Position measurements depend on position state
        pos_meas_dim = min(3, self.measurement_dim)
        H[:pos_meas_dim, :pos_meas_dim] = np.eye(pos_meas_dim)

        # Orientation measurements depend on orientation state
        if self.measurement_dim > 3:
            orient_meas_dim = min(4, self.measurement_dim - 3)
            H[3:3+orient_meas_dim, 6:6+orient_meas_dim] = np.eye(orient_meas_dim)

        return H

class UnscentedKalmanFilter:
    """
    Unscented Kalman Filter for more accurate nonlinear estimation.
    """

    def __init__(self, state_dim, measurement_dim, alpha=1e-3, beta=2, kappa=0):
        self.state_dim = state_dim
        self.measurement_dim = measurement_dim

        # UKF scaling parameters
        self.alpha = alpha
        self.beta = beta
        self.kappa = kappa

        # Calculate sigma point parameters
        self.lmbda = alpha**2 * (state_dim + kappa) - state_dim
        self.gamma = np.sqrt(state_dim + self.lmbda)

        # Initialize state and covariance
        self.state = np.zeros(state_dim)
        self.covariance = np.eye(state_dim) * 0.1

        # Process and measurement noise
        self.process_noise = np.eye(state_dim) * 0.1
        self.measurement_noise = np.eye(measurement_dim) * 0.1

    def generate_sigma_points(self):
        """
        Generate sigma points for UKF.
        """
        # Calculate square root of covariance
        sqrt_P = np.linalg.cholesky(self.covariance)

        # Generate sigma points
        sigma_points = np.zeros((2 * self.state_dim + 1, self.state_dim))
        sigma_points[0] = self.state  # Center point

        for i in range(self.state_dim):
            offset = self.gamma * sqrt_P[:, i]
            sigma_points[i + 1] = self.state + offset
            sigma_points[i + 1 + self.state_dim] = self.state - offset

        return sigma_points

    def predict(self, control_input, dt=0.01):
        """
        Prediction step for UKF.
        """
        # Generate sigma points
        sigma_points = self.generate_sigma_points()

        # Propagate sigma points through process model
        propagated_points = np.zeros_like(sigma_points)
        for i, point in enumerate(sigma_points):
            propagated_points[i] = self.state_transition(point, control_input, dt)

        # Calculate predicted state (weighted mean)
        weights = self.calculate_weights()
        predicted_state = np.zeros(self.state_dim)
        for i in range(len(propagated_points)):
            predicted_state += weights[i] * propagated_points[i]

        # Calculate predicted covariance
        predicted_covariance = np.zeros((self.state_dim, self.state_dim))
        for i in range(len(propagated_points)):
            diff = propagated_points[i] - predicted_state
            predicted_covariance += weights[i] * np.outer(diff, diff)

        predicted_covariance += self.process_noise

        self.state = predicted_state
        self.covariance = predicted_covariance

        return self.state, self.covariance

    def update(self, measurement):
        """
        Update step for UKF.
        """
        # Generate sigma points around predicted state
        sigma_points = self.generate_sigma_points()

        # Propagate sigma points through measurement model
        measurement_points = np.zeros((2 * self.state_dim + 1, self.measurement_dim))
        for i, point in enumerate(sigma_points):
            measurement_points[i] = self.measurement_model(point)

        # Calculate expected measurement (weighted mean)
        weights = self.calculate_weights()
        expected_measurement = np.zeros(self.measurement_dim)
        for i in range(len(measurement_points)):
            expected_measurement += weights[i] * measurement_points[i]

        # Calculate innovation covariance
        innovation_cov = np.zeros((self.measurement_dim, self.measurement_dim))
        for i in range(len(measurement_points)):
            diff = measurement_points[i] - expected_measurement
            innovation_cov += weights[i] * np.outer(diff, diff)

        innovation_cov += self.measurement_noise

        # Calculate cross-covariance
        cross_cov = np.zeros((self.state_dim, self.measurement_dim))
        for i in range(len(sigma_points)):
            state_diff = sigma_points[i] - self.state
            meas_diff = measurement_points[i] - expected_measurement
            cross_cov += weights[i] * np.outer(state_diff, meas_diff)

        # Calculate Kalman gain
        kalman_gain = cross_cov @ np.linalg.inv(innovation_cov)

        # Update state and covariance
        innovation = measurement - expected_measurement
        self.state = self.state + kalman_gain @ innovation
        self.covariance = self.covariance - kalman_gain @ innovation_cov @ kalman_gain.T

        return self.state, self.covariance

    def calculate_weights(self):
        """
        Calculate UKF weights.
        """
        weights = np.zeros(2 * self.state_dim + 1)
        weights[0] = self.lmbda / (self.state_dim + self.lmbda)
        weights[1:] = 1.0 / (2 * (self.state_dim + self.lmbda))

        return weights

    def state_transition(self, state, control_input, dt):
        """
        Simplified state transition for UKF (same as EKF).
        """
        # Same implementation as EKF
        pos = state[:3]
        vel = state[3:6]
        quat = state[6:10]
        omega = state[10:13]

        new_pos = pos + vel * dt
        new_vel = vel + control_input[:3] * dt
        new_quat = self.integrate_quaternion(quat, omega, dt)
        new_omega = omega + control_input[3:6] * dt

        return np.concatenate([new_pos, new_vel, new_quat, new_omega])

    def integrate_quaternion(self, quat, omega, dt):
        """
        Integrate quaternion using angular velocity.
        """
        # Same as EKF
        omega_skew = np.array([
            [0, -omega[2], omega[1]],
            [omega[2], 0, -omega[0]],
            [-omega[1], omega[0], 0]
        ])

        q_dot = 0.5 * omega_skew @ quat[:3]
        new_quat = quat.copy()
        new_quat[:3] += q_dot * dt
        new_quat[3] += 0.5 * (omega @ quat[:3]) * dt
        new_quat = new_quat / np.linalg.norm(new_quat)

        return new_quat

    def measurement_model(self, state):
        """
        Measurement model for UKF.
        """
        pos = state[:3]
        quat = state[6:10]

        # Return position and orientation
        measurement = np.concatenate([pos, quat])

        return measurement[:self.measurement_dim]

class ParticleFilter:
    """
    Particle Filter for humanoid state estimation with multimodal distributions.
    """

    def __init__(self, state_dim, n_particles=1000):
        self.state_dim = state_dim
        self.n_particles = n_particles

        # Initialize particles randomly around initial state
        self.particles = np.random.randn(n_particles, state_dim) * 0.1
        self.weights = np.ones(n_particles) / n_particles

    def predict(self, control_input, dt=0.01):
        """
        Prediction step: propagate particles through motion model.
        """
        for i in range(self.n_particles):
            # Sample process noise
            noise = np.random.normal(0, 0.01, self.state_dim)

            # Apply motion model with noise
            self.particles[i] = self.motion_model(
                self.particles[i], control_input, dt
            ) + noise

    def update(self, measurement):
        """
        Update step: weight particles based on measurement likelihood.
        """
        for i in range(self.n_particles):
            # Calculate predicted measurement for this particle
            pred_measurement = self.measurement_model(self.particles[i])

            # Calculate likelihood of measurement given particle
            likelihood = self.calculate_likelihood(measurement, pred_measurement)

            # Update weight
            self.weights[i] *= likelihood

        # Normalize weights
        self.weights = self.weights / np.sum(self.weights)

        # Resample if effective sample size is too low
        if self.effective_sample_size() < self.n_particles / 2:
            self.resample()

    def motion_model(self, state, control_input, dt):
        """
        Motion model for particle propagation.
        """
        # Simplified motion model (same as Kalman filters)
        pos = state[:3]
        vel = state[3:6]
        quat = state[6:10]
        omega = state[10:13]

        new_pos = pos + vel * dt
        new_vel = vel + control_input[:3] * dt
        new_quat = self.integrate_quaternion(quat, omega, dt)
        new_omega = omega + control_input[3:6] * dt

        return np.concatenate([new_pos, new_vel, new_quat, new_omega])

    def measurement_model(self, state):
        """
        Measurement model for particle filter.
        """
        pos = state[:3]
        quat = state[6:10]

        # Return position and orientation
        measurement = np.concatenate([pos, quat])

        return measurement

    def calculate_likelihood(self, measurement, predicted_measurement, std=0.1):
        """
        Calculate likelihood of measurement given predicted measurement.
        """
        # Gaussian likelihood
        diff = measurement - predicted_measurement
        exponent = -0.5 * np.sum((diff / std) ** 2)
        likelihood = np.exp(exponent)

        return likelihood

    def effective_sample_size(self):
        """
        Calculate effective sample size.
        """
        return 1.0 / np.sum(self.weights ** 2)

    def resample(self):
        """
        Resample particles based on weights.
        """
        # Systematic resampling
        indices = self.systematic_resample()

        # Resample particles
        self.particles = self.particles[indices]
        self.weights = np.ones(self.n_particles) / self.n_particles

    def systematic_resample(self):
        """
        Systematic resampling algorithm.
        """
        N = self.n_particles
        indices = np.zeros(N, dtype=int)

        # Cumulative sum of weights
        cumulative_sum = np.cumsum(self.weights)

        # Generate random starting point
        start = np.random.random() / N
        pointers = start + np.arange(N) / N

        i, j = 0, 0
        while i < N:
            if pointers[i] > cumulative_sum[j]:
                j += 1
            else:
                indices[i] = j
                i += 1

        return indices

    def estimate_state(self):
        """
        Estimate state from particles.
        """
        # Weighted mean of particles
        estimated_state = np.zeros(self.state_dim)
        for i in range(self.n_particles):
            estimated_state += self.weights[i] * self.particles[i]

        return estimated_state

    def integrate_quaternion(self, quat, omega, dt):
        """
        Integrate quaternion using angular velocity.
        """
        # Same as other filters
        omega_skew = np.array([
            [0, -omega[2], omega[1]],
            [omega[2], 0, -omega[0]],
            [-omega[1], omega[0], 0]
        ])

        q_dot = 0.5 * omega_skew @ quat[:3]
        new_quat = quat.copy()
        new_quat[:3] += q_dot * dt
        new_quat[3] += 0.5 * (omega @ quat[:3]) * dt
        new_quat = new_quat / np.linalg.norm(new_quat)

        return new_quat
```

## State Estimation for Humanoid Robots

### Multi-Sensor State Estimation

```python
class MultiSensorStateEstimator:
    """
    State estimator that fuses data from multiple sensors.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model

        # Individual estimators for different sensor types
        self.imu_estimator = ImuBasedEstimator()
        self.vision_estimator = VisionBasedEstimator()
        self.force_estimator = ForceBasedEstimator()
        self.encoders_estimator = EncoderBasedEstimator()

        # Combined state estimator
        self.combined_estimator = ExtendedKalmanFilter(
            state_dim=13,  # Position, velocity, orientation, angular velocity
            control_dim=6,  # Forces and torques
            measurement_dim=10  # Position, orientation, velocities
        )

        # Sensor fusion weights
        self.sensor_weights = {
            'imu': 0.4,
            'vision': 0.3,
            'force': 0.2,
            'encoders': 0.1
        }

        # Sensor timestamps
        self.last_sensor_updates = {
            'imu': 0,
            'vision': 0,
            'force': 0,
            'encoders': 0
        }

    def update_sensor_data(self, sensor_data):
        """
        Update with new sensor measurements.
        """
        # Update individual estimators
        if 'imu' in sensor_data:
            self.imu_estimator.update(sensor_data['imu'])
            self.last_sensor_updates['imu'] = sensor_data['timestamp']

        if 'vision' in sensor_data:
            self.vision_estimator.update(sensor_data['vision'])
            self.last_sensor_updates['vision'] = sensor_data['timestamp']

        if 'force' in sensor_data:
            self.force_estimator.update(sensor_data['force'])
            self.last_sensor_updates['force'] = sensor_data['timestamp']

        if 'encoders' in sensor_data:
            self.encoders_estimator.update(sensor_data['encoders'])
            self.last_sensor_updates['encoders'] = sensor_data['timestamp']

    def estimate_state(self, control_input, dt=0.01):
        """
        Estimate complete robot state by fusing all sensor data.
        """
        # Get individual estimates
        imu_state = self.imu_estimator.get_state_estimate()
        vision_state = self.vision_estimator.get_state_estimate()
        force_state = self.force_estimator.get_state_estimate()
        encoder_state = self.encoders_estimator.get_state_estimate()

        # Fuse estimates using weighted combination
        fused_state = self.fuse_sensor_estimates(
            imu_state, vision_state, force_state, encoder_state
        )

        # Update combined estimator
        measurement = self.extract_measurement(fused_state)
        self.combined_estimator.predict(control_input, dt)
        self.combined_estimator.update(measurement)

        return self.combined_estimator.state

    def fuse_sensor_estimates(self, imu_state, vision_state, force_state, encoder_state):
        """
        Fuse state estimates from different sensors using weighted averaging.
        """
        # Weighted combination of estimates
        fused_state = (self.sensor_weights['imu'] * imu_state +
                      self.sensor_weights['vision'] * vision_state +
                      self.sensor_weights['force'] * force_state +
                      self.sensor_weights['encoders'] * encoder_state)

        # Normalize weights
        total_weight = sum(self.sensor_weights.values())
        fused_state = fused_state / total_weight

        return fused_state

    def extract_measurement(self, state_estimate):
        """
        Extract measurement vector from state estimate for filter update.
        """
        # Extract relevant parts of state for measurement update
        # This would depend on what sensors are available
        position = state_estimate[:3]
        orientation = state_estimate[6:10]
        velocity = state_estimate[3:6]

        # Combine into measurement vector
        measurement = np.concatenate([position, orientation, velocity])

        # Truncate to expected measurement dimension
        return measurement[:self.combined_estimator.measurement_dim]

class ImuBasedEstimator:
    """
    State estimator using IMU data.
    """

    def __init__(self):
        # IMU bias estimation
        self.accel_bias = np.zeros(3)
        self.gyro_bias = np.zeros(3)

        # Previous state for integration
        self.prev_linear_accel = np.zeros(3)
        self.prev_angular_vel = np.zeros(3)
        self.prev_timestamp = 0

        # Estimated state
        self.position = np.zeros(3)
        self.velocity = np.zeros(3)
        self.orientation = np.array([0, 0, 0, 1])  # Quaternion

    def update(self, imu_data):
        """
        Update state estimate with new IMU data.
        """
        current_time = imu_data['timestamp']
        dt = current_time - self.prev_timestamp if self.prev_timestamp > 0 else 0.01

        # Extract IMU measurements
        linear_accel_raw = np.array(imu_data['linear_acceleration'])
        angular_vel_raw = np.array(imu_data['angular_velocity'])

        # Remove biases
        linear_accel = linear_accel_raw - self.accel_bias
        angular_vel = angular_vel_raw - self.gyro_bias

        # Account for gravity in linear acceleration
        # Transform gravity vector to body frame and subtract
        R = self.quaternion_to_rotation_matrix(self.orientation)
        gravity_body = R.T @ np.array([0, 0, 9.81])
        linear_accel_no_grav = linear_accel - gravity_body

        # Integrate to get velocity and position
        self.velocity += linear_accel_no_grav * dt
        self.position += self.velocity * dt

        # Update orientation using angular velocity integration
        self.orientation = self.integrate_orientation(
            self.orientation, angular_vel, dt
        )

        # Update previous values
        self.prev_linear_accel = linear_accel
        self.prev_angular_vel = angular_vel
        self.prev_timestamp = current_time

    def integrate_orientation(self, quat, omega, dt):
        """
        Integrate orientation using angular velocity.
        """
        # Convert angular velocity to quaternion derivative
        omega_quat = np.array([0, omega[0], omega[1], omega[2]])
        quat_dot = 0.5 * self.quaternion_multiply(omega_quat, quat)

        # Update quaternion
        new_quat = quat + quat_dot * dt

        # Normalize
        new_quat = new_quat / np.linalg.norm(new_quat)

        return new_quat

    def quaternion_multiply(self, q1, q2):
        """
        Multiply two quaternions.
        """
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2

        return np.array([w, x, y, z])

    def quaternion_to_rotation_matrix(self, quat):
        """
        Convert quaternion to rotation matrix.
        """
        w, x, y, z = quat

        R = np.array([
            [1 - 2*(y**2 + z**2), 2*(x*y - w*z), 2*(x*z + w*y)],
            [2*(x*y + w*z), 1 - 2*(x**2 + z**2), 2*(y*z - w*x)],
            [2*(x*z - w*y), 2*(y*z + w*x), 1 - 2*(x**2 + y**2)]
        ])

        return R

    def get_state_estimate(self):
        """
        Get current state estimate from IMU.
        """
        # Return state vector: [pos, vel, quat, omega]
        state = np.zeros(13)
        state[:3] = self.position
        state[3:6] = self.velocity
        state[6:10] = self.orientation
        state[10:13] = self.prev_angular_vel

        return state

class VisionBasedEstimator:
    """
    State estimator using vision data.
    """

    def __init__(self):
        # Feature tracking
        self.feature_points = {}
        self.camera_pose = np.eye(4)

        # Object detection and tracking
        self.tracked_objects = {}
        self.robot_pose_from_vision = np.zeros(7)  # Position + orientation

        # Previous frame data
        self.prev_features = {}
        self.prev_timestamp = 0

    def update(self, vision_data):
        """
        Update state estimate with vision data.
        """
        current_time = vision_data['timestamp']

        # Process visual odometry if available
        if 'visual_odometry' in vision_data:
            self.update_visual_odometry(vision_data['visual_odometry'])

        # Process object tracking if available
        if 'objects' in vision_data:
            self.update_object_tracking(vision_data['objects'])

        # Process SLAM if available
        if 'slam_pose' in vision_data:
            self.update_slam_pose(vision_data['slam_pose'])

        self.prev_timestamp = current_time

    def update_visual_odometry(self, vo_data):
        """
        Update state using visual odometry.
        """
        # Extract pose change from visual odometry
        delta_translation = np.array(vo_data['translation'])
        delta_rotation = np.array(vo_data['rotation'])  # As quaternion

        # Update estimated robot pose
        # This is a simplified approach - in practice would use proper integration
        self.robot_pose_from_vision[:3] += delta_translation
        # For rotation, would properly compose quaternions

    def update_object_tracking(self, objects):
        """
        Update state using tracked objects.
        """
        for obj in objects:
            obj_id = obj['id']
            obj_pose = obj['pose']

            if obj_id in self.tracked_objects:
                # Use object tracking to estimate robot motion
                prev_obj_pose = self.tracked_objects[obj_id]['pose']
                # Estimate robot motion based on object motion
                # (stationary objects indicate robot motion)
                if obj.get('is_stationary', False):
                    # Robot moved by inverse of object "motion"
                    pass
            else:
                # New object, store its pose
                pass

            self.tracked_objects[obj_id] = {
                'pose': obj_pose,
                'timestamp': time.time()
            }

    def update_slam_pose(self, slam_pose):
        """
        Update state using SLAM pose estimate.
        """
        # Slam pose: [x, y, z, qx, qy, qz, qw]
        self.robot_pose_from_vision = np.array(slam_pose)

    def get_state_estimate(self):
        """
        Get state estimate from vision.
        """
        # Return state vector with vision-estimated components
        state = np.zeros(13)
        state[:3] = self.robot_pose_from_vision[:3]  # Position
        state[6:10] = self.robot_pose_from_vision[3:]  # Orientation

        # Velocity estimation would come from pose differences over time
        # For now, return zeros
        state[3:6] = np.zeros(3)

        return state

class ForceBasedEstimator:
    """
    State estimator using force/torque sensors.
    """

    def __init__(self):
        # Contact state estimation
        self.contact_states = {}
        self.support_polygon = None
        self.zero_moment_point = np.zeros(3)

        # Estimated forces and torques
        self.estimated_external_forces = np.zeros(6)

    def update(self, force_data):
        """
        Update state estimate with force/torque data.
        """
        # Update contact information
        self.update_contacts(force_data['contacts'])

        # Update ZMP estimate
        self.update_zmp(force_data)

        # Estimate external forces
        self.estimate_external_forces(force_data)

    def update_contacts(self, contacts):
        """
        Update contact state information.
        """
        for contact in contacts:
            contact_id = contact['id']
            contact_force = np.array(contact['force'])
            contact_position = np.array(contact['position'])
            contact_normal = np.array(contact['normal'])

            self.contact_states[contact_id] = {
                'force': contact_force,
                'position': contact_position,
                'normal': contact_normal,
                'in_contact': contact['in_contact']
            }

        # Update support polygon
        self.update_support_polygon()

    def update_support_polygon(self):
        """
        Update the support polygon based on contact points.
        """
        contact_points = []
        for contact_id, contact_info in self.contact_states.items():
            if contact_info['in_contact']:
                contact_points.append(contact_info['position'])

        if contact_points:
            contact_points = np.array(contact_points)
            # Calculate bounding box as simple support polygon
            self.support_polygon = {
                'x_min': np.min(contact_points[:, 0]),
                'x_max': np.max(contact_points[:, 0]),
                'y_min': np.min(contact_points[:, 1]),
                'y_max': np.max(contact_points[:, 1])
            }

    def update_zmp(self, force_data):
        """
        Update Zero Moment Point estimate.
        """
        total_force = np.zeros(3)
        total_moment = np.zeros(3)

        for contact_id, contact_info in self.contact_states.items():
            if contact_info['in_contact']:
                force = contact_info['force']
                position = contact_info['position']

                total_force += force
                total_moment += np.cross(position, force)

        if total_force[2] != 0:  # Avoid division by zero
            zmp_x = position[0] - total_moment[1] / total_force[2]
            zmp_y = position[1] + total_moment[0] / total_force[2]
            self.zero_moment_point = np.array([zmp_x, zmp_y, 0])

    def estimate_external_forces(self, force_data):
        """
        Estimate external forces acting on the robot.
        """
        # This would use robot dynamics model to estimate external forces
        # from measured contact forces
        pass

    def get_state_estimate(self):
        """
        Get state estimate from force sensors.
        """
        state = np.zeros(13)

        # Use ZMP and contact information to estimate CoM state
        # This is a simplified approach
        if self.support_polygon:
            # Estimate CoM position within support polygon
            state[0] = (self.support_polygon['x_min'] + self.support_polygon['x_max']) / 2
            state[1] = (self.support_polygon['y_min'] + self.support_polygon['y_max']) / 2
            state[2] = 0.8  # Typical CoM height

        # For velocity, use changes in ZMP
        # For orientation, use force distribution

        return state

class EncoderBasedEstimator:
    """
    State estimator using joint encoder data.
    """

    def __init__(self):
        # Joint state
        self.joint_positions = np.zeros(28)  # Example: 28 DOF humanoid
        self.joint_velocities = np.zeros(28)
        self.joint_accelerations = np.zeros(28)

        # Previous measurements for differentiation
        self.prev_joint_positions = np.zeros(28)
        self.prev_timestamp = 0

        # Forward kinematics model
        self.kinematics_model = None

    def update(self, encoder_data):
        """
        Update state estimate with encoder data.
        """
        current_time = encoder_data['timestamp']
        dt = current_time - self.prev_timestamp if self.prev_timestamp > 0 else 0.01

        # Update joint positions
        new_positions = np.array(encoder_data['positions'])
        self.joint_velocities = (new_positions - self.prev_joint_positions) / dt if dt > 0 else np.zeros(len(new_positions))
        self.joint_accelerations = (self.joint_velocities - self.joint_velocities) / dt if dt > 0 else np.zeros(len(new_positions))

        self.joint_positions = new_positions
        self.prev_joint_positions = new_positions.copy()
        self.prev_timestamp = current_time

    def get_state_estimate(self):
        """
        Get state estimate from encoders.
        """
        state = np.zeros(13)

        # Use forward kinematics to estimate end-effector and CoM positions
        # This would require a proper kinematics model
        if self.kinematics_model:
            # Calculate CoM position from joint angles
            com_pos = self.kinematics_model.calculate_com(self.joint_positions)
            state[:3] = com_pos

            # Calculate CoM velocity from joint velocities
            com_vel = self.kinematics_model.calculate_com_velocity(
                self.joint_positions, self.joint_velocities
            )
            state[3:6] = com_vel

        return state
```

## Closed-Loop Control with Perception Feedback

### Adaptive Control Systems

```python
class AdaptiveController:
    """
    Adaptive controller that adjusts parameters based on perceptual feedback.
    """

    def __init__(self, initial_params=None):
        if initial_params is None:
            initial_params = {
                'kp': 100.0,
                'ki': 10.0,
                'kd': 20.0,
                'adaptation_rate': 0.01
            }

        self.params = initial_params
        self.param_history = []

        # Error tracking for adaptation
        self.error_integral = 0.0
        self.previous_error = 0.0
        self.error_derivative = 0.0

        # Performance metrics
        self.performance_history = []
        self.target_performance = 0.95  # 95% performance target

    def update_control(self, error, dt=0.01):
        """
        Update control with adaptive parameter adjustment.
        """
        # Update error derivatives
        self.error_derivative = (error - self.previous_error) / dt if dt > 0 else 0.0
        self.error_integral += error * dt

        # PID control with current parameters
        control_output = (self.params['kp'] * error +
                         self.params['ki'] * self.error_integral +
                         self.params['kd'] * self.error_derivative)

        # Adapt parameters based on performance
        self.adapt_parameters(error)

        # Store history
        self.previous_error = error
        self.param_history.append(self.params.copy())

        return control_output

    def adapt_parameters(self, error):
        """
        Adapt control parameters based on error and performance.
        """
        # Calculate performance metric (simplified)
        error_magnitude = abs(error)
        performance = 1.0 / (1.0 + error_magnitude)  # Higher is better

        # Store performance
        self.performance_history.append(performance)

        # Keep history to reasonable length
        if len(self.performance_history) > 100:
            self.performance_history.pop(0)

        # Calculate recent average performance
        if len(self.performance_history) > 10:
            recent_avg_performance = np.mean(self.performance_history[-10:])
        else:
            recent_avg_performance = np.mean(self.performance_history) if self.performance_history else 0.5

        # Adjust parameters based on performance
        if recent_avg_performance < self.target_performance * 0.8:
            # Performance is poor, increase gains
            self.params['kp'] *= 1.01
            self.params['ki'] *= 1.01
            self.params['kd'] *= 1.01
        elif recent_avg_performance > self.target_performance * 1.2:
            # Performance is excellent, decrease gains to save energy
            self.params['kp'] *= 0.99
            self.params['ki'] *= 0.99
            self.params['kd'] *= 0.99

        # Apply limits to parameters
        self.params['kp'] = np.clip(self.params['kp'], 10.0, 1000.0)
        self.params['ki'] = np.clip(self.params['ki'], 1.0, 100.0)
        self.params['kd'] = np.clip(self.params['kd'], 5.0, 200.0)

    def update_with_perception(self, perception_data, desired_state, current_state):
        """
        Update control using perception feedback.
        """
        # Calculate tracking error
        error = desired_state - current_state

        # Adapt based on perception quality
        if 'perception_confidence' in perception_data:
            confidence = perception_data['perception_confidence']

            # Reduce adaptation rate when perception is unreliable
            self.params['adaptation_rate'] = 0.01 * confidence

        # Apply control
        control_output = self.update_control(error)

        return control_output

class PerceptionBasedAdaptation:
    """
    System that adapts control based on perception quality and environmental conditions.
    """

    def __init__(self):
        self.environment_classifier = EnvironmentClassifier()
        self.surface_estimator = SurfaceEstimator()
        self.obstacle_detector = ObstacleDetector()

        # Control parameter mappings
        self.param_mappings = {
            'flat_ground': {
                'kp': 100.0, 'ki': 10.0, 'kd': 20.0,
                'step_height': 0.05, 'step_length': 0.3
            },
            'uneven_ground': {
                'kp': 80.0, 'ki': 8.0, 'kd': 25.0,
                'step_height': 0.1, 'step_length': 0.2
            },
            'slippery_surface': {
                'kp': 60.0, 'ki': 5.0, 'kd': 30.0,
                'step_height': 0.02, 'step_length': 0.15
            },
            'obstacle_dense': {
                'kp': 120.0, 'ki': 15.0, 'kd': 15.0,
                'step_height': 0.08, 'step_length': 0.25
            }
        }

    def adapt_control_for_environment(self, perception_data):
        """
        Adapt control parameters based on perceived environment.
        """
        # Classify environment
        env_type = self.environment_classifier.classify(perception_data)

        # Get appropriate parameters
        params = self.param_mappings.get(env_type, self.param_mappings['flat_ground'])

        # Estimate surface properties
        surface_properties = self.surface_estimator.estimate(perception_data)

        # Detect obstacles
        obstacles = self.obstacle_detector.detect(perception_data)

        # Combine information for final parameters
        final_params = self.combine_environmental_factors(
            params, surface_properties, obstacles
        )

        return final_params, env_type

    def combine_environmental_factors(self, base_params, surface_props, obstacles):
        """
        Combine environmental factors to determine final control parameters.
        """
        final_params = base_params.copy()

        # Adjust for surface friction
        friction_coeff = surface_props.get('friction', 0.8)
        if friction_coeff < 0.4:  # Slippery
            final_params['step_length'] *= 0.7
            final_params['kp'] *= 0.8
            final_params['step_height'] *= 0.5

        # Adjust for obstacle density
        obstacle_density = len(obstacles) / surface_props.get('area', 1.0)
        if obstacle_density > 0.1:  # Dense obstacles
            final_params['step_length'] *= 0.8
            final_params['kp'] *= 1.2  # More aggressive control for maneuvering

        # Adjust for surface roughness
        roughness = surface_props.get('roughness', 0.0)
        if roughness > 0.05:  # Rough surface
            final_params['step_height'] *= 1.5
            final_params['step_length'] *= 0.9

        return final_params

class EnvironmentClassifier:
    """
    Classify environment types based on sensor data.
    """

    def classify(self, perception_data):
        """
        Classify environment based on perception data.
        """
        # Analyze different aspects of the environment
        surface_type = self.analyze_surface(perception_data)
        obstacle_density = self.analyze_obstacles(perception_data)
        lighting_condition = self.analyze_lighting(perception_data)

        # Classification logic
        if obstacle_density > 0.2:
            return 'obstacle_dense'
        elif surface_type == 'slippery':
            return 'slippery_surface'
        elif surface_type == 'uneven':
            return 'uneven_ground'
        else:
            return 'flat_ground'

    def analyze_surface(self, perception_data):
        """
        Analyze surface properties.
        """
        # This would use vision, force, and tactile sensors
        if 'surface_data' in perception_data:
            surface_data = perception_data['surface_data']
            roughness = surface_data.get('roughness', 0.0)
            texture = surface_data.get('texture', 'smooth')

            if roughness > 0.1 or texture == 'rough':
                return 'uneven'
            elif texture == 'smooth' and surface_data.get('wet', False):
                return 'slippery'

        return 'flat'

    def analyze_obstacles(self, perception_data):
        """
        Analyze obstacle density in the environment.
        """
        if 'obstacles' in perception_data:
            obstacles = perception_data['obstacles']
            if len(obstacles) > 5:
                return len(obstacles) / 10.0  # Density estimate
        return 0.0

    def analyze_lighting(self, perception_data):
        """
        Analyze lighting conditions.
        """
        # This would use camera exposure, ambient light sensors, etc.
        return 'normal'

class SurfaceEstimator:
    """
    Estimate surface properties from sensor data.
    """

    def estimate(self, perception_data):
        """
        Estimate surface properties.
        """
        properties = {
            'friction': 0.8,
            'roughness': 0.0,
            'slope': 0.0,
            'area': 1.0
        }

        # Estimate from vision data
        if 'vision' in perception_data:
            vision_data = perception_data['vision']
            properties.update(self.estimate_from_vision(vision_data))

        # Estimate from force data
        if 'force' in perception_data:
            force_data = perception_data['force']
            properties.update(self.estimate_from_force(force_data))

        # Estimate from tactile data
        if 'tactile' in perception_data:
            tactile_data = perception_data['tactile']
            properties.update(self.estimate_from_tactile(tactile_data))

        return properties

    def estimate_from_vision(self, vision_data):
        """
        Estimate surface properties from vision data.
        """
        properties = {}

        if 'surface_texture' in vision_data:
            texture_analysis = vision_data['surface_texture']
            # Analyze texture for roughness
            properties['roughness'] = texture_analysis.get('roughness_measure', 0.0)

        if 'surface_normals' in vision_data:
            normals = vision_data['surface_normals']
            # Calculate average slope
            avg_normal = np.mean(normals, axis=0)
            properties['slope'] = np.arccos(avg_normal[2])  # Angle from vertical

        return properties

    def estimate_from_force(self, force_data):
        """
        Estimate surface properties from force data.
        """
        properties = {}

        if 'ground_reaction_forces' in force_data:
            grf_data = force_data['ground_reaction_forces']
            # Estimate friction from force ratios
            # This is a simplified approach
            vertical_forces = [f[2] for f in grf_data if len(f) > 2]
            horizontal_forces = [np.linalg.norm(f[:2]) for f in grf_data if len(f) > 2]

            if vertical_forces and horizontal_forces:
                avg_vertical = np.mean(vertical_forces)
                avg_horizontal = np.mean(horizontal_forces)
                if avg_vertical > 0:
                    properties['friction'] = avg_horizontal / avg_vertical

        return properties

    def estimate_from_tactile(self, tactile_data):
        """
        Estimate surface properties from tactile data.
        """
        properties = {}

        if 'tactile_readings' in tactile_data:
            readings = tactile_data['tactile_readings']
            # Analyze tactile patterns for surface properties
            pressure_variance = np.var([r.get('pressure', 0) for r in readings])
            properties['roughness'] = pressure_variance * 0.1

        return properties

class ObstacleDetector:
    """
    Detect and characterize obstacles in the environment.
    """

    def detect(self, perception_data):
        """
        Detect obstacles from perception data.
        """
        obstacles = []

        # Detect from vision data
        if 'vision' in perception_data:
            vision_obstacles = self.detect_from_vision(perception_data['vision'])
            obstacles.extend(vision_obstacles)

        # Detect from range data
        if 'range' in perception_data:
            range_obstacles = self.detect_from_range(perception_data['range'])
            obstacles.extend(range_obstacles)

        # Detect from planar data (2D map)
        if 'planar_map' in perception_data:
            map_obstacles = self.detect_from_planar_map(perception_data['planar_map'])
            obstacles.extend(map_obstacles)

        return obstacles

    def detect_from_vision(self, vision_data):
        """
        Detect obstacles from vision data.
        """
        obstacles = []

        if 'depth_image' in vision_data:
            depth_data = vision_data['depth_image']
            # Process depth image to find obstacles
            # This would use computer vision techniques
            pass

        if 'object_detections' in vision_data:
            detections = vision_data['object_detections']
            for detection in detections:
                obstacle = {
                    'position': detection['position'],
                    'size': detection['size'],
                    'type': detection['class'],
                    'confidence': detection['confidence']
                }
                obstacles.append(obstacle)

        return obstacles

    def detect_from_range(self, range_data):
        """
        Detect obstacles from range sensor data.
        """
        obstacles = []

        if 'laser_scan' in range_data:
            scan = range_data['laser_scan']
            # Analyze laser scan for obstacles
            for i, range_val in enumerate(scan['ranges']):
                if range_val < 1.0 and range_val > scan['range_min']:  # Within obstacle range
                    angle = scan['angle_min'] + i * scan['angle_increment']
                    x = range_val * np.cos(angle)
                    y = range_val * np.sin(angle)

                    obstacle = {
                        'position': [x, y, 0],
                        'size': [0.1, 0.1, 0.1],  # Estimated size
                        'type': 'unknown',
                        'confidence': 0.8
                    }
                    obstacles.append(obstacle)

        return obstacles

    def detect_from_planar_map(self, map_data):
        """
        Detect obstacles from 2D occupancy map.
        """
        obstacles = []

        if 'occupancy_grid' in map_data:
            grid = map_data['occupancy_grid']
            # Find occupied cells in grid
            occupied_cells = np.where(grid > 0.7)  # Threshold for obstacles
            for x_idx, y_idx in zip(occupied_cells[0], occupied_cells[1]):
                # Convert grid indices to world coordinates
                world_x = x_idx * map_data['resolution'] + map_data['origin'][0]
                world_y = y_idx * map_data['resolution'] + map_data['origin'][1]

                obstacle = {
                    'position': [world_x, world_y, 0],
                    'size': [map_data['resolution'], map_data['resolution'], 0.5],
                    'type': 'static',
                    'confidence': 0.9
                }
                obstacles.append(obstacle)

        return obstacles
```

## Integration with Control Systems

### Perception-Action Loop Implementation

```python
class PerceptionActionLoop:
    """
    Complete perception-action integration loop.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model

        # Perception system
        self.state_estimator = MultiSensorStateEstimator(robot_model)
        self.environment_analyzer = PerceptionBasedAdaptation()

        # Control system
        self.balance_controller = BalanceController()
        self.motor_controller = MotorController()
        self.adaptive_controller = AdaptiveController()

        # Task planner
        self.task_planner = TaskPlanner()

        # Synchronization
        self.synchronizer = DataSynchronizer()

        # Performance monitoring
        self.performance_monitor = PerformanceMonitor()

        # System state
        self.current_state = {
            'position': np.zeros(3),
            'velocity': np.zeros(3),
            'orientation': np.array([0, 0, 0, 1]),
            'joint_positions': np.zeros(robot_model.n_joints),
            'joint_velocities': np.zeros(robot_model.n_joints),
            'timestamp': 0
        }

        self.desired_state = {
            'position': np.zeros(3),
            'velocity': np.zeros(3),
            'orientation': np.array([0, 0, 0, 1])
        }

        self.control_commands = np.zeros(robot_model.n_joints)

    def update_perception(self, sensor_data):
        """
        Update perception system with new sensor data.
        """
        # Synchronize sensor data
        synchronized_data = self.synchronizer.synchronize(sensor_data)

        # Update state estimator
        self.state_estimator.update_sensor_data(synchronized_data)

        # Estimate current state
        self.current_state = self.estimate_current_state()

        # Analyze environment
        control_params, env_type = self.environment_analyzer.adapt_control_for_environment(
            sensor_data
        )

        # Update adaptive controller parameters
        self.adaptive_controller.params.update(control_params)

        return self.current_state

    def estimate_current_state(self):
        """
        Estimate complete current state from all sensors.
        """
        # Get control input (previous commands)
        control_input = np.zeros(6)  # Forces and torques

        # Estimate state using multi-sensor fusion
        estimated_state = self.state_estimator.estimate_state(control_input)

        # Update internal state representation
        state = {
            'position': estimated_state[:3],
            'velocity': estimated_state[3:6],
            'orientation': estimated_state[6:10],
            'angular_velocity': estimated_state[10:13],
            'timestamp': time.time()
        }

        return state

    def plan_action(self, task_specification):
        """
        Plan actions based on perception and task requirements.
        """
        # Plan high-level actions
        planned_actions = self.task_planner.plan_actions(
            self.current_state, task_specification
        )

        # Generate reference trajectories
        reference_trajectories = self.generate_reference_trajectories(planned_actions)

        return reference_trajectories

    def generate_reference_trajectories(self, planned_actions):
        """
        Generate reference trajectories for controllers.
        """
        trajectories = {}

        for action in planned_actions:
            action_type = action['type']
            target = action['target']

            if action_type == 'move_to':
                trajectory = self.generate_move_trajectory(target)
            elif action_type == 'reach_to':
                trajectory = self.generate_reach_trajectory(target)
            elif action_type == 'balance':
                trajectory = self.generate_balance_trajectory()
            else:
                trajectory = self.generate_default_trajectory()

            trajectories[action['id']] = trajectory

        return trajectories

    def generate_move_trajectory(self, target_pos):
        """
        Generate trajectory for locomotion.
        """
        # This would implement path planning and trajectory generation
        # For simplicity, return a straight-line trajectory
        current_pos = self.current_state['position']

        # Generate via points
        n_points = 50
        trajectory = []

        for i in range(n_points):
            ratio = i / (n_points - 1)
            pos = current_pos + ratio * (target_pos - current_pos)
            trajectory.append({
                'position': pos,
                'time': self.current_state['timestamp'] + ratio * 2.0  # 2 second movement
            })

        return trajectory

    def generate_reach_trajectory(self, target_pos):
        """
        Generate trajectory for arm reaching.
        """
        # This would use inverse kinematics to generate joint trajectories
        # For simplicity, return a basic trajectory
        trajectory = [{
            'target_position': target_pos,
            'duration': 1.0  # 1 second reach
        }]

        return trajectory

    def generate_balance_trajectory(self):
        """
        Generate balance maintenance trajectory.
        """
        # Maintain current position and orientation
        trajectory = [{
            'reference_position': self.current_state['position'],
            'reference_orientation': self.current_state['orientation'],
            'duration': float('inf')  # Continuous balance
        }]

        return trajectory

    def generate_default_trajectory(self):
        """
        Generate default trajectory.
        """
        return [{'type': 'hold', 'duration': 1.0}]

    def execute_control(self, reference_trajectories, dt=0.01):
        """
        Execute control based on reference trajectories and perception feedback.
        """
        # Calculate control errors
        errors = self.calculate_control_errors(reference_trajectories)

        # Apply adaptive control
        control_commands = []
        for error_type, error_value in errors.items():
            if error_type == 'balance_error':
                command = self.adaptive_controller.update_with_perception(
                    {'perception_confidence': 0.9},  # Assume high confidence
                    self.desired_state['position'],
                    self.current_state['position']
                )
            elif error_type == 'tracking_error':
                command = self.motor_controller.compute_command(error_value)
            else:
                command = np.zeros(self.robot_model.n_joints)

            control_commands.append(command)

        # Combine commands
        final_command = self.combine_control_commands(control_commands)

        # Apply safety limits
        final_command = self.apply_safety_limits(final_command)

        # Monitor performance
        self.performance_monitor.update(errors, final_command)

        return final_command

    def calculate_control_errors(self, reference_trajectories):
        """
        Calculate control errors from reference trajectories and current state.
        """
        errors = {}

        # Balance error
        if 'balance' in reference_trajectories:
            ref_balance = reference_trajectories['balance'][0]
            current_pos = self.current_state['position']
            errors['balance_error'] = ref_balance['reference_position'] - current_pos

        # Tracking error
        if 'move_to' in reference_trajectories:
            ref_trajectory = reference_trajectories['move_to']
            # Find closest point in trajectory
            closest_point = self.find_closest_trajectory_point(ref_trajectory)
            current_pos = self.current_state['position']
            errors['tracking_error'] = closest_point['position'] - current_pos

        return errors

    def find_closest_trajectory_point(self, trajectory):
        """
        Find the closest point in trajectory to current position.
        """
        current_pos = self.current_state['position']
        closest_point = trajectory[0]
        min_distance = float('inf')

        for point in trajectory:
            distance = np.linalg.norm(np.array(point['position']) - current_pos)
            if distance < min_distance:
                min_distance = distance
                closest_point = point

        return closest_point

    def combine_control_commands(self, commands_list):
        """
        Combine multiple control commands into final command.
        """
        if not commands_list:
            return np.zeros(self.robot_model.n_joints)

        # Simple summation (in practice, would use more sophisticated combination)
        final_command = np.zeros(self.robot_model.n_joints)
        for command in commands_list:
            final_command += command

        return final_command

    def apply_safety_limits(self, commands):
        """
        Apply safety limits to control commands.
        """
        # Joint position limits
        q_min = self.robot_model.joint_limits['min']
        q_max = self.robot_model.joint_limits['max']

        # Joint velocity limits
        qdot_max = np.ones(self.robot_model.n_joints) * 5.0  # 5 rad/s

        # Torque limits
        tau_max = np.ones(self.robot_model.n_joints) * 100.0  # 100 Nm

        # Apply limits
        limited_commands = np.clip(commands, -tau_max, tau_max)

        return limited_commands

    def run_perception_action_cycle(self, sensor_data, task_specification, dt=0.01):
        """
        Run complete perception-action cycle.
        """
        # 1. Update perception
        current_state = self.update_perception(sensor_data)

        # 2. Plan actions
        reference_trajectories = self.plan_action(task_specification)

        # 3. Execute control
        control_commands = self.execute_control(reference_trajectories, dt)

        # 4. Update desired state for next cycle
        self.update_desired_state(reference_trajectories)

        return control_commands, current_state

    def update_desired_state(self, reference_trajectories):
        """
        Update desired state for next control cycle.
        """
        # Update based on current reference trajectory
        if 'balance' in reference_trajectories:
            ref_balance = reference_trajectories['balance'][0]
            self.desired_state['position'] = ref_balance['reference_position']
            self.desired_state['orientation'] = ref_balance['reference_orientation']

class DataSynchronizer:
    """
    Synchronize data from multiple sensors with different rates.
    """

    def __init__(self):
        self.sensor_buffers = {}
        self.sync_window = 0.05  # 50ms synchronization window

    def synchronize(self, sensor_data):
        """
        Synchronize sensor data to common timestamp.
        """
        # Add new data to buffers
        for sensor_type, data in sensor_data.items():
            if sensor_type not in self.sensor_buffers:
                self.sensor_buffers[sensor_type] = []

            # Add data point with timestamp
            self.sensor_buffers[sensor_type].append({
                'data': data,
                'timestamp': data.get('timestamp', time.time())
            })

        # Remove old data outside sync window
        current_time = time.time()
        for sensor_type in self.sensor_buffers:
            self.sensor_buffers[sensor_type] = [
                item for item in self.sensor_buffers[sensor_type]
                if current_time - item['timestamp'] < self.sync_window
            ]

        # Find common timestamp
        common_timestamp = current_time

        # Interpolate data to common timestamp
        synchronized_data = {}
        for sensor_type, buffer in self.sensor_buffers.items():
            if buffer:
                # Use latest available data or interpolate
                synchronized_data[sensor_type] = self.interpolate_to_timestamp(
                    buffer, common_timestamp
                )

        return synchronized_data

    def interpolate_to_timestamp(self, buffer, target_timestamp):
        """
        Interpolate sensor data to target timestamp.
        """
        if len(buffer) == 1:
            return buffer[0]['data']

        # Find two closest timestamps
        buffer_sorted = sorted(buffer, key=lambda x: x['timestamp'])

        # Linear interpolation between closest points
        for i in range(len(buffer_sorted) - 1):
            t1 = buffer_sorted[i]['timestamp']
            t2 = buffer_sorted[i + 1]['timestamp']

            if t1 <= target_timestamp <= t2:
                # Interpolate between these two points
                ratio = (target_timestamp - t1) / (t2 - t1)

                # Simple linear interpolation (would be more complex for rotations)
                data1 = buffer_sorted[i]['data']
                data2 = buffer_sorted[i + 1]['data']

                # This is a simplified interpolation
                interpolated_data = {}
                for key in data1:
                    if isinstance(data1[key], (int, float)):
                        interpolated_data[key] = (
                            data1[key] + ratio * (data2[key] - data1[key])
                        )
                    else:
                        # For non-numeric data, use the earlier value
                        interpolated_data[key] = data1[key]

                return interpolated_data

        # If target timestamp is outside buffer range, use the closest
        return buffer_sorted[-1]['data']

class PerformanceMonitor:
    """
    Monitor system performance and detect anomalies.
    """

    def __init__(self):
        self.error_history = []
        self.command_history = []
        self.performance_metrics = {}
        self.anomaly_thresholds = {
            'tracking_error': 0.1,  # 10cm max tracking error
            'control_effort': 50.0,  # Max control effort
            'stability_metric': 0.05  # Max ZMP deviation
        }

    def update(self, errors, commands):
        """
        Update performance metrics with current errors and commands.
        """
        # Store error history
        self.error_history.append(errors.copy())
        self.command_history.append(commands.copy())

        # Keep history to reasonable length
        max_history = 1000
        if len(self.error_history) > max_history:
            self.error_history.pop(0)
            self.command_history.pop(0)

        # Calculate performance metrics
        self.calculate_performance_metrics()

        # Check for anomalies
        anomalies = self.detect_anomalies()

        return anomalies

    def calculate_performance_metrics(self):
        """
        Calculate various performance metrics.
        """
        if not self.error_history:
            return

        # Calculate average tracking error
        tracking_errors = []
        for error_set in self.error_history[-50:]:  # Last 50 samples
            if 'tracking_error' in error_set:
                tracking_errors.append(np.linalg.norm(error_set['tracking_error']))

        if tracking_errors:
            self.performance_metrics['avg_tracking_error'] = np.mean(tracking_errors)
            self.performance_metrics['max_tracking_error'] = np.max(tracking_errors)

        # Calculate average control effort
        if self.command_history:
            recent_commands = np.array(self.command_history[-50:])  # Last 50 samples
            self.performance_metrics['avg_control_effort'] = np.mean(np.abs(recent_commands))

    def detect_anomalies(self):
        """
        Detect performance anomalies.
        """
        anomalies = []

        # Check tracking error
        avg_error = self.performance_metrics.get('avg_tracking_error', 0)
        if avg_error > self.anomaly_thresholds['tracking_error']:
            anomalies.append({
                'type': 'high_tracking_error',
                'value': avg_error,
                'threshold': self.anomaly_thresholds['tracking_error']
            })

        # Check control effort
        avg_effort = self.performance_metrics.get('avg_control_effort', 0)
        if avg_effort > self.anomaly_thresholds['control_effort']:
            anomalies.append({
                'type': 'high_control_effort',
                'value': avg_effort,
                'threshold': self.anomaly_thresholds['control_effort']
            })

        return anomalies

class TaskPlanner:
    """
    Plan high-level tasks based on perception and goals.
    """

    def __init__(self):
        self.path_planner = PathPlanner()
        self.motion_primitive_library = MotionPrimitiveLibrary()

    def plan_actions(self, current_state, task_specification):
        """
        Plan sequence of actions to achieve task specification.
        """
        actions = []

        task_type = task_specification.get('type', 'move_to')
        target = task_specification.get('target', [0, 0, 0])

        if task_type == 'move_to':
            actions = self.plan_locomotion(current_state, target)
        elif task_type == 'manipulate_object':
            actions = self.plan_manipulation(current_state, task_specification)
        elif task_type == 'navigate_and_grasp':
            actions = self.plan_navigate_and_grasp(current_state, task_specification)
        else:
            actions = self.plan_default_action(current_state, task_specification)

        return actions

    def plan_locomotion(self, current_state, target_pos):
        """
        Plan locomotion to target position.
        """
        # Plan path
        path = self.path_planner.plan_path(current_state['position'], target_pos)

        # Convert path to locomotion actions
        actions = []
        for i, waypoint in enumerate(path):
            action = {
                'id': f'walk_to_waypoint_{i}',
                'type': 'move_to',
                'target': waypoint,
                'priority': 5
            }
            actions.append(action)

        return actions

    def plan_manipulation(self, current_state, task_specification):
        """
        Plan manipulation actions.
        """
        target_object = task_specification.get('object', None)
        action_type = task_specification.get('action', 'reach')

        if target_object:
            # Plan manipulation sequence
            actions = [
                {
                    'id': 'approach_object',
                    'type': 'move_to',
                    'target': self.calculate_approach_position(target_object, current_state),
                    'priority': 8
                },
                {
                    'id': 'reach_object',
                    'type': 'reach_to',
                    'target': target_object['position'],
                    'priority': 10
                }
            ]

            if action_type == 'grasp':
                actions.append({
                    'id': 'grasp_object',
                    'type': 'grasp',
                    'target': target_object,
                    'priority': 10
                })

        return actions

    def calculate_approach_position(self, target_object, current_state):
        """
        Calculate approach position for manipulation.
        """
        obj_pos = np.array(target_object['position'])
        robot_pos = current_state['position']

        # Calculate approach vector (from robot to object)
        approach_vec = obj_pos - robot_pos
        approach_vec = approach_vec / np.linalg.norm(approach_vec)

        # Calculate approach position (1m from object)
        approach_dist = 1.0  # 1 meter approach distance
        approach_pos = obj_pos - approach_vec * approach_dist

        return approach_pos

    def plan_navigate_and_grasp(self, current_state, task_specification):
        """
        Plan complex task: navigate to object and grasp it.
        """
        target_object = task_specification.get('object', None)
        if not target_object:
            return []

        # 1. Plan navigation to object
        navigate_actions = self.plan_locomotion(
            current_state, self.calculate_approach_position(target_object, current_state)
        )

        # 2. Plan grasping
        grasp_actions = [
            {
                'id': 'reach_object',
                'type': 'reach_to',
                'target': target_object['position'],
                'priority': 10
            },
            {
                'id': 'grasp_object',
                'type': 'grasp',
                'target': target_object,
                'priority': 10
            }
        ]

        # Combine actions
        all_actions = navigate_actions + grasp_actions

        # Set priorities to ensure proper sequencing
        for i, action in enumerate(all_actions):
            action['priority'] = 5 + i  # Increasing priority

        return all_actions

    def plan_default_action(self, current_state, task_specification):
        """
        Plan default action when task type is unknown.
        """
        return [{
            'id': 'hold_position',
            'type': 'balance',
            'target': current_state['position'],
            'priority': 1
        }]

class PathPlanner:
    """
    Plan paths through environment considering obstacles.
    """

    def __init__(self):
        self.map_resolution = 0.1  # 10cm resolution
        self.inflation_radius = 0.3  # 30cm obstacle inflation

    def plan_path(self, start_pos, goal_pos, obstacles=None):
        """
        Plan path from start to goal considering obstacles.
        """
        if obstacles is None:
            obstacles = []

        # For simplicity, implement A* algorithm on grid
        # In practice, would use more sophisticated planners

        # Create grid map
        grid_map = self.create_grid_map(start_pos, goal_pos, obstacles)

        # Plan path using A* (simplified implementation)
        path = self.a_star_plan(grid_map, start_pos, goal_pos)

        return path

    def create_grid_map(self, start_pos, goal_pos, obstacles):
        """
        Create grid map from continuous space.
        """
        # Calculate map bounds
        margin = 2.0  # 2m margin around start/goal
        x_min = min(start_pos[0], goal_pos[0]) - margin
        x_max = max(start_pos[0], goal_pos[0]) + margin
        y_min = min(start_pos[1], goal_pos[1]) - margin
        y_max = max(start_pos[1], goal_pos[1]) + margin

        # Create grid
        width = int((x_max - x_min) / self.map_resolution)
        height = int((y_max - y_min) / self.map_resolution)

        grid_map = np.zeros((height, width))

        # Add inflated obstacles to grid
        for obstacle in obstacles:
            obs_pos = obstacle['position']
            obs_size = obstacle['size']

            # Calculate grid coordinates
            grid_x = int((obs_pos[0] - x_min) / self.map_resolution)
            grid_y = int((obs_pos[1] - y_min) / self.map_resolution)

            # Inflate obstacle
            inflation_cells = int(self.inflation_radius / self.map_resolution)
            for dx in range(-inflation_cells, inflation_cells + 1):
                for dy in range(-inflation_cells, inflation_cells + 1):
                    x_cell = grid_x + dx
                    y_cell = grid_y + dy
                    if 0 <= x_cell < width and 0 <= y_cell < height:
                        grid_map[y_cell, x_cell] = 1  # Occupied

        return {
            'map': grid_map,
            'bounds': (x_min, x_max, y_min, y_max),
            'resolution': self.map_resolution
        }

    def a_star_plan(self, grid_map, start_pos, goal_pos):
        """
        Simple A* path planning (conceptual implementation).
        """
        # Convert start/goal to grid coordinates
        x_min, x_max, y_min, y_max = grid_map['bounds']
        resolution = grid_map['resolution']

        start_grid = (
            int((start_pos[0] - x_min) / resolution),
            int((start_pos[1] - y_min) / resolution)
        )
        goal_grid = (
            int((goal_pos[0] - x_min) / resolution),
            int((goal_pos[1] - y_min) / resolution)
        )

        # For this example, return straight line (in practice, implement A*)
        path = [start_pos, goal_pos]

        return path

class MotionPrimitiveLibrary:
    """
    Library of pre-defined motion primitives for various tasks.
    """

    def __init__(self):
        self.primitives = {
            'walk_forward': self.create_walk_forward_primitive(),
            'turn_left': self.create_turn_primitive(angle=np.pi/4),
            'turn_right': self.create_turn_primitive(angle=-np.pi/4),
            'step_left': self.create_lateral_step_primitive(direction='left'),
            'step_right': self.create_lateral_step_primitive(direction='right'),
            'reach_forward': self.create_reach_primitive(direction='forward'),
            'reach_left': self.create_reach_primitive(direction='left'),
            'grasp': self.create_grasp_primitive()
        }

    def create_walk_forward_primitive(self):
        """
        Create walking forward primitive.
        """
        return {
            'type': 'locomotion',
            'duration': 1.0,
            'trajectory': 'walking_pattern',
            'parameters': {
                'step_length': 0.3,
                'step_height': 0.05,
                'frequency': 1.0
            }
        }

    def create_turn_primitive(self, angle):
        """
        Create turning primitive.
        """
        return {
            'type': 'locomotion',
            'duration': 2.0,
            'trajectory': 'turning_pattern',
            'parameters': {
                'angle': angle,
                'step_width': 0.2
            }
        }

    def create_lateral_step_primitive(self, direction):
        """
        Create lateral stepping primitive.
        """
        return {
            'type': 'locomotion',
            'duration': 1.5,
            'trajectory': 'lateral_step_pattern',
            'parameters': {
                'direction': direction,
                'step_distance': 0.1
            }
        }

    def create_reach_primitive(self, direction):
        """
        Create reaching primitive.
        """
        return {
            'type': 'manipulation',
            'duration': 1.0,
            'trajectory': 'reach_pattern',
            'parameters': {
                'direction': direction,
                'distance': 0.3
            }
        }

    def create_grasp_primitive(self):
        """
        Create grasping primitive.
        """
        return {
            'type': 'manipulation',
            'duration': 2.0,
            'trajectory': 'grasp_pattern',
            'parameters': {
                'pre_grasp_distance': 0.1,
                'grasp_force': 10.0
            }
        }

    def get_primitive(self, primitive_name):
        """
        Get motion primitive by name.
        """
        return self.primitives.get(primitive_name, None)
```

## Implementation Example: Complete Perception-Action System

```python
#!/usr/bin/env python3
"""
Complete implementation of perception-action integration for humanoid robots.
"""

import rospy
import numpy as np
from sensor_msgs.msg import JointState, Imu, Image, LaserScan
from geometry_msgs.msg import Vector3, Pose, Twist
from std_msgs.msg import Float64MultiArray
from nav_msgs.msg import Odometry
import time
import threading
from queue import Queue

class HumanoidPerceptionActionNode:
    """
    ROS node for complete perception-action integration.
    """

    def __init__(self):
        rospy.init_node('humanoid_perception_action_node')

        # Initialize perception-action loop
        self.perception_action_loop = PerceptionActionLoop(robot_model=None)  # Will be initialized

        # State variables
        self.current_joint_positions = np.zeros(28)  # Example: 28 DOF humanoid
        self.current_joint_velocities = np.zeros(28)
        self.current_joint_efforts = np.zeros(28)
        self.current_imu_data = {'linear_acceleration': [0, 0, 0], 'angular_velocity': [0, 0, 0]}
        self.current_laser_scan = {'ranges': [], 'angle_min': 0, 'angle_max': 0, 'angle_increment': 0}
        self.current_camera_image = None

        # Publishers and subscribers
        self.joint_command_pub = rospy.Publisher(
            '/joint_group_position_controller/command',
            Float64MultiArray,
            queue_size=10
        )

        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)
        rospy.Subscriber('/imu/data', Imu, self.imu_callback)
        rospy.Subscriber('/scan', LaserScan, self.laser_scan_callback)
        rospy.Subscriber('/camera/image_raw', Image, self.camera_callback)

        # Task command subscribers
        rospy.Subscriber('/move_to_target', Pose, self.move_to_callback)
        rospy.Subscriber('/grasp_object', Pose, self.grasp_callback)
        rospy.Subscriber('/balance_command', Vector3, self.balance_callback)

        # Performance monitoring
        self.performance_pub = rospy.Publisher('/system_performance', Vector3, queue_size=10)

        # Control parameters
        self.control_rate = 100  # 100 Hz
        self.rate = rospy.Rate(self.control_rate)

        # Task queue
        self.task_queue = Queue()
        self.current_task = None

        # System status
        self.system_active = False
        self.emergency_stop = False

        print("Humanoid Perception-Action Node initialized")

    def joint_state_callback(self, msg):
        """
        Handle joint state updates.
        """
        if len(msg.position) == len(self.current_joint_positions):
            self.current_joint_positions = np.array(msg.position)
            if len(msg.velocity) == len(self.current_joint_velocities):
                self.current_joint_velocities = np.array(msg.velocity)
            if len(msg.effort) == len(self.current_joint_efforts):
                self.current_joint_efforts = np.array(msg.effort)

    def imu_callback(self, msg):
        """
        Handle IMU data for perception.
        """
        self.current_imu_data = {
            'linear_acceleration': [msg.linear_acceleration.x, msg.linear_acceleration.y, msg.linear_acceleration.z],
            'angular_velocity': [msg.angular_velocity.x, msg.angular_velocity.y, msg.angular_velocity.z],
            'timestamp': rospy.Time.now().to_sec()
        }

    def laser_scan_callback(self, msg):
        """
        Handle laser scan data for obstacle detection.
        """
        self.current_laser_scan = {
            'ranges': list(msg.ranges),
            'intensities': list(msg.intensities),
            'angle_min': msg.angle_min,
            'angle_max': msg.angle_max,
            'angle_increment': msg.angle_increment,
            'range_min': msg.range_min,
            'range_max': msg.range_max,
            'timestamp': rospy.Time.now().to_sec()
        }

    def camera_callback(self, msg):
        """
        Handle camera image data for vision processing.
        """
        # In practice, would convert ROS image to OpenCV format
        # For simulation, just store timestamp
        self.current_camera_image = {
            'width': msg.width,
            'height': msg.height,
            'encoding': msg.encoding,
            'timestamp': rospy.Time.now().to_sec()
        }

    def move_to_callback(self, msg):
        """
        Handle move-to-target commands.
        """
        target = [msg.position.x, msg.position.y, msg.position.z]
        task_spec = {
            'type': 'move_to',
            'target': target
        }
        self.task_queue.put(task_spec)

    def grasp_callback(self, msg):
        """
        Handle grasp-object commands.
        """
        target = [msg.position.x, msg.position.y, msg.position.z]
        task_spec = {
            'type': 'manipulate_object',
            'action': 'grasp',
            'object': {
                'position': target,
                'type': 'unknown'
            }
        }
        self.task_queue.put(task_spec)

    def balance_callback(self, msg):
        """
        Handle balance commands.
        """
        task_spec = {
            'type': 'balance',
            'target_orientation': [msg.x, msg.y, msg.z]
        }
        self.task_queue.put(task_spec)

    def prepare_sensor_data(self):
        """
        Prepare sensor data for perception system.
        """
        sensor_data = {
            'timestamp': rospy.Time.now().to_sec(),
            'joint_states': {
                'positions': self.current_joint_positions.tolist(),
                'velocities': self.current_joint_velocities.tolist(),
                'efforts': self.current_joint_efforts.tolist()
            },
            'imu': self.current_imu_data,
            'range': {
                'laser_scan': self.current_laser_scan
            },
            'vision': {
                'image': self.current_camera_image,
                'object_detections': []  # Would come from vision processing
            }
        }

        return sensor_data

    def run_perception_action_cycle(self):
        """
        Run complete perception-action cycle.
        """
        if self.emergency_stop:
            # Send zero commands
            zero_commands = Float64MultiArray()
            zero_commands.data = [0.0] * len(self.current_joint_positions)
            self.joint_command_pub.publish(zero_commands)
            return

        # Prepare sensor data
        sensor_data = self.prepare_sensor_data()

        # Get current task
        current_task = self.current_task
        if current_task is None and not self.task_queue.empty():
            current_task = self.task_queue.get_nowait()
            self.current_task = current_task

        if current_task is None:
            # No active task, maintain current position
            current_task = {
                'type': 'balance',
                'target': self.current_joint_positions.tolist()
            }

        # Run perception-action cycle
        control_commands, current_state = self.perception_action_loop.run_perception_action_cycle(
            sensor_data, current_task
        )

        # Publish control commands
        cmd_msg = Float64MultiArray()
        cmd_msg.data = control_commands.tolist()
        self.joint_command_pub.publish(cmd_msg)

        # Publish performance metrics periodically
        if int(rospy.Time.now().to_sec()) % 2 == 0:  # Every 2 seconds
            perf_msg = Vector3()
            perf_msg.x = float(len(control_commands))  # Number of joints controlled
            perf_msg.y = float(np.mean(np.abs(control_commands)))  # Average control effort
            perf_msg.z = float(np.max(np.abs(control_commands)))  # Max control effort
            self.performance_pub.publish(perf_msg)

    def run(self):
        """
        Main control loop.
        """
        print("Starting perception-action control loop...")

        loop_count = 0
        while not rospy.is_shutdown():
            try:
                # Run perception-action cycle
                self.run_perception_action_cycle()

                # Sleep to maintain control rate
                self.rate.sleep()
                loop_count += 1

                # Print status periodically
                if loop_count % 100 == 0:
                    rospy.loginfo(f"Perception-action cycle running, loop count: {loop_count}")

            except rospy.ROSInterruptException:
                print("Perception-action controller interrupted")
                break
            except Exception as e:
                rospy.logerr(f"Error in perception-action cycle: {e}")
                rospy.sleep(0.1)  # Brief pause before continuing

def main():
    """
    Main function to start the perception-action controller.
    """
    try:
        perception_node = HumanoidPerceptionActionNode()
        perception_node.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("Perception-action controller stopped by user")

if __name__ == '__main__':
    main()
```

## Exercises

### Exercise 1: Sensor Fusion Implementation
Implement a complete sensor fusion system that combines IMU, vision, and force sensor data to estimate the humanoid robot's state. Test the system's robustness when individual sensors fail or provide noisy data.

### Exercise 2: Adaptive Control Tuning
Create an adaptive control system that automatically tunes PID parameters based on environmental conditions (flat ground vs. uneven terrain) and performance metrics. Compare the performance of adaptive vs. fixed-parameter control.

### Exercise 3: Perception-Action Latency Analysis
Analyze the latency introduced by different perception processing steps (image processing, state estimation, planning) and implement optimizations to reduce overall system latency for real-time performance.

### Exercise 4: Robustness Testing
Test the perception-action system under various challenging conditions: sensor noise, occlusions, lighting changes, and unexpected obstacles. Evaluate the system's ability to maintain stable operation.

## Summary

This chapter covered the fundamental concepts of perception-action integration for humanoid robots, including sensor fusion techniques, state estimation methods, and closed-loop control systems. We explored Extended Kalman Filters, Unscented Kalman Filters, and Particle Filters for state estimation, and developed adaptive control strategies that adjust to environmental conditions.

The key takeaways include:
- Sensor fusion combines multiple sensor modalities for robust state estimation
- Kalman filtering provides optimal state estimates for linear/nonlinear systems
- Adaptive control adjusts parameters based on perceptual feedback
- Real-time performance requires careful system design and optimization
- Closed-loop integration enables responsive and robust robot behavior

In the next chapter, we'll explore the complete integration of all the concepts covered in Module 4 into a comprehensive humanoid robot control system that can perform complex autonomous tasks.