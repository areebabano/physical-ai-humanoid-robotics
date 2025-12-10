---
id: module_2_4
title: "Module 2.4 - Chapter 4: Sensor Simulation"
sidebar_position: 4
---

# Module 2.4 - Sensor Simulation

## Overview

This chapter focuses on simulating various sensors for humanoid robots in virtual environments. Accurate sensor simulation is crucial for developing perception systems, testing algorithms, and enabling sim-to-real transfer. We'll explore how to model different sensor types, configure their properties, and integrate them with ROS 2 for realistic humanoid robot simulation.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand different types of sensors used in humanoid robots
- Configure and implement simulated sensors in Gazebo
- Model sensor noise, limitations, and characteristics
- Integrate simulated sensors with ROS 2
- Validate sensor simulation accuracy
- Optimize sensor configurations for computational efficiency

## 4.1 Sensor Types for Humanoid Robotics

### 4.1.1 Overview of Humanoid Robot Sensors

Humanoid robots require various sensor types to perceive their environment and internal state:

```xml
<!-- Example of multiple sensor types in a humanoid model -->
<model name="humanoid_with_sensors">
  <!-- IMU sensor in the torso -->
  <link name="torso">
    <sensor name="torso_imu" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <imu>
        <angular_velocity>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.01</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.01</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.01</stddev>
            </noise>
          </z>
        </angular_velocity>
        <linear_acceleration>
          <x>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.017</stddev>
            </noise>
          </x>
          <y>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.017</stddev>
            </noise>
          </y>
          <z>
            <noise type="gaussian">
              <mean>0.0</mean>
              <stddev>0.017</stddev>
            </noise>
          </z>
        </linear_acceleration>
      </imu>
    </sensor>
  </link>

  <!-- Camera sensor in the head -->
  <link name="head">
    <sensor name="head_camera" type="camera">
      <camera>
        <horizontal_fov>1.047</horizontal_fov> <!-- 60 degrees -->
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.1</near>
          <far>10.0</far>
        </clip>
      </camera>
      <always_on>true</always_on>
      <update_rate>30</update_rate>
    </sensor>
  </link>

  <!-- LiDAR sensor -->
  <link name="lidar_mount">
    <sensor name="humanoid_lidar" type="ray">
      <ray>
        <scan>
          <horizontal>
            <samples>360</samples>
            <resolution>1</resolution>
            <min_angle>-3.14159</min_angle> <!-- -π -->
            <max_angle>3.14159</max_angle>   <!-- π -->
          </horizontal>
        </scan>
        <range>
          <min>0.1</min>
          <max>10.0</max>
          <resolution>0.01</resolution>
        </range>
      </ray>
      <always_on>true</always_on>
      <update_rate>10</update_rate>
    </sensor>
  </link>
</model>
```

### 4.1.2 Classification of Sensors

Humanoid robot sensors can be classified into several categories:

1. **Proprioceptive Sensors**: Measure internal robot state
2. **Exteroceptive Sensors**: Measure external environment
3. **Interoceptive Sensors**: Measure internal robot conditions

```python
# Sensor classification example
class SensorTypes:
    """Classification of sensors used in humanoid robots"""

    # Proprioceptive sensors
    PROPRIOCEPTIVE = {
        'joint_position': 'Joint position encoders',
        'joint_velocity': 'Joint velocity sensors',
        'joint_effort': 'Joint effort/torque sensors',
        'imu': 'Inertial Measurement Unit',
        'force_torque': '6-axis force/torque sensors',
        'motor_current': 'Motor current sensors'
    }

    # Exteroceptive sensors
    EXTEROCEPTIVE = {
        'camera': 'Vision sensors (RGB, stereo, depth)',
        'lidar': 'Laser range finders',
        'sonar': 'Ultrasonic range sensors',
        'tactile': 'Tactile sensors',
        'microphone': 'Audio sensors'
    }

    # Interoceptive sensors
    INTEROCEPTIVE = {
        'temperature': 'Temperature sensors',
        'battery': 'Battery level sensors',
        'power': 'Power consumption sensors'
    }

# Example usage
print("Proprioceptive sensors:", list(SensorTypes.PROPRIOCEPTIVE.keys()))
print("Exteroceptive sensors:", list(SensorTypes.EXTEROCEPTIVE.keys()))
```

## 4.2 Implementing Simulated Sensors

### 4.2.1 IMU Sensor Configuration

Inertial Measurement Units (IMUs) are crucial for humanoid balance and orientation:

```xml
<!-- Detailed IMU configuration with realistic noise parameters -->
<sensor name="torso_imu" type="imu">
  <pose>0 0 0 0 0 0</pose>
  <topic>imu/data</topic>
  <update_rate>100</update_rate>

  <imu>
    <!-- Angular velocity measurements with noise -->
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.001</stddev>  <!-- 1 mrad/s accuracy -->
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0001</bias_stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.001</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0001</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.001</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.0001</bias_stddev>
        </noise>
      </z>
    </angular_velocity>

    <!-- Linear acceleration measurements with noise -->
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01</stddev>   <!-- 10 mg accuracy -->
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.001</bias_stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.001</bias_stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>0.01</stddev>
          <bias_mean>0.0</bias_mean>
          <bias_stddev>0.001</bias_stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
</sensor>
```

