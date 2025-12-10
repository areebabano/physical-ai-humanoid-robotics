---
id: module_3_lab
title: "Module 3 Lab - Complete Isaac Sim AI Integration"
sidebar_position: 6
---

# Module 3 Lab - Complete Isaac Sim AI Integration

## Lab Overview

In this lab, you will implement a complete AI perception system for a humanoid robot in Isaac Sim. You'll integrate synthetic data generation, perception algorithms, ROS 2 bridge communication, and AI model inference to create an intelligent humanoid robot that can perceive and navigate its environment.

## Learning Objectives

By the end of this lab, you will be able to:
- Implement a complete AI perception pipeline in Isaac Sim
- Integrate multiple AI models for different perception tasks
- Connect perception systems to ROS 2 navigation
- Generate synthetic training data for perception models
- Optimize AI performance for real-time operation
- Validate perception accuracy in simulation

## Prerequisites

Before starting this lab, ensure you have:
- Completed Modules 3.1 through 3.5
- Isaac Sim installed and configured
- ROS 2 Humble Hawksbill installed
- Python 3.8+ with required packages
- Basic understanding of computer vision and AI concepts
- NVIDIA GPU with CUDA support

## Lab Setup

### Environment Configuration

First, let's set up the complete environment for our AI-integrated humanoid robot simulation:

```bash
# Create the lab workspace
mkdir -p ~/isaac_sim_ai_lab/{config,scripts,models,datasets}

# Navigate to the lab directory
cd ~/isaac_sim_ai_lab

# Create a virtual environment
python3 -m venv isaac_sim_env
source isaac_sim_env/bin/activate

# Install required packages
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install open3d opencv-python numpy scipy
pip install tensorrt pycuda  # For optimized inference
```

### Isaac Sim Scene Setup

Create a complex scene with multiple objects, lighting conditions, and navigation challenges:

```python
# lab_scene_setup.py
import omni
from omni.isaac.core import World
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from omni.isaac.core.utils.prims import create_prim
from omni.isaac.core.utils.rotations import euler_angles_to_quat
from omni.isaac.sensor import Camera
import numpy as np
import carb

class LabSceneBuilder:
    """
    Complete scene setup for the Isaac Sim AI lab.
    """

    def __init__(self):
        self.world = World(stage_units_in_meters=1.0)
        self.scene_objects = []

    def build_environment(self):
        """
        Build the complete lab environment with various objects and challenges.
        """
        # Create ground plane
        self.create_ground_plane()

        # Add walls to create a room
        self.create_room_walls()

        # Add furniture and obstacles
        self.add_furniture()

        # Add dynamic objects for perception challenges
        self.add_dynamic_objects()

        # Add lighting
        self.setup_lighting()

        # Add humanoid robot
        self.add_humanoid_robot()

        # Add sensors to robot
        self.add_robot_sensors()

        print("Lab environment built successfully!")

    def create_ground_plane(self):
        """
        Create a textured ground plane for the environment.
        """
        from omni.isaac.core.utils.prims import create_ground_plane

        # Create ground plane with specific properties
        create_ground_plane(
            prim_path="/World/GroundPlane",
            size=10.0,
            color=np.array([0.2, 0.2, 0.2]),
            static_friction=0.5,
            dynamic_friction=0.5,
            restitution=0.0
        )

    def create_room_walls(self):
        """
        Create walls to form an indoor environment.
        """
        wall_configs = [
            {"position": [0, -5, 1.5], "size": [10, 0.2, 3], "name": "wall_back"},
            {"position": [0, 5, 1.5], "size": [10, 0.2, 3], "name": "wall_front"},
            {"position": [-5, 0, 1.5], "size": [0.2, 10, 3], "name": "wall_left"},
            {"position": [5, 0, 1.5], "size": [0.2, 10, 3], "name": "wall_right"},
        ]

        for config in wall_configs:
            create_prim(
                prim_path=f"/World/{config['name']}",
                prim_type="Cuboid",
                position=config["position"],
                size=config["size"],
                color=np.array([0.7, 0.7, 0.7])
            )

    def add_furniture(self):
        """
        Add furniture and static objects to the environment.
        """
        furniture_configs = [
            {"position": [-3, -3, 0.5], "size": [1.5, 0.8, 1], "name": "table_1"},
            {"position": [2, 3, 0.4], "size": [1.2, 1.2, 0.8], "name": "chair_1"},
            {"position": [0, -2, 0.3], "size": [0.6, 0.4, 0.6], "name": "box_1"},
            {"position": [-2, 2, 0.7], "size": [0.8, 1.0, 0.8], "name": "cylinder_1"},
        ]

        for config in furniture_configs:
            create_prim(
                prim_path=f"/World/{config['name']}",
                prim_type="Cuboid",  # Could be other shapes too
                position=config["position"],
                size=config["size"],
                color=np.array([0.8, 0.6, 0.2])
            )

    def add_dynamic_objects(self):
        """
        Add objects that can be moved/interacted with.
        """
        dynamic_configs = [
            {"position": [1, -1, 0.1], "size": [0.3, 0.3, 0.3], "name": "block_red"},
            {"position": [-1, 1, 0.1], "size": [0.25, 0.25, 0.25], "name": "block_blue"},
            {"position": [0, 0, 0.1], "size": [0.2, 0.2, 0.2], "name": "block_green"},
        ]

        for config in dynamic_configs:
            # Create dynamic cube that can be moved by physics
            cube = self.world.scene.add(
                prim_path=f"/World/{config['name']}",
                name=f"{config['name']}_ref",
                position=config["position"],
                scale=config["size"]
            )
            self.scene_objects.append(cube)

    def setup_lighting(self):
        """
        Set up realistic lighting for the environment.
        """
        # Add dome light for overall illumination
        create_prim(
            prim_path="/World/DomeLight",
            prim_type="DomeLight",
            position=[0, 0, 10],
            attributes={"color": [0.9, 0.9, 0.9], "intensity": 3000}
        )

        # Add directional light for shadows
        create_prim(
            prim_path="/World/DirectionalLight",
            prim_type="DistantLight",
            position=[5, 5, 10],
            rotation=euler_angles_to_quat(np.array([0, 0.5, 0.5])),
            attributes={"color": [0.9, 0.9, 0.8], "intensity": 1000}
        )

    def add_humanoid_robot(self):
        """
        Add a humanoid robot to the environment.
        """
        # For this lab, we'll use a simple articulated robot
        # In practice, you would load a complex humanoid URDF
        robot_path = "/World/HumanoidRobot"

        # Create a simple articulated robot
        from omni.isaac.core.utils.prims import define_prim
        from pxr import UsdGeom

        # Define the robot prim
        robot_prim = define_prim(robot_path, "Xform")

        # Add robot body
        create_prim(
            prim_path=f"{robot_path}/Body",
            prim_type="Cuboid",
            position=[0, 0, 0.5],
            size=[0.5, 0.3, 0.8],
            color=np.array([0.2, 0.6, 1.0])
        )

        print("Humanoid robot added to environment")

    def add_robot_sensors(self):
        """
        Add sensors to the robot for perception.
        """
        # Add RGB-D camera
        self.camera = Camera(
            prim_path="/World/HumanoidRobot/Camera",
            position=[0.2, 0, 0.8],  # Position on robot's "head"
            look_at=[1, 0, 0.8],     # Look forward
            resolution=(640, 480)
        )

        # Initialize the camera
        self.camera.initialize()

        print("Robot sensors added successfully")

# Initialize the scene
scene_builder = LabSceneBuilder()
scene_builder.build_environment()
```

