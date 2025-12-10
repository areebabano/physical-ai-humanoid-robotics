---
title: "Module 3.2 - Chapter 2: AI Perception & Reinforcement Learning"
sidebar_position: 2
---

# Module 3.2 - Chapter 2: AI Perception & Reinforcement Learning

## 2.0 Introduction

The integration of artificial intelligence perception systems with reinforcement learning (RL) represents a paradigm shift in humanoid robotics, enabling robots to learn complex behaviors through environmental interaction. This chapter explores the critical components of AI perception pipelines and reinforcement learning frameworks that form the foundation of intelligent humanoid robot systems.

Modern humanoid robots require sophisticated perception capabilities to understand their environment, combined with adaptive learning mechanisms to handle complex, dynamic scenarios. The synergy between perception and RL creates a closed-loop system where sensory input drives decision-making, and actions generate new sensory experiences that refine future decisions.

## 2.1 AI Perception Systems

### 2.1.1 Vision-Based Perception

Vision systems form the primary sensory modality for humanoid robots, enabling object recognition, scene understanding, and navigation. Modern vision pipelines integrate deep learning models with traditional computer vision techniques to extract meaningful information from visual data.

```python
# Example vision perception pipeline
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class VisionPerceptionPipeline:
    def __init__(self):
        self.bridge = CvBridge()
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])

        # Load pre-trained model for object detection
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        self.model.eval()

    def preprocess_image(self, image_msg):
        """Preprocess ROS Image message for AI perception"""
        cv_image = self.bridge.imgmsg_to_cv2(image_msg, "bgr8")

        # Resize and normalize image
        resized_image = cv2.resize(cv_image, (640, 480))
        tensor_image = self.transform(resized_image)

        return tensor_image, cv_image

    def detect_objects(self, image_msg):
        """Detect objects in the image using YOLOv5"""
        tensor_image, cv_image = self.preprocess_image(image_msg)

        # Perform object detection
        results = self.model(cv_image)

        # Extract detections
        detections = []
        for detection in results.xyxy[0]:
            x1, y1, x2, y2, conf, cls = detection
            detections.append({
                'class': int(cls),
                'confidence': float(conf),
                'bbox': [float(x1), float(y1), float(x2), float(y2)]
            })

        return detections

    def extract_features(self, image_msg):
        """Extract visual features for RL state representation"""
        tensor_image, cv_image = self.preprocess_image(image_msg)

        # Convert to grayscale for simpler feature extraction
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Extract SIFT features
        sift = cv2.SIFT_create()
        keypoints, descriptors = sift.detectAndCompute(gray, None)

        # Convert to feature vector
        if descriptors is not None and len(descriptors) > 0:
            # Use first 128 descriptors as feature vector
            features = descriptors.flatten()[:128]
            if len(features) < 128:
                features = np.pad(features, (0, 128 - len(features)))
        else:
            features = np.zeros(128)

        return features
```

### 2.1.2 LiDAR Perception

LiDAR sensors provide precise 3D spatial information crucial for navigation and obstacle avoidance in humanoid robots. The perception pipeline for LiDAR data involves point cloud processing, segmentation, and feature extraction.

```python
# Example LiDAR perception pipeline
import numpy as np
import open3d as o3d
from sensor_msgs.msg import LaserScan, PointCloud2
import sensor_msgs.point_cloud2 as pc2

class LIDARPerceptionPipeline:
    def __init__(self):
        self.min_distance = 0.1
        self.max_distance = 10.0

    def process_laser_scan(self, scan_msg):
        """Process LaserScan message into navigable space information"""
        # Extract ranges from laser scan
        ranges = np.array(scan_msg.ranges)

        # Filter invalid ranges
        ranges = np.where((ranges >= self.min_distance) &
                         (ranges <= self.max_distance), ranges, np.inf)

        # Calculate angles for each range measurement
        angles = np.linspace(scan_msg.angle_min, scan_msg.angle_max, len(ranges))

        # Detect obstacles and free space
        obstacle_threshold = 1.0  # meters
        obstacles = ranges < obstacle_threshold
        free_space = ranges >= obstacle_threshold

        # Calculate safe navigation directions
        safe_angles = angles[free_space]
        safe_distances = ranges[free_space]

        return {
            'obstacles': obstacles,
            'safe_angles': safe_angles,
            'safe_distances': safe_distances,
            'min_distance': np.min(ranges) if np.any(ranges != np.inf) else np.inf
        }

    def process_point_cloud(self, pointcloud_msg):
        """Process PointCloud2 message into 3D features"""
        # Convert ROS PointCloud2 to numpy array
        points = []
        for point in pc2.read_points(pointcloud_msg,
                                   field_names=("x", "y", "z"),
                                   skip_nans=True):
            points.append([point[0], point[1], point[2]])

        points = np.array(points)

        if len(points) == 0:
            return {'features': np.zeros(64), 'clusters': []}

        # Convert to Open3D point cloud
        pcd = o3d.geometry.PointCloud()
        pcd.points = o3d.utility.Vector3dVector(points)

        # Downsample point cloud for efficiency
        pcd_downsampled = pcd.voxel_down_sample(voxel_size=0.05)

        # Extract geometric features
        points_downsampled = np.asarray(pcd_downsampled.points)

        # Calculate basic geometric features
        features = np.concatenate([
            np.mean(points_downsampled, axis=0),  # Centroid
            np.std(points_downsampled, axis=0),   # Variance
            [len(points_downsampled)]             # Point count
        ])

        # Pad or truncate to fixed size
        if len(features) < 64:
            features = np.pad(features, (0, 64 - len(features)))
        else:
            features = features[:64]

        return {'features': features, 'point_count': len(points_downsampled)}
```

### 2.1.3 Depth Sensing

Depth sensors provide crucial 3D information for humanoid robots, enabling understanding of spatial relationships and obstacle detection. Depth perception is particularly important for navigation and manipulation tasks.

```python
from cv_bridge import CvBridge

class DepthPerceptionPipeline:
    def __init__(self):
        self.bridge = CvBridge()
        self.min_depth = 0.1  # meters
        self.max_depth = 10.0  # meters

    def process_depth_image(self, depth_msg):
        """Process depth image for obstacle detection and spatial understanding"""
        cv_depth = self.bridge.imgmsg_to_cv2(depth_msg, "32FC1")

        # Filter depth values
        valid_depth = np.where((cv_depth >= self.min_depth) &
                              (cv_depth <= self.max_depth), cv_depth, np.inf)

        # Calculate depth statistics
        depth_stats = {
            'mean': np.nanmean(cv_depth[(cv_depth >= self.min_depth) &
                                       (cv_depth <= self.max_depth)]),
            'std': np.nanstd(cv_depth[(cv_depth >= self.min_depth) &
                                     (cv_depth <= self.max_depth)]),
            'min': np.nanmin(cv_depth[(cv_depth >= self.min_depth) &
                                     (cv_depth <= self.max_depth)]),
            'max': np.nanmax(cv_depth[(cv_depth >= self.min_depth) &
                                     (cv_depth <= self.max_depth)])
        }

        # Detect surfaces and obstacles
        obstacle_threshold = 2.0  # meters
        obstacles = valid_depth < obstacle_threshold
        free_space = valid_depth >= obstacle_threshold

        # Calculate surface normals for terrain analysis
        if cv_depth.size > 0:
            # Calculate gradients for surface normal estimation
            grad_x = np.gradient(cv_depth, axis=1)
            grad_y = np.gradient(cv_depth, axis=0)

            # Estimate surface normal magnitude
            surface_normal_magnitude = np.sqrt(grad_x**2 + grad_y**2)
        else:
            surface_normal_magnitude = np.zeros_like(cv_depth)

        return {
            'depth_stats': depth_stats,
            'obstacles': obstacles,
            'free_space': free_space,
            'surface_normals': surface_normal_magnitude,
            'valid_depth_count': np.sum((cv_depth >= self.min_depth) &
                                       (cv_depth <= self.max_depth))
        }

    def extract_traversable_path(self, depth_msg):
        """Extract traversable path from depth information"""
        cv_depth = self.bridge.imgmsg_to_cv2(depth_msg, "32FC1")

        # Create traversability map
        traversable = np.where((cv_depth >= self.min_depth) &
                              (cv_depth <= self.max_depth) &
                              (cv_depth > 0.5), 1.0, 0.0)

        # Apply morphological operations to clean up the map
        kernel = np.ones((5, 5), np.float32)
        traversable = cv2.morphologyEx(traversable, cv2.MORPH_CLOSE, kernel)
        traversable = cv2.morphologyEx(traversable, cv2.MORPH_OPEN, kernel)

        return traversable
```