### 4.2.2 Camera Sensor Configuration

Vision sensors are essential for perception and navigation:

```xml
<!-- RGB camera configuration -->
<sensor name="head_camera" type="camera">
  <pose>0.05 0 0 0 0 0</pose>  <!-- Offset from head center -->
  <topic>camera/rgb/image_raw</topic>
  <update_rate>30</update_rate>

  <camera name="head_camera">
    <horizontal_fov>1.047</horizontal_fov>  <!-- 60 degrees -->
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10.0</far>
    </clip>
    <noise>
      <type>gaussian</type>
      <mean>0.0</mean>
      <stddev>0.007</stddev>  <!-- Noise level -->
    </noise>
  </camera>

  <always_on>true</always_on>
  <visualize>true</visualize>
</sensor>

<!-- Depth camera configuration -->
<sensor name="depth_camera" type="depth">
  <pose>0.07 0 0 0 0 0</pose>  <!-- Stereo baseline -->
  <topic>camera/depth/image_raw</topic>
  <camera name="depth_camera">
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>320</width>
      <height>240</height>
      <format>R16G16B16</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>5.0</far>
    </clip>
  </camera>
  <always_on>true</always_on>
  <update_rate>30</update_rate>
</sensor>
```

### 4.2.3 LiDAR Sensor Configuration

Range sensors are critical for navigation and obstacle detection:

```xml
<!-- 2D LiDAR configuration -->
<sensor name="laser_2d" type="ray">
  <pose>0 0 0.8 0 0 0</pose>  <!-- Mount on torso at 80cm height -->
  <topic>scan</topic>
  <ray>
    <scan>
      <horizontal>
        <samples>720</samples>  <!-- Higher resolution -->
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>  <!-- -π -->
        <max_angle>3.14159</max_angle>   <!-- π -->
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>10.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <always_on>true</always_on>
  <update_rate>10</update_rate>
  <visualize>false</visualize>
</sensor>

<!-- 3D LiDAR configuration -->
<sensor name="laser_3d" type="ray">
  <pose>0 0 1.0 0 0 0</pose>  <!-- Mount higher for better view -->
  <topic>points</topic>
  <ray>
    <scan>
      <horizontal>
        <samples>1080</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
      <vertical>
        <samples>32</samples>  <!-- 32 vertical beams -->
        <resolution>1</resolution>
        <min_angle>-0.5236</min_angle>  <!-- -30 degrees -->
        <max_angle>0.3491</max_angle>    <!-- 20 degrees -->
      </vertical>
    </scan>
    <range>
      <min>0.1</min>
      <max>20.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <always_on>true</always_on>
  <update_rate>10</update_rate>
</sensor>
```

## 4.3 Sensor Noise and Realism

### 4.3.1 Modeling Sensor Noise

Realistic noise modeling is essential for effective sim-to-real transfer:

```python
import numpy as np
import matplotlib.pyplot as plt

class SensorNoiseModel:
    """Models different types of sensor noise for humanoid robots"""

    @staticmethod
    def gaussian_noise(mean=0.0, std_dev=1.0, size=1):
        """Generate Gaussian noise"""
        return np.random.normal(mean, std_dev, size)

    @staticmethod
    def uniform_noise(low=-1.0, high=1.0, size=1):
        """Generate uniform noise"""
        return np.random.uniform(low, high, size)

    @staticmethod
    def quantization_noise(signal, resolution=0.01):
        """Simulate quantization noise"""
        quantized = np.round(signal / resolution) * resolution
        return quantized - signal

    @staticmethod
    def drift_noise(initial_bias=0.0, drift_rate=0.001, time_step=0.001):
        """Simulate sensor drift over time"""
        return initial_bias + np.cumsum(np.random.normal(0, drift_rate, int(1/time_step)))

    @staticmethod
    def bias_noise(bias_mean=0.0, bias_std=0.01):
        """Simulate sensor bias"""
        return np.random.normal(bias_mean, bias_std)

# Example: Apply noise to IMU sensor readings
def simulate_imu_readings(true_angular_velocity, true_linear_acceleration, dt=0.01):
    """Simulate IMU readings with realistic noise"""

    # Add Gaussian noise to angular velocity
    noisy_angular_vel = true_angular_velocity + SensorNoiseModel.gaussian_noise(
        mean=0.0, std_dev=0.001, size=3
    )

    # Add Gaussian noise to linear acceleration
    noisy_linear_acc = true_linear_acceleration + SensorNoiseModel.gaussian_noise(
        mean=0.0, std_dev=0.01, size=3
    )

    # Add quantization noise
    resolution = 0.001  # 1 mrad/s for gyroscope
    noisy_angular_vel = noisy_angular_vel + SensorNoiseModel.quantization_noise(
        noisy_angular_vel, resolution
    )

    resolution = 0.001  # 1 mg for accelerometer
    noisy_linear_acc = noisy_linear_acc + SensorNoiseModel.quantization_noise(
        noisy_linear_acc, resolution
    )

    return noisy_angular_vel, noisy_linear_acc

# Example usage
true_angular_vel = np.array([0.1, 0.05, -0.02])  # rad/s
true_linear_acc = np.array([0.5, -0.1, 9.2])     # m/s²

noisy_av, noisy_acc = simulate_imu_readings(true_angular_vel, true_linear_acc)
print(f"Noisy angular velocity: {noisy_av}")
print(f"Noisy linear acceleration: {noisy_acc}")
```

