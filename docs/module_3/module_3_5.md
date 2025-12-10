---
title: "Module 3.5 - Chapter 5: Advanced Perception and AI in Isaac Sim"
sidebar_position: 5
---

# Module 3.5 - Advanced Perception and AI in Isaac Sim

## Overview

This chapter explores Isaac Sim's advanced perception and AI capabilities, focusing on how to leverage NVIDIA's AI frameworks within the Isaac Sim environment. We'll cover synthetic data generation, perception algorithms, and AI model training within the simulation environment.

## Learning Objectives

By the end of this chapter, you will be able to:
- Implement advanced perception algorithms in Isaac Sim
- Generate synthetic training data for AI models
- Integrate NVIDIA AI frameworks with Isaac Sim
- Train perception models using simulation data
- Apply computer vision techniques in photorealistic environments
- Validate AI models in simulation before real-world deployment

## Introduction to AI in Isaac Sim

Isaac Sim provides native integration with NVIDIA's AI ecosystem, enabling researchers and developers to train and validate AI models in photorealistic simulation environments. This integration is crucial for humanoid robotics, where perception systems must handle complex, dynamic environments.

### Key AI Capabilities in Isaac Sim

1. **Synthetic Data Generation**: Create large-scale datasets with perfect ground truth annotations
2. **Perception Training**: Train computer vision models directly within the simulation
3. **AI Framework Integration**: Native support for NVIDIA's AI tools and frameworks
4. **Real-time Inference**: Run AI models within the simulation loop for intelligent agents

## Synthetic Data Generation

Synthetic data generation is a cornerstone of Isaac Sim's AI capabilities, allowing for the creation of diverse, labeled datasets that would be expensive or impossible to collect in the real world.

### Domain Randomization

Domain randomization is a technique used to improve the sim-to-real transfer of AI models by varying the appearance and dynamics of objects in the simulation.

```python
import omni
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.core.utils.stage import add_reference_to_stage
from pxr import Gf, UsdGeom
import random

class DomainRandomizer:
    """
    Implements domain randomization for synthetic data generation in Isaac Sim.
    """

    def __init__(self, stage, prim_path):
        self.stage = stage
        self.prim_path = prim_path
        self.prim = get_prim_at_path(prim_path)

    def randomize_appearance(self):
        """
        Randomize the visual appearance of objects in the scene.
        """
        # Randomize material properties
        material_path = f"{self.prim_path}/Material"

        # Randomize color
        color = Gf.Vec3f(
            random.uniform(0.0, 1.0),
            random.uniform(0.0, 1.0),
            random.uniform(0.0, 1.0)
        )

        # Randomize texture properties
        roughness = random.uniform(0.1, 1.0)
        metallic = random.uniform(0.0, 1.0)

        # Apply randomization to USD prim
        prim = self.stage.GetPrimAtPath(self.prim_path)
        if prim:
            # Set color
            color_attr = prim.GetAttribute("xformOp:translate")
            if not color_attr:
                color_attr = prim.CreateAttribute("xformOp:translate", Sdf.ValueTypeNames.Float3)
            color_attr.Set(color)

    def randomize_lighting(self):
        """
        Randomize lighting conditions in the scene.
        """
        # Find all lights in the scene
        light_prims = [prim for prim in self.stage.GetPrimAtPath("/World").GetChildren()
                      if prim.GetTypeName() in ["DistantLight", "SphereLight", "DomeLight"]]

        for light_prim in light_prims:
            # Randomize intensity
            intensity_attr = light_prim.GetAttribute("inputs:intensity")
            if intensity_attr:
                new_intensity = random.uniform(100, 1000)  # Random intensity
                intensity_attr.Set(new_intensity)

            # Randomize color temperature
            color_attr = light_prim.GetAttribute("inputs:color")
            if color_attr:
                # Random color temperature (warm to cool)
                temp_factor = random.uniform(0.5, 2.0)
                base_color = Gf.Vec3f(1.0, 1.0, 1.0) * temp_factor
                color_attr.Set(base_color)

    def randomize_camera_parameters(self, camera_prim_path):
        """
        Randomize camera parameters for diverse viewpoints.
        """
        camera_prim = self.stage.GetPrimAtPath(camera_prim_path)
        if camera_prim:
            # Randomize focal length
            focal_length_attr = camera_prim.GetAttribute("focalLength")
            if focal_length_attr:
                focal_length = random.uniform(18.0, 50.0)  # Random focal length in mm
                focal_length_attr.Set(focal_length)

            # Randomize sensor settings
            sensor_width_attr = camera_prim.GetAttribute("horizontalAperture")
            sensor_height_attr = camera_prim.GetAttribute("verticalAperture")
            if sensor_width_attr:
                sensor_width_attr.Set(random.uniform(24.0, 36.0))
            if sensor_height_attr:
                sensor_height_attr.Set(random.uniform(16.0, 24.0))

class SyntheticDataGenerator:
    """
    Comprehensive synthetic data generation system for Isaac Sim.
    """

    def __init__(self, world, camera_sensors):
        self.world = world
        self.camera_sensors = camera_sensors
        self.domain_randomizer = None
        self.data_buffer = []

    def setup_domain_randomization(self, prim_paths):
        """
        Set up domain randomization for specified prims.
        """
        self.domain_randomizers = []
        for prim_path in prim_paths:
            randomizer = DomainRandomizer(self.world.scene.stage, prim_path)
            self.domain_randomizers.append(randomizer)

    def generate_dataset(self, num_samples, output_dir):
        """
        Generate synthetic dataset with domain randomization.
        """
        import os
        import json
        import numpy as np

        os.makedirs(output_dir, exist_ok=True)

        for i in range(num_samples):
            # Apply domain randomization
            for randomizer in self.domain_randomizers:
                randomizer.randomize_appearance()
                randomizer.randomize_lighting()

            # Update simulation
            self.world.step(render=True)

            # Capture data from all sensors
            sample_data = self.capture_sensor_data()

            # Save RGB image
            rgb_image = sample_data['rgb']
            rgb_path = os.path.join(output_dir, f"rgb_{i:06d}.png")
            rgb_image.save(rgb_path)

            # Save depth image
            depth_image = sample_data['depth']
            depth_path = os.path.join(output_dir, f"depth_{i:06d}.npy")
            np.save(depth_path, np.array(depth_image))

            # Save segmentation mask
            seg_mask = sample_data['segmentation']
            seg_path = os.path.join(output_dir, f"seg_{i:06d}.png")
            seg_mask.save(seg_path)

            # Save annotations
            annotations = {
                'objects': sample_data['objects'],
                'poses': sample_data['poses'],
                'camera_intrinsics': sample_data['camera_intrinsics']
            }
            annot_path = os.path.join(output_dir, f"annot_{i:06d}.json")
            with open(annot_path, 'w') as f:
                json.dump(annotations, f)

            print(f"Generated sample {i+1}/{num_samples}")

    def capture_sensor_data(self):
        """
        Capture synchronized data from all sensors.
        """
        # Capture RGB from camera
        rgb_data = self.camera_sensors[0].get_rgb()

        # Capture depth
        depth_data = self.camera_sensors[0].get_depth()

        # Capture segmentation
        seg_data = self.camera_sensors[0].get_segmentation()

        # Get object poses
        objects = []
        poses = []
        for prim in self.world.scene.get_objects():
            if hasattr(prim, 'get_world_pose'):
                pos, quat = prim.get_world_pose()
                objects.append(prim.name)
                poses.append({'position': pos, 'orientation': quat})

        # Get camera intrinsics
        intrinsics = self.camera_sensors[0].get_intrinsics()

        return {
            'rgb': rgb_data,
            'depth': depth_data,
            'segmentation': seg_data,
            'objects': objects,
            'poses': poses,
            'camera_intrinsics': intrinsics
        }

# Example usage
def setup_synthetic_data_generation():
    """
    Example of setting up synthetic data generation in Isaac Sim.
    """
    from omni.isaac.core import World
    from omni.isaac.sensor import Camera

    # Create world
    world = World(stage_units_in_meters=1.0)

    # Add objects to scene
    # ... add objects ...

    # Create camera sensor
    camera = Camera(
        prim_path="/World/Camera",
        position=[0.5, 0.5, 1.0],
        look_at=[0.0, 0.0, 0.0]
    )

    # Initialize data generator
    data_gen = SyntheticDataGenerator(world, [camera])

    # Set up domain randomization
    object_paths = ["/World/Object1", "/World/Object2"]  # Paths to objects to randomize
    data_gen.setup_domain_randomization(object_paths)

    # Generate dataset
    data_gen.generate_dataset(num_samples=1000, output_dir="./synthetic_dataset")
```

