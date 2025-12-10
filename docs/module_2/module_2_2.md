---
id: module_2_2
title: "Module 2.2 - Chapter 2: Unity Visualization"
sidebar_position: 2
---

# Module 2.2 - Chapter 2: Unity Visualization

## 2.0 Introduction to Unity Visualization

Unity visualization represents a critical component in modern robotics development, particularly for humanoid robots where high-fidelity rendering and human-robot interaction are paramount. This chapter explores the integration of Unity with ROS 2 to create sophisticated visualization environments that bridge the gap between simulation and reality.

Unity's powerful rendering engine, combined with its extensive asset ecosystem and real-time capabilities, makes it an ideal platform for visualizing complex humanoid robot behaviors, sensor data, and environmental interactions. Through this chapter, you will learn to create immersive visualization environments that enhance robot development, debugging, and human-robot interaction studies.

## 2.1 Core Unity Concepts for Robotics

### 2.1.1 High-Fidelity Rendering

Unity's rendering pipeline provides the foundation for creating photorealistic humanoid robot visualizations. The key components include lighting systems, shadow mapping, materials, and textures that work together to create convincing visual representations.

#### 2.1.1.1 Lighting Systems

Unity supports multiple lighting systems, but for robotics applications, the Universal Render Pipeline (URP) or High Definition Render Pipeline (HDRP) provide the best balance of performance and visual quality:

```csharp
// Example Unity C# script for dynamic lighting
using UnityEngine;

public class RobotLightingController : MonoBehaviour
{
    [Header("Light Configuration")]
    public Light mainLight;
    public float intensity = 1.0f;
    public Color lightColor = Color.white;

    void Start()
    {
        ConfigureLighting();
    }

    void ConfigureLighting()
    {
        if (mainLight != null)
        {
            mainLight.intensity = intensity;
            mainLight.color = lightColor;
            mainLight.shadows = LightShadows.Soft;
        }
    }

    public void UpdateLighting(float newIntensity, Color newColor)
    {
        if (mainLight != null)
        {
            mainLight.intensity = newIntensity;
            mainLight.color = newColor;
        }
    }
}
```

#### 2.1.1.2 Materials and Textures

For humanoid robots, realistic materials are crucial for accurate visualization. Unity's Material system allows for complex surface properties that can simulate metal, plastic, fabric, and other materials commonly found in robot construction:

```csharp
// Example material configuration for robot parts
using UnityEngine;

public class RobotMaterialManager : MonoBehaviour
{
    [Header("Material References")]
    public Material metalMaterial;
    public Material plasticMaterial;
    public Material rubberMaterial;

    [Header("Visual Properties")]
    public float metalSmoothness = 0.8f;
    public float plasticSmoothness = 0.3f;

    void Start()
    {
        ConfigureMaterials();
    }

    void ConfigureMaterials()
    {
        if (metalMaterial != null)
        {
            metalMaterial.SetFloat("_Smoothness", metalSmoothness);
        }

        if (plasticMaterial != null)
        {
            plasticMaterial.SetFloat("_Smoothness", plasticSmoothness);
        }
    }
}
```

### 2.1.2 Human-Robot Interaction

Creating effective human-robot interaction interfaces in Unity requires careful consideration of user experience, input methods, and visualization techniques that make robot states and intentions clear to human operators.

#### 2.1.2.1 Avatars and Gestures

Unity's animation system provides powerful tools for creating humanoid robot avatars that can demonstrate gestures and movements:

```csharp
// Example gesture controller for humanoid robot
using UnityEngine;
using UnityEngine.Animations;

public class RobotGestureController : MonoBehaviour
{
    [Header("Animation References")]
    public Animator robotAnimator;
    public AnimationClip[] gestureClips;

    [Header("Gesture Parameters")]
    public string gestureParameter = "Gesture";
    public float gestureSpeed = 1.0f;

    void Start()
    {
        if (robotAnimator == null)
        {
            robotAnimator = GetComponent<Animator>();
        }
    }

    public void PlayGesture(int gestureIndex)
    {
        if (robotAnimator != null && gestureIndex < gestureClips.Length)
        {
            robotAnimator.SetFloat(gestureParameter, gestureIndex);
            robotAnimator.speed = gestureSpeed;
        }
    }

    public void SetGestureSpeed(float speed)
    {
        if (robotAnimator != null)
        {
            gestureAnimator.speed = speed;
        }
    }
}
```

#### 2.1.2.2 Input Devices Integration

Unity supports various input devices for controlling robot visualization, from standard keyboards and mice to specialized VR controllers and haptic devices:

```csharp
// Example input controller for robot interaction
using UnityEngine;
using UnityEngine.InputSystem;

public class RobotInputController : MonoBehaviour
{
    [Header("Input Configuration")]
    public float moveSpeed = 5.0f;
    public float rotateSpeed = 2.0f;

    [Header("Camera References")]
    public Camera mainCamera;
    public Transform robotTransform;

    Vector2 movementInput;
    Vector2 lookInput;

    void Update()
    {
        HandleInput();
        UpdateRobotPosition();
    }

    void HandleInput()
    {
        // Get input from new input system
        movementInput = Keyboard.current.wKey.isPressed ? Vector2.up :
                       Keyboard.current.sKey.isPressed ? Vector2.down : Vector2.zero;
        lookInput = Keyboard.current.aKey.isPressed ? Vector2.left :
                   Keyboard.current.dKey.isPressed ? Vector2.right : Vector2.zero;
    }

    void UpdateRobotPosition()
    {
        Vector3 moveDirection = transform.forward * movementInput.y +
                               transform.right * lookInput.x;
        robotTransform.position += moveDirection * moveSpeed * Time.deltaTime;
        robotTransform.Rotate(Vector3.up, lookInput.x * rotateSpeed * Time.deltaTime);
    }
}
```

## 2.2 Robot Model Import and Integration

### 2.2.1 URDF/Xacro to Unity Conversion

Importing robot models from URDF (Unified Robot Description Format) or Xacro files into Unity requires careful consideration of scale, joint mapping, and kinematic chains. The process involves several steps:

1. **Scale Conversion**: URDF models are typically in meters, while Unity uses a different scale system
2. **Joint Mapping**: Converting URDF joint types to Unity's articulation body system
3. **Material Preservation**: Maintaining visual properties from the original model

#### 2.2.1.1 Scale and Joint Mapping

```csharp
// Example URDF to Unity scale converter
using UnityEngine;

public class URDFScaleConverter : MonoBehaviour
{
    [Header("Scale Configuration")]
    public float urdfToUnityScale = 1.0f; // URDF uses meters, Unity default scale
    public Vector3 unityScaleFactor = Vector3.one;

    [Header("Joint Configuration")]
    public ArticulationBody[] jointBodies;
    public float jointDamping = 0.1f;
    public float jointFriction = 0.1f;

    void Start()
    {
        ConvertURDFModel();
    }

    void ConvertURDFModel()
    {
        // Apply scale conversion
        transform.localScale = unityScaleFactor;

        // Configure joints
        ConfigureJoints();
    }

    void ConfigureJoints()
    {
        foreach (ArticulationBody joint in jointBodies)
        {
            joint.linearDamping = jointDamping;
            joint.angularDamping = jointDamping;
            joint.linearFriction = jointFriction;
            joint.angularFriction = jointFriction;
        }
    }
}
```

### 2.2.2 Scene Setup and Environment

Creating effective visualization scenes requires careful attention to camera placement, environment assets, and physics integration to ensure realistic robot behavior visualization.

#### 2.2.2.1 Camera Configuration

```csharp
// Example camera controller for robot visualization
using UnityEngine;

public class RobotVisualizationCamera : MonoBehaviour
{
    [Header("Camera Configuration")]
    public Transform target;
    public float distance = 10.0f;
    public float height = 5.0f;
    public float smoothSpeed = 12.0f;

    [Header("Rotation Controls")]
    public float rotationSpeed = 100.0f;
    public float minVerticalAngle = -45.0f;
    public float maxVerticalAngle = 45.0f;

    private float verticalAngle = 0.0f;
    private float horizontalAngle = 0.0f;

    void LateUpdate()
    {
        if (target != null)
        {
            UpdateCameraPosition();
        }
    }

    void UpdateCameraPosition()
    {
        // Calculate camera position
        Vector3 desiredPosition = target.position;
        desiredPosition += Quaternion.Euler(verticalAngle, horizontalAngle, 0) *
                          new Vector3(0, height, -distance);

        // Smoothly move camera to target position
        transform.position = Vector3.Lerp(transform.position, desiredPosition,
                                         smoothSpeed * Time.deltaTime);

        // Look at target
        transform.LookAt(target);
    }

    public void RotateCamera(float horizontal, float vertical)
    {
        horizontalAngle += horizontal * rotationSpeed * Time.deltaTime;
        verticalAngle -= vertical * rotationSpeed * Time.deltaTime;
        verticalAngle = Mathf.Clamp(verticalAngle, minVerticalAngle, maxVerticalAngle);
    }
}
```

## 2.3 Real-Time Visualization of ROS 2 Data Streams

### 2.3.1 ROS 2 Unity Integration

Unity can visualize real-time ROS 2 data streams through various integration methods, including the Unity Robotics Hub and custom TCP/IP communication layers.

#### 2.3.1.1 Sensor Data Visualization