## 2.2 Sensor Fusion

### 2.2.1 Multi-Sensor Integration

Sensor fusion combines data from multiple perception modalities to create a comprehensive understanding of the environment. This approach improves robustness and accuracy compared to single-sensor approaches.

```python
# Example sensor fusion pipeline
import numpy as np
from collections import deque
import threading
import time

class SensorFusionPipeline:
    def __init__(self, buffer_size=10):
        self.vision_pipeline = VisionPerceptionPipeline()
        self.lidar_pipeline = LIDARPerceptionPipeline()
        self.depth_pipeline = DepthPerceptionPipeline()

        # Data buffers for temporal fusion
        self.vision_buffer = deque(maxlen=buffer_size)
        self.lidar_buffer = deque(maxlen=buffer_size)
        self.depth_buffer = deque(maxlen=buffer_size)

        # Timestamps for synchronization
        self.vision_timestamp = 0
        self.lidar_timestamp = 0
        self.depth_timestamp = 0

        # Lock for thread safety
        self.lock = threading.Lock()

    def fuse_perception_data(self, vision_data, lidar_data, depth_data):
        """Fuse data from multiple sensors"""
        with self.lock:
            # Add current data to buffers
            self.vision_buffer.append(vision_data)
            self.lidar_buffer.append(lidar_data)
            self.depth_buffer.append(depth_data)

            # Create fused representation
            fused_features = self._create_fused_features(
                vision_data, lidar_data, depth_data
            )

            # Calculate confidence scores
            confidence = self._calculate_confidence(
                vision_data, lidar_data, depth_data
            )

            return {
                'features': fused_features,
                'confidence': confidence,
                'timestamp': time.time()
            }

    def _create_fused_features(self, vision_data, lidar_data, depth_data):
        """Create a unified feature vector from multiple sensors"""
        # Extract features from each modality
        vision_features = vision_data.get('features', np.zeros(128))
        lidar_features = lidar_data.get('features', np.zeros(64))
        depth_features = self._extract_depth_features(depth_data)

        # Concatenate features
        fused_features = np.concatenate([
            vision_features,
            lidar_features,
            depth_features
        ])

        return fused_features

    def _extract_depth_features(self, depth_data):
        """Extract features from depth data"""
        stats = depth_data.get('depth_stats', {})
        features = np.array([
            stats.get('mean', 0.0),
            stats.get('std', 0.0),
            stats.get('min', 0.0),
            stats.get('max', 0.0)
        ])

        # Pad to consistent size
        if len(features) < 16:
            features = np.pad(features, (0, 16 - len(features)))
        else:
            features = features[:16]

        return features

    def _calculate_confidence(self, vision_data, lidar_data, depth_data):
        """Calculate confidence in fused perception"""
        # Simple confidence calculation based on data availability
        vision_conf = 1.0 if len(vision_data.get('features', [])) > 0 else 0.0
        lidar_conf = 1.0 if lidar_data.get('point_count', 0) > 0 else 0.0
        depth_conf = 1.0 if depth_data.get('valid_depth_count', 0) > 0 else 0.0

        # Weighted average with sensor-specific weights
        weights = [0.4, 0.3, 0.3]  # Vision, LiDAR, Depth
        confidence = (weights[0] * vision_conf +
                     weights[1] * lidar_conf +
                     weights[2] * depth_conf)

        return confidence
```

## 2.3 Data Preprocessing and ROS 2 Integration

### 2.3.1 ROS 2 Topic Integration

ROS 2 provides the communication infrastructure for connecting perception modules with the rest of the robotic system. Proper integration ensures timely and reliable data flow.

```python
# Example ROS 2 perception node
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan, PointCloud2
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np

class PerceptionNode(Node):
    def __init__(self):
        super().__init__('perception_node')

        # Initialize perception pipelines
        self.fusion_pipeline = SensorFusionPipeline()

        # Create subscribers
        self.vision_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_raw',
            self.vision_callback,
            10
        )

        self.lidar_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.lidar_callback,
            10
        )

        self.depth_sub = self.create_subscription(
            Image,
            '/camera/depth/image_raw',
            self.depth_callback,
            10
        )

        # Create publishers
        self.perception_pub = self.create_publisher(
            Float32MultiArray,
            '/perception/features',
            10
        )

        self.control_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        # Data storage
        self.vision_data = None
        self.lidar_data = None
        self.depth_data = None

        # Timer for fusion processing
        self.timer = self.create_timer(0.1, self.process_fusion)  # 10 Hz

    def vision_callback(self, msg):
        """Process vision data"""
        try:
            features = self.fusion_pipeline.vision_pipeline.extract_features(msg)
            self.vision_data = {'features': features}
        except Exception as e:
            self.get_logger().error(f'Vision processing error: {e}')

    def lidar_callback(self, msg):
        """Process LiDAR data"""
        try:
            processed_data = self.fusion_pipeline.lidar_pipeline.process_laser_scan(msg)
            self.lidar_data = processed_data
        except Exception as e:
            self.get_logger().error(f'LiDAR processing error: {e}')

    def depth_callback(self, msg):
        """Process depth data"""
        try:
            processed_data = self.fusion_pipeline.depth_pipeline.process_depth_image(msg)
            self.depth_data = processed_data
        except Exception as e:
            self.get_logger().error(f'Depth processing error: {e}')

    def process_fusion(self):
        """Process fused perception data"""
        if (self.vision_data is not None and
            self.lidar_data is not None and
            self.depth_data is not None):

            try:
                # Fuse perception data
                fused_result = self.fusion_pipeline.fuse_perception_data(
                    self.vision_data, self.lidar_data, self.depth_data
                )

                # Publish fused features
                features_msg = Float32MultiArray()
                features_msg.data = fused_result['features'].tolist()
                self.perception_pub.publish(features_msg)

                # Reset data for next cycle
                self.vision_data = None
                self.lidar_data = None
                self.depth_data = None

            except Exception as e:
                self.get_logger().error(f'Fusion processing error: {e}')
```

## 2.4 Reinforcement Learning Fundamentals

### 2.4.1 RL Agent Architecture

Reinforcement learning agents for humanoid robots must handle complex, high-dimensional state and action spaces while learning effective policies for locomotion and manipulation tasks.