### Data Annotation Pipeline

Isaac Sim provides automatic annotation capabilities that generate perfect ground truth data for training AI models.

```python
import omni
from omni.isaac.core.utils.prims import get_prim_at_path
from omni.isaac.synthetic_utils import SyntheticDataHelper
import numpy as np

class AnnotationPipeline:
    """
    Automated annotation pipeline for synthetic data in Isaac Sim.
    """

    def __init__(self, world, camera_sensors):
        self.world = world
        self.camera_sensors = camera_sensors
        self.synthetic_data_helper = SyntheticDataHelper()

    def generate_2d_bounding_boxes(self, camera_sensor):
        """
        Generate 2D bounding boxes for objects in camera view.
        """
        # Get 3D bounding boxes from USD prims
        bbox_3d_data = self.synthetic_data_helper.get_bounding_box_3d()

        # Project 3D bounding boxes to 2D camera space
        bbox_2d_list = []
        for bbox_3d in bbox_3d_data:
            # Project 8 corners of 3D bbox to 2D
            corners_3d = self.get_bbox_corners(bbox_3d)
            corners_2d = []

            for corner_3d in corners_3d:
                # Project to camera space
                corner_2d = self.project_3d_to_2d(corner_3d, camera_sensor)
                if corner_2d is not None:
                    corners_2d.append(corner_2d)

            if corners_2d:
                # Compute 2D bounding box from projected corners
                min_x = min([c[0] for c in corners_2d])
                max_x = max([c[0] for c in corners_2d])
                min_y = min([c[1] for c in corners_2d])
                max_y = max([c[1] for c in corners_2d])

                bbox_2d = {
                    'x_min': min_x,
                    'x_max': max_x,
                    'y_min': min_y,
                    'y_max': max_y,
                    'object_id': bbox_3d['object_id'],
                    'class': bbox_3d['class']
                }
                bbox_2d_list.append(bbox_2d)

        return bbox_2d_list

    def generate_segmentation_masks(self):
        """
        Generate instance and semantic segmentation masks.
        """
        # Get segmentation data from synthetic data helper
        seg_data = self.synthetic_data_helper.get_semantic_segmentation()

        # Create segmentation masks
        semantic_mask = seg_data['semantic']
        instance_mask = seg_data['instance']

        return {
            'semantic': semantic_mask,
            'instance': instance_mask
        }

    def generate_keypoints(self, humanoid_robot):
        """
        Generate 2D keypoints for humanoid robot joints.
        """
        # Get joint positions in world coordinates
        joint_positions = humanoid_robot.get_joint_positions()

        # Project to camera space
        keypoints_2d = []
        for joint_name, world_pos in joint_positions.items():
            pixel_pos = self.project_3d_to_2d(world_pos, self.camera_sensors[0])
            if pixel_pos is not None:
                keypoints_2d.append({
                    'name': joint_name,
                    'x': pixel_pos[0],
                    'y': pixel_pos[1],
                    'visibility': True  # Always visible in simulation
                })

        return keypoints_2d

    def project_3d_to_2d(self, point_3d, camera_sensor):
        """
        Project 3D point to 2D camera coordinates.
        """
        # Get camera intrinsic matrix
        intrinsics = camera_sensor.get_intrinsics()

        # Get camera extrinsic matrix (world to camera transform)
        cam_pos, cam_rot = camera_sensor.get_world_pose()
        # Convert rotation to matrix and compute extrinsic
        extrinsic = self.pose_to_matrix(cam_pos, cam_rot)

        # Transform point to camera space
        point_cam = np.dot(extrinsic, np.append(point_3d, 1.0))[:3]

        # Project to image plane
        if point_cam[2] > 0:  # Point is in front of camera
            x = intrinsics[0, 0] * point_cam[0] / point_cam[2] + intrinsics[0, 2]
            y = intrinsics[1, 1] * point_cam[1] / point_cam[2] + intrinsics[1, 2]

            # Check if point is within image bounds
            img_width, img_height = camera_sensor.get_resolution()
            if 0 <= x < img_width and 0 <= y < img_height:
                return [x, y]

        return None

    def pose_to_matrix(self, position, rotation):
        """
        Convert position and rotation to transformation matrix.
        """
        # Convert quaternion to rotation matrix
        # This is a simplified version - in practice use proper quaternion to matrix conversion
        rot_matrix = np.eye(4)
        # ... fill rotation matrix ...

        # Add translation
        rot_matrix[:3, 3] = position

        return rot_matrix

    def get_bbox_corners(self, bbox_3d):
        """
        Get 8 corners of 3D bounding box.
        """
        center = bbox_3d['center']
        size = bbox_3d['size']

        half_size = [s/2 for s in size]

        corners = [
            [center[0] - half_size[0], center[1] - half_size[1], center[2] - half_size[2]],  # min
            [center[0] + half_size[0], center[1] - half_size[1], center[2] - half_size[2]],  # max x
            [center[0] - half_size[0], center[1] + half_size[1], center[2] - half_size[2]],  # max y
            [center[0] + half_size[0], center[1] + half_size[1], center[2] - half_size[2]],  # max x,y
            [center[0] - half_size[0], center[1] - half_size[1], center[2] + half_size[2]],  # max z
            [center[0] + half_size[0], center[1] - half_size[1], center[2] + half_size[2]],  # max x,z
            [center[0] - half_size[0], center[1] + half_size[1], center[2] + half_size[2]],  # max y,z
            [center[0] + half_size[0], center[1] + half_size[1], center[2] + half_size[2]]   # max
        ]

        return corners
```