```csharp
// Example sensor data visualization manager
using UnityEngine;
using System.Collections.Generic;

public class SensorVisualizationManager : MonoBehaviour
{
    [Header("Sensor Visualization")]
    public GameObject lidarPointPrefab;
    public GameObject cameraOverlay;
    public Material pointCloudMaterial;

    [Header("Data Buffers")]
    public List<Vector3> lidarPoints = new List<Vector3>();
    public Texture2D cameraTexture;

    [Header("Visualization Parameters")]
    public float pointSize = 0.1f;
    public Color pointColor = Color.red;

    void Update()
    {
        UpdateLidarVisualization();
        UpdateCameraVisualization();
    }

    void UpdateLidarVisualization()
    {
        // Clear existing points
        foreach (Transform child in transform)
        {
            if (child.name.Contains("LidarPoint"))
                Destroy(child.gameObject);
        }

        // Create new points based on lidar data
        foreach (Vector3 point in lidarPoints)
        {
            GameObject lidarPoint = Instantiate(lidarPointPrefab, point, Quaternion.identity);
            lidarPoint.name = "LidarPoint";
            lidarPoint.transform.SetParent(transform);

            // Apply material properties
            Renderer renderer = lidarPoint.GetComponent<Renderer>();
            if (renderer != null)
            {
                renderer.material = pointCloudMaterial;
                renderer.material.color = pointColor;
            }
        }
    }

    void UpdateCameraVisualization()
    {
        if (cameraTexture != null && cameraOverlay != null)
        {
            RawImage rawImage = cameraOverlay.GetComponent<RawImage>();
            if (rawImage != null)
            {
                rawImage.texture = cameraTexture;
            }
        }
    }

    public void UpdateLidarData(List<Vector3> newPoints)
    {
        lidarPoints = newPoints;
    }

    public void UpdateCameraTexture(Texture2D newTexture)
    {
        cameraTexture = newTexture;
    }
}
```

### 2.3.2 ROS 2 Topic Integration

```csharp
// Example ROS 2 topic subscriber for Unity
using UnityEngine;
using System;
using System.Collections.Generic;

public class ROSSubscriber : MonoBehaviour
{
    [Header("ROS Connection")]
    public string rosMasterUri = "http://localhost:11311";
    public string robotName = "humanoid_robot";

    [Header("Topic Subscriptions")]
    public List<string> subscribedTopics = new List<string>();

    void Start()
    {
        InitializeROSConnection();
    }

    void InitializeROSConnection()
    {
        // Initialize ROS connection (this would typically use Unity Robotics Hub)
        Debug.Log($"Connecting to ROS master: {rosMasterUri}");

        // Subscribe to topics
        foreach (string topic in subscribedTopics)
        {
            SubscribeToTopic(topic);
        }
    }

    void SubscribeToTopic(string topicName)
    {
        Debug.Log($"Subscribed to topic: {topicName}");
        // Implementation would handle actual ROS subscription
    }

    public void ProcessSensorData(string topic, object data)
    {
        // Process incoming sensor data and update visualization
        switch (topic)
        {
            case "lidar_scan":
                ProcessLidarData(data);
                break;
            case "camera_image":
                ProcessCameraData(data);
                break;
            case "joint_states":
                ProcessJointData(data);
                break;
        }
    }

    void ProcessLidarData(object data)
    {
        // Convert ROS lidar data to Unity visualization format
        // This would typically involve converting ROS LaserScan to Vector3 array
    }

    void ProcessCameraData(object data)
    {
        // Convert ROS camera data to Unity texture
        // This would typically involve converting ROS Image to Texture2D
    }

    void ProcessJointData(object data)
    {
        // Convert ROS joint state data to Unity joint positions
        // This would typically involve updating ArticulationBody positions
    }
}
```

## 2.4 Hands-On Examples

### 2.4.1 Example 1: Visualize a Humanoid Robot Walking in a Virtual Room

This example demonstrates creating a complete visualization environment with a humanoid robot walking in a virtual room:

```csharp
// Complete walking visualization example
using UnityEngine;
using UnityEngine.AI;

public class HumanoidWalkingVisualization : MonoBehaviour
{
    [Header("Robot Configuration")]
    public Transform robotRoot;
    public Animator robotAnimator;
    public NavMeshAgent agent;

    [Header("Environment Configuration")]
    public Transform[] waypoints;
    public int currentWaypoint = 0;

    [Header("Walking Parameters")]
    public float walkSpeed = 2.0f;
    public float turnSpeed = 100.0f;

    void Start()
    {
        InitializeWalkingBehavior();
    }

    void InitializeWalkingBehavior()
    {
        if (agent != null)
        {
            agent.speed = walkSpeed;
            agent.SetDestination(waypoints[currentWaypoint].position);
        }
    }

    void Update()
    {
        UpdateWalkingBehavior();
        UpdateAnimation();
    }

    void UpdateWalkingBehavior()
    {
        if (agent != null && waypoints.Length > 0)
        {
            // Check if reached current waypoint
            if (Vector3.Distance(transform.position, waypoints[currentWaypoint].position) < 1.0f)
            {
                currentWaypoint = (currentWaypoint + 1) % waypoints.Length;
                agent.SetDestination(waypoints[currentWaypoint].position);
            }
        }
    }

    void UpdateAnimation()
    {
        if (robotAnimator != null && agent != null)
        {
            // Calculate movement speed for animation blending
            float speed = agent.velocity.magnitude;
            robotAnimator.SetFloat("Speed", speed);

            // Calculate turn angle for animation
            Vector3 targetDirection = agent.steeringTarget - transform.position;
            if (targetDirection != Vector3.zero)
            {
                float turnAngle = Vector3.SignedAngle(transform.forward, targetDirection, Vector3.up);
                robotAnimator.SetFloat("Turn", turnAngle / 180.0f);
            }
        }
    }
}
```

### 2.4.2 Example 2: Display LiDAR Point Clouds and Camera Streams in Unity

This example shows how to visualize LiDAR point clouds and camera streams simultaneously:

```csharp
// LiDAR and camera visualization example
using UnityEngine;
using UnityEngine.UI;

public class LiDARCameraVisualization : MonoBehaviour
{
    [Header("LiDAR Visualization")]
    public GameObject pointCloudParent;
    public GameObject lidarPointPrefab;
    public Material lidarMaterial;

    [Header("Camera Visualization")]
    public RawImage cameraDisplay;
    public RenderTexture cameraTexture;

    [Header("Visualization Parameters")]
    public float maxRange = 10.0f;
    public float pointSize = 0.05f;
    public Color pointColor = Color.green;

    private GameObject[] pointObjects;
    private int pointCount = 1000; // Number of points to visualize

    void Start()
    {
        InitializeVisualization();
    }

    void InitializeVisualization()
    {
        // Create point cloud objects
        pointObjects = new GameObject[pointCount];
        for (int i = 0; i < pointCount; i++)
        {
            pointObjects[i] = Instantiate(lidarPointPrefab, Vector3.zero, Quaternion.identity);
            pointObjects[i].transform.SetParent(pointCloudParent.transform);

            Renderer renderer = pointObjects[i].GetComponent<Renderer>();
            if (renderer != null)
            {
                renderer.material = lidarMaterial;
                renderer.material.color = pointColor;
            }
        }

        // Set up camera display
        if (cameraDisplay != null && cameraTexture != null)
        {
            cameraDisplay.texture = cameraTexture;
        }
    }

    public void UpdatePointCloud(float[] ranges, float[] angles)
    {
        // Update point cloud visualization based on LiDAR data
        for (int i = 0; i < Mathf.Min(ranges.Length, pointObjects.Length); i++)
        {
            if (ranges[i] < maxRange)
            {
                float x = ranges[i] * Mathf.Cos(angles[i]);
                float z = ranges[i] * Mathf.Sin(angles[i]);

                pointObjects[i].transform.position = new Vector3(x, 0, z);
                pointObjects[i].SetActive(true);
            }
            else
            {
                pointObjects[i].SetActive(false);
            }
        }
    }

    public void UpdateCameraTexture(Texture2D newTexture)
    {
        if (cameraDisplay != null)
        {
            cameraDisplay.texture = newTexture;
        }
    }
}
```

### 2.4.3 Example 3: Control Robot Joints Through ROS 2 Topics and Unity UI

This example demonstrates creating a Unity UI that allows users to control robot joint positions:

```csharp
// Unity UI for joint control
using UnityEngine;
using UnityEngine.UI;
using System.Collections.Generic;

public class JointControlUI : MonoBehaviour
{
    [Header("Joint Control UI")]
    public Slider[] jointSliders;
    public Text[] jointLabels;
    public Button[] jointButtons;

    [Header("Robot Reference")]
    public ArticulationBody[] robotJoints;

    [Header("Control Parameters")]
    public float controlSpeed = 10.0f;

    private List<float> targetJointPositions = new List<float>();

    void Start()
    {
        InitializeJointControls();
    }

    void InitializeJointControls()
    {
        if (robotJoints.Length > 0)
        {
            jointSliders = new Slider[robotJoints.Length];
            jointLabels = new Text[robotJoints.Length];

            // Create UI elements for each joint
            for (int i = 0; i < robotJoints.Length; i++)
            {
                targetJointPositions.Add(robotJoints[i].jointPosition.x);

                // Create slider for joint
                GameObject sliderGO = new GameObject("JointSlider" + i);
                sliderGO.transform.SetParent(transform);
                Slider slider = sliderGO.AddComponent<Slider>();
                jointSliders[i] = slider;

                // Configure slider
                slider.minValue = -180.0f;
                slider.maxValue = 180.0f;
                slider.value = targetJointPositions[i];

                // Add listener for value changes
                int index = i; // Capture for closure
                slider.onValueChanged.AddListener(delegate { UpdateJointTarget(index, slider.value); });
            }
        }
    }

    void Update()
    {
        UpdateJointPositions();
    }

    void UpdateJointPositions()
    {
        for (int i = 0; i < robotJoints.Length && i < targetJointPositions.Count; i++)
        {
            ArticulationDrive drive = robotJoints[i].xDrive;
            drive.target = Mathf.Lerp(drive.target, targetJointPositions[i],
                                    controlSpeed * Time.deltaTime);
            robotJoints[i].xDrive = drive;
        }
    }

    void UpdateJointTarget(int jointIndex, float newValue)
    {
        if (jointIndex < targetJointPositions.Count)
        {
            targetJointPositions[jointIndex] = newValue;

            // Update label
            if (jointIndex < jointLabels.Length && jointLabels[jointIndex] != null)
            {
                jointLabels[jointIndex].text = $"Joint {jointIndex}: {newValue:F2}°";
            }
        }
    }

    public void SetJointPosition(int jointIndex, float position)
    {
        if (jointIndex < targetJointPositions.Count)
        {
            targetJointPositions[jointIndex] = position;
            if (jointIndex < jointSliders.Length)
            {
                jointSliders[jointIndex].value = position;
            }
        }
    }
}
```

### 2.4.4 Example 4: Create Interactive Simulations for Human-Robot Collaboration

This example demonstrates creating interactive scenarios for human-robot collaboration studies:

```csharp
// Human-robot collaboration simulation
using UnityEngine;
using UnityEngine.UI;

public class HumanRobotCollaboration : MonoBehaviour
{
    [Header("Robot and Human References")]
    public GameObject robot;
    public GameObject humanAvatar;
    public Transform interactionZone;

    [Header("Collaboration Parameters")]
    public float interactionDistance = 2.0f;
    public float collaborationRadius = 5.0f;

    [Header("UI Elements")]
    public Slider collaborationProgress;
    public Text collaborationStatus;
    public Button collaborationButton;

    [Header("Task Configuration")]
    public string[] collaborationTasks;
    public int currentTask = 0;

    private bool isCollaborating = false;
    private float collaborationProgressValue = 0.0f;

    void Start()
    {
        InitializeCollaborationSimulation();
    }

    void Update()
    {
        CheckForCollaborationOpportunities();
        UpdateCollaborationState();
    }

    void InitializeCollaborationSimulation()
    {
        if (collaborationButton != null)
        {
            collaborationButton.onClick.AddListener(StartCollaboration);
        }
    }

    void CheckForCollaborationOpportunities()
    {
        if (robot != null && humanAvatar != null)
        {
            float distance = Vector3.Distance(robot.transform.position,
                                           humanAvatar.transform.position);

            if (distance <= interactionDistance)
            {
                // Enable collaboration when human is close enough
                EnableCollaborationMode();
            }
            else
            {
                DisableCollaborationMode();
            }
        }
    }

    void EnableCollaborationMode()
    {
        if (collaborationButton != null)
        {
            collaborationButton.interactable = true;
            collaborationStatus.text = "Collaboration Available";
        }
    }

    void DisableCollaborationMode()
    {
        if (collaborationButton != null)
        {
            collaborationButton.interactable = false;
            collaborationStatus.text = "Move closer to collaborate";
        }
    }

    void StartCollaboration()
    {
        if (!isCollaborating)
        {
            isCollaborating = true;
            collaborationStatus.text = $"Task: {collaborationTasks[currentTask]}";

            // Start collaboration task
            StartCoroutine(ExecuteCollaborationTask());
        }
    }

    System.Collections.IEnumerator ExecuteCollaborationTask()
    {
        while (isCollaborating && collaborationProgressValue < 1.0f)
        {
            collaborationProgressValue += Time.deltaTime * 0.1f;
            collaborationProgress.value = collaborationProgressValue;

            yield return null;
        }

        if (collaborationProgressValue >= 1.0f)
        {
            CompleteTask();
        }
    }

    void CompleteTask()
    {
        collaborationProgressValue = 0.0f;
        collaborationProgress.value = 0.0f;

        currentTask = (currentTask + 1) % collaborationTasks.Length;
        collaborationStatus.text = $"Completed: {collaborationTasks[currentTask - 1 >= 0 ? currentTask - 1 : collaborationTasks.Length - 1]}";

        isCollaborating = false;
    }

    void UpdateCollaborationState()
    {
        if (isCollaborating)
        {
            // Update robot behavior during collaboration
            UpdateRobotBehavior();
        }
    }

    void UpdateRobotBehavior()
    {
        if (robot != null && humanAvatar != null)
        {
            // Make robot face human during collaboration
            Vector3 direction = humanAvatar.transform.position - robot.transform.position;
            direction.y = 0; // Keep rotation on horizontal plane
            robot.transform.rotation = Quaternion.LookRotation(direction);
        }
    }
}
```

## 2.5 Data Flow Diagrams

### 2.5.1 ROS 2 ↔ Unity ↔ Robot Data Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   ROS 2 Nodes   │◄──►│   Unity Bridge   │◄──►│   Unity Scene   │
│                 │    │                  │    │                 │
│ - Joint States  │    │ - TCP/IP Comm    │    │ - Robot Model   │
│ - Sensor Data   │    │ - Message Conv   │    │ - Visualization │
│ - TF Tree       │    │ - Data Mapping   │    │ - Animation     │
│ - Robot State   │    │ - Topic Mapping  │    │ - UI Elements   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                       ▲                       ▲
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Robot Control │    │   Visualization  │    │   Human Input   │
│   Systems       │    │   Pipeline       │    │   Interface     │
│                 │    │                  │    │                 │
│ - Navigation    │    │ - Rendering      │    │ - Keyboard      │
│ - Perception    │    │ - Post-Process   │    │ - Mouse         │
│ - Manipulation  │    │ - VR/AR Support  │    │ - VR Controllers│
└─────────────────┘    └─────────────────┘     └─────────────────┘
```

### 2.5.2 Sensor Data Pipeline Visualization

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Robot Sensors │    │   ROS 2 Topics   │    │   Unity Visual  │
│                 │    │                  │    │   Components    │
│ - LiDAR         │───►│ /scan            │───►│ Point Cloud     │
│ - Cameras       │───►│ /camera/image    │───►│ Texture Overlay │
│ - IMU           │───►│ /imu/data        │───►│ Orientation     │
│ - Joint Encoders│───►│ /joint_states    │───►│ Joint Animation │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Data      │    │   Data Filtering │    │   Real-time     │
│   Acquisition   │    │   & Processing   │    │   Rendering     │
│                 │    │                  │    │                 │
│ - Scan Points   │    │ - Noise Filter  │    │ - Point Shaders │
│ - Image Frames  │    │ - Data Sync     │    │ - Material      │
│ - Orientation   │    │ - Interpolation │    │   Animation     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 2.5.3 Scene Hierarchy and Camera Setup

```
Scene Root
├── Main Camera
│   ├── Camera Controller
│   └── Post-Processing Volume
├── Lighting System
│   ├── Directional Light
│   ├── Point Lights
│   └── Reflection Probes
├── Robot Root
│   ├── Robot Model (Imported from URDF)
│   │   ├── Link_1
│   │   │   ├── Joint_1
│   │   │   └── Visual_1
│   │   ├── Link_2
│   │   │   ├── Joint_2
│   │   │   └── Visual_2
│   │   └── ...
│   ├── Robot Controller
│   └── Animation Controller
├── Environment
│   ├── Floor
│   ├── Walls
│   ├── Obstacles
│   └── Environment Assets
├── Sensor Visualizers
│   ├── LiDAR Visualizer
│   ├── Camera Overlay
│   └── IMU Indicator
└── UI Canvas
    ├── Robot Status Panel
    ├── Control Interface
    └── Data Visualization
```

## 2.6 Tables for Clarity

### 2.6.1 Common Unity Assets and Plugins for Robotics Visualization

| Asset/Plugin | Purpose | Use Case | License |
|--------------|---------|----------|---------|
| Unity Robotics Hub | ROS 2 integration | Real-time data streaming | MIT |
| Unity ML-Agents | AI training | Robot behavior learning | MIT |
| HDRP/URP | Rendering pipeline | High-fidelity graphics | Unity License |
| NavMesh | Pathfinding | Robot navigation visualization | Unity License |
| Cinemachine | Camera control | Dynamic camera following | Unity License |
| DOTween | Animation | Smooth transitions | MIT |
| TextMeshPro | Text rendering | UI and status displays | Unity License |

### 2.6.2 Recommended Physics and Rendering Settings for Humanoid Robots

| Setting Category | Recommended Value | Rationale |
|------------------|-------------------|-----------|
| Fixed Timestep | 0.02 (50 Hz) | Balance between performance and accuracy |
| Maximum Allowed Timestep | 0.333 | Prevent physics instability |
| Solver Iterations | 8 | Adequate for humanoid joint constraints |
| Solver Velocity Iterations | 1 | Additional velocity solving |
| Gravity | (0, -9.81, 0) | Earth gravity simulation |
| Shadow Resolution | High | Clear shadow visualization |
| Shadow Distance | 50m | Visibility of robot shadows |
| Anti-Aliasing | 4x MSAA | Smooth edge rendering |

### 2.6.3 Mapping URDF Joints to Unity Articulations

| URDF Joint Type | Unity Articulation | Configuration | Notes |
|-----------------|-------------------|---------------|-------|
| revolute | Hinge Joint | X-axis rotation | Limited range |
| continuous | Hinge Joint | X-axis rotation | Unlimited range |
| prismatic | Slider Joint | X-axis translation | Linear motion |
| fixed | No joint | Parent-child | Rigid connection |
| floating | None | Use constraints | 6-DOF freedom |
| planar | Planar Joint | X-Y plane | 2D movement |

## 2.7 Exercises

### 2.7.1 Exercise 1: Import a Robot Model into Unity
Import a URDF robot model into Unity and configure the scale and joint properties. Verify that the model appears correctly scaled and that all joints are properly configured with appropriate articulation bodies.

### 2.7.2 Exercise 2: Visualize Sensor Data Streams
Create a Unity scene that visualizes LiDAR point clouds and camera image streams from ROS 2 topics. Implement proper scaling and coordinate system conversion between ROS and Unity.

### 2.7.3 Exercise 3: Add Environment Assets
Design and implement a virtual environment in Unity with appropriate lighting, textures, and obstacles that reflect a real-world scenario where the humanoid robot would operate.

### 2.7.4 Exercise 4: Create Interactive Controls
Implement a Unity UI that allows users to control individual robot joints through sliders and buttons, with real-time feedback showing the current joint positions.

### 2.7.5 Exercise 5: Optimize Rendering Performance
Configure Unity's rendering settings and implement Level of Detail (LOD) systems to maintain high frame rates when visualizing complex humanoid robots with multiple sensors.

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Robot Model Import into Unity</summary>

```csharp
// RobotModelImporter.cs
using UnityEngine;
using System.Collections;
using System.IO;

public class RobotModelImporter : MonoBehaviour
{
    [Header("Robot Configuration")]
    public string robotUrdfPath = "Assets/Models/Robot/urdf/";
    public float modelScale = 1.0f;

    [Header("Joint Configuration")]
    public bool autoConfigureJoints = true;
    public ArticulationBody[] jointComponents;

    [Header("Visual Settings")]
    public Material defaultMaterial;
    public Color robotColor = Color.gray;

    void Start()
    {
        ImportRobotModel();
        ConfigureRobotScale();

        if (autoConfigureJoints)
        {
            ConfigureJointsAutomatically();
        }
    }