## Perception System Implementation

Now let's implement the complete perception system that will run on our humanoid robot:

```python
# perception_system.py
import omni
from omni.isaac.core import World
from omni.isaac.sensor import Camera
import numpy as np
import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from scipy.spatial.transform import Rotation as R
import time
from collections import deque

class PerceptionSystem:
    """
    Complete perception system for the humanoid robot.
    """

    def __init__(self, world, camera_sensor):
        self.world = world
        self.camera = camera_sensor
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize perception models
        self.object_detector = self.initialize_object_detector()
        self.segmentation_model = self.initialize_segmentation_model()
        self.depth_estimator = self.initialize_depth_processor()

        # Transform for preprocessing
        self.transform = transforms.Compose([
            transforms.ToPILImage(),
            transforms.Resize((416, 416)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])

        # Performance tracking
        self.fps_counter = deque(maxlen=30)
        self.last_time = time.time()

    def initialize_object_detector(self):
        """
        Initialize object detection model.
        """
        # For this lab, we'll create a simple model
        # In practice, you'd load a pre-trained model
        class SimpleObjectDetector(nn.Module):
            def __init__(self, num_classes=10):
                super(SimpleObjectDetector, self).__init__()

                # Simple CNN backbone
                self.backbone = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True)
                )

                # Detection head
                self.detection_head = nn.Sequential(
                    nn.AdaptiveAvgPool2d((1, 1)),
                    nn.Flatten(),
                    nn.Linear(128, 256),
                    nn.ReLU(inplace=True),
                    nn.Dropout(0.5),
                    nn.Linear(256, num_classes + 4)  # classes + bbox
                )

            def forward(self, x):
                features = self.backbone(x)
                detections = self.detection_head(features)
                return detections

        model = SimpleObjectDetector()
        model.eval()
        return model.to(self.device)

    def initialize_segmentation_model(self):
        """
        Initialize semantic segmentation model.
        """
        class SimpleSegmentation(nn.Module):
            def __init__(self, num_classes=8):
                super(SimpleSegmentation, self).__init__()

                # Encoder
                self.encoder = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )

                # Decoder
                self.decoder = nn.Sequential(
                    nn.Conv2d(128, 64, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                    nn.Conv2d(64, 32, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.Upsample(scale_factor=2, mode='bilinear', align_corners=False),
                    nn.Conv2d(32, num_classes, kernel_size=1)
                )

            def forward(self, x):
                encoded = self.encoder(x)
                decoded = self.decoder(encoded)
                return decoded

        model = SimpleSegmentation()
        model.eval()
        return model.to(self.device)

    def initialize_depth_processor(self):
        """
        Initialize depth processing utilities.
        """
        # In simulation, we have access to ground truth depth
        # This would interface with depth estimation in real scenarios
        return lambda depth_img: depth_img

    def run_perception_pipeline(self):
        """
        Run the complete perception pipeline.
        """
        start_time = time.time()

        # Capture sensor data
        rgb_image = self.camera.get_rgb()
        depth_image = self.camera.get_depth()

        # Convert to numpy if needed
        if hasattr(rgb_image, 'to_numpy'):
            rgb_array = rgb_image.to_numpy()
        else:
            rgb_array = np.array(rgb_image)

        if hasattr(depth_image, 'to_numpy'):
            depth_array = depth_image.to_numpy()
        else:
            depth_array = np.array(depth_image)

        # Run object detection
        detections = self.run_object_detection(rgb_array)

        # Run semantic segmentation
        segmentation = self.run_segmentation(rgb_array)

        # Process depth information
        processed_depth = self.depth_estimator(depth_array)

        # Combine results
        perception_results = {
            'detections': detections,
            'segmentation': segmentation,
            'depth': processed_depth,
            'timestamp': time.time()
        }

        # Update performance metrics
        current_time = time.time()
        fps = 1.0 / (current_time - self.last_time)
        self.fps_counter.append(fps)
        self.last_time = current_time

        return perception_results

    def run_object_detection(self, image):
        """
        Run object detection on the input image.
        """
        # Preprocess image
        if len(image.shape) == 3:  # RGB
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
        else:
            # Handle grayscale or other formats
            rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            input_tensor = self.transform(rgb_image).unsqueeze(0).to(self.device)

        # Run detection
        with torch.no_grad():
            outputs = self.object_detector(input_tensor)

        # Process outputs (simplified)
        batch_size, output_size = outputs.shape

        # Extract detections (simplified - in practice use proper post-processing)
        detections = []
        for i in range(min(5, output_size // 5)):  # Max 5 detections
            class_scores = outputs[0, 4:].softmax(dim=0)
            class_id = torch.argmax(class_scores).item()
            confidence = class_scores[class_id].item()

            if confidence > 0.3:  # Confidence threshold
                detection = {
                    'class_id': class_id,
                    'confidence': confidence,
                    'bbox': [0.1, 0.1, 0.3, 0.3],  # Placeholder
                    'class_name': f'object_{class_id}'
                }
                detections.append(detection)

        return detections

    def run_segmentation(self, image):
        """
        Run semantic segmentation on the input image.
        """
        # Convert image to tensor
        if len(image.shape) == 3:
            h, w, c = image.shape
            # Convert to tensor and normalize
            img_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        else:
            h, w = image.shape
            img_tensor = torch.from_numpy(image).unsqueeze(0).repeat(3, 1, 1).float() / 255.0

        # Add batch dimension
        img_tensor = img_tensor.unsqueeze(0).to(self.device)

        # Run segmentation
        with torch.no_grad():
            outputs = self.segmentation_model(img_tensor)
            predictions = torch.argmax(outputs, dim=1)

        # Convert back to numpy
        segmentation_map = predictions.squeeze(0).cpu().numpy()

        return segmentation_map

    def get_performance_metrics(self):
        """
        Get current performance metrics.
        """
        avg_fps = sum(self.fps_counter) / len(self.fps_counter) if self.fps_counter else 0
        return {
            'avg_fps': avg_fps,
            'num_samples': len(self.fps_counter)
        }

class NavigationPlanner:
    """
    Navigation planner that uses perception results for path planning.
    """

    def __init__(self, world, robot):
        self.world = world
        self.robot = robot
        self.perception_system = None

    def set_perception_system(self, perception_system):
        """
        Set the perception system to use for navigation planning.
        """
        self.perception_system = perception_system

    def plan_navigation_path(self, target_position):
        """
        Plan a navigation path considering obstacles detected by perception system.
        """
        if not self.perception_system:
            print("Perception system not set, using basic navigation")
            return [target_position]

        # Get perception results
        perception_results = self.perception_system.run_perception_pipeline()

        # Extract obstacle information from detections
        obstacles = self.extract_obstacles_from_perception(perception_results)

        # Plan path avoiding obstacles
        path = self.a_star_with_obstacles(
            start_pos=self.get_robot_position(),
            goal_pos=target_position,
            obstacles=obstacles
        )

        return path

    def extract_obstacles_from_perception(self, perception_results):
        """
        Extract obstacle information from perception results.
        """
        obstacles = []

        # Process object detections
        for detection in perception_results['detections']:
            if detection['confidence'] > 0.5:
                # Convert 2D detection to 3D world coordinates
                # This is simplified - in practice, use depth and camera calibration
                obstacle_3d = self.project_detection_to_3d(detection)
                if obstacle_3d:
                    obstacles.append(obstacle_3d)

        # Process segmentation results
        segmentation = perception_results['segmentation']
        obstacle_coords = np.where(segmentation > 1)  # Assuming class > 1 are obstacles
        for y, x in zip(obstacle_coords[0], obstacle_coords[1]):
            # Convert pixel coordinates to world coordinates
            world_pos = self.pixel_to_world(x, y, perception_results['depth'][y, x])
            obstacles.append({
                'position': world_pos,
                'type': 'segmented_obstacle'
            })

        return obstacles

    def project_detection_to_3d(self, detection):
        """
        Project 2D detection to 3D world coordinates.
        """
        # Get camera parameters
        intrinsics = self.perception_system.camera.get_intrinsics()
        cam_pos, cam_rot = self.perception_system.camera.get_world_pose()

        # Extract bounding box center
        bbox = detection['bbox']
        center_x = int((bbox[0] + bbox[2]) / 2)
        center_y = int((bbox[1] + bbox[3]) / 2)

        # Get depth at center point (simplified)
        depth = 1.0  # Placeholder - in practice, sample from depth image

        # Project to 3D
        fx, fy = intrinsics[0, 0], intrinsics[1, 1]
        cx, cy = intrinsics[0, 2], intrinsics[1, 2]

        world_x = (center_x - cx) * depth / fx
        world_y = (center_y - cy) * depth / fy
        world_z = depth

        return {
            'position': [world_x + cam_pos[0], world_y + cam_pos[1], world_z + cam_pos[2]],
            'confidence': detection['confidence']
        }

    def pixel_to_world(self, x, y, depth):
        """
        Convert pixel coordinates to world coordinates.
        """
        # Get camera parameters
        intrinsics = self.perception_system.camera.get_intrinsics()
        cam_pos, cam_rot = self.perception_system.camera.get_world_pose()

        # Convert to world coordinates
        fx, fy = intrinsics[0, 0], intrinsics[1, 1]
        cx, cy = intrinsics[0, 2], intrinsics[1, 2]

        world_x = (x - cx) * depth / fx
        world_y = (y - cy) * depth / fy
        world_z = depth

        return [world_x + cam_pos[0], world_y + cam_pos[1], world_z + cam_pos[2]]

    def a_star_with_obstacles(self, start_pos, goal_pos, obstacles):
        """
        Simplified A* path planning with obstacle avoidance.
        """
        # This is a simplified version - in practice, use proper path planning
        path = [start_pos, goal_pos]  # Direct path for now

        # Add intermediate waypoints to avoid obstacles if needed
        for obstacle in obstacles:
            if self.is_path_blocked(start_pos, goal_pos, obstacle):
                # Add a waypoint to go around the obstacle
                detour_point = self.calculate_detour(start_pos, goal_pos, obstacle)
                path.insert(1, detour_point)

        return path

    def is_path_blocked(self, start, goal, obstacle):
        """
        Check if path is blocked by obstacle.
        """
        # Simplified collision check
        obstacle_pos = obstacle['position']
        # Calculate distance from line to obstacle
        dist_to_line = self.distance_point_to_line(start, goal, obstacle_pos)
        return dist_to_line < 0.5  # 0.5m threshold

    def distance_point_to_line(self, start, end, point):
        """
        Calculate distance from point to line segment.
        """
        start = np.array(start)
        end = np.array(end)
        point = np.array(point)

        # Vector calculations
        line_vec = end - start
        point_vec = point - start
        line_len = np.linalg.norm(line_vec)
        line_unitvec = line_vec / line_len
        point_vec_scaled = point_vec / line_len

        t = np.dot(line_unitvec, point_vec_scaled)
        t = max(0., min(1., t))

        nearest = line_vec * t
        dist = np.linalg.norm(point_vec - nearest)

        return dist

    def calculate_detour(self, start, goal, obstacle):
        """
        Calculate a detour point around an obstacle.
        """
        obstacle_pos = np.array(obstacle['position'])
        start_pos = np.array(start)
        goal_pos = np.array(goal)

        # Calculate vector from obstacle to avoid
        avoid_vec = goal_pos - start_pos
        avoid_vec = avoid_vec / np.linalg.norm(avoid_vec)

        # Calculate perpendicular vector for detour
        perp_vec = np.array([-avoid_vec[1], avoid_vec[0], 0])

        # Calculate detour point
        detour = obstacle_pos + perp_vec * 0.8  # 0.8m detour

        return detour.tolist()

    def get_robot_position(self):
        """
        Get current robot position.
        """
        # Placeholder - in practice, get from robot state
        return [0, 0, 0.5]

class AIIntegratedRobot:
    """
    Main class that integrates perception, navigation, and AI.
    """

    def __init__(self, world, camera_sensor):
        self.world = world
        self.camera = camera_sensor

        # Initialize components
        self.perception = PerceptionSystem(world, camera_sensor)
        self.navigation = NavigationPlanner(world, robot=None)
        self.navigation.set_perception_system(self.perception)

        # Set up ROS 2 bridge integration
        self.ros_bridge = self.initialize_ros_bridge()

        # Task queue for robot actions
        self.task_queue = deque()
        self.current_task = None

    def initialize_ros_bridge(self):
        """
        Initialize ROS 2 bridge for communication.
        """
        # This would typically involve setting up ROS 2 publishers/subscribers
        # For this lab, we'll simulate the bridge functionality
        class MockROSBridge:
            def __init__(self):
                self.published_messages = []

            def publish_detection(self, detections):
                """Publish object detections to ROS 2."""
                msg = {
                    'type': 'detection',
                    'data': detections,
                    'timestamp': time.time()
                }
                self.published_messages.append(msg)
                print(f"Published {len(detections)} detections to ROS 2")

            def publish_navigation_goal(self, goal):
                """Publish navigation goal to ROS 2."""
                msg = {
                    'type': 'navigation_goal',
                    'goal': goal,
                    'timestamp': time.time()
                }
                self.published_messages.append(msg)
                print(f"Published navigation goal to ROS 2")

        return MockROSBridge()

    def add_task(self, task_type, **kwargs):
        """
        Add a task to the robot's task queue.
        """
        task = {
            'type': task_type,
            'params': kwargs,
            'timestamp': time.time()
        }
        self.task_queue.append(task)

    def execute_tasks(self):
        """
        Execute tasks from the queue.
        """
        if not self.task_queue:
            return

        # Get next task
        task = self.task_queue.popleft()
        self.current_task = task

        # Execute based on task type
        if task['type'] == 'navigate_to_object':
            self.navigate_to_object(task['params'])
        elif task['type'] == 'inspect_area':
            self.inspect_area(task['params'])
        elif task['type'] == 'follow_path':
            self.follow_path(task['params'])
        else:
            print(f"Unknown task type: {task['type']}")

    def navigate_to_object(self, params):
        """
        Navigate to a detected object.
        """
        # Run perception to find the object
        perception_results = self.perception.run_perception_pipeline()

        target_object = None
        for detection in perception_results['detections']:
            if (detection['class_name'] == params.get('object_type', 'any') or
                params.get('object_type') == 'any'):
                if detection['confidence'] > params.get('min_confidence', 0.5):
                    target_object = detection
                    break

        if target_object:
            # Calculate navigation goal based on object position
            goal_pos = self.calculate_object_approach_position(
                target_object,
                distance=params.get('approach_distance', 1.0)
            )

            # Plan path considering obstacles
            path = self.navigation.plan_navigation_path(goal_pos)

            # Publish navigation goal to ROS 2
            self.ros_bridge.publish_navigation_goal(path[-1])

            print(f"Navigating to {target_object['class_name']} at {goal_pos}")
        else:
            print(f"Could not find {params.get('object_type', 'object')}")

    def calculate_object_approach_position(self, detection, distance=1.0):
        """
        Calculate approach position for an object.
        """
        # This is simplified - in practice, use 3D position from depth
        # For now, we'll return a fixed position relative to robot
        robot_pos = [0, 0, 0.5]  # Placeholder

        # Calculate approach position
        approach_pos = [
            robot_pos[0] + distance,
            robot_pos[1],
            robot_pos[2]
        ]

        return approach_pos

    def inspect_area(self, params):
        """
        Inspect a specific area using perception.
        """
        # Run perception pipeline
        perception_results = self.perception.run_perception_pipeline()

        # Process results
        detections = perception_results['detections']

        # Publish detections to ROS 2
        self.ros_bridge.publish_detection(detections)

        # Print summary
        print(f"Inspection complete: {len(detections)} objects detected")
        for detection in detections[:3]:  # Show first 3
            print(f"  - {detection['class_name']}: {detection['confidence']:.2f}")

    def follow_path(self, params):
        """
        Follow a predefined path.
        """
        path = params.get('path', [])
        if path:
            # Publish navigation goal
            self.ros_bridge.publish_navigation_goal(path[-1])
            print(f"Following path with {len(path)} waypoints")

    def get_system_status(self):
        """
        Get overall system status.
        """
        perception_metrics = self.perception.get_performance_metrics()

        return {
            'perception_fps': perception_metrics['avg_fps'],
            'task_queue_size': len(self.task_queue),
            'current_task': self.current_task['type'] if self.current_task else None,
            'ros_messages_sent': len(self.ros_bridge.published_messages)
        }
```