## Perception Algorithms in Isaac Sim

Isaac Sim supports various perception algorithms that can be implemented and tested within the simulation environment.

### Object Detection and Recognition

```python
import omni
from omni.isaac.core import World
from omni.isaac.sensor import Camera
import cv2
import numpy as np
import torch
import torchvision.transforms as transforms

class IsaacSimObjectDetector:
    """
    Object detection system integrated with Isaac Sim.
    """

    def __init__(self, camera_sensor, model_path=None):
        self.camera_sensor = camera_sensor
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load pre-trained model or initialize
        if model_path:
            self.model = torch.load(model_path)
        else:
            # Initialize with a simple model for simulation
            self.model = self.create_simple_detector()

        self.model.to(self.device)
        self.model.eval()

        # Preprocessing transforms
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Resize((416, 416)),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                               std=[0.229, 0.224, 0.225])
        ])

    def create_simple_detector(self):
        """
        Create a simple object detection model for simulation.
        """
        import torch.nn as nn

        class SimpleDetector(nn.Module):
            def __init__(self, num_classes=80):
                super(SimpleDetector, self).__init__()
                # Simple CNN for demonstration
                self.features = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2),
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.ReLU(inplace=True),
                    nn.AdaptiveAvgPool2d((7, 7))
                )

                # Detection head
                self.classifier = nn.Sequential(
                    nn.Linear(128 * 7 * 7, 512),
                    nn.ReLU(inplace=True),
                    nn.Dropout(0.5),
                    nn.Linear(512, num_classes + 4)  # classes + bbox offsets
                )

            def forward(self, x):
                x = self.features(x)
                x = torch.flatten(x, 1)
                x = self.classifier(x)
                return x

        return SimpleDetector()

    def detect_objects(self, image):
        """
        Detect objects in the captured image.
        """
        # Preprocess image
        input_tensor = self.transform(image).unsqueeze(0).to(self.device)

        # Run detection
        with torch.no_grad():
            outputs = self.model(input_tensor)

        # Process outputs (simplified - in practice use proper NMS, etc.)
        batch_size, num_outputs = outputs.shape

        # For demonstration, return dummy detections
        # In practice, parse the model outputs properly
        detections = []

        # Convert outputs to bounding boxes and class probabilities
        # This is a simplified example - real implementation would be more complex
        for i in range(min(5, num_outputs // 5)):  # Process first 5 detections
            # Extract bbox and class info (simplified)
            bbox_x = float(outputs[0, i*5])
            bbox_y = float(outputs[0, i*5 + 1])
            bbox_w = float(outputs[0, i*5 + 2])
            bbox_h = float(outputs[0, i*5 + 3])
            class_prob = torch.softmax(outputs[0, i*5 + 4:], dim=0)
            class_id = torch.argmax(class_prob).item()

            detection = {
                'bbox': [bbox_x, bbox_y, bbox_w, bbox_h],
                'class_id': class_id,
                'confidence': float(class_prob[class_id])
            }
            detections.append(detection)

        return detections

    def run_detection_pipeline(self):
        """
        Complete detection pipeline from camera capture to results.
        """
        # Capture image from camera
        rgb_image = self.camera_sensor.get_rgb()

        # Convert to numpy array if needed
        if hasattr(rgb_image, 'to_numpy'):
            rgb_array = rgb_image.to_numpy()
        else:
            rgb_array = np.array(rgb_image)

        # Run object detection
        detections = self.detect_objects(rgb_array)

        # Filter detections by confidence
        filtered_detections = [det for det in detections if det['confidence'] > 0.5]

        return filtered_detections

class IsaacSimSemanticSegmenter:
    """
    Semantic segmentation system for Isaac Sim.
    """

    def __init__(self, camera_sensor):
        self.camera_sensor = camera_sensor
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Initialize segmentation model
        self.model = self.create_segmentation_model()
        self.model.to(self.device)
        self.model.eval()

        # Class mapping for Isaac Sim
        self.class_names = [
            "background", "robot", "obstacle", "furniture",
            "floor", "wall", "ceiling", "human"
        ]

        self.color_map = self.generate_color_map(len(self.class_names))

    def create_segmentation_model(self):
        """
        Create a simple segmentation model for simulation.
        """
        import torch.nn as nn
        import torch.nn.functional as F

        class SimpleSegmentation(nn.Module):
            def __init__(self, num_classes=8):
                super(SimpleSegmentation, self).__init__()

                # Encoder (simplified)
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

                # Decoder (simplified)
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
                x = self.encoder(x)
                x = self.decoder(x)
                return x

        return SimpleSegmentation()

    def segment_image(self, image):
        """
        Perform semantic segmentation on the input image.
        """
        # Convert image to tensor
        if isinstance(image, np.ndarray):
            # Convert from HWC to CHW and normalize
            image_tensor = torch.from_numpy(image).permute(2, 0, 1).float() / 255.0
        else:
            image_tensor = image

        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0).to(self.device)

        # Run segmentation
        with torch.no_grad():
            outputs = self.model(image_tensor)
            predictions = torch.argmax(outputs, dim=1)

        # Convert to numpy array
        segmentation_map = predictions.squeeze(0).cpu().numpy()

        return segmentation_map

    def visualize_segmentation(self, image, segmentation_map):
        """
        Visualize segmentation results by overlaying colored masks.
        """
        # Create color overlay
        overlay = image.copy()

        for class_id in range(len(self.class_names)):
            mask = (segmentation_map == class_id)
            if np.any(mask):
                # Get color for this class
                color = self.color_map[class_id]
                # Apply color to mask region
                overlay[mask] = (overlay[mask] * 0.5 + np.array(color) * 0.5).astype(np.uint8)

        return overlay

    def generate_color_map(self, num_classes):
        """
        Generate a color map for different classes.
        """
        import random
        colors = []
        for i in range(num_classes):
            # Generate random RGB color
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            colors.append((r, g, b))
        return colors
```