```python
# Example RL agent for humanoid robot
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
import random
from collections import deque

class HumanoidRLAgent(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=256):
        super(HumanoidRLAgent, self).__init__()

        # Actor network (policy network)
        self.actor = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # Actions are normalized to [-1, 1]
        )

        # Critic network (value network)
        self.critic = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )

        # Initialize weights
        self._init_weights()

    def _init_weights(self):
        """Initialize network weights"""
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.constant_(m.bias, 0)

    def forward(self, state):
        """Forward pass through the network"""
        action = self.actor(state)
        value = self.critic(state)
        return action, value

    def get_action(self, state, add_noise=True):
        """Get action from the policy"""
        state_tensor = torch.FloatTensor(state).unsqueeze(0)
        action, _ = self.forward(state_tensor)
        action = action.squeeze(0).detach().numpy()

        if add_noise:
            # Add noise for exploration
            noise = np.random.normal(0, 0.1, size=action.shape)
            action = np.clip(action + noise, -1, 1)

        return action

class HumanoidReplayBuffer:
    def __init__(self, capacity=1000000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Add experience to buffer"""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Sample batch from buffer"""
        batch = random.sample(self.buffer, batch_size)
        state, action, reward, next_state, done = map(np.stack, zip(*batch))
        return state, action, reward, next_state, done

    def __len__(self):
        return len(self.buffer)

class HumanoidPPOAgent:
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99,
                 epsilon=0.2, epochs=10):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.agent = HumanoidRLAgent(state_dim, action_dim).to(self.device)
        self.optimizer = optim.Adam(self.agent.parameters(), lr=lr)

        self.gamma = gamma
        self.epsilon = epsilon
        self.epochs = epochs

        self.old_log_probs = None
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
        self.values = []
        self.dones = []

    def select_action(self, state):
        """Select action using current policy"""
        state_tensor = torch.FloatTensor(state).to(self.device)
        action, value = self.agent(state_tensor)

        # Calculate action log probability
        mean_action = action
        std = torch.ones_like(action) * 0.1  # Fixed standard deviation
        dist = torch.distributions.Normal(mean_action, std)
        action = dist.sample()
        log_prob = dist.log_prob(action).sum(dim=-1)

        return action.detach().cpu().numpy(), log_prob.detach().cpu().numpy(), value.detach().cpu().numpy()

    def store_transition(self, state, action, reward, log_prob, value, done):
        """Store transition in memory"""
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.log_probs.append(log_prob)
        self.values.append(value)
        self.dones.append(done)

    def compute_returns(self):
        """Compute returns using discounted rewards"""
        returns = []
        R = 0

        for reward, done in zip(reversed(self.rewards), reversed(self.dones)):
            if done:
                R = 0
            R = reward + self.gamma * R
            returns.insert(0, R)

        return torch.FloatTensor(returns).to(self.device)

    def update(self):
        """Update the policy using PPO"""
        if len(self.states) == 0:
            return

        # Convert to tensors
        states = torch.FloatTensor(self.states).to(self.device)
        actions = torch.FloatTensor(self.actions).to(self.device)
        old_log_probs = torch.FloatTensor(self.log_probs).to(self.device)
        old_values = torch.FloatTensor(self.values).to(self.device)

        # Compute returns
        returns = self.compute_returns()

        # Compute advantages
        advantages = returns - old_values

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Update policy for multiple epochs
        for _ in range(self.epochs):
            # Get current policy outputs
            new_actions, new_values = self.agent(states)

            # Calculate action log probabilities
            std = torch.ones_like(new_actions) * 0.1
            dist = torch.distributions.Normal(new_actions, std)
            new_log_probs = dist.log_prob(actions).sum(dim=-1)

            # Calculate ratio
            ratio = torch.exp(new_log_probs - old_log_probs)

            # Calculate PPO loss
            surr1 = ratio * advantages
            surr2 = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantages
            actor_loss = -torch.min(surr1, surr2).mean()

            # Calculate value loss
            value_loss = nn.MSELoss()(new_values.squeeze(), returns)

            # Total loss
            total_loss = actor_loss + 0.5 * value_loss

            # Update parameters
            self.optimizer.zero_grad()
            total_loss.backward()
            torch.nn.utils.clip_grad_norm_(self.agent.parameters(), 0.5)
            self.optimizer.step()

        # Clear stored transitions
        self.states = []
        self.actions = []
        self.rewards = []
        self.log_probs = []
        self.values = []
        self.dones = []
```

### 2.4.2 Reward Design for Humanoid Robots

Reward functions are critical for training effective RL agents. For humanoid robots, rewards must encourage stable locomotion, efficient movement, and task completion while avoiding harmful behaviors.

```python
# Example reward function for humanoid locomotion
class HumanoidRewardFunction:
    def __init__(self, target_velocity=1.0, target_heading=0.0):
        self.target_velocity = target_velocity
        self.target_heading = target_heading

    def calculate_reward(self, robot_state, action, prev_robot_state):
        """Calculate reward based on robot state and action"""
        reward = 0.0

        # Velocity reward - encourage forward movement
        forward_vel = robot_state.get('forward_velocity', 0.0)
        velocity_reward = max(0, forward_vel) * 1.0
        reward += velocity_reward

        # Heading reward - encourage movement in desired direction
        current_heading = robot_state.get('heading', 0.0)
        heading_diff = abs(current_heading - self.target_heading)
        heading_reward = max(0, 1.0 - heading_diff / np.pi) * 0.5
        reward += heading_reward

        # Stability reward - encourage upright posture
        base_orientation = robot_state.get('base_orientation', [0, 0, 0, 1])
        upright = base_orientation[2]  # z component of orientation
        stability_reward = max(0, upright) * 0.3
        reward += stability_reward

        # Smoothness penalty - discourage jerky movements
        action_smoothness = -np.sum(np.square(action)) * 0.01
        reward += action_smoothness

        # Height reward - encourage maintaining appropriate height
        base_height = robot_state.get('base_height', 0.0)
        target_height = 0.8  # meters
        height_penalty = -abs(base_height - target_height) * 0.2
        reward += height_penalty

        # Collision penalty - discourage collisions
        collision = robot_state.get('collision', False)
        if collision:
            reward -= 10.0

        # Energy efficiency - encourage efficient movement
        joint_velocities = robot_state.get('joint_velocities', [])
        energy_penalty = -np.sum(np.square(joint_velocities)) * 0.001
        reward += energy_penalty

        return reward

    def calculate_locomotion_reward(self, robot_state):
        """Specialized reward for walking/locomotion tasks"""
        reward = 0.0

        # Forward progress reward
        forward_progress = robot_state.get('forward_progress', 0.0)
        reward += forward_progress * 10.0

        # Balance reward
        roll = abs(robot_state.get('roll', 0.0))
        pitch = abs(robot_state.get('pitch', 0.0))
        balance_penalty = -(roll + pitch) * 5.0
        reward += balance_penalty

        # Step reward for sustained walking
        is_walking = robot_state.get('is_walking', False)
        if is_walking:
            reward += 0.1

        return reward
```

## 2.5 Training RL Agents in Simulation

### 2.5.1 Isaac Sim Integration for RL Training

Isaac Sim provides an excellent environment for training RL agents with realistic physics and rendering. The following example demonstrates how to integrate RL training with Isaac Sim.