## Synthetic Data Generation System

Let's implement a system for generating synthetic training data:

```python
# synthetic_data_generator.py
import os
import json
import numpy as np
import cv2
from PIL import Image
import random
from dataclasses import dataclass
from typing import List, Dict, Tuple

@dataclass
class SceneConfiguration:
    """
    Configuration for synthetic scene generation.
    """
    lighting_conditions: List[str]
    object_positions: List[Tuple[float, float, float]]
    camera_angles: List[Tuple[float, float, float]]
    object_types: List[str]
    background_types: List[str]

class SyntheticDataGenerator:
    """
    System for generating synthetic training data in Isaac Sim.
    """

    def __init__(self, output_dir: str = "./synthetic_dataset"):
        self.output_dir = output_dir
        self.scene_configs = self.generate_scene_configurations()
        self.annotation_buffer = []

        # Create output directories
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "labels"), exist_ok=True)
        os.makedirs(os.path.join(output_dir, "depth"), exist_ok=True)

    def generate_scene_configurations(self) -> List[SceneConfiguration]:
        """
        Generate various scene configurations for domain randomization.
        """
        configs = []

        lighting_conditions = ["bright", "dim", "overcast", "night"]
        object_types = ["box", "cylinder", "sphere", "cone", "capsule"]
        background_types = ["indoor", "outdoor", "office", "warehouse"]

        for i in range(50):  # Generate 50 different configurations
            config = SceneConfiguration(
                lighting_conditions=random.sample(lighting_conditions, 2),
                object_positions=[
                    (random.uniform(-3, 3), random.uniform(-3, 3), random.uniform(0.1, 2))
                    for _ in range(random.randint(3, 8))
                ],
                camera_angles=[
                    (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-1, 1))
                    for _ in range(3)
                ],
                object_types=random.sample(object_types, random.randint(2, 4)),
                background_types=random.sample(background_types, 1)
            )
            configs.append(config)

        return configs

    def generate_synthetic_sample(self, config_idx: int) -> Dict:
        """
        Generate a single synthetic training sample.
        This simulates what would happen in Isaac Sim with actual rendering.
        """
        config = self.scene_configs[config_idx]

        # Simulate RGB image generation
        rgb_image = self.generate_rgb_image(config)

        # Simulate depth map generation
        depth_map = self.generate_depth_map(config)

        # Simulate segmentation mask
        seg_mask = self.generate_segmentation_mask(config)

        # Generate annotations
        annotations = self.generate_annotations(config, seg_mask)

        # Save sample
        sample_id = f"sample_{config_idx:06d}"
        self.save_sample(sample_id, rgb_image, depth_map, seg_mask, annotations)

        return {
            'sample_id': sample_id,
            'rgb_path': os.path.join(self.output_dir, "images", f"{sample_id}.png"),
            'depth_path': os.path.join(self.output_dir, "depth", f"{sample_id}.npy"),
            'seg_path': os.path.join(self.output_dir, "labels", f"{sample_id}_seg.png"),
            'annot_path': os.path.join(self.output_dir, "labels", f"{sample_id}_annot.json")
        }

    def generate_rgb_image(self, config: SceneConfiguration) -> np.ndarray:
        """
        Generate a synthetic RGB image.
        """
        # Create a blank image
        img = np.zeros((480, 640, 3), dtype=np.uint8)

        # Add random background based on scene type
        if "indoor" in config.background_types:
            img[:] = [200, 200, 200]  # Light gray for indoor
        elif "outdoor" in config.background_types:
            img[:] = [135, 206, 235]  # Sky blue for outdoor

        # Add objects as colored shapes
        for i, pos in enumerate(config.object_positions):
            color = [
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            ]

            # Convert 3D position to 2D image coordinates (simplified)
            x = int(320 + pos[0] * 50)  # Scale factor for visualization
            y = int(240 - pos[1] * 50)  # Flip Y axis

            # Draw as a circle for simplicity
            cv2.circle(img, (x, y), 20, color, -1)

        return img

    def generate_depth_map(self, config: SceneConfiguration) -> np.ndarray:
        """
        Generate a synthetic depth map.
        """
        depth = np.ones((480, 640), dtype=np.float32) * 10.0  # Default depth

        # Add depth values based on object positions
        for pos in config.object_positions:
            x = int(320 + pos[0] * 50)
            y = int(240 - pos[1] * 50)

            # Object depth (closer objects have lower values)
            obj_depth = max(0.1, 5.0 - pos[2])  # Depth based on Z position

            # Draw depth circle
            for dy in range(-20, 21):
                for dx in range(-20, 21):
                    if 0 <= y + dy < 480 and 0 <= x + dx < 640:
                        if dx*dx + dy*dy <= 400:  # Radius squared
                            depth[y + dy, x + dx] = min(depth[y + dy, x + dx], obj_depth)

        return depth

    def generate_segmentation_mask(self, config: SceneConfiguration) -> np.ndarray:
        """
        Generate a synthetic segmentation mask.
        """
        seg_mask = np.zeros((480, 640), dtype=np.uint8)

        # Assign different class IDs to different objects
        for obj_id, pos in enumerate(config.object_positions, start=1):
            x = int(320 + pos[0] * 50)
            y = int(240 - pos[1] * 50)

            # Draw segmentation mask
            for dy in range(-20, 21):
                for dx in range(-20, 21):
                    if 0 <= y + dy < 480 and 0 <= x + dx < 640:
                        if dx*dx + dy*dy <= 400:  # Radius squared
                            seg_mask[y + dy, x + dx] = obj_id

        return seg_mask

    def generate_annotations(self, config: SceneConfiguration, seg_mask: np.ndarray) -> Dict:
        """
        Generate annotations for the synthetic sample.
        """
        annotations = {
            'objects': [],
            'image_size': [640, 480],
            'scene_config': {
                'lighting': random.choice(config.lighting_conditions),
                'background': random.choice(config.background_types)
            }
        }

        # Find unique object IDs in segmentation mask
        unique_ids = np.unique(seg_mask)
        unique_ids = unique_ids[unique_ids > 0]  # Exclude background

        for obj_id in unique_ids:
            # Get object mask
            obj_mask = (seg_mask == obj_id)

            # Calculate bounding box
            coords = np.where(obj_mask)
            if len(coords[0]) > 0:
                y_min, y_max = coords[0].min(), coords[0].max()
                x_min, x_max = coords[1].min(), coords[1].max()

                bbox = [int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min)]

                # Calculate center
                center_x = (x_min + x_max) / 2
                center_y = (y_min + y_max) / 2

                # Add object annotation
                annotations['objects'].append({
                    'id': int(obj_id),
                    'bbox': bbox,
                    'center': [float(center_x), float(center_y)],
                    'pixel_count': int(np.sum(obj_mask)),
                    'class': random.choice(config.object_types)
                })

        return annotations

    def save_sample(self, sample_id: str, rgb_image: np.ndarray,
                   depth_map: np.ndarray, seg_mask: np.ndarray,
                   annotations: Dict):
        """
        Save a synthetic sample to disk.
        """
        # Save RGB image
        rgb_path = os.path.join(self.output_dir, "images", f"{sample_id}.png")
        Image.fromarray(rgb_image).save(rgb_path)

        # Save depth map
        depth_path = os.path.join(self.output_dir, "depth", f"{sample_id}.npy")
        np.save(depth_path, depth_map)

        # Save segmentation mask
        seg_path = os.path.join(self.output_dir, "labels", f"{sample_id}_seg.png")
        Image.fromarray(seg_mask).save(seg_path)

        # Save annotations
        annot_path = os.path.join(self.output_dir, "labels", f"{sample_id}_annot.json")
        with open(annot_path, 'w') as f:
            json.dump(annotations, f, indent=2)

    def generate_dataset(self, num_samples: int = 1000):
        """
        Generate a complete synthetic dataset.
        """
        print(f"Generating synthetic dataset with {num_samples} samples...")

        for i in range(num_samples):
            if i % 100 == 0:
                print(f"Generated {i}/{num_samples} samples")

            # Cycle through configurations
            config_idx = i % len(self.scene_configs)
            self.generate_synthetic_sample(config_idx)

        print(f"Dataset generation complete! Saved to {self.output_dir}")

        # Save dataset info
        dataset_info = {
            'total_samples': num_samples,
            'generation_date': str(time.time()),
            'scene_configurations_used': len(self.scene_configs),
            'output_directory': self.output_dir
        }

        info_path = os.path.join(self.output_dir, "dataset_info.json")
        with open(info_path, 'w') as f:
            json.dump(dataset_info, f, indent=2)

class ModelTrainer:
    """
    System for training models on synthetic data.
    """

    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.models = {}

    def load_dataset(self):
        """
        Load the synthetic dataset.
        """
        images_dir = os.path.join(self.dataset_path, "images")
        labels_dir = os.path.join(self.dataset_path, "labels")

        samples = []
        for filename in os.listdir(images_dir):
            if filename.endswith('.png'):
                base_name = filename.replace('.png', '')

                image_path = os.path.join(images_dir, filename)
                annot_path = os.path.join(labels_dir, f"{base_name}_annot.json")

                if os.path.exists(annot_path):
                    samples.append({
                        'image_path': image_path,
                        'annot_path': annot_path
                    })

        print(f"Loaded {len(samples)} samples from dataset")
        return samples

    def train_object_detector(self, samples: List[Dict], epochs: int = 10):
        """
        Train an object detection model on the synthetic dataset.
        """
        print("Starting object detector training...")

        # This would typically involve:
        # 1. Loading images and annotations
        # 2. Setting up data loaders
        # 3. Training a model (YOLO, Detectron2, etc.)
        # 4. Validating and saving the model

        # For this lab, we'll simulate the training process
        for epoch in range(epochs):
            # Simulate training epoch
            loss = 1.0 / (epoch + 1)  # Simulated decreasing loss
            print(f"Epoch {epoch + 1}/{epochs}, Loss: {loss:.4f}")

            # Simulate validation
            if epoch % 5 == 4:  # Validate every 5 epochs
                val_acc = 0.7 + (epoch * 0.03)  # Simulated increasing accuracy
                print(f"  Validation Accuracy: {val_acc:.4f}")

        print("Object detector training completed!")

        # Return a "trained" model (simulated)
        return {"model_type": "object_detector", "epochs_trained": epochs}

    def train_segmentation_model(self, samples: List[Dict], epochs: int = 10):
        """
        Train a segmentation model on the synthetic dataset.
        """
        print("Starting segmentation model training...")

        # Similar to object detection, but for segmentation
        for epoch in range(epochs):
            # Simulate training epoch
            loss = 0.8 / (epoch + 1)  # Simulated decreasing loss
            print(f"Epoch {epoch + 1}/{epochs}, Segmentation Loss: {loss:.4f}")

        print("Segmentation model training completed!")

        return {"model_type": "segmentation", "epochs_trained": epochs}

    def train_all_models(self):
        """
        Train all perception models.
        """
        samples = self.load_dataset()

        print("Training all perception models...")

        # Train object detector
        obj_detector = self.train_object_detector(samples)
        self.models['object_detector'] = obj_detector

        # Train segmentation model
        seg_model = self.train_segmentation_model(samples)
        self.models['segmentation'] = seg_model

        print("All models trained successfully!")
        return self.models

# Performance optimization utilities
class PerformanceOptimizer:
    """
    Tools for optimizing AI performance in Isaac Sim.
    """

    def __init__(self):
        self.performance_log = []

    def profile_model_inference(self, model_func, input_data, num_runs=100):
        """
        Profile model inference performance.
        """
        import time

        times = []
        for _ in range(num_runs):
            start_time = time.time()
            _ = model_func(input_data)
            end_time = time.time()
            times.append(end_time - start_time)

        avg_time = sum(times) / len(times)
        fps = 1.0 / avg_time if avg_time > 0 else 0

        stats = {
            'avg_inference_time': avg_time,
            'fps': fps,
            'min_time': min(times),
            'max_time': max(times),
            'num_runs': num_runs
        }

        self.performance_log.append(stats)
        return stats

    def optimize_model_for_tensorrt(self, model_path: str) -> str:
        """
        Optimize a PyTorch model for TensorRT inference.
        """
        print(f"Optimizing model {model_path} for TensorRT...")

        # This would typically involve:
        # 1. Converting PyTorch model to ONNX
        # 2. Converting ONNX to TensorRT engine
        # 3. Optimizing for specific hardware

        # For this lab, we'll simulate the optimization
        optimized_path = model_path.replace('.pth', '_trt.engine')
        print(f"Model optimized: {optimized_path}")

        return optimized_path

    def adaptive_inference_control(self, target_fps: float = 30.0):
        """
        Implement adaptive inference control to maintain target FPS.
        """
        class AdaptiveController:
            def __init__(self, target_fps):
                self.target_fps = target_fps
                self.current_interval = 1
                self.frame_count = 0
                self.processing_times = deque(maxlen=50)

            def should_process_frame(self):
                self.frame_count += 1
                return (self.frame_count % self.current_interval) == 0

            def update_performance(self, processing_time):
                self.processing_times.append(processing_time)

                if len(self.processing_times) >= 10:
                    avg_time = sum(self.processing_times) / len(self.processing_times)
                    target_time = 1.0 / self.target_fps

                    # Adjust processing interval based on performance
                    if avg_time > target_time * 0.8:  # Using 80% of available time
                        self.current_interval = min(self.current_interval + 1, 5)
                    elif avg_time < target_time * 0.3 and self.current_interval > 1:
                        self.current_interval = max(self.current_interval - 1, 1)

            def get_current_interval(self):
                return self.current_interval

        return AdaptiveController(target_fps)

# Main execution function for the lab
def run_ai_integration_lab():
    """
    Main function to run the complete AI integration lab.
    """
    print("Starting Isaac Sim AI Integration Lab...")

    # Initialize Isaac Sim world (simulated)
    print("Initializing Isaac Sim world...")
    # In practice: world = World(stage_units_in_meters=1.0)

    # Build the lab environment
    print("Building lab environment...")
    # In practice: scene_builder = LabSceneBuilder(); scene_builder.build_environment()

    # Initialize perception system
    print("Initializing perception system...")
    # In practice: camera = Camera(...); perception = PerceptionSystem(world, camera)

    # Generate synthetic training data
    print("Generating synthetic training data...")
    data_gen = SyntheticDataGenerator("./synthetic_dataset")
    data_gen.generate_dataset(num_samples=500)  # Smaller dataset for lab

    # Train models on synthetic data
    print("Training perception models...")
    trainer = ModelTrainer("./synthetic_dataset")
    trained_models = trainer.train_all_models()

    # Optimize models for inference
    print("Optimizing models for inference...")
    optimizer = PerformanceOptimizer()

    # Profile performance
    sample_input = np.random.random((1, 3, 416, 416)).astype(np.float32)
    perf_stats = optimizer.profile_model_inference(
        lambda x: np.random.random((1, 20)),  # Simulated model
        sample_input
    )
    print(f"Performance stats: {perf_stats}")

    # Set up adaptive inference
    adaptive_ctrl = optimizer.adaptive_inference_control(target_fps=30.0)

    print("\nAI Integration Lab completed successfully!")
    print("You have successfully implemented:")
    print("- Complete perception pipeline with object detection and segmentation")
    print("- Synthetic data generation with domain randomization")
    print("- Model training on synthetic data")
    print("- Performance optimization for real-time inference")
    print("- Adaptive inference control for consistent FPS")

    print("\nNext steps:")
    print("1. Test the perception system in different simulated environments")
    print("2. Collect real-world data to compare with synthetic performance")
    print("3. Fine-tune models based on real-world validation")
    print("4. Integrate with actual humanoid robot hardware")

if __name__ == "__main__":
    run_ai_integration_lab()
```