### 3D Object Detection and Pose Estimation

```python
import numpy as np
import open3d as o3d
from scipy.spatial.transform import Rotation as R

class IsaacSim3DObjectDetector:
    """
    3D object detection and pose estimation in Isaac Sim.
    """

    def __init__(self, camera_sensor, lidar_sensor=None):
        self.camera_sensor = camera_sensor
        self.lidar_sensor = lidar_sensor
        self.intrinsics = camera_sensor.get_intrinsics()

    def detect_3d_objects(self, rgb_image, depth_image, segmentation_mask):
        """
        Detect 3D objects using RGB-D data and segmentation.
        """
        # Convert depth image to point cloud
        point_cloud = self.depth_to_pointcloud(depth_image, self.intrinsics)

        # Segment point cloud based on segmentation mask
        segmented_objects = self.segment_pointcloud(point_cloud, segmentation_mask)

        # Perform 3D object detection on each segment
        detected_objects = []
        for obj_id, points in segmented_objects.items():
            if len(points) > 100:  # Minimum points for valid object
                # Estimate object pose using PCA or other methods
                pose = self.estimate_object_pose(points)

                # Classify object type based on geometric properties
                obj_type = self.classify_object_type(points)

                detected_objects.append({
                    'id': obj_id,
                    'type': obj_type,
                    'pose': pose,
                    'point_cloud': points
                })

        return detected_objects

    def depth_to_pointcloud(self, depth_image, intrinsics):
        """
        Convert depth image to 3D point cloud.
        """
        height, width = depth_image.shape

        # Create coordinate grids
        x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

        # Convert to 3D coordinates
        x_3d = (x_coords - intrinsics[0, 2]) * depth_image / intrinsics[0, 0]
        y_3d = (y_coords - intrinsics[1, 2]) * depth_image / intrinsics[1, 1]
        z_3d = depth_image

        # Stack coordinates
        points = np.stack([x_3d.flatten(), y_3d.flatten(), z_3d.flatten()], axis=1)

        # Remove invalid points (depth = 0 or inf)
        valid_mask = (z_3d.flatten() > 0) & (np.isfinite(points).all(axis=1))
        valid_points = points[valid_mask]

        return valid_points

    def segment_pointcloud(self, point_cloud, segmentation_mask):
        """
        Segment point cloud based on segmentation mask.
        """
        height, width = segmentation_mask.shape
        segmented_objects = {}

        # Flatten segmentation mask to match point cloud
        seg_flat = segmentation_mask.flatten()
        valid_mask = (seg_flat > 0)  # Non-background pixels

        # Group points by object ID
        for obj_id in np.unique(seg_flat[valid_mask]):
            if obj_id > 0:  # Skip background
                obj_mask = (seg_flat == obj_id)
                obj_points = point_cloud[obj_mask]
                segmented_objects[obj_id] = obj_points

        return segmented_objects

    def estimate_object_pose(self, points):
        """
        Estimate object pose using Principal Component Analysis (PCA).
        """
        if len(points) < 3:
            return {'position': [0, 0, 0], 'orientation': [0, 0, 0, 1]}  # Identity quaternion

        # Compute centroid
        centroid = np.mean(points, axis=0)

        # Compute covariance matrix
        centered_points = points - centroid
        cov_matrix = np.cov(centered_points.T)

        # Compute eigenvectors and eigenvalues
        eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

        # Sort eigenvectors by eigenvalues (largest first)
        idx = np.argsort(eigenvalues)[::-1]
        eigenvectors = eigenvectors[:, idx]

        # Ensure right-handed coordinate system
        if np.linalg.det(eigenvectors) < 0:
            eigenvectors[:, -1] *= -1

        # Convert rotation matrix to quaternion
        rotation = R.from_matrix(eigenvectors)
        quaternion = rotation.as_quat()  # [x, y, z, w]

        return {
            'position': centroid.tolist(),
            'orientation': quaternion.tolist()
        }

    def classify_object_type(self, points):
        """
        Classify object type based on geometric properties.
        """
        if len(points) < 3:
            return "unknown"

        # Compute bounding box
        min_coords = np.min(points, axis=0)
        max_coords = np.max(points, axis=0)
        dimensions = max_coords - min_coords

        # Compute aspect ratios
        sorted_dims = np.sort(dimensions)
        aspect_ratios = sorted_dims / sorted_dims[2]  # Normalize by largest dimension

        # Simple classification based on dimensions
        if aspect_ratios[0] < 0.3 and aspect_ratios[1] < 0.3:
            return "thin_object"  # Tall/thin object
        elif aspect_ratios[2] > 0.8:
            return "cuboid"  # Nearly cube-shaped
        elif aspect_ratios[0] < 0.2:
            return "elongated"  # Long object
        else:
            return "irregular"

    def track_objects(self, current_detections, previous_detections, max_distance=0.1):
        """
        Simple object tracking by matching detections based on position.
        """
        tracked_objects = []

        for curr_obj in current_detections:
            matched = False
            for prev_obj in previous_detections:
                # Calculate distance between object positions
                dist = np.linalg.norm(
                    np.array(curr_obj['pose']['position']) -
                    np.array(prev_obj['pose']['position'])
                )

                if dist < max_distance:
                    # Match found - assign same ID
                    tracked_objects.append({
                        **curr_obj,
                        'tracked_id': prev_obj.get('tracked_id', len(tracked_objects))
                    })
                    matched = True
                    break

            if not matched:
                # New object - assign new ID
                tracked_objects.append({
                    **curr_obj,
                    'tracked_id': len(tracked_objects)
                })

        return tracked_objects
```