    void ImportRobotModel()
    {
        // In practice, you would use a URDF importer plugin
        // This is a simplified example showing the process

        // Example: Load robot model assets
        GameObject robotModel = null;

        // Try to load the robot model from the specified path
        if (!string.IsNullOrEmpty(robotUrdfPath))
        {
            // Load model using AssetBundle or Resources
            // This is a placeholder for actual URDF import logic
            robotModel = GameObject.Find("RobotModel"); // This would be created by URDF importer

            if (robotModel != null)
            {
                robotModel.transform.SetParent(this.transform);
                robotModel.transform.localPosition = Vector3.zero;
                robotModel.transform.localRotation = Quaternion.identity;

                Debug.Log("Robot model imported successfully");
            }
            else
            {
                Debug.LogWarning("Robot model not found at specified path, creating placeholder");
                CreatePlaceholderRobot();
            }
        }
        else
        {
            CreatePlaceholderRobot();
        }
    }

    void CreatePlaceholderRobot()
    {
        // Create a simple placeholder robot model for demonstration
        // Base link
        GameObject baseLink = new GameObject("base_link");
        baseLink.transform.SetParent(this.transform);
        baseLink.AddComponent<MeshRenderer>().material = defaultMaterial;
        baseLink.AddComponent<MeshFilter>().mesh = CreateBoxMesh(0.5f, 0.3f, 0.4f);

        // Torso
        GameObject torso = new GameObject("torso");
        torso.transform.SetParent(baseLink.transform);
        torso.transform.localPosition = new Vector3(0, 0.2f, 0);
        torso.AddComponent<MeshRenderer>().material = defaultMaterial;
        torso.AddComponent<MeshFilter>().mesh = CreateBoxMesh(0.3f, 0.2f, 0.6f);

        // Head
        GameObject head = new GameObject("head");
        head.transform.SetParent(torso.transform);
        head.transform.localPosition = new Vector3(0, 0.35f, 0);
        head.AddComponent<MeshRenderer>().material = CreateSkinMaterial();
        head.AddComponent<MeshFilter>().mesh = CreateSphereMesh(0.1f);

        // Arms
        CreateArm("left_arm", torso.transform, new Vector3(0.2f, 0.1f, 0), true);
        CreateArm("right_arm", torso.transform, new Vector3(-0.2f, 0.1f, 0), false);

        // Legs
        CreateLeg("left_leg", baseLink.transform, new Vector3(0.1f, -0.3f, 0), true);
        CreateLeg("right_leg", baseLink.transform, new Vector3(-0.1f, -0.3f, 0), false);

        Debug.Log("Placeholder robot created");
    }

    void CreateArm(string name, Transform parent, Vector3 position, bool isLeft)
    {
        GameObject armRoot = new GameObject(name);
        armRoot.transform.SetParent(parent);
        armRoot.transform.localPosition = position;
        armRoot.transform.localRotation = Quaternion.identity;

        // Upper arm
        GameObject upperArm = new GameObject("upper_arm");
        upperArm.transform.SetParent(armRoot.transform);
        upperArm.transform.localPosition = Vector3.zero;
        upperArm.transform.localRotation = Quaternion.identity;
        upperArm.AddComponent<MeshRenderer>().material = defaultMaterial;
        upperArm.AddComponent<MeshFilter>().mesh = CreateCylinderMesh(0.05f, 0.3f);

        // Shoulder joint
        ArticulationBody shoulderJoint = upperArm.AddComponent<ArticulationBody>();
        ConfigureArticulationJoint(shoulderJoint, ArticulationJointType.RevoluteJoint);

        // Lower arm
        GameObject lowerArm = new GameObject("lower_arm");
        lowerArm.transform.SetParent(upperArm.transform);
        lowerArm.transform.localPosition = new Vector3(0, -0.3f, 0);
        lowerArm.transform.localRotation = Quaternion.identity;
        lowerArm.AddComponent<MeshRenderer>().material = defaultMaterial;
        lowerArm.AddComponent<MeshFilter>().mesh = CreateCylinderMesh(0.04f, 0.25f);

        // Elbow joint
        ArticulationBody elbowJoint = lowerArm.AddComponent<ArticulationBody>();
        ConfigureArticulationJoint(elbowJoint, ArticulationJointType.RevoluteJoint);
    }

    void CreateLeg(string name, Transform parent, Vector3 position, bool isLeft)
    {
        GameObject legRoot = new GameObject(name);
        legRoot.transform.SetParent(parent);
        legRoot.transform.localPosition = position;
        legRoot.transform.localRotation = Quaternion.identity;

        // Thigh
        GameObject thigh = new GameObject("thigh");
        thigh.transform.SetParent(legRoot.transform);
        thigh.transform.localPosition = Vector3.zero;
        thigh.transform.localRotation = Quaternion.identity;
        thigh.AddComponent<MeshRenderer>().material = defaultMaterial;
        thigh.AddComponent<MeshFilter>().mesh = CreateCylinderMesh(0.06f, 0.4f);

        // Hip joint
        ArticulationBody hipJoint = thigh.AddComponent<ArticulationBody>();
        ConfigureArticulationJoint(hipJoint, ArticulationJointType.RevoluteJoint);

        // Shin
        GameObject shin = new GameObject("shin");
        shin.transform.SetParent(thigh.transform);
        shin.transform.localPosition = new Vector3(0, -0.4f, 0);
        shin.transform.localRotation = Quaternion.identity;
        shin.AddComponent<MeshRenderer>().material = defaultMaterial;
        shin.AddComponent<MeshFilter>().mesh = CreateCylinderMesh(0.05f, 0.4f);

        // Knee joint
        ArticulationBody kneeJoint = shin.AddComponent<ArticulationBody>();
        ConfigureArticulationJoint(kneeJoint, ArticulationJointType.RevoluteJoint);
    }

    void ConfigureArticulationJoint(ArticulationBody joint, ArticulationJointType jointType)
    {
        joint.jointType = jointType;

        // Set up joint limits and drive parameters
        ArticulationDrive drive = joint.xDrive;
        drive.forceLimit = 100f;
        drive.damping = 10f;
        drive.stiffness = 1000f;
        joint.xDrive = drive;

        if (jointType == ArticulationJointType.RevoluteJoint)
        {
            joint.linearLockX = ArticulationDofLock.Locked;
            joint.linearLockY = ArticulationDofLock.Locked;
            joint.linearLockZ = ArticulationDofLock.Locked;

            joint.angularLockX = ArticulationDofLock.LimitedMotion;
            joint.angularLockY = ArticulationDofLock.Locked;
            joint.angularLockZ = ArticulationDofLock.LimitedMotion;
        }
    }

    void ConfigureRobotScale()
    {
        this.transform.localScale = Vector3.one * modelScale;
    }

    void ConfigureJointsAutomatically()
    {
        // Automatically find and configure all joints in the robot
        ArticulationBody[] allJoints = this.GetComponentsInChildren<ArticulationBody>();

        foreach (ArticulationBody joint in allJoints)
        {
            ConfigureArticulationJoint(joint, joint.jointType);
        }

        jointComponents = allJoints;
        Debug.Log($"Auto-configured {allJoints.Length} joints");
    }

    // Helper methods to create primitive meshes
    Mesh CreateBoxMesh(float width, float height, float depth)
    {
        // This is a simplified mesh creation - in practice, use proper mesh generation
        Mesh mesh = new Mesh();

        // Create vertices for a box
        Vector3[] vertices = new Vector3[8];
        vertices[0] = new Vector3(-width/2, -height/2, -depth/2);
        vertices[1] = new Vector3(width/2, -height/2, -depth/2);
        vertices[2] = new Vector3(width/2, height/2, -depth/2);
        vertices[3] = new Vector3(-width/2, height/2, -depth/2);
        vertices[4] = new Vector3(-width/2, -height/2, depth/2);
        vertices[5] = new Vector3(width/2, -height/2, depth/2);
        vertices[6] = new Vector3(width/2, height/2, depth/2);
        vertices[7] = new Vector3(-width/2, height/2, depth/2);

        // Create triangles (indices)
        int[] triangles = new int[] {
            // Front face
            0, 2, 1, 0, 3, 2,
            // Back face
            5, 7, 6, 5, 4, 7,
            // Top face
            3, 6, 2, 3, 7, 6,
            // Bottom face
            4, 1, 5, 4, 0, 1,
            // Right face
            1, 6, 5, 1, 2, 6,
            // Left face
            4, 7, 0, 7, 3, 0
        };

        mesh.vertices = vertices;
        mesh.triangles = triangles;
        mesh.RecalculateNormals();

        return mesh;
    }

    Mesh CreateSphereMesh(float radius)
    {
        GameObject sphereObj = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        SphereCollider collider = sphereObj.GetComponent<SphereCollider>();
        collider.enabled = false; // Remove default collider

        MeshFilter filter = sphereObj.GetComponent<MeshFilter>();
        Mesh originalMesh = filter.mesh;

        // Scale the mesh
        Vector3[] vertices = originalMesh.vertices;
        for (int i = 0; i < vertices.Length; i++)
        {
            vertices[i] = vertices[i] * radius;
        }
        originalMesh.vertices = vertices;

        DestroyImmediate(sphereObj);
        return originalMesh;
    }

    Mesh CreateCylinderMesh(float radius, float height)
    {
        GameObject cylinderObj = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
        MeshFilter filter = cylinderObj.GetComponent<MeshFilter>();
        Mesh originalMesh = filter.mesh;

        // Scale the mesh properly
        Vector3[] vertices = originalMesh.vertices;
        for (int i = 0; i < vertices.Length; i++)
        {
            Vector3 v = vertices[i];
            // Scale x and z by radius, y by height/2
            v.x *= radius;
            v.z *= radius;
            v.y *= height / 2f;
            vertices[i] = v;
        }
        originalMesh.vertices = vertices;

        DestroyImmediate(cylinderObj);
        return originalMesh;
    }

    Material CreateSkinMaterial()
    {
        Material skinMat = new Material(Shader.Find("Standard"));
        skinMat.color = new Color(0.8f, 0.6f, 0.4f); // Skin-like color
        return skinMat;
    }
}
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Sensor Data Visualization</summary>