### 4.3.2 Sensor Fusion Simulation

Simulating multiple sensors for fusion algorithms:

```python
class MultiSensorFusion:
    """Simulate multiple sensors for fusion algorithms"""

    def __init__(self):
        self.imu_noise_model = SensorNoiseModel()
        self.camera_noise_model = SensorNoiseModel()
        self.lidar_noise_model = SensorNoiseModel()

    def simulate_imu_data(self, true_orientation, true_angular_vel, true_linear_acc):
        """Simulate IMU data with noise"""
        noisy_angular_vel, noisy_linear_acc = simulate_imu_readings(
            true_angular_vel, true_linear_acc
        )

        # Add orientation noise (quaternion)
        orientation_noise = self.imu_noise_model.gaussian_noise(0, 0.01, 4)
        noisy_orientation = true_orientation + orientation_noise
        # Normalize quaternion
        noisy_orientation = noisy_orientation / np.linalg.norm(noisy_orientation)

        return {
            'orientation': noisy_orientation,
            'angular_velocity': noisy_angular_vel,
            'linear_acceleration': noisy_linear_acc
        }

    def simulate_camera_data(self, depth_image, rgb_image):
        """Simulate camera data with noise"""
        # Add Gaussian noise to depth image
        depth_noise = self.camera_noise_model.gaussian_noise(0, 0.01, depth_image.shape)
        noisy_depth = depth_image + depth_noise

        # Add noise to RGB image
        rgb_noise = self.camera_noise_model.gaussian_noise(0, 10, rgb_image.shape)
        noisy_rgb = np.clip(rgb_image + rgb_noise, 0, 255).astype(np.uint8)

        return {
            'rgb': noisy_rgb,
            'depth': noisy_depth
        }

    def simulate_lidar_data(self, true_ranges):
        """Simulate LiDAR data with noise"""
        # Add range noise
        range_noise = self.lidar_noise_model.gaussian_noise(0, 0.02, len(true_ranges))
        noisy_ranges = true_ranges + range_noise

        # Ensure valid range values
        noisy_ranges = np.clip(noisy_ranges, 0.1, 10.0)

        return noisy_ranges

# Example usage
fusion_sim = MultiSensorFusion()

# Simulated true values
true_orient = np.array([0, 0, 0, 1])  # quaternion (w, x, y, z)
true_ang_vel = np.array([0.1, 0.05, -0.02])
true_lin_acc = np.array([0.5, -0.1, 9.81])

imu_data = fusion_sim.simulate_imu_data(true_orient, true_ang_vel, true_lin_acc)
print(f"Simulated IMU data: {imu_data}")
```

## 4.4 ROS 2 Integration

### 4.4.1 Sensor Message Types

ROS 2 provides standardized message types for different sensors:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Image, LaserScan, PointCloud2, JointState
from std_msgs.msg import Header
from geometry_msgs.msg import Point, Point32
import cv2
import numpy as np
from cv_bridge import CvBridge