## AI Framework Integration

Isaac Sim provides native integration with NVIDIA's AI frameworks, enabling seamless training and deployment of AI models.

### NVIDIA TAO Toolkit Integration

```python
import os
import subprocess
import json

class IsaacSimTAOIntegration:
    """
    Integration with NVIDIA TAO Toolkit for AI model training.
    """

    def __init__(self, tao_config_path):
        self.tao_config_path = tao_config_path
        self.models_path = "./tao_models"
        os.makedirs(self.models_path, exist_ok=True)

    def prepare_dataset(self, synthetic_data_path, output_path):
        """
        Prepare synthetic dataset for TAO training.
        """
        # Create TAO-compatible dataset structure
        os.makedirs(os.path.join(output_path, "train"), exist_ok=True)
        os.makedirs(os.path.join(output_path, "val"), exist_ok=True)

        # Convert annotations to TAO format
        self.convert_annotations(synthetic_data_path, output_path)

        # Create class mapping
        class_mapping = {
            "robot": 0,
            "obstacle": 1,
            "furniture": 2,
            "human": 3
        }

        with open(os.path.join(output_path, "class_mapping.json"), 'w') as f:
            json.dump(class_mapping, f)

        return output_path

    def convert_annotations(self, input_path, output_path):
        """
        Convert Isaac Sim annotations to TAO format.
        """
        import shutil
        import json

        # Copy images
        for img_file in os.listdir(os.path.join(input_path, "images")):
            if img_file.endswith(('.png', '.jpg', '.jpeg')):
                src = os.path.join(input_path, "images", img_file)
                dst = os.path.join(output_path, "train", img_file)
                shutil.copy2(src, dst)

        # Convert annotations
        for annot_file in os.listdir(os.path.join(input_path, "annotations")):
            if annot_file.endswith('.json'):
                with open(os.path.join(input_path, "annotations", annot_file), 'r') as f:
                    annot_data = json.load(f)

                # Convert to TAO format (example for object detection)
                tao_format = self.convert_to_tao_format(annot_data)

                # Save converted annotation
                output_annot_file = os.path.join(output_path, "train",
                                               annot_file.replace('.json', '_tao.json'))
                with open(output_annot_file, 'w') as f:
                    json.dump(tao_format, f)

    def convert_to_tao_format(self, annot_data):
        """
        Convert Isaac Sim annotation format to TAO format.
        """
        tao_annotations = {
            "images": [],
            "annotations": [],
            "categories": []
        }

        # Example conversion for object detection
        for obj in annot_data.get('objects', []):
            # Convert bounding box format
            bbox = obj.get('bbox', [0, 0, 0, 0])
            tao_bbox = [bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]]  # x, y, w, h

            annotation = {
                "id": len(tao_annotations["annotations"]),
                "image_id": 0,  # Would be set based on image
                "category_id": obj.get('class_id', 0),
                "bbox": tao_bbox,
                "area": tao_bbox[2] * tao_bbox[3],
                "iscrowd": 0
            }
            tao_annotations["annotations"].append(annotation)

        return tao_annotations

    def train_model(self, model_type, dataset_path, config_overrides=None):
        """
        Train a model using TAO Toolkit.
        """
        # Define model-specific training command
        if model_type == "detectnet_v2":
            cmd = [
                "tao", "detectnet_v2", "train",
                "-e", f"{self.tao_config_path}/detectnet_v2_train.yaml",
                "-r", f"{self.models_path}/{model_type}_model",
                "-k", "nvidia_tlt",
                "--dataset_config", f"{dataset_path}/dataset.yaml"
            ]
        elif model_type == "classification":
            cmd = [
                "tao", "classification", "train",
                "-e", f"{self.tao_config_path}/classification_train.yaml",
                "-r", f"{self.models_path}/{model_type}_model",
                "-k", "nvidia_tlt",
                "--dataset", dataset_path
            ]
        else:
            raise ValueError(f"Unsupported model type: {model_type}")

        # Add config overrides if provided
        if config_overrides:
            for key, value in config_overrides.items():
                cmd.extend(["--", f"+{key}={value}"])

        # Run training
        print(f"Starting TAO training for {model_type}...")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"Training completed successfully for {model_type}")
            return f"{self.models_path}/{model_type}_model"
        else:
            print(f"Training failed: {result.stderr}")
            return None

    def optimize_model(self, model_path, optimization_config):
        """
        Optimize trained model for deployment.
        """
        cmd = [
            "tao", "model_optimization", "optimize",
            "-m", model_path,
            "-c", optimization_config,
            "-o", f"{model_path}_optimized.etlt"
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print("Model optimization completed successfully")
            return f"{model_path}_optimized.etlt"
        else:
            print(f"Model optimization failed: {result.stderr}")
            return None

class IsaacSimInferenceEngine:
    """
    Inference engine for running trained models in Isaac Sim.
    """

    def __init__(self, model_path, model_type="tensorrt"):
        self.model_path = model_path
        self.model_type = model_type
        self.engine = None
        self.input_shape = None

        # Initialize the inference engine
        self.initialize_engine()

    def initialize_engine(self):
        """
        Initialize the inference engine based on model type.
        """
        if self.model_type == "tensorrt":
            import tensorrt as trt
            import pycuda.driver as cuda
            import pycuda.autoinit

            # Load TensorRT engine
            with open(self.model_path, 'rb') as f:
                engine_data = f.read()

            runtime = trt.Runtime(trt.Logger(trt.Logger.WARNING))
            self.engine = runtime.deserialize_cuda_engine(engine_data)

            # Get input shape from engine
            for binding in self.engine:
                if self.engine.binding_is_input(binding):
                    self.input_shape = self.engine.get_binding_shape(binding)
                    break

        elif self.model_type == "torch":
            import torch
            self.engine = torch.load(self.model_path)
            self.engine.eval()

        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def preprocess_input(self, input_data):
        """
        Preprocess input data for the model.
        """
        if self.model_type == "tensorrt":
            import numpy as np
            # Normalize and reshape input
            if isinstance(input_data, np.ndarray):
                # Ensure input is in the correct format
                if input_data.dtype != np.float32:
                    input_data = input_data.astype(np.float32)

                # Resize if needed
                if input_data.shape != self.input_shape[1:]:
                    import cv2
                    input_data = cv2.resize(input_data,
                                          (self.input_shape[2], self.input_shape[3]))

                # Normalize to [0, 1] then to [-1, 1] or ImageNet normalization
                input_data = input_data / 255.0
                input_data = (input_data - 0.5) / 0.5  # Normalize to [-1, 1]

                # Add batch dimension
                input_data = np.expand_dims(input_data, axis=0)

        return input_data

    def run_inference(self, input_data):
        """
        Run inference on input data.
        """
        if self.model_type == "tensorrt":
            import numpy as np
            import pycuda.driver as cuda
            import tensorrt as trt

            # Preprocess input
            input_data = self.preprocess_input(input_data)

            # Allocate device memory
            d_input = cuda.mem_alloc(input_data.nbytes)
            d_output = cuda.mem_alloc(1 * 1000 * 4)  # Assuming 1000 classes output

            bindings = [int(d_input), int(d_output)]
            stream = cuda.Stream()

            # Transfer input data to device
            cuda.memcpy_htod_async(d_input, input_data, stream)

            # Run inference
            context = self.engine.create_execution_context()
            context.execute_async_v2(bindings=bindings, stream_handle=stream.handle)

            # Transfer predictions back to host
            output = np.empty((1, 1000), dtype=np.float32)
            cuda.memcpy_dtoh_async(output, d_output, stream)
            stream.synchronize()

            return output[0]  # Return first batch output

        elif self.model_type == "torch":
            import torch

            # Convert to tensor if needed
            if not isinstance(input_data, torch.Tensor):
                input_tensor = torch.from_numpy(input_data).to(next(self.engine.parameters()).device)
            else:
                input_tensor = input_data.to(next(self.engine.parameters()).device)

            # Run inference
            with torch.no_grad():
                output = self.engine(input_tensor)

            return output.cpu().numpy()

        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def postprocess_output(self, raw_output):
        """
        Postprocess model output to meaningful results.
        """
        # Example: convert classification output to class probabilities
        if self.model_type in ["tensorrt", "torch"]:
            import numpy as np

            # Apply softmax to get probabilities
            exp_output = np.exp(raw_output - np.max(raw_output))  # For numerical stability
            probabilities = exp_output / np.sum(exp_output)

            # Get top predictions
            top_indices = np.argsort(probabilities)[::-1][:5]  # Top 5
            top_probs = probabilities[top_indices]

            results = []
            for idx, prob in zip(top_indices, top_probs):
                results.append({
                    'class_id': int(idx),
                    'confidence': float(prob),
                    'class_name': f"class_{idx}"  # Would be mapped to actual class names
                })

            return results
```