```csharp
// SensorDataVisualizer.cs
using UnityEngine;
using System.Collections.Generic;
using System.Linq;

public class SensorDataVisualizer : MonoBehaviour
{
    [Header("LiDAR Visualization")]
    public GameObject lidarPointCloudPrefab;
    public Material lidarPointMaterial;
    public float lidarPointSize = 0.02f;
    public Color lidarColor = Color.red;

    [Header("Camera Stream Visualization")]
    public Renderer cameraTextureRenderer;
    public RenderTexture cameraRenderTexture;

    [Header("IMU Visualization")]
    public GameObject imuArrowPrefab;
    public Color imuOrientationColor = Color.blue;

    [Header("Display Settings")]
    public float maxLidarRange = 10.0f;
    public int maxPointsToShow = 1000;

    private List<GameObject> lidarPoints;
    private List<GameObject> imuArrows;

    void Start()
    {
        lidarPoints = new List<GameObject>();
        imuArrows = new List<GameObject>();

        SetupLidarVisualization();
        SetupCameraVisualization();
        SetupIMUVisualization();
    }

    void SetupLidarVisualization()
    {
        // Create a container for LiDAR points
        GameObject lidarContainer = new GameObject("LiDAR Points");
        lidarContainer.transform.SetParent(this.transform);
    }

    void SetupCameraVisualization()
    {
        if (cameraTextureRenderer != null && cameraRenderTexture != null)
        {
            cameraTextureRenderer.material.mainTexture = cameraRenderTexture;
        }
    }

    void SetupIMUVisualization()
    {
        // Create arrow for IMU orientation visualization
        if (imuArrowPrefab != null)
        {
            GameObject imuArrow = Instantiate(imuArrowPrefab, this.transform);
            imuArrow.SetActive(false); // Initially hidden
            imuArrows.Add(imuArrow);
        }
        else
        {
            // Create a simple arrow if prefab not provided
            GameObject imuArrow = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            imuArrow.name = "IMU Arrow";
            imuArrow.transform.SetParent(this.transform);
            imuArrow.GetComponent<Renderer>().material.color = imuOrientationColor;
            imuArrow.SetActive(false);
            imuArrows.Add(imuArrow);
        }
    }

    public void UpdateLiDARPoints(float[] ranges, float[] angles)
    {
        // Clear previous points
        ClearLiDARPoints();

        if (ranges == null || angles == null || ranges.Length != angles.Length)
        {
            Debug.LogError("Invalid LiDAR data");
            return;
        }

        // Create new points based on ranges and angles
        int pointCount = Mathf.Min(ranges.Length, maxPointsToShow);

        for (int i = 0; i < pointCount; i++)
        {
            float range = ranges[i];
            float angle = angles[i];

            if (range > 0 && range <= maxLidarRange)
            {
                // Calculate position in 2D (x, y plane)
                float x = range * Mathf.Cos(angle);
                float y = range * Mathf.Sin(angle);

                // Create LiDAR point
                GameObject point = GameObject.CreatePrimitive(PrimitiveType.Sphere);
                point.transform.SetParent(this.transform);
                point.transform.position = new Vector3(x, 0.1f, y); // Slightly above ground
                point.transform.localScale = Vector3.one * lidarPointSize;

                // Apply material
                if (lidarPointMaterial != null)
                {
                    point.GetComponent<Renderer>().material = lidarPointMaterial;
                }
                else
                {
                    point.GetComponent<Renderer>().material.color = lidarColor;
                }

                // Remove collider to improve performance
                DestroyImmediate(point.GetComponent<Collider>());

                lidarPoints.Add(point);
            }
        }
    }

    public void UpdateLiDARPoints3D(Vector3[] points)
    {
        // Clear previous points
        ClearLiDARPoints();

        if (points == null) return;

        int pointCount = Mathf.Min(points.Length, maxPointsToShow);

        for (int i = 0; i < pointCount; i++)
        {
            // Create LiDAR point
            GameObject point = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            point.transform.SetParent(this.transform);
            point.transform.position = points[i];
            point.transform.localScale = Vector3.one * lidarPointSize;

            // Apply material
            if (lidarPointMaterial != null)
            {
                point.GetComponent<Renderer>().material = lidarPointMaterial;
            }
            else
            {
                point.GetComponent<Renderer>().material.color = lidarColor;
            }

            // Remove collider to improve performance
            DestroyImmediate(point.GetComponent<Collider>());

            lidarPoints.Add(point);
        }
    }

    public void UpdateCameraTexture(Texture2D cameraImage)
    {
        if (cameraTextureRenderer != null && cameraImage != null)
        {
            // Create a texture from the camera image
            Texture2D unityTexture = new Texture2D(cameraImage.width, cameraImage.height, TextureFormat.RGB24, false);
            Graphics.CopyTexture(cameraImage, unityTexture);

            // Apply to renderer
            cameraTextureRenderer.material.mainTexture = unityTexture;
        }
    }

    public void UpdateIMUVisualization(Vector3 orientation, Vector3 angularVelocity)
    {
        if (imuArrows.Count > 0)
        {
            GameObject imuArrow = imuArrows[0];
            imuArrow.SetActive(true);

            // Set orientation of the arrow based on IMU data
            imuArrow.transform.rotation = Quaternion.Euler(orientation);

            // Scale the arrow based on angular velocity magnitude
            float velocityMagnitude = angularVelocity.magnitude;
            float scale = Mathf.Clamp(velocityMagnitude, 0.1f, 2.0f);
            imuArrow.transform.localScale = new Vector3(0.1f, scale, 0.1f);
        }
    }

    public void ClearLiDARPoints()
    {
        // Destroy existing LiDAR points
        foreach (GameObject point in lidarPoints)
        {
            if (point != null)
            {
                DestroyImmediate(point);
            }
        }
        lidarPoints.Clear();
    }

    public void ClearAllVisualizations()
    {
        ClearLiDARPoints();

        // Hide IMU arrows
        foreach (GameObject arrow in imuArrows)
        {
            if (arrow != null)
            {
                arrow.SetActive(false);
            }
        }
    }

    // Simulate receiving ROS 2 sensor data
    public void SimulateLiDARData()
    {
        // Generate simulated LiDAR data for testing
        int numPoints = 360; // 360-degree scan
        float[] ranges = new float[numPoints];
        float[] angles = new float[numPoints];

        for (int i = 0; i < numPoints; i++)
        {
            float angle = Mathf.Deg2Rad * i; // Convert index to angle
            angles[i] = angle;

            // Simulate some obstacles
            float distance = maxLidarRange;

            // Create a circular obstacle
            if (Mathf.Abs(angle - Mathf.PI/2) < 0.2f)
            {
                distance = 3.0f + Mathf.Sin(angle * 5) * 0.5f; // Obstacle at ~3m
            }

            ranges[i] = distance;
        }

        UpdateLiDARPoints(ranges, angles);
    }
}
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Environment Assets Implementation</summary>

```csharp
// EnvironmentAssetManager.cs
using UnityEngine;
using System.Collections.Generic;

public class EnvironmentAssetManager : MonoBehaviour
{
    [Header("Environment Configuration")]
    public string environmentName = "Humanoid Lab";
    public float environmentSize = 20.0f;

    [Header("Asset Prefabs")]
    public GameObject floorPrefab;
    public GameObject wallPrefab;
    public GameObject tablePrefab;
    public GameObject chairPrefab;
    public GameObject rampPrefab;
    public GameObject stairsPrefab;
    public GameObject obstaclePrefab;

    [Header("Lighting Configuration")]
    public Light mainLight;
    public Color ambientLightColor = Color.white;
    public float ambientIntensity = 0.5f;

    [Header("Physics Configuration")]
    public PhysicMaterial defaultMaterial;
    public float gravity = -9.81f;

    private List<GameObject> environmentObjects;

    void Start()
    {
        environmentObjects = new List<GameObject>();

        // Set up environment
        SetupEnvironment();
        SetupLighting();
        SetupPhysics();
        CreateScenarioAssets();
    }

    void SetupEnvironment()
    {
        // Create a basic environment floor
        if (floorPrefab != null)
        {
            GameObject floor = Instantiate(floorPrefab, Vector3.zero, Quaternion.identity);
            floor.name = "Environment Floor";
            floor.transform.localScale = new Vector3(environmentSize / 10f, 1, environmentSize / 10f);
            environmentObjects.Add(floor);
        }
        else
        {
            // Create a default floor if no prefab provided
            GameObject floor = GameObject.CreatePrimitive(PrimitiveType.Plane);
            floor.name = "Default Floor";
            floor.transform.position = Vector3.zero;
            floor.transform.localScale = Vector3.one * (environmentSize / 10f);
            environmentObjects.Add(floor);
        }

        // Create boundary walls
        CreateBoundaryWalls();

        Debug.Log($"Environment '{environmentName}' set up with size {environmentSize}x{environmentSize}");
    }

    void CreateBoundaryWalls()
    {
        float halfSize = environmentSize / 2f;

        // Create four walls around the boundary
        CreateWall(new Vector3(0, 0, halfSize), new Vector3(environmentSize, 0.1f, 0.1f)); // North wall
        CreateWall(new Vector3(0, 0, -halfSize), new Vector3(environmentSize, 0.1f, 0.1f)); // South wall
        CreateWall(new Vector3(halfSize, 0, 0), new Vector3(0.1f, 0.1f, environmentSize)); // East wall
        CreateWall(new Vector3(-halfSize, 0, 0), new Vector3(0.1f, 0.1f, environmentSize)); // West wall
    }

    GameObject CreateWall(Vector3 position, Vector3 scale)
    {
        GameObject wall;
        if (wallPrefab != null)
        {
            wall = Instantiate(wallPrefab, position, Quaternion.identity);
        }
        else
        {
            wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
            wall.GetComponent<Renderer>().material.color = Color.gray;
        }

        wall.name = $"Wall_{position}";
        wall.transform.localScale = scale;

        // Add physics properties
        if (defaultMaterial != null)
        {
            var collider = wall.GetComponent<Collider>();
            if (collider != null)
            {
                collider.material = defaultMaterial;
            }
        }

        environmentObjects.Add(wall);
        return wall;
    }