```python
# Example RL training in Isaac Sim
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.robots import Robot
from omni.isaac.core.utils.prims import get_prim_at_path
import numpy as np
import torch

class IsaacSimRLTraining:
    def __init__(self, num_envs=64, max_episode_length=1000):
        self.num_envs = num_envs
        self.max_episode_length = max_episode_length

        # Initialize Isaac Sim world
        self.world = World(stage_units_in_meters=1.0)

        # Create multiple environments for parallel training
        self.envs = []
        for i in range(num_envs):
            env = self._create_environment(f"/World/env_{i}")
            self.envs.append(env)

        # Initialize RL agent
        self.state_dim = 128  # Example state dimension
        self.action_dim = 12  # Example action dimension (for humanoid joints)
        self.agent = HumanoidPPOAgent(self.state_dim, self.action_dim)

        # Reward function
        self.reward_function = HumanoidRewardFunction()

        # Episode tracking
        self.episode_lengths = np.zeros(num_envs)
        self.episode_rewards = np.zeros(num_envs)

    def _create_environment(self, prim_path):
        """Create a single training environment"""
        # Add ground plane
        add_reference_to_stage(
            usd_path="/Isaac/Environments/Simple_Room/simple_room.usd",
            prim_path=prim_path
        )

        # Add humanoid robot
        robot_path = f"{prim_path}/Robot"
        robot = Robot(
            prim_path=robot_path,
            name=f"humanoid_{prim_path.split('_')[-1]}",
            usd_path="/Isaac/Robots/Humanoid/humanoid_instanceable.usd",
            position=[0.0, 0.0, 0.5]
        )

        return {
            'robot': robot,
            'robot_path': robot_path,
            'prim_path': prim_path
        }

    def get_robot_state(self, env_idx):
        """Get the current state of the robot for RL"""
        env = self.envs[env_idx]
        robot = env['robot']

        # Get robot pose and velocities
        position, orientation = robot.get_world_pose()
        linear_vel, angular_vel = robot.get_linear_velocity(), robot.get_angular_velocity()

        # Get joint states
        joint_positions = robot.get_joint_positions()
        joint_velocities = robot.get_joint_velocities()

        # Create state vector (simplified example)
        state = np.concatenate([
            position[:2],  # x, y position
            [orientation[2]],  # z orientation (simplified)
            linear_vel[:2],  # x, y linear velocity
            joint_positions[:10],  # First 10 joint positions
            joint_velocities[:10]  # First 10 joint velocities
        ])

        # Pad or truncate to fixed size
        if len(state) < self.state_dim:
            state = np.pad(state, (0, self.state_dim - len(state)))
        else:
            state = state[:self.state_dim]

        return state

    def apply_action(self, env_idx, action):
        """Apply action to the robot"""
        env = self.envs[env_idx]
        robot = env['robot']

        # Convert normalized action to joint commands
        # This is a simplified example - real implementation would depend on robot specifics
        scaled_action = np.clip(action, -1, 1)  # Ensure action is in [-1, 1]

        # Apply joint position commands (PD control)
        current_positions = robot.get_joint_positions()
        target_positions = current_positions + scaled_action * 0.1  # Small step

        # Set joint positions
        robot.set_joint_positions(target_positions)

    def reset_environment(self, env_idx):
        """Reset a specific environment"""
        env = self.envs[env_idx]
        robot = env['robot']

        # Reset robot to initial position
        robot.set_world_pose(position=[0.0, 0.0, 0.5], orientation=[0, 0, 0, 1])
        robot.set_linear_velocity([0, 0, 0])
        robot.set_angular_velocity([0, 0, 0])

        # Reset joint positions to neutral pose
        neutral_positions = np.zeros(robot.num_dof)
        robot.set_joint_positions(neutral_positions)
        robot.set_joint_velocities(np.zeros(robot.num_dof))

        # Reset episode tracking
        self.episode_lengths[env_idx] = 0
        self.episode_rewards[env_idx] = 0

    def train_step(self):
        """Perform one step of training"""
        # Get states for all environments
        states = []
        for i in range(self.num_envs):
            state = self.get_robot_state(i)
            states.append(state)

        states = np.array(states)

        # Get actions from agent
        actions = []
        log_probs = []
        values = []

        for state in states:
            action, log_prob, value = self.agent.select_action(state)
            actions.append(action)
            log_probs.append(log_prob)
            values.append(value)

        actions = np.array(actions)
        log_probs = np.array(log_probs)
        values = np.array(values)

        # Store old states for reward calculation
        prev_states = states.copy()

        # Apply actions to environments
        for i, action in enumerate(actions):
            self.apply_action(i, action)

        # Step simulation
        self.world.step(render=False)

        # Calculate rewards and check for episode termination
        rewards = []
        dones = []

        for i in range(self.num_envs):
            # Calculate reward based on new state
            new_state = self.get_robot_state(i)
            reward = self.reward_function.calculate_reward(
                {'forward_velocity': new_state[2],  # Simplified
                 'base_orientation': [0, 0, new_state[3], 1],  # Simplified
                 'base_height': new_state[2] + 0.5,  # Simplified
                 'collision': False},  # Simplified
                actions[i],
                {'forward_velocity': prev_states[i][2]}
            )

            # Check if episode should terminate
            done = (self.episode_lengths[i] >= self.max_episode_length or
                   abs(new_state[2]) > 1.0)  # Fall down check

            rewards.append(reward)
            dones.append(done)

            # Update episode tracking
            self.episode_lengths[i] += 1
            self.episode_rewards[i] += reward

            # Reset environment if done
            if done:
                self.reset_environment(i)

        # Store transitions in agent's memory
        for i in range(self.num_envs):
            self.agent.store_transition(
                states[i], actions[i], rewards[i], log_probs[i], values[i], dones[i]
            )

        # Update agent if enough samples collected
        if len(self.agent.states) >= self.num_envs * 10:  # Update every 10 episodes
            self.agent.update()

    def train(self, num_episodes=10000):
        """Train the RL agent"""
        for episode in range(num_episodes):
            self.train_step()

            # Print progress every 100 episodes
            if episode % 100 == 0:
                avg_reward = np.mean(self.episode_rewards)
                print(f"Episode {episode}, Average Reward: {avg_reward:.2f}")

                # Reset episode rewards
                self.episode_rewards.fill(0)
```

## 2.6 Sim-to-Real Transfer

### 2.6.1 Domain Randomization

Domain randomization is a key technique for improving sim-to-real transfer by training agents in varied simulation conditions.

```python
# Example domain randomization for sim-to-real transfer
class DomainRandomization:
    def __init__(self):
        self.param_ranges = {
            'mass_multiplier': (0.8, 1.2),  # 80% to 120% of original mass
            'friction_coefficient': (0.4, 0.8),  # Friction range
            'restitution': (0.0, 0.2),  # Bounciness range
            'gravity_scale': (0.9, 1.1),  # Gravity variation
            'motor_strength': (0.8, 1.2),  # Motor strength variation
            'sensor_noise': (0.0, 0.01),  # Sensor noise level
        }

    def randomize_environment(self, robot_prim_path):
        """Randomize physical parameters of the robot"""
        import omni
        from pxr import Gf, UsdPhysics, UsdShade

        # Randomize mass
        mass_mult = np.random.uniform(*self.param_ranges['mass_multiplier'])
        mass_api = UsdPhysics.MassAPI.Apply(get_prim_at_path(robot_prim_path))
        if mass_api:
            original_mass = mass_api.GetMassAttr().Get()
            randomized_mass = original_mass * mass_mult
            mass_api.GetMassAttr().Set(randomized_mass)

        # Randomize friction
        friction_mult = np.random.uniform(*self.param_ranges['friction_coefficient'])
        friction_api = UsdPhysics.FrictionAPI.Apply(get_prim_at_path(robot_prim_path))
        if friction_api:
            friction_api.GetStaticFrictionAttr().Set(friction_mult)
            friction_api.GetDynamicFrictionAttr().Set(friction_mult)

        # Randomize restitution
        restitution = np.random.uniform(*self.param_ranges['restitution'])
        # Apply restitution through material properties

        # Randomize other parameters as needed
        return {
            'mass_multiplier': mass_mult,
            'friction_coefficient': friction_mult,
            'restitution': restitution
        }

    def randomize_sensors(self, sensor_params):
        """Randomize sensor parameters"""
        randomized_params = sensor_params.copy()

        # Add noise to sensor readings
        noise_level = np.random.uniform(*self.param_ranges['sensor_noise'])
        randomized_params['noise_level'] = noise_level

        return randomized_params

    def randomize_dynamics(self, robot):
        """Randomize robot dynamics parameters"""
        # Randomize joint parameters
        joint_params = {
            'damping_range': (0.05, 0.2),
            'friction_range': (0.01, 0.05),
            'stiffness_range': (1000, 5000)
        }

        # Apply randomization to joints
        for joint_name in robot.get_articulation_joint_names():
            joint_path = f"{robot.prim_path}/{joint_name}"
            joint_prim = get_prim_at_path(joint_path)

            if joint_prim:
                # Randomize joint damping
                damping = np.random.uniform(*joint_params['damping_range'])
                # Apply damping randomization

                # Randomize joint friction
                friction = np.random.uniform(*joint_params['friction_range'])
                # Apply friction randomization

        return joint_params
```

### 2.6.2 Policy Transfer Techniques

Effective sim-to-real transfer requires careful consideration of the differences between simulation and reality.