## Performance Optimization for AI in Simulation

Running AI models in simulation requires careful optimization to maintain real-time performance.

```python
import threading
import queue
import time
from collections import deque

class OptimizedAIPipeline:
    """
    Optimized AI pipeline for real-time performance in Isaac Sim.
    """

    def __init__(self, world, camera_sensors, ai_models):
        self.world = world
        self.camera_sensors = camera_sensors
        self.ai_models = ai_models
        self.input_queue = queue.Queue(maxsize=2)  # Limit queue size to prevent lag
        self.output_queue = queue.Queue(maxsize=2)
        self.running = False
        self.fps_counter = deque(maxlen=30)  # Track last 30 FPS measurements

        # Performance metrics
        self.total_inference_time = 0
        self.frame_count = 0

    def start_pipeline(self):
        """
        Start the optimized AI pipeline with separate threads.
        """
        self.running = True

        # Start input capture thread
        self.input_thread = threading.Thread(target=self.capture_thread)
        self.input_thread.start()

        # Start AI processing thread
        self.ai_thread = threading.Thread(target=self.ai_processing_thread)
        self.ai_thread.start()

        # Start output processing thread
        self.output_thread = threading.Thread(target=self.output_thread)
        self.output_thread.start()

    def stop_pipeline(self):
        """
        Stop the AI pipeline gracefully.
        """
        self.running = False

        # Wait for threads to finish
        if hasattr(self, 'input_thread'):
            self.input_thread.join()
        if hasattr(self, 'ai_thread'):
            self.ai_thread.join()
        if hasattr(self, 'output_thread'):
            self.output_thread.join()

    def capture_thread(self):
        """
        Thread for capturing sensor data.
        """
        while self.running:
            start_time = time.time()

            # Capture data from all sensors
            sensor_data = {}
            for i, camera in enumerate(self.camera_sensors):
                rgb_data = camera.get_rgb()
                depth_data = camera.get_depth()

                sensor_data[f'camera_{i}'] = {
                    'rgb': rgb_data,
                    'depth': depth_data,
                    'timestamp': time.time()
                }

            # Add to input queue if not full
            try:
                self.input_queue.put_nowait(sensor_data)
            except queue.Full:
                # Skip frame if queue is full (oldest frame will be dropped)
                continue

            # Maintain target frame rate
            capture_time = time.time() - start_time
            sleep_time = max(0, 1.0/30.0 - capture_time)  # Target 30 FPS
            time.sleep(sleep_time)

    def ai_processing_thread(self):
        """
        Thread for running AI inference.
        """
        while self.running:
            try:
                # Get sensor data from queue
                sensor_data = self.input_queue.get(timeout=1.0)

                inference_start = time.time()

                # Run AI models on sensor data
                ai_results = {}
                for model_name, model in self.ai_models.items():
                    if f'camera_0' in sensor_data:
                        input_data = sensor_data[f'camera_0']['rgb']
                        result = model.run_inference(input_data)
                        ai_results[model_name] = result

                inference_time = time.time() - inference_start
                self.total_inference_time += inference_time
                self.frame_count += 1

                # Add results to output queue
                output_data = {
                    'sensor_data': sensor_data,
                    'ai_results': ai_results,
                    'inference_time': inference_time,
                    'timestamp': time.time()
                }

                try:
                    self.output_queue.put_nowait(output_data)
                except queue.Full:
                    # Skip result if output queue is full
                    continue

            except queue.Empty:
                continue  # No data available, continue loop

    def output_thread(self):
        """
        Thread for processing AI results and updating simulation.
        """
        while self.running:
            try:
                output_data = self.output_queue.get(timeout=1.0)

                # Process AI results
                self.process_ai_results(output_data['ai_results'])

                # Update performance metrics
                fps = 1.0 / (time.time() - output_data['timestamp'])
                self.fps_counter.append(fps)

                # Log performance if needed
                if self.frame_count % 100 == 0:
                    avg_fps = sum(self.fps_counter) / len(self.fps_counter)
                    avg_inference_time = self.total_inference_time / self.frame_count
                    print(f"Performance - FPS: {avg_fps:.2f}, "
                          f"Avg Inference Time: {avg_inference_time*1000:.2f}ms")

            except queue.Empty:
                continue  # No results available, continue loop

    def process_ai_results(self, ai_results):
        """
        Process AI results and update simulation state.
        """
        # Example: Update robot behavior based on perception results
        if 'object_detector' in ai_results:
            detections = ai_results['object_detector']

            # Process detections and update robot goals
            for detection in detections:
                if detection['confidence'] > 0.7:  # High confidence detection
                    # Update robot navigation goal based on detected object
                    self.update_robot_navigation(detection)

    def update_robot_navigation(self, detection):
        """
        Update robot navigation based on AI perception results.
        """
        # Example: Move robot towards detected object
        object_position = detection.get('position', [0, 0, 0])

        # Send navigation command to robot
        # This would typically involve ROS 2 navigation or similar
        print(f"Detected object at {object_position}, updating navigation goal")

    def get_performance_metrics(self):
        """
        Get current performance metrics.
        """
        if self.frame_count > 0:
            avg_fps = sum(self.fps_counter) / len(self.fps_counter) if self.fps_counter else 0
            avg_inference_time = self.total_inference_time / self.frame_count
            return {
                'avg_fps': avg_fps,
                'avg_inference_time_ms': avg_inference_time * 1000,
                'total_frames': self.frame_count
            }
        return None

class AdaptiveInferenceScheduler:
    """
    Adaptive scheduler for AI inference to maintain real-time performance.
    """

    def __init__(self, target_fps=30):
        self.target_fps = target_fps
        self.current_interval = 1  # Process every N frames initially
        self.performance_history = deque(maxlen=50)
        self.frame_count = 0

    def should_process_frame(self):
        """
        Determine if the current frame should be processed by AI.
        """
        self.frame_count += 1

        # Process every Nth frame based on current interval
        return (self.frame_count % self.current_interval) == 0

    def update_performance(self, processing_time):
        """
        Update scheduler based on processing performance.
        """
        target_time = 1.0 / self.target_fps

        # Calculate performance ratio
        performance_ratio = processing_time / target_time

        # Add to history
        self.performance_history.append(performance_ratio)

        # Adjust interval based on average performance
        if len(self.performance_history) >= 10:
            avg_ratio = sum(self.performance_history) / len(self.performance_history)

            # Adjust interval: if processing takes too long, increase interval
            if avg_ratio > 0.8:  # Using 80% of available time
                self.current_interval = min(self.current_interval + 1, 10)  # Cap at 10
            elif avg_ratio < 0.5 and self.current_interval > 1:  # Plenty of time available
                self.current_interval = max(self.current_interval - 1, 1)  # Minimum 1

    def get_current_interval(self):
        """
        Get current processing interval.
        """
        return self.current_interval
```