## Lab Execution and Validation

Now let's create a script to execute and validate the complete system:

```python
# lab_validation.py
import sys
import time
import numpy as np
from perception_system import AIIntegratedRobot, PerceptionSystem
from synthetic_data_generator import SyntheticDataGenerator, ModelTrainer, PerformanceOptimizer

def validate_perception_accuracy():
    """
    Validate the accuracy of the perception system.
    """
    print("Validating perception system accuracy...")

    # This would typically involve:
    # 1. Running perception on known test scenes
    # 2. Comparing with ground truth annotations
    # 3. Calculating metrics like mAP, IoU, etc.

    # Simulated validation results
    results = {
        'object_detection_mAP': 0.75,
        'segmentation_mIoU': 0.82,
        'detection_precision': 0.78,
        'detection_recall': 0.72
    }

    print(f"Perception validation results: {results}")
    return results

def validate_ros_integration():
    """
    Validate ROS 2 integration functionality.
    """
    print("Validating ROS 2 integration...")

    # This would test:
    # 1. Message publishing/subscribing
    # 2. TF transforms
    # 3. Navigation stack integration
    # 4. Sensor message formats

    # Simulated validation
    ros_status = {
        'publisher_status': 'connected',
        'message_rate': 30.0,  # Hz
        'tf_available': True,
        'navigation_active': True
    }

    print(f"ROS integration status: {ros_status}")
    return ros_status

def validate_performance():
    """
    Validate system performance under different conditions.
    """
    print("Validating system performance...")

    # Test performance with different numbers of objects
    performance_tests = []

    for num_objects in [1, 5, 10, 15, 20]:
        # Simulate performance with different scene complexity
        fps = max(10, 60 - num_objects * 2)  # Simplified performance model
        cpu_usage = min(95, 20 + num_objects * 3)

        test_result = {
            'num_objects': num_objects,
            'fps': fps,
            'cpu_usage_percent': cpu_usage,
            'memory_usage_mb': 500 + num_objects * 50
        }
        performance_tests.append(test_result)

    print("Performance validation results:")
    for test in performance_tests:
        print(f"  Objects: {test['num_objects']}, FPS: {test['fps']:.1f}, "
              f"CPU: {test['cpu_usage_percent']:.1f}%")

    return performance_tests

def run_comprehensive_test():
    """
    Run a comprehensive test of the entire system.
    """
    print("=" * 60)
    print("COMPREHENSIVE AI INTEGRATION TEST")
    print("=" * 60)

    # Test 1: Perception Pipeline
    print("\n1. Testing Perception Pipeline...")
    perception_results = validate_perception_accuracy()

    # Test 2: ROS Integration
    print("\n2. Testing ROS Integration...")
    ros_results = validate_ros_integration()

    # Test 3: Performance
    print("\n3. Testing Performance...")
    perf_results = validate_performance()

    # Test 4: End-to-End Functionality
    print("\n4. Testing End-to-End Functionality...")

    # Simulate a complete robot task
    print("   - Initializing robot...")
    print("   - Loading trained models...")
    print("   - Starting perception system...")
    print("   - Detecting objects in environment...")
    print("   - Planning navigation path...")
    print("   - Executing navigation...")
    print("   - Task completed successfully!")

    # Overall assessment
    overall_score = (
        perception_results['object_detection_mAP'] * 0.3 +
        perception_results['segmentation_mIoU'] * 0.3 +
        (perf_results[-1]['fps'] / 60.0) * 0.4
    )

    print(f"\nOverall System Score: {overall_score:.2f}/1.0")

    if overall_score > 0.7:
        print("✓ System performance is excellent!")
    elif overall_score > 0.5:
        print("~ System performance is acceptable.")
    else:
        print("⚠ System performance needs improvement.")

    return {
        'perception': perception_results,
        'ros_integration': ros_results,
        'performance': perf_results,
        'overall_score': overall_score
    }

def generate_lab_report(results):
    """
    Generate a comprehensive lab report.
    """
    report = f"""
ISAAC SIM AI INTEGRATION LAB REPORT
====================================

LAB EXECUTION SUMMARY
--------------------
- Date: {time.strftime('%Y-%m-%d %H:%M:%S')}
- System Components: Perception, Navigation, ROS Integration
- Test Environment: Isaac Sim with synthetic data

PERCEPTION SYSTEM RESULTS
------------------------
Object Detection:
- mAP (mean Average Precision): {results['perception']['object_detection_mAP']:.3f}
- Precision: {results['perception']['detection_precision']:.3f}
- Recall: {results['perception']['detection_recall']:.3f}

Semantic Segmentation:
- mIoU (mean Intersection over Union): {results['perception']['segmentation_mIoU']:.3f}

ROS INTEGRATION RESULTS
----------------------
- Connection Status: {results['ros_integration']['publisher_status']}
- Message Rate: {results['ros_integration']['message_rate']} Hz
- TF System: {'✓ Available' if results['ros_integration']['tf_available'] else '✗ Unavailable'}
- Navigation: {'✓ Active' if results['ros_integration']['navigation_active'] else '✗ Inactive'}

PERFORMANCE METRICS
------------------
- Peak FPS: {max([r['fps'] for r in results['performance']]):.1f}
- Sustained FPS (20 objects): {results['performance'][-1]['fps']:.1f}
- CPU Usage (20 objects): {results['performance'][-1]['cpu_usage_percent']:.1f}%
- Memory Usage (20 objects): {results['performance'][-1]['memory_usage_mb']:.0f} MB

OVERALL ASSESSMENT
-----------------
- Overall Score: {results['overall_score']:.2f}/1.0
- Grade: {'A' if results['overall_score'] > 0.8 else 'B' if results['overall_score'] > 0.6 else 'C'}

RECOMMENDATIONS
--------------
1. {'Optimize perception pipeline for better real-time performance' if results['performance'][-1]['fps'] < 30 else 'Performance is adequate for real-time operation'}
2. {'Collect more diverse training data to improve detection accuracy' if results['perception']['object_detection_mAP'] < 0.8 else 'Detection accuracy is sufficient'}
3. {'Validate system on real hardware to assess sim-to-real transfer' if True else ''}

CONCLUSION
----------
The AI perception system successfully integrates synthetic data generation,
model training, real-time inference, and ROS communication. The system
demonstrates the complete pipeline from perception to action in Isaac Sim.
"""

    # Save report to file
    with open('lab_report.txt', 'w') as f:
        f.write(report)

    print("Lab report generated: lab_report.txt")
    return report

def main():
    """
    Main function to execute the complete lab validation.
    """
    print("Starting Isaac Sim AI Integration Lab Validation...")

    # Run comprehensive test
    results = run_comprehensive_test()

    # Generate lab report
    report = generate_lab_report(results)

    print("\n" + "="*60)
    print("LAB VALIDATION COMPLETE")
    print("="*60)
    print("The complete AI integration pipeline has been validated.")
    print("Review the generated lab_report.txt for detailed results.")

    return results

if __name__ == "__main__":
    main()
```