```python
# Example sim-to-real transfer techniques
class SimToRealTransfer:
    def __init__(self):
        self.domain_randomization = DomainRandomization()
        self.transfer_metrics = {
            'sim_performance': 0.0,
            'real_performance': 0.0,
            'transfer_gap': 0.0
        }

    def adapt_policy(self, trained_policy, real_robot_params):
        """Adapt simulation-trained policy for real robot"""
        # Get simulation parameters
        sim_params = self.get_simulation_parameters()

        # Calculate parameter differences
        param_ratios = {}
        for param_name in sim_params:
            if param_name in real_robot_params:
                param_ratios[param_name] = (
                    real_robot_params[param_name] / sim_params[param_name]
                )

        # Adapt policy based on parameter differences
        adapted_policy = self._scale_policy_actions(trained_policy, param_ratios)

        return adapted_policy

    def get_simulation_parameters(self):
        """Get current simulation parameters"""
        return {
            'mass': 30.0,  # kg
            'height': 1.5,  # meters
            'max_velocity': 2.0,  # m/s
            'max_torque': 100.0,  # Nm
            'sensor_delay': 0.0,  # seconds
            'actuator_response_time': 0.001  # seconds
        }

    def _scale_policy_actions(self, policy, param_ratios):
        """Scale policy actions based on parameter differences"""
        # Create adapted policy with scaled actions
        adapted_policy = policy.copy()

        # Scale actions based on torque differences
        if 'max_torque' in param_ratios:
            torque_ratio = param_ratios['max_torque']
            # Scale action outputs by torque ratio
            adapted_policy['action_scaling'] = torque_ratio

        # Scale velocity commands based on velocity differences
        if 'max_velocity' in param_ratios:
            velocity_ratio = param_ratios['max_velocity']
            adapted_policy['velocity_scaling'] = velocity_ratio

        return adapted_policy

    def validate_transfer(self, policy, real_env):
        """Validate policy performance in real environment"""
        # Test policy on real robot
        real_performance = self._evaluate_policy(policy, real_env)

        # Compare with simulation performance
        sim_performance = self._evaluate_policy(policy, self._get_sim_env())

        # Calculate transfer gap
        transfer_gap = sim_performance - real_performance

        self.transfer_metrics.update({
            'sim_performance': sim_performance,
            'real_performance': real_performance,
            'transfer_gap': transfer_gap
        })

        return {
            'success': transfer_gap < 0.2,  # Acceptable gap threshold
            'metrics': self.transfer_metrics
        }

    def _evaluate_policy(self, policy, env):
        """Evaluate policy performance in environment"""
        total_reward = 0
        episode_length = 0

        # Run evaluation episode
        state = env.reset()
        done = False

        while not done and episode_length < 1000:  # Max 1000 steps
            action = policy.get_action(state)
            state, reward, done, info = env.step(action)
            total_reward += reward
            episode_length += 1

        return total_reward / episode_length if episode_length > 0 else 0.0

    def _get_sim_env(self):
        """Get simulation environment for comparison"""
        # Return simulation environment instance
        pass
```

## 2.7 Integration of Perception and RL

### 2.7.1 Perception-Guided RL Pipeline

The integration of perception systems with RL creates powerful autonomous agents capable of adapting to dynamic environments.

```python
# Example perception-guided RL system
class PerceptionGuidedRL:
    def __init__(self, state_dim, action_dim):
        # Initialize perception pipeline
        self.perception_pipeline = SensorFusionPipeline()

        # Initialize RL agent
        self.rl_agent = HumanoidPPOAgent(state_dim, action_dim)

        # Initialize reward function
        self.reward_function = HumanoidRewardFunction()

        # State representation module
        self.state_encoder = self._build_state_encoder(state_dim)

    def _build_state_encoder(self, state_dim):
        """Build neural network to encode perception data into RL state"""
        import torch.nn as nn

        return nn.Sequential(
            nn.Linear(208, 512),  # Input: fused features from vision(128) + lidar(64) + depth(16)
            nn.ReLU(),
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.Linear(256, state_dim),
            nn.Tanh()
        )

    def process_perception_to_state(self, perception_data):
        """Convert perception data to RL state representation"""
        # Fuse perception data from multiple sensors
        fused_features = perception_data['features']

        # Encode features into state representation
        state_tensor = torch.FloatTensor(fused_features).unsqueeze(0)
        encoded_state = self.state_encoder(state_tensor)

        return encoded_state.squeeze(0).detach().numpy()

    def get_action(self, perception_data):
        """Get action from perception data"""
        # Convert perception to state
        state = self.process_perception_to_state(perception_data)

        # Get action from RL agent
        action, log_prob, value = self.rl_agent.select_action(state)

        return action, state

    def train_step(self, perception_data, action, reward, next_perception_data, done):
        """Perform one training step"""
        # Convert perception data to states
        state = self.process_perception_to_state(perception_data)
        next_state = self.process_perception_to_state(next_perception_data)

        # Store transition in replay buffer
        self.rl_agent.store_transition(
            state, action, reward, 0.0, 0.0, done  # Simplified
        )

        # Update agent if enough samples
        if len(self.rl_agent.states) >= 32:  # Batch size
            self.rl_agent.update()

    def run_perception_guided_control(self, robot_interface):
        """Run perception-guided control loop"""
        while True:
            # Get perception data from robot
            vision_data = robot_interface.get_vision_data()
            lidar_data = robot_interface.get_lidar_data()
            depth_data = robot_interface.get_depth_data()

            # Fuse perception data
            fused_data = self.perception_pipeline.fuse_perception_data(
                vision_data, lidar_data, depth_data
            )

            # Get action from RL agent
            action, state = self.get_action(fused_data)

            # Execute action on robot
            robot_interface.execute_action(action)

            # Get reward based on action and state
            reward = self.reward_function.calculate_reward(
                {'forward_velocity': state[2]},  # Simplified
                action,
                {}
            )

            # Store for training (in real-time operation, this might be done offline)
            # self.train_step(prev_fused_data, action, reward, fused_data, done)
```

## 2.8 Hands-On Examples

### 2.8.1 Example 1: Python Perception Pipeline with ROS 2

This example demonstrates subscribing to perception topics and preprocessing data:

```python
#!/usr/bin/env python3
"""
Example perception pipeline that subscribes to ROS 2 topics
and preprocesses data for RL agents.
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from std_msgs.msg import Float32MultiArray
from cv_bridge import CvBridge
import numpy as np
import cv2
import torch

class PerceptionPreprocessor(Node):
    def __init__(self):
        super().__init__('perception_preprocessor')

        # Initialize CV bridge
        self.bridge = CvBridge()

        # Create subscribers
        self.image_sub = self.create_subscription(
            Image,
            '/camera/rgb/image_raw',
            self.image_callback,
            10
        )

        self.scan_sub = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            10
        )

        # Create publisher for preprocessed features
        self.features_pub = self.create_publisher(
            Float32MultiArray,
            '/perception/features',
            10
        )

        # Storage for sensor data
        self.latest_image = None
        self.latest_scan = None

        # Timer for processing
        self.timer = self.create_timer(0.1, self.process_data)  # 10 Hz

        self.get_logger().info('Perception preprocessor initialized')

    def image_callback(self, msg):
        """Process incoming image messages"""
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")

            # Preprocess image: resize and normalize
            resized = cv2.resize(cv_image, (224, 224))
            normalized = resized.astype(np.float32) / 255.0

            # Convert to tensor format
            tensor_image = torch.from_numpy(normalized).permute(2, 0, 1).float()

            self.latest_image = tensor_image

        except Exception as e:
            self.get_logger().error(f'Image processing error: {e}')

    def scan_callback(self, msg):
        """Process incoming laser scan messages"""
        try:
            # Convert scan ranges to numpy array
            ranges = np.array(msg.ranges)

            # Filter invalid ranges
            ranges = np.where((ranges >= msg.range_min) &
                             (ranges <= msg.range_max), ranges, 0.0)

            # Downsample for efficiency (take every 10th point)
            downsampled = ranges[::10]

            # Pad or truncate to fixed size
            if len(downsampled) < 36:  # 360 degrees / 10
                downsampled = np.pad(downsampled, (0, 36 - len(downsampled)), 'constant')
            else:
                downsampled = downsampled[:36]

            self.latest_scan = downsampled

        except Exception as e:
            self.get_logger().error(f'Scan processing error: {e}')

    def process_data(self):
        """Process combined sensor data"""
        if self.latest_image is not None and self.latest_scan is not None:
            try:
                # Extract features from image (simplified: just flatten central region)
                central_region = self.latest_image[:, 100:124, 100:124]
                image_features = central_region.flatten()[:128]  # Take first 128 values

                # Combine with scan features
                combined_features = np.concatenate([image_features.numpy(), self.latest_scan])

                # Ensure fixed size
                if len(combined_features) < 256:
                    combined_features = np.pad(combined_features,
                                            (0, 256 - len(combined_features)), 'constant')
                else:
                    combined_features = combined_features[:256]

                # Publish features
                features_msg = Float32MultiArray()
                features_msg.data = combined_features.tolist()
                self.features_pub.publish(features_msg)

                # Clear processed data
                self.latest_image = None
                self.latest_scan = None

            except Exception as e:
                self.get_logger().error(f'Data processing error: {e}')

def main(args=None):
    rclpy.init(args=args)

    preprocessor = PerceptionPreprocessor()

    try:
        rclpy.spin(preprocessor)
    except KeyboardInterrupt:
        pass
    finally:
        preprocessor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### 2.8.2 Example 2: RL Training in Simulation

This example demonstrates training an RL agent in simulation:

```python
#!/usr/bin/env python3
"""
Example RL training in simulation environment
"""
import gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from collections import deque
import random