    void SetupLighting()
    {
        // Configure main directional light
        if (mainLight == null)
        {
            // Create a default light if none provided
            GameObject lightObj = new GameObject("Main Light");
            mainLight = lightObj.AddComponent<Light>();
            mainLight.type = LightType.Directional;
            mainLight.color = Color.white;
            mainLight.intensity = 1.0f;
            mainLight.transform.rotation = Quaternion.Euler(50, -30, 0);
        }

        // Set lighting properties
        RenderSettings.ambientLight = ambientLightColor * ambientIntensity;
        RenderSettings.ambientIntensity = ambientIntensity;

        Debug.Log("Lighting configured for environment");
    }

    void SetupPhysics()
    {
        // Set global physics properties
        Physics.gravity = new Vector3(0, gravity, 0);

        if (defaultMaterial != null)
        {
            // Default material is already assigned to objects that need it
            Debug.Log("Physics materials configured");
        }
    }

    void CreateScenarioAssets()
    {
        // Create furniture and obstacles that reflect a real-world scenario

        // Create tables
        if (tablePrefab != null)
        {
            // Conference table
            GameObject conferenceTable = Instantiate(tablePrefab, new Vector3(5, 0, 0), Quaternion.identity);
            conferenceTable.name = "Conference Table";
            conferenceTable.transform.localScale = new Vector3(2, 1, 1);
            environmentObjects.Add(conferenceTable);

            // Desk
            GameObject desk = Instantiate(tablePrefab, new Vector3(-3, 0, 4), Quaternion.Euler(0, 45, 0));
            desk.name = "Desk";
            desk.transform.localScale = new Vector3(1.5f, 1, 0.8f);
            environmentObjects.Add(desk);
        }

        // Create chairs
        if (chairPrefab != null)
        {
            // Chairs around the conference table
            for (int i = 0; i < 6; i++)
            {
                float angle = (i * 60) * Mathf.Deg2Rad;
                float radius = 1.5f;
                Vector3 position = new Vector3(
                    5 + radius * Mathf.Cos(angle),
                    0,
                    radius * Mathf.Sin(angle)
                );

                GameObject chair = Instantiate(chairPrefab, position, Quaternion.identity);
                chair.name = $"Chair_{i}";
                chair.transform.LookAt(new Vector3(5, 0, 0)); // Face the table
                environmentObjects.Add(chair);
            }
        }

        // Create ramps for humanoid navigation
        if (rampPrefab != null)
        {
            GameObject ramp = Instantiate(rampPrefab, new Vector3(8, 0, -5), Quaternion.identity);
            ramp.name = "Training Ramp";
            ramp.transform.localScale = new Vector3(2, 1, 0.5f);
            environmentObjects.Add(ramp);
        }

        // Create stairs
        if (stairsPrefab != null)
        {
            GameObject stairs = Instantiate(stairsPrefab, new Vector3(-8, 0, 3), Quaternion.identity);
            stairs.name = "Training Stairs";
            stairs.transform.localScale = new Vector3(1, 1, 1);
            environmentObjects.Add(stairs);
        }

        // Create random obstacles
        if (obstaclePrefab != null)
        {
            for (int i = 0; i < 5; i++)
            {
                Vector3 randomPos = new Vector3(
                    Random.Range(-environmentSize/3f, environmentSize/3f),
                    0,
                    Random.Range(-environmentSize/3f, environmentSize/3f)
                );

                GameObject obstacle = Instantiate(obstaclePrefab, randomPos, Quaternion.identity);
                obstacle.name = $"Obstacle_{i}";
                environmentObjects.Add(obstacle);
            }
        }

        Debug.Log("Scenario-specific environment assets created");
    }

    // Method to dynamically add assets during runtime
    public GameObject AddAsset(GameObject prefab, Vector3 position, Quaternion rotation)
    {
        if (prefab == null)
        {
            Debug.LogError("Cannot add null prefab");
            return null;
        }

        GameObject asset = Instantiate(prefab, position, rotation);
        asset.transform.SetParent(this.transform);
        environmentObjects.Add(asset);

        return asset;
    }

    // Method to remove assets during runtime
    public bool RemoveAsset(GameObject asset)
    {
        if (asset == null || !environmentObjects.Contains(asset))
        {
            return false;
        }

        environmentObjects.Remove(asset);
        Destroy(asset);
        return true;
    }

    // Method to reset the environment to initial state
    public void ResetEnvironment()
    {
        // Remove all dynamically added objects
        for (int i = environmentObjects.Count - 1; i >= 0; i--)
        {
            if (environmentObjects[i] != null)
            {
                DestroyImmediate(environmentObjects[i]);
            }
            environmentObjects.RemoveAt(i);
        }

        // Rebuild environment
        SetupEnvironment();
        SetupLighting();
        SetupPhysics();
        CreateScenarioAssets();

        Debug.Log("Environment reset to initial state");
    }
}
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: Interactive Controls Implementation</summary>