class SensorPublisherNode(Node):
    """Node to publish simulated sensor data"""

    def __init__(self):
        super().__init__('sensor_publisher_node')

        # Publishers
        self.imu_pub = self.create_publisher(Imu, 'imu/data', 10)
        self.image_pub = self.create_publisher(Image, 'camera/rgb/image_raw', 10)
        self.scan_pub = self.create_publisher(LaserScan, 'scan', 10)
        self.joint_state_pub = self.create_publisher(JointState, 'joint_states', 10)

        # Timer for publishing
        self.timer = self.create_timer(0.033, self.publish_sensors)  # ~30 Hz

        # Sensor fusion simulator
        self.sensor_fusion = MultiSensorFusion()
        self.cv_bridge = CvBridge()

        self.get_logger().info('Sensor publisher node initialized')

    def publish_sensors(self):
        """Publish all sensor data"""
        self.publish_imu_data()
        self.publish_camera_data()
        self.publish_lidar_data()
        self.publish_joint_states()

    def publish_imu_data(self):
        """Publish IMU sensor data"""
        msg = Imu()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'imu_link'

        # Simulate orientation (with some movement)
        roll = np.sin(self.get_clock().now().nanoseconds * 1e-9) * 0.1
        pitch = np.cos(self.get_clock().now().nanoseconds * 1e-9) * 0.1
        yaw = 0.0

        # Convert to quaternion
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)

        msg.orientation.w = cr * cp * cy + sr * sp * sy
        msg.orientation.x = sr * cp * cy - cr * sp * sy
        msg.orientation.y = cr * sp * cy + sr * cp * sy
        msg.orientation.z = cr * cp * sy - sr * sp * cy

        # Angular velocity
        msg.angular_velocity.x = 0.1 * np.cos(self.get_clock().now().nanoseconds * 1e-9)
        msg.angular_velocity.y = 0.05 * np.sin(self.get_clock().now().nanoseconds * 1e-9)
        msg.angular_velocity.z = 0.02

        # Linear acceleration (with gravity and movement)
        msg.linear_acceleration.x = 0.5 * np.sin(self.get_clock().now().nanoseconds * 1e-9)
        msg.linear_acceleration.y = -0.1 * np.cos(self.get_clock().now().nanoseconds * 1e-9)
        msg.linear_acceleration.z = 9.81

        self.imu_pub.publish(msg)

    def publish_camera_data(self):
        """Publish camera sensor data"""
        # Create a simulated RGB image
        width, height = 640, 480
        timestamp = self.get_clock().now().nanoseconds * 1e-9

        # Generate a pattern that changes over time
        img = np.zeros((height, width, 3), dtype=np.uint8)
        img[:, :, 0] = np.sin(np.linspace(0, 4*np.pi, width) + timestamp) * 127 + 128  # R
        img[:, :, 1] = np.cos(np.linspace(0, 4*np.pi, height)[:, None] + timestamp) * 127 + 128  # G
        img[:, :, 2] = 100  # B (constant)

        # Convert to ROS message
        ros_image = self.cv_bridge.cv2_to_imgmsg(img, encoding='bgr8')
        ros_image.header.stamp = self.get_clock().now().to_msg()
        ros_image.header.frame_id = 'camera_link'

        self.image_pub.publish(ros_image)

    def publish_lidar_data(self):
        """Publish LiDAR sensor data"""
        msg = LaserScan()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'laser_link'

        # Configure scan parameters
        msg.angle_min = -np.pi
        msg.angle_max = np.pi
        msg.angle_increment = 2 * np.pi / 360  # 360 points
        msg.time_increment = 0.0
        msg.scan_time = 0.1
        msg.range_min = 0.1
        msg.range_max = 10.0

        # Generate simulated ranges (with some obstacles)
        angles = np.linspace(msg.angle_min, msg.angle_max, 360)
        ranges = np.full(360, 5.0)  # Default range

        # Add some obstacles
        obstacle_angles = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]
        obstacle_distances = [1.5, 2.0, 1.0, 2.5, 1.8]

        for angle, dist in zip(obstacle_angles, obstacle_distances):
            idx = int((angle - msg.angle_min) / msg.angle_increment)
            if 0 <= idx < 360:
                ranges[idx] = dist
                # Add some spread to the obstacle
                for offset in [-1, 1]:
                    if 0 <= idx + offset < 360:
                        ranges[idx + offset] = dist + 0.1

        # Add noise to ranges
        noise = np.random.normal(0, 0.02, len(ranges))
        ranges = np.clip(ranges + noise, msg.range_min, msg.range_max)

        msg.ranges = ranges.tolist()
        msg.intensities = [100.0] * len(ranges)  # Constant intensity

        self.scan_pub.publish(msg)

    def publish_joint_states(self):
        """Publish joint state sensor data"""
        msg = JointState()
        msg.header = Header()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['left_hip_joint', 'left_knee_joint', 'right_hip_joint', 'right_knee_joint',
                   'left_shoulder_joint', 'left_elbow_joint', 'right_shoulder_joint', 'right_elbow_joint']

        # Simulate joint positions with some movement
        timestamp = self.get_clock().now().nanoseconds * 1e-9
        positions = []

        for i, _ in enumerate(msg.name):
            # Create different movement patterns for each joint
            pos = 0.1 * np.sin(timestamp + i * 0.5)
            positions.append(pos)

        msg.position = positions
        msg.velocity = [0.0] * len(positions)  # Zero velocity for simplicity
        msg.effort = [0.0] * len(positions)    # Zero effort for simplicity

        self.joint_state_pub.publish(msg)

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

### 4.4.2 Sensor Processing Node

Create a node that processes the simulated sensor data:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Image, LaserScan, JointState
from geometry_msgs.msg import Twist, PointStamped
from std_msgs.msg import Float32, Bool
from cv_bridge import CvBridge
import numpy as np
import math