class SimpleHumanoidEnv(gym.Env):
    """Simple humanoid environment for demonstration"""
    def __init__(self):
        super(SimpleHumanoidEnv, self).__init__()

        # Define action and observation spaces
        self.action_space = gym.spaces.Box(
            low=-1.0, high=1.0, shape=(6,), dtype=np.float32
        )
        self.observation_space = gym.spaces.Box(
            low=-np.inf, high=np.inf, shape=(24,), dtype=np.float32
        )

        # Environment parameters
        self.max_steps = 1000
        self.current_step = 0
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])

    def reset(self):
        """Reset environment to initial state"""
        self.current_step = 0
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])

        # Return initial observation
        return self._get_observation()

    def step(self, action):
        """Execute one step in the environment"""
        # Update position based on action
        self.velocity += action[:2] * 0.1  # First 2 actions for movement
        self.position += self.velocity * 0.1

        # Calculate reward
        reward = self._calculate_reward()

        # Check termination
        self.current_step += 1
        done = self.current_step >= self.max_steps

        # Return step information
        return self._get_observation(), reward, done, {}

    def _get_observation(self):
        """Get current observation"""
        # Combine position, velocity, and some history
        obs = np.concatenate([
            self.position,
            self.velocity,
            np.sin(self.current_step * 0.01),  # Time-based feature
            np.cos(self.current_step * 0.01),
            np.random.normal(0, 0.1, 18)  # Additional random features
        ])
        return obs

    def _calculate_reward(self):
        """Calculate reward based on current state"""
        # Encourage forward movement
        forward_reward = self.velocity[0] * 0.1

        # Penalize excessive movement
        movement_penalty = -np.sum(np.abs(self.velocity)) * 0.01

        # Encourage staying upright (simplified)
        stability_reward = 0.1

        total_reward = forward_reward + movement_penalty + stability_reward
        return max(total_reward, -1.0)  # Clamp reward

class PolicyNetwork(nn.Module):
    """Simple policy network for RL"""
    def __init__(self, state_dim, action_dim):
        super(PolicyNetwork, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, action_dim),
            nn.Tanh()
        )

    def forward(self, state):
        return self.network(state)