```csharp
// RobotInteractiveControls.cs
using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.Collections;
using System.Collections.Generic;

public class RobotInteractiveControls : MonoBehaviour
{
    [Header("Robot Reference")]
    public Transform robotTransform;  // The robot transform to control

    [Header("Joint Control UI Elements")]
    public Slider[] jointSliders;  // Array of sliders for joint control
    public TextMeshProUGUI[] jointValueTexts;  // Text displays for joint values
    public Button[] jointButtons;  // Buttons for preset poses

    [Header("Joint Names and Configuration")]
    public string[] jointNames;  // Names of joints corresponding to sliders
    public Transform[] jointTransforms;  // Transforms for each joint
    public float[] jointMinValues;  // Minimum joint values
    public float[] jointMaxValues;  // Maximum joint values

    [Header("Robot Control UI")]
    public Slider linearVelocitySlider;
    public Slider angularVelocitySlider;
    public Button walkButton;
    public Button stopButton;
    public Button homePositionButton;

    [Header("Status Display")]
    public TextMeshProUGUI statusText;
    public TextMeshProUGUI jointPositionsText;

    [Header("Animation Controls")]
    public Animator robotAnimator;
    public TMP_Dropdown animationDropdown;

    private Dictionary<string, float> currentJointPositions;
    private bool robotEnabled = true;

    void Start()
    {
        currentJointPositions = new Dictionary<string, float>();

        InitializeJointControls();
        InitializeRobotControls();
        InitializeAnimationControls();
        UpdateStatusDisplay();

        Debug.Log("Robot interactive controls initialized");
    }

    void InitializeJointControls()
    {
        if (jointSliders.Length != jointNames.Length ||
            jointValueTexts.Length != jointNames.Length ||
            jointTransforms.Length != jointNames.Length)
        {
            Debug.LogError("Joint control arrays have inconsistent lengths");
            return;
        }

        // Initialize joint value arrays if not set
        if (jointMinValues == null || jointMinValues.Length != jointNames.Length)
        {
            jointMinValues = new float[jointNames.Length];
            for (int i = 0; i < jointMinValues.Length; i++)
            {
                jointMinValues[i] = -1.57f; // Default: -π/2
            }
        }

        if (jointMaxValues == null || jointMaxValues.Length != jointNames.Length)
        {
            jointMaxValues = new float[jointNames.Length];
            for (int i = 0; i < jointMaxValues.Length; i++)
            {
                jointMaxValues[i] = 1.57f; // Default: π/2
            }
        }

        // Set up slider callbacks
        for (int i = 0; i < jointSliders.Length; i++)
        {
            int index = i; // Closure variable
            float initialValue = (jointMinValues[i] + jointMaxValues[i]) / 2f;

            jointSliders[i].minValue = jointMinValues[i];
            jointSliders[i].maxValue = jointMaxValues[i];
            jointSliders[i].value = initialValue;

            jointSliders[i].onValueChanged.AddListener(delegate { OnJointSliderChanged(index); });

            // Initialize current positions
            currentJointPositions[jointNames[i]] = initialValue;
            UpdateJointValueDisplay(index);
        }

        // Set up joint buttons for preset positions
        if (jointButtons != null)
        {
            for (int i = 0; i < jointButtons.Length; i++)
            {
                int index = i;
                jointButtons[i].onClick.AddListener(delegate { OnJointButtonClicked(index); });
            }
        }
    }

    void InitializeRobotControls()
    {
        if (linearVelocitySlider != null)
        {
            linearVelocitySlider.minValue = 0f;
            linearVelocitySlider.maxValue = 1f;
            linearVelocitySlider.value = 0.3f; // Default walking speed
        }

        if (angularVelocitySlider != null)
        {
            angularVelocitySlider.minValue = -1f;
            angularVelocitySlider.maxValue = 1f;
            angularVelocitySlider.value = 0f; // Default: no turning
        }

        if (walkButton != null)
        {
            walkButton.onClick.AddListener(OnWalkButtonClicked);
        }

        if (stopButton != null)
        {
            stopButton.onClick.AddListener(OnStopButtonClicked);
        }

        if (homePositionButton != null)
        {
            homePositionButton.onClick.AddListener(OnHomePositionButtonClicked);
        }
    }

    void InitializeAnimationControls()
    {
        if (animationDropdown != null && robotAnimator != null)
        {
            // Populate animation dropdown
            animationDropdown.options.Clear();
            animationDropdown.options.Add(new TMP_Dropdown.OptionData("Idle"));
            animationDropdown.options.Add(new TMP_Dropdown.OptionData("Walking"));
            animationDropdown.options.Add(new TMP_Dropdown.OptionData("Standing"));
            animationDropdown.options.Add(new TMP_Dropdown.OptionData("Waving"));
            animationDropdown.options.Add(new TMP_Dropdown.OptionData("Saluting"));
            animationDropdown.RefreshShownValue();

            animationDropdown.onValueChanged.AddListener(delegate { OnAnimationChanged(); });
        }
    }

    void OnJointSliderChanged(int jointIndex)
    {
        if (jointIndex < 0 || jointIndex >= jointNames.Length) return;

        string jointName = jointNames[jointIndex];
        float newValue = jointSliders[jointIndex].value;

        // Update joint position in dictionary
        currentJointPositions[jointName] = newValue;

        // Update joint transform if available
        if (jointTransforms[jointIndex] != null)
        {
            // For revolute joints, rotate around Z axis
            jointTransforms[jointIndex].localRotation = Quaternion.Euler(0, 0, newValue * Mathf.Rad2Deg);
        }

        // Update display
        UpdateJointValueDisplay(jointIndex);
        UpdateStatusDisplay();
    }

    void UpdateJointValueDisplay(int jointIndex)
    {
        if (jointValueTexts != null && jointIndex < jointValueTexts.Length)
        {
            jointValueTexts[jointIndex].text = $"{jointNames[jointIndex]}: {jointSliders[jointIndex].value:F2}";
        }
    }

    void OnJointButtonClicked(int buttonIndex)
    {
        if (buttonIndex < 0 || buttonIndex >= jointNames.Length) return;

        // Example: Toggle joint position between min and max
        if (jointSliders[buttonIndex].value == jointMinValues[buttonIndex])
        {
            jointSliders[buttonIndex].value = jointMaxValues[buttonIndex];
        }
        else
        {
            jointSliders[buttonIndex].value = jointMinValues[buttonIndex];
        }
    }

    void OnWalkButtonClicked()
    {
        if (!robotEnabled) return;

        // Set walking animation if available
        if (robotAnimator != null)
        {
            robotAnimator.SetBool("IsWalking", true);
            robotAnimator.SetFloat("WalkSpeed", linearVelocitySlider.value);
        }

        // In a real implementation, this would send a command to the ROS 2 system
        Debug.Log("Walk command sent");
        UpdateStatusDisplay();
    }

    void OnStopButtonClicked()
    {
        // Stop walking animation if available
        if (robotAnimator != null)
        {
            robotAnimator.SetBool("IsWalking", false);
            robotAnimator.SetFloat("WalkSpeed", 0f);
        }

        // Stop any movement
        if (linearVelocitySlider != null) linearVelocitySlider.value = 0f;
        if (angularVelocitySlider != null) angularVelocitySlider.value = 0f;

        Debug.Log("Stop command sent");
        UpdateStatusDisplay();
    }

    void OnHomePositionButtonClicked()
    {
        // Return all joints to home position (middle of range)
        for (int i = 0; i < jointSliders.Length; i++)
        {
            float homePosition = (jointMinValues[i] + jointMaxValues[i]) / 2f;
            jointSliders[i].value = homePosition;
            currentJointPositions[jointNames[i]] = homePosition;
        }

        // Reset animation to idle
        if (robotAnimator != null)
        {
            robotAnimator.SetBool("IsWalking", false);
            robotAnimator.SetTrigger("ResetToHome");
        }

        Debug.Log("Home position command sent");
        UpdateStatusDisplay();
    }

    void OnAnimationChanged()
    {
        if (robotAnimator == null || animationDropdown == null) return;

        string selectedAnimation = animationDropdown.options[animationDropdown.value].text;

        // Set animation parameters based on selection
        switch (selectedAnimation)
        {
            case "Idle":
                robotAnimator.SetBool("IsWalking", false);
                robotAnimator.SetBool("IsStanding", true);
                robotAnimator.SetBool("IsWaving", false);
                robotAnimator.SetBool("IsSaluting", false);
                break;
            case "Walking":
                robotAnimator.SetBool("IsWalking", true);
                robotAnimator.SetBool("IsStanding", false);
                robotAnimator.SetFloat("WalkSpeed", linearVelocitySlider.value);
                break;
            case "Standing":
                robotAnimator.SetBool("IsWalking", false);
                robotAnimator.SetBool("IsStanding", true);
                break;
            case "Waving":
                robotAnimator.SetBool("IsWaving", true);
                robotAnimator.SetBool("IsSaluting", false);
                break;
            case "Saluting":
                robotAnimator.SetBool("IsSaluting", true);
                robotAnimator.SetBool("IsWaving", false);
                break;
        }

        Debug.Log($"Animation changed to: {selectedAnimation}");
    }

    void UpdateStatusDisplay()
    {
        if (statusText != null)
        {
            string status = robotEnabled ? "ACTIVE" : "DISABLED";
            statusText.text = $"Robot Status: {status}\n" +
                             $"Linear Vel: {linearVelocitySlider?.value:F2}\n" +
                             $"Angular Vel: {angularVelocitySlider?.value:F2}";
        }

        if (jointPositionsText != null)
        {
            string jointInfo = "Current Joint Positions:\n";
            foreach (var kvp in currentJointPositions)
            {
                jointInfo += $"{kvp.Key}: {kvp.Value:F2}\n";
            }
            jointPositionsText.text = jointInfo;
        }
    }

    // Simulate sending joint positions to ROS 2 system
    public void SendJointCommandsToROS2()
    {
        if (!robotEnabled) return;

        // In a real implementation, this would send the joint positions
        // to the ROS 2 system via the Unity ROS 2 bridge
        List<float> positions = new List<float>();
        foreach (string jointName in jointNames)
        {
            positions.Add(currentJointPositions[jointName]);
        }

        Debug.Log($"Sending joint commands to ROS 2: {string.Join(", ", positions)}");

        // This would typically call a ROS 2 publisher to send joint trajectory commands
        // Example: ROS2UnityBridge.PublishJointTrajectory(jointNames, positions.ToArray());
    }

    // Simulate receiving joint positions from ROS 2 system
    public void ReceiveJointPositionsFromROS2(Dictionary<string, float> jointPositions)
    {
        foreach (var kvp in jointPositions)
        {
            if (currentJointPositions.ContainsKey(kvp.Key))
            {
                currentJointPositions[kvp.Key] = kvp.Value;

                // Find the corresponding slider and update it
                for (int i = 0; i < jointNames.Length; i++)
                {
                    if (jointNames[i] == kvp.Key)
                    {
                        jointSliders[i].SetValueWithoutNotify(kvp.Value);
                        UpdateJointValueDisplay(i);

                        // Update the joint transform
                        if (jointTransforms[i] != null)
                        {
                            jointTransforms[i].localRotation = Quaternion.Euler(0, 0, kvp.Value * Mathf.Rad2Deg);
                        }
                        break;
                    }
                }
            }
        }

        UpdateStatusDisplay();
    }

    // Toggle robot enable/disable
    public void ToggleRobotEnabled()
    {
        robotEnabled = !robotEnabled;
        string state = robotEnabled ? "enabled" : "disabled";
        Debug.Log($"Robot {state}");

        // Disable controls when robot is disabled
        if (jointSliders != null)
        {
            foreach (Slider slider in jointSliders)
            {
                slider.interactable = robotEnabled;
            }
        }

        if (walkButton != null) walkButton.interactable = robotEnabled;
        if (stopButton != null) stopButton.interactable = robotEnabled;

        UpdateStatusDisplay();
    }

    void Update()
    {
        // Send joint commands periodically if auto-send is enabled
        if (Time.time % 0.1f < Time.deltaTime) // Every 0.1 seconds
        {
            SendJointCommandsToROS2();
        }
    }
}
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Rendering Performance Optimization</summary>

```csharp
// RenderingPerformanceOptimizer.cs
using UnityEngine;
using System.Collections.Generic;

public class RenderingPerformanceOptimizer : MonoBehaviour
{
    [Header("LOD Configuration")]
    public LODGroup[] robotLODs;
    public float[] lodDistances = { 10f, 20f, 50f };
    public int[] lodRenderersCount = { 50, 20, 5 }; // Number of renderers for each LOD

    [Header("Occlusion Culling")]
    public bool enableOcclusionCulling = true;

    [Header("Dynamic Batching")]
    public bool enableDynamicBatching = true;

    [Header("Lighting Optimization")]
    public Light[] lightsToOptimize;
    public float maxLightRange = 10f;
    public int maxShadowResolution = 512;

    [Header("Material Optimization")]
    public Material[] robotMaterials;
    public Shader optimizedShader;

    [Header("Performance Metrics")]
    public TextMeshProUGUI performanceText;
    public float updateInterval = 0.5f;

    private float lastUpdateTime;
    private int lastFrameCount;
    private float fps;
    private List<Renderer> robotRenderers;
    private List<ParticleSystem> robotParticleSystems;

    void Start()
    {
        robotRenderers = new List<Renderer>();
        robotParticleSystems = new List<ParticleSystem>();

        // Collect all renderers and particle systems
        CollectRobotComponents();

        // Apply optimizations
        ConfigureLODSystems();
        OptimizeLighting();
        OptimizeMaterials();
        ConfigureRenderingSettings();

        lastUpdateTime = Time.realtimeSinceStartup;
        lastFrameCount = 0;

        Debug.Log("Rendering performance optimizer initialized");
    }

    void CollectRobotComponents()
    {
        // Find all robot-related renderers
        Renderer[] allRenderers = this.GetComponentsInChildren<Renderer>();
        foreach (Renderer renderer in allRenderers)
        {
            robotRenderers.Add(renderer);
        }

        // Find all particle systems (for sensor visualization, etc.)
        ParticleSystem[] allParticleSystems = this.GetComponentsInChildren<ParticleSystem>();
        foreach (ParticleSystem ps in allParticleSystems)
        {
            robotParticleSystems.Add(ps);
        }

        Debug.Log($"Collected {robotRenderers.Count} renderers and {robotParticleSystems.Count} particle systems");
    }

    void ConfigureLODSystems()
    {
        if (robotLODs == null || robotLODs.Length == 0)
        {
            // Create LOD groups programmatically if not provided
            CreateLODGroupsAutomatically();
            return;
        }

        // Configure existing LOD groups
        foreach (LODGroup lodGroup in robotLODs)
        {
            ConfigureLODGroup(lodGroup);
        }
    }

    void CreateLODGroupsAutomatically()
    {
        // For each major robot part, create an LOD group
        Transform[] robotParts = this.GetComponentsInChildren<Transform>();

        foreach (Transform part in robotParts)
        {
            // Create LOD group for parts with multiple renderers
            Renderer[] partRenderers = part.GetComponents<Renderer>();
            if (partRenderers.Length > 1)
            {
                LODGroup lodGroup = part.gameObject.AddComponent<LODGroup>();
                ConfigureLODGroup(lodGroup);
            }
        }
    }