## Exercises

### Exercise 1: Synthetic Data Generation
Create a synthetic dataset with 500 samples for object detection, including domain randomization for lighting, textures, and object positions. Calculate the mean and standard deviation of object positions in the generated dataset.

### Exercise 2: 3D Object Detection
Implement a 3D object detection pipeline that can detect and estimate the pose of 5 different object types in Isaac Sim. Test the pipeline with objects at various distances and orientations.

### Exercise 3: AI Model Integration
Integrate a pre-trained YOLO model with Isaac Sim for real-time object detection. Optimize the model for inference within the simulation loop to maintain 30 FPS performance.

### Exercise 4: Performance Optimization
Implement the adaptive inference scheduler and measure the performance improvement when processing different numbers of objects in the scene. Plot the FPS vs. number of objects.

## Summary

This chapter covered advanced perception and AI capabilities in Isaac Sim, including synthetic data generation with domain randomization, perception algorithms, AI framework integration, and performance optimization. We explored how to implement object detection, semantic segmentation, and 3D perception systems within Isaac Sim, and how to integrate with NVIDIA's AI frameworks for training and inference.

The key takeaways include:
- Synthetic data generation enables large-scale training with perfect ground truth
- Domain randomization improves sim-to-real transfer of AI models
- Isaac Sim provides native integration with NVIDIA's AI ecosystem
- Performance optimization is crucial for real-time AI in simulation
- Proper annotation pipelines enable high-quality training data

In the next lab, you'll implement a complete AI perception system for a humanoid robot in Isaac Sim, integrating all the concepts covered in this module.