class ValueNetwork(nn.Module):
    """Value network for advantage calculation"""
    def __init__(self, state_dim):
        super(ValueNetwork, self).__init__()

        self.network = nn.Sequential(
            nn.Linear(state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )

    def forward(self, state):
        return self.network(state)

class PPOAgent:
    """PPO RL agent implementation"""
    def __init__(self, state_dim, action_dim, lr=3e-4, gamma=0.99, epsilon=0.2):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize networks
        self.policy_net = PolicyNetwork(state_dim, action_dim).to(self.device)
        self.value_net = ValueNetwork(state_dim).to(self.device)

        # Initialize optimizers
        self.policy_optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.value_optimizer = optim.Adam(self.value_net.parameters(), lr=lr)

        # Hyperparameters
        self.gamma = gamma
        self.epsilon = epsilon

        # Storage for training
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.next_states = []
        self.dones = []

    def select_action(self, state):
        """Select action using current policy"""
        state_tensor = torch.FloatTensor(state).to(self.device)

        # Get action from policy
        action_mean = self.policy_net(state_tensor)

        # Add noise for exploration
        action_std = torch.ones_like(action_mean) * 0.1
        dist = torch.distributions.Normal(action_mean, action_std)
        action = dist.sample()

        # Calculate log probability
        log_prob = dist.log_prob(action).sum(dim=-1)
        value = self.value_net(state_tensor)

        return (action.cpu().numpy(),
                log_prob.cpu().item(),
                value.cpu().item())

    def store_transition(self, log_prob, value, reward, done):
        """Store transition for training"""
        self.log_probs.append(log_prob)
        self.values.append(value)
        self.rewards.append(reward)
        self.dones.append(done)

    def update(self):
        """Update policy using PPO"""
        if len(self.rewards) == 0:
            return

        # Convert to tensors
        rewards = torch.FloatTensor(self.rewards).to(self.device)
        values = torch.FloatTensor(self.values).to(self.device)
        log_probs = torch.FloatTensor(self.log_probs).to(self.device)

        # Compute returns and advantages
        returns = []
        R = 0
        for reward, done in zip(reversed(rewards), reversed(self.dones)):
            if done:
                R = 0
            R = reward + self.gamma * R
            returns.insert(0, R)

        returns = torch.FloatTensor(returns).to(self.device)
        advantages = returns - values

        # Normalize advantages
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

        # Compute policy loss
        ratio = torch.exp(log_probs - log_probs.detach())
        surr1 = ratio * advantages
        surr2 = torch.clamp(ratio, 1 - self.epsilon, 1 + self.epsilon) * advantages
        policy_loss = -torch.min(surr1, surr2).mean()

        # Compute value loss
        value_loss = nn.MSELoss()(values, returns)

        # Update networks
        self.policy_optimizer.zero_grad()
        policy_loss.backward()
        self.policy_optimizer.step()

        self.value_optimizer.zero_grad()
        value_loss.backward()
        self.value_optimizer.step()

        # Clear storage
        self.log_probs = []
        self.values = []
        self.rewards = []
        self.dones = []

def train_rl_agent():
    """Train RL agent in simulation"""
    env = SimpleHumanoidEnv()
    agent = PPOAgent(
        state_dim=env.observation_space.shape[0],
        action_dim=env.action_space.shape[0]
    )

    num_episodes = 1000
    max_steps = 1000

    for episode in range(num_episodes):
        state = env.reset()
        episode_reward = 0

        for step in range(max_steps):
            # Select action
            action, log_prob, value = agent.select_action(state)

            # Execute action
            next_state, reward, done, _ = env.step(action)
            episode_reward += reward

            # Store transition
            agent.store_transition(log_prob, value, reward, done)

            # Update agent every 32 steps
            if len(agent.rewards) >= 32:
                agent.update()

            if done:
                break

            state = next_state

        # Update at end of episode
        agent.update()

        if episode % 100 == 0:
            print(f"Episode {episode}, Average Reward: {episode_reward:.2f}")

if __name__ == "__main__":
    train_rl_agent()
```

### 2.8.3 Example 3: Sim-to-Real Transfer Workflow

This example demonstrates the workflow for transferring trained policies to real robots:

```python
#!/usr/bin/env python3
"""
Example sim-to-real transfer workflow
"""
import torch
import numpy as np
import yaml
from pathlib import Path

class SimToRealTransferWorkflow:
    def __init__(self, config_path):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)

        self.sim_model_path = self.config['sim_model_path']
        self.real_robot_params = self.config['real_robot_params']
        self.transfer_params = self.config['transfer_params']

    def load_sim_model(self):
        """Load trained simulation model"""
        # Load the trained model from simulation
        model_path = Path(self.sim_model_path)
        if model_path.exists():
            model = torch.load(model_path)
            print(f"Loaded simulation model from {model_path}")
            return model
        else:
            raise FileNotFoundError(f"Simulation model not found: {model_path}")

    def calibrate_real_robot(self):
        """Calibrate real robot parameters"""
        # In practice, this would involve actual calibration procedures
        real_params = {
            'mass': self.real_robot_params.get('mass', 30.0),
            'com_offset': self.real_robot_params.get('com_offset', [0.0, 0.0, 0.0]),
            'joint_friction': self.real_robot_params.get('joint_friction', [0.1] * 12),
            'sensor_bias': self.real_robot_params.get('sensor_bias', [0.0] * 6),
            'actuator_delay': self.real_robot_params.get('actuator_delay', 0.02)
        }

        print("Real robot calibrated with parameters:")
        for param, value in real_params.items():
            print(f"  {param}: {value}")

        return real_params

    def adapt_policy(self, sim_model, real_params):
        """Adapt simulation policy for real robot"""
        # Calculate parameter ratios between sim and real
        sim_params = {
            'mass': 30.0,  # Default simulation mass
            'com_offset': [0.0, 0.0, 0.0],
            'joint_friction': [0.05] * 12,  # Default simulation friction
            'sensor_bias': [0.0] * 6,
            'actuator_delay': 0.001  # Default simulation delay
        }

        # Calculate adaptation factors
        adaptation_factors = {}
        for param in real_params:
            if param in sim_params:
                adaptation_factors[param] = (
                    real_params[param] / sim_params[param] if sim_params[param] != 0 else 1.0
                )

        print("Adaptation factors calculated:")
        for param, factor in adaptation_factors.items():
            print(f"  {param}: {factor:.3f}")

        # Create adapted model (in practice, this would involve more complex adaptation)
        adapted_model = sim_model  # Simplified - in reality, weights might need adjustment

        # Store adaptation factors for action scaling
        adapted_model['adaptation_factors'] = adaptation_factors

        return adapted_model

    def validate_transfer(self, adapted_model, real_robot_interface):
        """Validate the transferred policy on real robot"""
        # Test the adapted policy on the real robot
        test_episodes = self.transfer_params.get('test_episodes', 10)
        success_threshold = self.transfer_params.get('success_threshold', 0.7)

        successful_episodes = 0
        total_reward = 0

        for episode in range(test_episodes):
            # Reset robot to initial state
            real_robot_interface.reset()

            episode_reward = 0
            done = False
            step_count = 0
            max_steps = 1000

            while not done and step_count < max_steps:
                # Get observation from real robot
                observation = real_robot_interface.get_observation()

                # Get action from adapted policy
                action = self._get_adapted_action(adapted_model, observation)

                # Execute action on real robot
                real_robot_interface.execute_action(action)

                # Get reward and check termination
                reward = real_robot_interface.get_reward()
                done = real_robot_interface.is_terminal()

                episode_reward += reward
                step_count += 1

            total_reward += episode_reward

            # Check if episode was successful
            if episode_reward > success_threshold * max_steps:
                successful_episodes += 1

            print(f"Test episode {episode + 1}: Reward = {episode_reward:.2f}, "
                  f"Success = {'Yes' if episode_reward > success_threshold * max_steps else 'No'}")

        success_rate = successful_episodes / test_episodes
        avg_reward = total_reward / test_episodes

        print(f"\nTransfer validation results:")
        print(f"  Success rate: {success_rate:.2f}")
        print(f"  Average reward: {avg_reward:.2f}")
        print(f"  Successful episodes: {successful_episodes}/{test_episodes}")

        return {
            'success_rate': success_rate,
            'avg_reward': avg_reward,
            'successful_episodes': successful_episodes,
            'total_episodes': test_episodes
        }

    def _get_adapted_action(self, adapted_model, observation):
        """Get action from adapted model with parameter scaling"""
        # In a real implementation, this would involve running the neural network
        # and applying adaptation factors to the output

        # For demonstration, return a simple action
        base_action = np.random.randn(12)  # 12 joint actions

        # Apply adaptation if available
        if 'adaptation_factors' in adapted_model:
            friction_factor = adapted_model['adaptation_factors'].get('joint_friction', 1.0)
            # Scale action based on friction differences
            adapted_action = base_action * friction_factor
        else:
            adapted_action = base_action

        return np.clip(adapted_action, -1.0, 1.0)  # Clamp to valid range

    def execute_transfer(self):
        """Execute complete sim-to-real transfer workflow"""
        print("Starting sim-to-real transfer workflow...")

        # Step 1: Load simulation model
        print("\n1. Loading simulation model...")
        sim_model = self.load_sim_model()

        # Step 2: Calibrate real robot
        print("\n2. Calibrating real robot...")
        real_params = self.calibrate_real_robot()

        # Step 3: Adapt policy
        print("\n3. Adapting policy for real robot...")
        adapted_model = self.adapt_policy(sim_model, real_params)

        # Step 4: Validate transfer (this would connect to real robot)
        print("\n4. Validating transfer on real robot...")
        # Note: In practice, you would connect to actual robot interface
        # For this example, we'll simulate the validation
        validation_results = {
            'success_rate': 0.85,
            'avg_reward': 0.72,
            'successful_episodes': 17,
            'total_episodes': 20
        }

        print(f"\n5. Transfer completed successfully!")
        print(f"   Success rate: {validation_results['success_rate']:.2f}")
        print(f"   Average reward: {validation_results['avg_reward']:.2f}")

        return validation_results

# Example configuration file content (to be saved as transfer_config.yaml):
config_content = """
sim_model_path: "trained_models/humanoid_sim_model.pt"
real_robot_params:
  mass: 32.5
  com_offset: [0.01, -0.02, 0.0]
  joint_friction: [0.12, 0.15, 0.1, 0.13, 0.11, 0.14, 0.12, 0.13, 0.11, 0.12, 0.14, 0.13]
  sensor_bias: [0.001, -0.002, 0.0015, -0.001, 0.002, -0.0015]
  actuator_delay: 0.025
transfer_params:
  test_episodes: 20
  success_threshold: 0.6
  adaptation_method: "parameter_scaling"
"""

if __name__ == "__main__":
    # Create config file
    with open("transfer_config.yaml", "w") as f:
        f.write(config_content)

    # Execute transfer workflow
    workflow = SimToRealTransferWorkflow("transfer_config.yaml")
    results = workflow.execute_transfer()

    print(f"\nFinal transfer results: {results}")
```

## 2.9 Data Flow Diagrams

### 2.9.1 Perception → RL Agent → Robot Action Loop

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Robot         │    │   Perception     │    │   RL Agent      │
│   Sensors       │───►│   Pipeline       │───►│   (Policy)      │
│                 │    │                  │    │                 │
│ - Cameras       │    │ - Data Fusion    │    │ - State         │
│ - LiDAR         │    │ - Feature        │    │   Processing    │
│ - IMU           │    │   Extraction     │    │ - Action        │
│ - Joint Encoders│    │ - Preprocessing  │    │   Selection     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Sensor    │    │   Processed      │    │   Selected      │
│   Data          │    │   Features       │    │   Action        │
│                 │    │                  │    │                 │
│ - Image Frames  │    │ - State Vector   │    │ - Joint         │
│ - Point Clouds  │    │ - Normalized     │    │   Commands      │
│ - IMU Readings  │    │   Features       │    │ - Velocity      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         └───────────────────────┴───────────────────────┘
                            Feedback Loop
```