    void ConfigureLODGroup(LODGroup lodGroup)
    {
        // Create LOD levels based on distance
        LOD[] lods = new LOD[lodDistances.Length];

        for (int i = 0; i < lodDistances.Length; i++)
        {
            // Calculate which renderers to include at this LOD level
            Renderer[] renderersForLOD = GetRenderersForLODLevel(lodGroup, i);

            // Create a combined mesh or hide renderers for lower LODs
            if (i == 0) // Highest detail - keep all renderers
            {
                lods[i] = new LOD(lodDistances[i], renderersForLOD);
            }
            else // Lower detail - fewer renderers
            {
                Renderer[] lowDetailRenderers = GetLowDetailRenderers(renderersForLOD, lodRenderersCount[i]);
                lods[i] = new LOD(lodDistances[i], lowDetailRenderers);
            }
        }

        lodGroup.SetLODs(lods);
        lodGroup.RecalculateBounds();

        Debug.Log($"Configured LOD group with {lods.Length} levels");
    }

    Renderer[] GetRenderersForLODLevel(LODGroup lodGroup, int level)
    {
        // Return renderers for the given LOD level
        Renderer[] allRenderers = lodGroup.GetComponents<Renderer>();
        return allRenderers;
    }

    Renderer[] GetLowDetailRenderers(Renderer[] originalRenderers, int count)
    {
        // Return a subset of renderers for low-detail LOD
        if (count >= originalRenderers.Length)
        {
            return originalRenderers;
        }

        Renderer[] lowDetailRenderers = new Renderer[count];
        for (int i = 0; i < count; i++)
        {
            lowDetailRenderers[i] = originalRenderers[i];
        }

        // Hide remaining renderers
        for (int i = count; i < originalRenderers.Length; i++)
        {
            originalRenderers[i].enabled = false;
        }

        return lowDetailRenderers;
    }

    void OptimizeLighting()
    {
        if (lightsToOptimize == null) return;

        foreach (Light light in lightsToOptimize)
        {
            // Reduce light range if too large
            if (light.range > maxLightRange)
            {
                light.range = maxLightRange;
            }

            // Optimize shadow resolution
            if (light.shadows != LightShadows.None)
            {
                light.shadowResolution = (LightShadowResolution)Mathf.Min((int)light.shadowResolution, maxShadowResolution);
            }

            // Use appropriate light type for performance
            if (light.type == LightType.Point)
            {
                // Point lights are more expensive, consider using spot lights instead
                if (light.range > 5f)
                {
                    // For large areas, consider using multiple smaller lights instead of one large light
                    Debug.LogWarning($"Consider using multiple smaller lights instead of one large point light: {light.name}");
                }
            }
        }
    }

    void OptimizeMaterials()
    {
        if (robotMaterials == null) return;

        foreach (Material mat in robotMaterials)
        {
            if (mat != null)
            {
                // Use optimized shader if available
                if (optimizedShader != null)
                {
                    mat.shader = optimizedShader;
                }

                // Reduce expensive material properties
                if (mat.HasProperty("_Metallic"))
                {
                    mat.SetFloat("_Metallic", 0f); // Disable metallic reflections
                }

                if (mat.HasProperty("_Smoothness"))
                {
                    mat.SetFloat("_Smoothness", 0.2f); // Reduce smoothness
                }

                // Use texture compression
                if (mat.mainTexture != null)
                {
                    Texture2D texture = mat.mainTexture as Texture2D;
                    if (texture != null)
                    {
                        // In editor, you would compress the texture
                        // For runtime, we'll just log a recommendation
                        Debug.Log($"Recommendation: Compress texture {texture.name} for better performance");
                    }
                }
            }
        }
    }

    void ConfigureRenderingSettings()
    {
        // Configure occlusion culling
        if (enableOcclusionCulling)
        {
            // This is typically configured in the Scene settings, not at runtime
            // But we can provide a warning if it's not enabled
            if (!OcclusionCulling.enabled)
            {
                Debug.LogWarning("Occlusion culling is not enabled in scene - consider enabling for better performance");
            }
        }

        // Dynamic batching is controlled by Unity, but we can ensure materials support it
        if (enableDynamicBatching)
        {
            // Ensure robot materials support dynamic batching
            foreach (Material mat in robotMaterials)
            {
                if (mat != null)
                {
                    // Dynamic batching requires materials to share the same properties
                    mat.enableInstancing = false; // Instancing conflicts with dynamic batching
                }
            }
        }

        // Configure particle systems for performance
        foreach (ParticleSystem ps in robotParticleSystems)
        {
            var main = ps.main;
            main.maxParticles = Mathf.Min(main.maxParticles, 1000); // Limit particles

            var emission = ps.emission;
            emission.rateOverTime = Mathf.Min(emission.rateOverTime.constant, 50f); // Limit emission rate
        }
    }

    // Frustum culling optimization for sensor visualization
    public void OptimizeSensorVisualization(Camera mainCamera)
    {
        // Only render sensor visualization when the sensor is within camera view
        foreach (Renderer renderer in robotRenderers)
        {
            // Check if renderer is part of sensor visualization
            if (renderer.name.Contains("LiDAR") || renderer.name.Contains("Camera") ||
                renderer.name.Contains("Point") || renderer.CompareTag("SensorVisualization"))
            {
                // Only render if within camera frustum
                renderer.enabled = IsInCameraFrustum(renderer.bounds, mainCamera);
            }
        }
    }

    bool IsInCameraFrustum(Bounds bounds, Camera camera)
    {
        // Check if bounds are within camera frustum
        Plane[] planes = GeometryUtility.CalculateFrustumPlanes(camera);
        return GeometryUtility.TestPlanesAABB(planes, bounds);
    }

    // Update performance metrics
    void UpdatePerformanceMetrics()
    {
        if (performanceText != null)
        {
            float currentFPS = 1f / Time.unscaledDeltaTime;
            fps = 0.9f * fps + 0.1f * currentFPS; // Smooth FPS

            performanceText.text = $"FPS: {fps:F1}\n" +
                                  $"Tris: {(int)(Time.renderedFrameCount * 1000):F0}\n" +
                                  $"Renderers: {robotRenderers.Count}\n" +
                                  $"Particles: {robotParticleSystems.Count}";
        }
    }

    void Update()
    {
        // Update performance metrics
        if (Time.realtimeSinceStartup - lastUpdateTime >= updateInterval)
        {
            int frames = Time.frameCount - lastFrameCount;
            fps = frames / (Time.realtimeSinceStartup - lastUpdateTime);

            lastUpdateTime = Time.realtimeSinceStartup;
            lastFrameCount = Time.frameCount;

            UpdatePerformanceMetrics();
        }

        // Perform occlusion culling check
        Camera mainCam = Camera.main;
        if (mainCam != null)
        {
            OptimizeSensorVisualization(mainCam);
        }
    }

    // Method to toggle performance optimization levels
    public void SetPerformanceLevel(int level)
    {
        switch (level)
        {
            case 0: // Low (mobile/VR)
                QualitySettings.SetQualityLevel(0);
                OptimizeForMobile();
                break;
            case 1: // Medium (desktop)
                QualitySettings.SetQualityLevel(2);
                OptimizeForDesktop();
                break;
            case 2: // High (development)
                QualitySettings.SetQualityLevel(4);
                OptimizeForQuality();
                break;
        }

        Debug.Log($"Performance level set to: {level}");
    }

    void OptimizeForMobile()
    {
        // Aggressive optimization for mobile/VR
        foreach (Renderer renderer in robotRenderers)
        {
            renderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.Off;
            renderer.receiveShadows = false;
        }

        // Reduce particle systems
        foreach (ParticleSystem ps in robotParticleSystems)
        {
            var main = ps.main;
            main.maxParticles = Mathf.Min(main.maxParticles, 100);
        }

        // Use mobile-optimized shaders
        if (optimizedShader != null)
        {
            foreach (Material mat in robotMaterials)
            {
                if (mat != null)
                {
                    mat.shader = optimizedShader;
                }
            }
        }
    }

    void OptimizeForDesktop()
    {
        // Moderate optimization for desktop
        foreach (Renderer renderer in robotRenderers)
        {
            renderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.On;
            renderer.receiveShadows = true;
        }

        // Moderate particle settings
        foreach (ParticleSystem ps in robotParticleSystems)
        {
            var main = ps.main;
            main.maxParticles = Mathf.Min(main.maxParticles, 500);
        }
    }

    void OptimizeForQuality()
    {
        // Minimal optimization, prioritize quality
        foreach (Renderer renderer in robotRenderers)
        {
            renderer.shadowCastingMode = UnityEngine.Rendering.ShadowCastingMode.TwoSided;
            renderer.receiveShadows = true;
        }

        // Allow full particle settings
        foreach (ParticleSystem ps in robotParticleSystems)
        {
            var main = ps.main;
            main.maxParticles = 10000; // Reset to higher value
        }
    }
}
```

</details>

## 2.8 Mini-Project: Unity Scene for Humanoid Robot with LiDAR Feedback

Create a complete Unity scene that visualizes a humanoid robot walking in a custom environment while displaying real-time LiDAR feedback. The scene should include:

1. A humanoid robot model imported from URDF with proper joint configuration
2. A walking animation system that moves the robot through the environment
3. LiDAR point cloud visualization that updates in real-time
4. Camera system that follows the robot with multiple viewing angles
5. UI elements showing robot status and sensor data
6. Interactive controls for adjusting robot behavior and visualization parameters

The project should demonstrate the complete pipeline from ROS 2 data to Unity visualization, including proper coordinate system handling, data conversion, and real-time rendering optimization.

## 2.9 Summary

This chapter has covered the essential aspects of Unity visualization for humanoid robots, including high-fidelity rendering, human-robot interaction interfaces, robot model import and integration, and real-time ROS 2 data visualization. Unity's powerful rendering capabilities combined with its extensive development tools make it an excellent platform for creating sophisticated visualization environments for robotics applications.

Key concepts covered include:
- Setting up Unity for robotics visualization with proper lighting, materials, and rendering
- Importing and configuring URDF robot models with correct scale and joint mapping
- Creating human-robot interaction interfaces with avatars, gestures, and input devices
- Visualizing real-time sensor data from ROS 2 topics
- Implementing complete visualization workflows with proper data flow management

The examples and exercises provided demonstrate practical applications of these concepts, preparing you to create your own sophisticated visualization environments for humanoid robot development and research.