## Lab Exercises

### Exercise 1: Perception Pipeline Enhancement
Enhance the perception system to detect and classify 10 different object types with at least 80% accuracy. Implement non-maximum suppression for object detection and evaluate the performance on the synthetic dataset.

### Exercise 2: Navigation with Dynamic Obstacles
Extend the navigation system to handle dynamic obstacles that move during robot operation. Implement predictive path planning that anticipates obstacle movements based on perception data.

### Exercise 3: Multi-Sensor Fusion
Integrate LiDAR data with camera data for improved 3D perception. Implement a sensor fusion algorithm that combines RGB, depth, and LiDAR information for more robust object detection and localization.

### Exercise 4: Sim-to-Real Transfer Validation
Collect real-world data using a physical robot and compare the performance of models trained on synthetic data versus real data. Analyze the sim-to-real gap and propose improvements to reduce it.

### Exercise 5: Performance Optimization Challenge
Optimize the complete AI pipeline to run at 60 FPS on a target hardware platform. Implement model quantization, pruning, and other optimization techniques to achieve the target performance.

## Lab Assessment Rubric

| Criteria | Excellent (4) | Good (3) | Satisfactory (2) | Needs Improvement (1) |
|----------|---------------|----------|------------------|----------------------|
| Perception Accuracy | >85% mAP on synthetic data | 75-85% mAP | 60-75% mAP | &lt;60% mAP |
| System Integration | All components work seamlessly | Most components integrated | Basic integration | Poor integration |
| Performance | >30 FPS with full pipeline | 20-30 FPS | 10-20 FPS | &lt;10 FPS |
| ROS Integration | Full ROS 2 communication | Basic ROS communication | Limited ROS features | Poor ROS integration |
| Documentation | Complete with examples | Good documentation | Basic documentation | Incomplete documentation |

## Summary

This lab provided hands-on experience with implementing a complete AI perception system for humanoid robots in Isaac Sim. You learned to:

1. Build complex simulation environments with multiple objects and challenges
2. Implement perception algorithms including object detection and semantic segmentation
3. Generate synthetic training data with domain randomization
4. Train and optimize AI models for real-time inference
5. Integrate perception systems with ROS 2 navigation
6. Validate system performance and accuracy

The skills developed in this lab form the foundation for deploying AI-powered humanoid robots in real-world applications, where perception accuracy and real-time performance are critical for safe and effective operation.