### 2.9.2 Sensor Fusion Pipeline for Humanoid Robots

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vision        │    │   Data           │    │   Fused         │
│   Sensors       │───►│   Preprocessing  │───►│   Perception    │
│                 │    │                  │    │   Output        │
│ - RGB Camera    │    │ - Normalization  │    │                 │
│ - Depth Camera  │    │ - Filtering      │    │ - State Vector  │
│ - Stereo Cam    │    │ - Alignment      │    │ - Confidence    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Range         │    │   Temporal       │    │   Integrated    │
│   Sensors       │───►│   Integration    │───►│   Features      │
│                 │    │                  │    │                 │
│ - LiDAR         │    │ - Buffering      │    │ - 3D Scene      │
│ - Ultrasonic    │    │ - Synchronization│    │ - Object        │
│ - Time-of-Flight│    │ - Interpolation  │    │   Detection     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Inertial      │    │   Feature        │    │   Multi-modal   │
│   Sensors       │───►│   Weighting      │───►│   Representation│
│                 │    │                  │    │                 │
│ - IMU           │    │ - Confidence     │    │ - Rich State    │
│ - Gyroscope     │    │   Scoring        │    │   for RL        │
│ - Accelerometer │    │ - Uncertainty    │    │ - Action        │
└─────────────────┘    │   Modeling       │    │   Guidance      │
                       └──────────────────┘    └─────────────────┘
```

### 2.9.3 Sim-to-Real Transfer Workflow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Simulation    │    │   Domain         │    │   Policy        │
│   Training      │───►│   Randomization  │───►│   Adaptation    │
│                 │    │                  │    │                 │
│ - Isaac Sim     │    │ - Parameter      │    │ - Parameter     │
│ - High Fidelity │    │   Variation      │    │   Scaling       │
│ - Physics Acc.  │    │ - Noise Injection│    │ - Action        │
└─────────────────┘    └──────────────────┘    │   Adjustment    │
         │                       │              └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Trained       │    │   Real Robot     │    │   Transferred   │
│   Policy        │───►│   Calibration    │───►│   Policy        │
│                 │    │                  │    │                 │
│ - Neural Net    │    │ - Mass, Friction │    │ - Adapted       │
│ - Parameters    │    │ - Sensor Bias    │    │   Weights       │
│ - Checkpoints   │    │ - Actuator Delay │    │ - Calibrated    │
└─────────────────┘    └──────────────────┘    │   Actions       │
         │                       │              └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Validation    │    │   Performance    │    │   Deployment    │
│   in Sim        │───►│   Comparison     │───►│   Ready         │
│                 │    │                  │    │                 │
│ - High Score    │    │ - Sim vs Real    │    │ - Operational   │
│ - Converged     │    │ - Transfer Gap   │    │ - Safe          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## 2.10 Tables for Clarity

### 2.10.1 Common Perception Sensors and ROS 2 Topics

| Sensor Type | ROS 2 Topic | Message Type | Purpose | Data Rate |
|-------------|-------------|--------------|---------|-----------|
| RGB Camera | /camera/rgb/image_raw | sensor_msgs/Image | Visual perception | 30 Hz |
| Depth Camera | /camera/depth/image_raw | sensor_msgs/Image | Depth estimation | 30 Hz |
| LiDAR | /scan | sensor_msgs/LaserScan | Range sensing | 10 Hz |
| 3D LiDAR | /point_cloud | sensor_msgs/PointCloud2 | 3D mapping | 10 Hz |
| IMU | /imu/data | sensor_msgs/Imu | Orientation/acceleration | 100 Hz |
| Joint State | /joint_states | sensor_msgs/JointState | Joint positions/velocities | 100 Hz |
| Odometry | /odom | nav_msgs/Odometry | Robot pose estimation | 50 Hz |
| Force/Torque | /ft_sensor | geometry_msgs/WrenchStamped | Contact sensing | 100 Hz |

### 2.10.2 RL Environment Parameters and Hyperparameters

| Parameter | Symbol | Default Value | Description |
|-----------|--------|---------------|-------------|
| Learning Rate | α | 3e-4 | Rate of parameter updates |
| Discount Factor | γ | 0.99 | Future reward importance |
| GAE Lambda | λ | 0.95 | Generalized Advantage Estimation |
| PPO Epsilon | ε | 0.2 | Clipping parameter |
| Batch Size | - | 64 | Training batch size |
| Replay Buffer Size | - | 1e6 | Experience storage capacity |
| Update Frequency | - | 2048 | Steps between updates |
| Max Gradient Norm | - | 0.5 | Gradient clipping threshold |
| Entropy Coefficient | β | 0.01 | Exploration encouragement |
| Value Loss Coefficient | - | 0.5 | Value function weighting |

### 2.10.3 Sim-to-Real Best Practices

| Practice | Description | Benefit |
|----------|-------------|---------|
| Domain Randomization | Randomize simulation parameters during training | Improves robustness to sim-real differences |
| System Identification | Identify real robot parameters accurately | Better model alignment |
| Gradual Transfer | Start with simple tasks, increase complexity | Safer deployment |
| Safety Constraints | Implement physical and software safety limits | Prevent robot damage |
| Sensor Calibration | Regularly calibrate all sensors | Accurate perception |
| Model Predictive Control | Use model-based approaches as backup | Enhanced safety |
| Human Supervision | Maintain human oversight during initial deployment | Quick intervention capability |
| Performance Monitoring | Continuously monitor robot performance | Early problem detection |

## 2.11 Exercises

### 2.11.1 Exercise 1: Building Perception Pipelines
Create a perception pipeline that fuses data from RGB camera, depth camera, and LiDAR sensors. Implement the pipeline to output a unified feature vector suitable for RL agents.

### 2.11.2 Exercise 2: Training RL Agents
Implement a simple RL agent (such as DQN or PPO) to learn basic navigation tasks in a simulated environment. Train the agent and evaluate its performance.

### 2.11.3 Exercise 3: Sensor Fusion Implementation
Develop a sensor fusion algorithm that combines multiple sensor modalities with appropriate weighting based on sensor confidence and environmental conditions.

### 2.11.4 Exercise 4: Reward Function Design
Design and implement reward functions for specific humanoid robot tasks such as walking, object manipulation, or obstacle avoidance.

### 2.11.5 Exercise 5: Sim-to-Real Transfer Analysis
Analyze the differences between simulation and reality for your specific robot platform and design appropriate adaptation strategies.

## 2.12 Mini-Project: Perception-Guided RL for Humanoid Robot

Implement a complete system where a humanoid robot uses perception-guided reinforcement learning to navigate an environment. The project should include:

1. A perception pipeline that processes visual, range, and inertial data
2. An RL agent trained in simulation to perform navigation tasks
3. A sim-to-real transfer mechanism to deploy the trained policy on a physical robot
4. Real-time performance monitoring and safety measures
5. Comprehensive evaluation of the system's performance in both simulation and reality
6. Analysis of the transfer gap and strategies for improvement

The project should demonstrate the complete pipeline from sensory input through perception processing to RL-based decision making and action execution, showcasing the integration of AI perception and reinforcement learning for humanoid robotics.

## 2.13 Summary

This chapter has covered the integration of AI perception systems with reinforcement learning for humanoid robots, highlighting the critical components needed for intelligent autonomous behavior. The combination of sophisticated perception pipelines with adaptive RL agents enables robots to learn complex behaviors through environmental interaction.

Key concepts covered include:
- Vision, LiDAR, and depth perception systems for humanoid robots
- Sensor fusion techniques for combining multiple modalities
- Data preprocessing and ROS 2 integration for real-time processing
- Reinforcement learning fundamentals with applications to humanoid control
- Simulation-based training with Isaac Sim integration
- Sim-to-real transfer techniques for deploying learned policies on physical robots
- Integration of perception and RL systems for closed-loop control

The examples and exercises provided demonstrate practical applications of these concepts, preparing you to develop sophisticated perception-guided RL systems for humanoid robot applications. The field continues to evolve rapidly, with advances in both perception and learning algorithms driving increasingly capable autonomous robotic systems.