class SensorProcessingNode(Node):
    """Process sensor data from humanoid robot"""

    def __init__(self):
        super().__init__('sensor_processing_node')

        # Subscribers
        self.imu_sub = self.create_subscription(Imu, 'imu/data', self.imu_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        self.joint_sub = self.create_subscription(JointState, 'joint_states', self.joint_callback, 10)
        self.image_sub = self.create_subscription(Image, 'camera/rgb/image_raw', self.image_callback, 10)

        # Publishers
        self.balance_pub = self.create_publisher(Float32, 'balance_state', 10)
        self.obstacle_pub = self.create_publisher(Bool, 'obstacle_detected', 10)
        self.control_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Internal state
        self.orientation = None
        self.angular_velocity = None
        self.linear_acceleration = None
        self.scan_ranges = None
        self.joint_positions = {}
        self.cv_bridge = CvBridge()

        # Processing timer
        self.processing_timer = self.create_timer(0.1, self.process_sensors)

        self.get_logger().info('Sensor processing node initialized')

    def imu_callback(self, msg):
        """Process IMU data"""
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

    def scan_callback(self, msg):
        """Process laser scan data"""
        self.scan_ranges = np.array(msg.ranges)

    def joint_callback(self, msg):
        """Process joint state data"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]

    def image_callback(self, msg):
        """Process image data (placeholder for vision processing)"""
        try:
            cv_image = self.cv_bridge.imgmsg_to_cv2(msg, "bgr8")
            # In a real implementation, this would process the image
            # for object detection, tracking, etc.
        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

    def process_sensors(self):
        """Process all sensor data and generate outputs"""
        # Calculate balance state from IMU data
        if self.orientation is not None:
            balance_state = self.calculate_balance_state()
            balance_msg = Float32()
            balance_msg.data = balance_state
            self.balance_pub.publish(balance_msg)

        # Detect obstacles from laser scan
        if self.scan_ranges is not None:
            has_obstacle = self.detect_obstacles()
            obstacle_msg = Bool()
            obstacle_msg.data = has_obstacle
            self.obstacle_pub.publish(obstacle_msg)

        # Generate control commands based on sensor data
        self.generate_control_commands()

    def calculate_balance_state(self):
        """Calculate balance state from IMU data"""
        if self.orientation is None:
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

        # Balance score (0 = perfectly balanced, higher = less balanced)
        balance_score = abs(roll) + abs(pitch)
        return balance_score

    def detect_obstacles(self):
        """Detect obstacles from laser scan data"""
        if self.scan_ranges is None:
            return False

        # Check for obstacles within 1 meter
        obstacle_distances = self.scan_ranges[self.scan_ranges < 1.0]
        return len(obstacle_distances) > 0

    def generate_control_commands(self):
        """Generate control commands based on sensor processing"""
        cmd_msg = Twist()

        # Simple control logic
        if self.orientation is not None:
            # If robot is tilting too much, try to correct
            w, x, y, z = self.orientation
            pitch = math.asin(2 * (w * y - z * x))

            # Apply corrective rotation
            cmd_msg.angular.z = -pitch * 2.0  # PD control with kp=2.0

        if self.scan_ranges is not None:
            # If obstacle detected, slow down forward motion
            if self.detect_obstacles():
                cmd_msg.linear.x = 0.0
            else:
                cmd_msg.linear.x = 0.5  # Move forward at 0.5 m/s

        self.control_pub.publish(cmd_msg)

def main(args=None):
    rclpy.init(args=args)

    node = SensorProcessingNode()

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

## 4.5 Sensor Validation and Testing

### 4.5.1 Sensor Accuracy Validation

Validating simulated sensors against real-world expectations:

```python
import unittest
import numpy as np

class TestSensorSimulation(unittest.TestCase):
    """Test suite for sensor simulation accuracy"""

    def setUp(self):
        """Set up test fixtures"""
        self.noise_model = SensorNoiseModel()

    def test_imu_noise_characteristics(self):
        """Test that IMU noise follows expected distribution"""
        samples = 1000
        noise_values = self.noise_model.gaussian_noise(0, 0.01, samples)

        # Check mean is close to expected
        self.assertAlmostEqual(np.mean(noise_values), 0.0, delta=0.005)

        # Check standard deviation is close to expected
        self.assertAlmostEqual(np.std(noise_values), 0.01, delta=0.002)

    def test_lidar_range_limits(self):
        """Test that LiDAR ranges stay within expected limits"""
        true_ranges = np.full(360, 5.0)  # 360 ranges at 5m
        noisy_ranges = self.noise_model.gaussian_noise(0, 0.02, len(true_ranges))
        noisy_ranges = np.clip(true_ranges + noisy_ranges, 0.1, 10.0)

        # All ranges should be within limits
        self.assertTrue(np.all(noise_ranges >= 0.1))
        self.assertTrue(np.all(noise_ranges <= 10.0))

    def test_camera_resolution_preserved(self):
        """Test that camera resolution is maintained after noise addition"""
        original_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        # Add noise to image
        noise = self.noise_model.gaussian_noise(0, 10, original_image.shape)
        noisy_image = np.clip(original_image.astype(np.float32) + noise, 0, 255).astype(np.uint8)

        # Resolution should be preserved
        self.assertEqual(original_image.shape, noisy_image.shape)

# Run tests
if __name__ == '__main__':
    unittest.main()
```

### 4.5.2 Performance Testing

Testing sensor simulation performance:

```python
import time
import psutil
import matplotlib.pyplot as plt

class SensorPerformanceTester:
    """Test performance of sensor simulation"""

    def __init__(self):
        self.metrics = {
            'sensor_generation_times': [],
            'publish_rates': [],
            'cpu_usage': [],
            'memory_usage': []
        }

    def test_sensor_generation_performance(self, num_iterations=1000):
        """Test performance of sensor data generation"""

        for i in range(num_iterations):
            start_time = time.time()

            # Simulate generating sensor data
            self.generate_test_sensor_data()

            generation_time = time.time() - start_time
            self.metrics['sensor_generation_times'].append(generation_time)

            # Record system metrics
            self.metrics['cpu_usage'].append(psutil.cpu_percent())
            self.metrics['memory_usage'].append(psutil.virtual_memory().percent)

            # Calculate publish rate
            if i > 0:
                publish_rate = 1.0 / generation_time
                self.metrics['publish_rates'].append(publish_rate)

    def generate_test_sensor_data(self):
        """Generate test sensor data for performance testing"""
        # Simulate IMU data
        imu_orientation = np.random.normal(0, 0.1, 4)
        imu_angular_vel = np.random.normal(0, 0.01, 3)
        imu_linear_acc = np.random.normal(0, 0.1, 3)

        # Simulate camera data
        camera_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)

        # Simulate LiDAR data
        lidar_ranges = np.random.uniform(0.1, 10.0, 360)

        # Add processing delays
        time.sleep(0.001)  # Simulate processing time

    def plot_performance_results(self):
        """Plot performance test results"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        # Sensor generation times
        axes[0, 0].plot(self.metrics['sensor_generation_times'])
        axes[0, 0].set_title('Sensor Generation Times')
        axes[0, 0].set_xlabel('Iteration')
        axes[0, 0].set_ylabel('Time (s)')

        # Publish rates
        if self.metrics['publish_rates']:
            axes[0, 1].plot(self.metrics['publish_rates'])
            axes[0, 1].set_title('Publish Rates')
            axes[0, 1].set_xlabel('Iteration')
            axes[0, 1].set_ylabel('Rate (Hz)')

        # CPU usage
        axes[1, 0].plot(self.metrics['cpu_usage'])
        axes[1, 0].set_title('CPU Usage')
        axes[1, 0].set_xlabel('Iteration')
        axes[1, 0].set_ylabel('CPU %')

        # Memory usage
        axes[1, 1].plot(self.metrics['memory_usage'])
        axes[1, 1].set_title('Memory Usage')
        axes[1, 1].set_xlabel('Iteration')
        axes[1, 1].set_ylabel('Memory %')

        plt.tight_layout()
        plt.show()

    def get_performance_summary(self):
        """Get performance summary"""
        if len(self.metrics['sensor_generation_times']) > 0:
            avg_gen_time = np.mean(self.metrics['sensor_generation_times'])
            avg_cpu = np.mean(self.metrics['cpu_usage'])
            avg_memory = np.mean(self.metrics['memory_usage'])

            summary = {
                'avg_generation_time_ms': avg_gen_time * 1000,
                'avg_cpu_percent': avg_cpu,
                'avg_memory_percent': avg_memory,
                'max_generation_time_ms': max(self.metrics['sensor_generation_times']) * 1000
            }

            return summary
        return None

# Example usage
tester = SensorPerformanceTester()
tester.test_sensor_generation_performance(num_iterations=500)
summary = tester.get_performance_summary()
print("Performance Summary:", summary)
```

## 4.6 Advanced Sensor Configurations

### 4.6.1 Multi-Sensor Setup for Humanoid Perception

```xml
<!-- Complex sensor configuration for full humanoid perception -->
<sdf version="1.7">
  <model name="humanoid_with_perception_sensors">
    <!-- Main body links with sensors -->
    <link name="base_link">
      <pose>0 0 0.8 0 0 0</pose>
    </link>

    <!-- Torso with IMU and center of mass sensor -->
    <link name="torso">
      <pose>0 0 0.2 0 0 0</pose>

      <!-- Main IMU for balance and orientation -->
      <sensor name="torso_imu" type="imu">
        <pose>0 0 0 0 0 0</pose>
        <topic>imu/data</topic>
        <update_rate>200</update_rate>
        <always_on>true</always_on>
        <imu>
          <angular_velocity>
            <x><noise type="gaussian"><mean>0.0</mean><stddev>0.0005</stddev></noise></x>
            <y><noise type="gaussian"><mean>0.0</mean><stddev>0.0005</stddev></noise></y>
            <z><noise type="gaussian"><mean>0.0</mean><stddev>0.0005</stddev></noise></z>
          </angular_velocity>
          <linear_acceleration>
            <x><noise type="gaussian"><mean>0.0</mean><stddev>0.005</stddev></noise></x>
            <y><noise type="gaussian"><mean>0.0</mean><stddev>0.005</stddev></noise></y>
            <z><noise type="gaussian"><mean>0.0</mean><stddev>0.005</stddev></noise></z>
          </linear_acceleration>
        </imu>
      </sensor>

      <!-- Body-mounted camera for torso-relative vision -->
      <sensor name="torso_camera" type="camera">
        <pose>0.05 0 0 0 0 0</pose>
        <topic>torso_camera/image_raw</topic>
        <camera name="torso_camera">
          <horizontal_fov>1.22</horizontal_fov> <!-- 70 degrees -->
          <image><width>640</width><height>480</height><format>R8G8B8</format></image>
          <clip><near>0.1</near><far>10.0</far></clip>
          <noise><type>gaussian</type><mean>0.0</mean><stddev>0.007</stddev></noise>
        </camera>
        <update_rate>30</update_rate>
        <always_on>true</always_on>
      </sensor>
    </link>

    <!-- Head with multiple sensors -->
    <link name="head">
      <pose>0 0 0.3 0 0 0</pose>

      <!-- Stereo camera pair -->
      <sensor name="stereo_left" type="camera">
        <pose>0.05 0.03 0 0 0 0</pose>
        <topic>stereo/left/image_raw</topic>
        <camera name="left_cam">
          <horizontal_fov>1.047</horizontal_fov>
          <image><width>640</width><height>480</height><format>R8G8B8</format></image>
          <clip><near>0.1</near><far>10.0</far></clip>
        </camera>
        <update_rate>30</update_rate>
        <always_on>true</always_on>
      </sensor>

      <sensor name="stereo_right" type="camera">
        <pose>0.05 -0.03 0 0 0 0</pose>
        <topic>stereo/right/image_raw</topic>
        <camera name="right_cam">
          <horizontal_fov>1.047</horizontal_fov>
          <image><width>640</width><height>480</height><format>R8G8B8</format></image>
          <clip><near>0.1</near><far>10.0</far></clip>
        </camera>
        <update_rate>30</update_rate>
        <always_on>true</always_on>
      </sensor>

      <!-- Head-mounted depth sensor -->
      <sensor name="head_depth" type="depth">
        <pose>0.07 0 0 0 0 0</pose>
        <topic>head_depth/image_raw</topic>
        <camera name="depth_cam">
          <horizontal_fov>1.047</horizontal_fov>
          <image><width>320</width><height>240</height><format>R16G16B16</format></image>
          <clip><near>0.1</near><far>5.0</far></clip>
        </camera>
        <update_rate>30</update_rate>
        <always_on>true</always_on>
      </sensor>

      <!-- Microphone array -->
      <sensor name="microphone_array" type="audio">
        <pose>0 0 0.05 0 0 0</pose>
        <topic>audio_data</topic>
        <audio><type>microphone</type></audio>
        <update_rate>44100</update_rate>
        <always_on>true</always_on>
      </sensor>
    </link>

    <!-- Feet with force/torque sensors -->
    <link name="left_foot">
      <pose>0 0.1 -0.4 0 0 0</pose>

      <sensor name="left_foot_force" type="force_torque">
        <pose>0 0 0 0 0 0</pose>
        <topic>left_foot/force_torque</topic>
        <force_torque>
          <frame>child</frame>
          <measure_direction>child_to_parent</measure_direction>
        </force_torque>
        <update_rate>100</update_rate>
        <always_on>true</always_on>
      </sensor>
    </link>

    <link name="right_foot">
      <pose>0 -0.1 -0.4 0 0 0</pose>

      <sensor name="right_foot_force" type="force_torque">
        <pose>0 0 0 0 0 0</pose>
        <topic>right_foot/force_torque</topic>
        <force_torque>
          <frame>child</frame>
          <measure_direction>child_to_parent</measure_direction>
        </force_torque>
        <update_rate>100</update_rate>
        <always_on>true</always_on>
      </sensor>
    </link>

    <!-- 3D LiDAR on top of head -->
    <link name="lidar_mount">
      <pose>0 0 0.4 0 0 0</pose>

      <sensor name="3d_lidar" type="ray">
        <pose>0 0 0.05 0 0 0</pose>
        <topic>points</topic>
        <ray>
          <scan>
            <horizontal><samples>1080</samples><resolution>1</resolution>
            <min_angle>-3.14159</min_angle><max_angle>3.14159</max_angle></horizontal>
            <vertical><samples>32</samples><resolution>1</resolution>
            <min_angle>-0.5236</min_angle><max_angle>0.3491</max_angle></vertical>
          </scan>
          <range><min>0.1</min><max>20.0</max><resolution>0.01</resolution></range>
        </ray>
        <update_rate>10</update_rate>
        <always_on>true</always_on>
      </sensor>
    </link>
  </model>
</sdf>
```

## 4.7 Data Flow Diagrams

### 4.7.1 Sensor Data Flow Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Physical      │    │   Sensor         │    │   ROS 2         │
│   World         │───►│   Simulation     │───►│   Interface     │
│                 │    │                  │    │                 │
│ - Environment   │    │ - IMU           │    │ - sensor_msgs   │
│ - Objects       │    │ - Cameras       │    │ - Publishers    │
│ - Lighting      │    │ - LiDAR         │    │ - Subscribers   │
│ - Occlusions    │    │ - Force/Torque  │    │ - Topics        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Sensor        │    │   Noise &        │    │   Data          │
│   Physics       │    │   Distortion     │    │   Processing    │
│   Modeling      │    │   Modeling       │    │                 │
│                 │    │                  │    │ - Filtering     │
│ - Ray Tracing   │    │ - Gaussian       │    │ - Fusion        │
│ - Collision     │    │ - Bias           │    │ - Feature       │
│ - Occlusion     │    │ - Drift          │    │   Extraction    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 4.7.2 Multi-Sensor Fusion Pipeline

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   IMU Sensor    │    │   Data           │    │   State         │
│   (Orientation, │───►│   Preprocessing  │───►│   Estimation    │
│   Acceleration) │    │   & Synchronization│    │   (Kalman      │
└─────────────────┘    │                  │    │   Filter)       │
         │               │ - Time sync      │    │                 │
         │               │ - Calibration    │    │ - Position      │
         ▼               │ - Noise removal  │    │ - Velocity      │
┌─────────────────┐    └──────────────────┘    │ - Orientation   │
│   Camera        │              │              └─────────────────┘
│   (Vision)      │              │                       │
└─────────────────┘              ▼                       │
         │               ┌──────────────────┐    ┌─────────────────┐
         │               │   Sensor         │    │   Output        │
         ▼               │   Fusion         │    │   Generation    │
┌─────────────────┐    │   (Extended       │    │                 │
│   LiDAR         │───►│   Kalman Filter) │───►│ - Control       │
│   (Range)       │    │   & Data         │    │   Commands      │
└─────────────────┘    │   Association    │    │ - Navigation    │
         │               │                  │    │   Plans         │
         │               └──────────────────┘    │ - Perception    │
         ▼                       │               │   Results       │
┌─────────────────┐              │              └─────────────────┘
│   Force/Torque  │              ▼
│   (Contact)     │    ┌──────────────────┐
└─────────────────┘    │   Validation &   │
                       │   Monitoring     │
                       │                  │
                       │ - Consistency    │
                       │   Checks         │
                       │ - Error Bounds   │
                       │ - Performance    │
                       │   Metrics        │
                       └──────────────────┘
```

## 4.8 Tables for Clarity

### 4.8.1 Sensor Comparison Table

| Sensor Type | Update Rate | Range | Accuracy | Power | Application |
|-------------|-------------|-------|----------|-------|-------------|
| IMU | 100-1000 Hz | N/A | High | Low | Balance, Orientation |
| RGB Camera | 15-60 Hz | Visual | Medium | Medium | Vision, Recognition |
| Depth Camera | 15-30 Hz | 0.5-5m | Medium | Medium | 3D Reconstruction |
| 2D LiDAR | 5-20 Hz | 0.1-30m | High | Medium | Navigation, Mapping |
| 3D LiDAR | 5-20 Hz | 0.1-100m | High | High | Environment Mapping |
| Force/Torque | 100-1000 Hz | N/A | Very High | Low | Contact Sensing |

### 4.8.2 Noise Characteristics Table

| Sensor | Noise Type | Std Dev | Bias | Drift Rate |
|--------|------------|---------|------|------------|
| IMU Gyro | Gaussian | 0.001 rad/s | 0.0001 rad/s | 0.00001 rad/s² |
| IMU Accel | Gaussian | 0.01 m/s² | 0.001 m/s² | 0.0001 m/s³ |
| Camera | Gaussian | 0.5% of signal | - | - |
| LiDAR Range | Gaussian | 0.01-0.02 m | - | - |
| Joint Encoder | Quantization | 0.001 rad | - | - |

## 4.9 Exercises

### Exercise 1: Sensor Configuration
Configure a complete sensor suite for a humanoid robot model, including IMU, cameras, LiDAR, and force/torque sensors. Test the configuration in Gazebo and verify that all sensors publish data correctly.

### Exercise 2: Noise Modeling
Implement realistic noise models for each sensor type and validate that the noise characteristics match expected real-world sensor behavior.

### Exercise 3: Multi-Sensor Fusion
Create a node that fuses data from multiple sensors (IMU and cameras) to estimate robot pose and validate the fused estimate against ground truth.

### Exercise 4: Performance Testing
Test the performance impact of different sensor configurations and identify bottlenecks in sensor data processing.

### Exercise 5: Sim-to-Real Validation
Compare the behavior of perception algorithms using simulated vs. real sensor data and document the differences.

## 4.10 Mini-Project: Complete Perception System

Implement a complete perception system for a humanoid robot that includes:
1. Multi-sensor data acquisition and synchronization
2. Sensor fusion algorithms for state estimation
3. Object detection and tracking using vision data
4. Obstacle detection and mapping using range sensors
5. Integration with ROS 2 for real-time processing
6. Performance optimization for real-time execution

## 4.11 Summary

This chapter has covered the comprehensive simulation of sensors for humanoid robots, which is critical for developing robust perception systems. Key concepts include:

- Different types of sensors required for humanoid robotics
- Proper configuration of sensor parameters and noise models
- Integration with ROS 2 messaging system
- Sensor fusion techniques for combining multiple sensor inputs
- Validation methods to ensure realistic sensor behavior
- Performance considerations for real-time sensor processing

Accurate sensor simulation is essential for effective sim-to-real transfer, allowing algorithms to be developed and tested in simulation before deployment on physical robots. The proper configuration of sensor models with realistic noise and characteristics significantly impacts the success of humanoid robot systems.