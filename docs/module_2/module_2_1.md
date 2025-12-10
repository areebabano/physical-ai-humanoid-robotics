---
title: "Module 2.1 - Chapter 1: Gazebo Simulation"
sidebar_position: 1
---

# Module 2.1 - Chapter 1: Gazebo Simulation

## 1.0 Introduction to Gazebo Simulation

### What is Gazebo?

Gazebo is a 3D dynamic simulator that enables accurate and efficient simulation of robotic systems. It provides physics simulation, sensor simulation, and rendering capabilities that allow developers to test and validate robotic applications in realistic virtual environments before deploying them on physical robots. For humanoid robotics, Gazebo offers essential tools to simulate complex multi-body dynamics, sensor data, and environmental interactions.

```
Gazebo Simulation Architecture
┌─────────────────────────────────────────────────────────────────┐
│                        Gazebo Simulator                         │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │   Physics       │  │   Rendering      │  │   Sensors       │ │
│  │   Engine        │  │   Engine         │  │   Simulation    │ │
│  │ (ODE, Bullet,   │  │ (OGRE, OpenGL)   │  │ (LiDAR, Camera,│ │
│  │  SimBody)       │  │                  │  │  IMU, etc.)     │ │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘ │
│         │                       │                       │       │
│         ▼                       ▼                       ▼       │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │   Collision     │  │   Visualization  │  │   Data Streams  │ │
│  │   Detection     │  │   & GUI          │  │   (ROS 2 msgs)  │ │
│  │                 │  │                  │  │                 │ │
│  │   Dynamics      │  │   World Editor   │  │   Plugins       │ │
│  └─────────────────┘  └──────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

Gazebo is used in:
- **Robot development**: Testing algorithms before deployment
- **Research**: Prototyping new control strategies
- **Education**: Teaching robotics concepts
- **Competition**: Providing standardized simulation environments

### Gazebo vs. Other Simulators

| Feature | Gazebo | PyBullet | MuJoCo | Webots |
|---------|--------|----------|--------|--------|
| Physics Accuracy | High | High | Very High | High |
| Sensor Simulation | Excellent | Good | Good | Excellent |
| Graphics Quality | Excellent | Good | Good | Excellent |
| ROS Integration | Native | Good | Good | Good |
| Free/Open Source | Yes | Yes | No | Yes |

:::note
Gazebo is the de facto standard for ROS-based robotics simulation, offering excellent integration with the ROS ecosystem.
:::

## 1.1 Physics Engine Fundamentals

### Understanding Dynamics and Gravity

Gazebo's physics engine simulates real-world physics by modeling forces, torques, collisions, and dynamics. For humanoid robots, accurate physics simulation is crucial for realistic movement and interaction with the environment.

```xml
<!-- Example physics configuration in SDF -->
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics engine configuration -->
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>
          <sor>1.3</sor>
        </solver>
        <constraints>
          <cfm>0.0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>
  </world>
</sdf>
```

### Collision Detection and Response

Collision detection in Gazebo is handled through collision meshes and contact detection algorithms:

```xml
<!-- Collision detection example -->
<link name="humanoid_link">
  <collision name="collision">
    <geometry>
      <cylinder>
        <radius>0.05</radius>
        <length>0.3</length>
      </cylinder>
    </geometry>
    <surface>
      <friction>
        <ode>
          <mu>0.5</mu>
          <mu2>0.5</mu2>
          <slip1>0.0</slip1>
          <slip2>0.0</slip2>
        </ode>
      </friction>
      <bounce>
        <restitution_coefficient>0.1</restitution_coefficient>
        <threshold>100000.0</threshold>
      </bounce>
      <contact>
        <ode>
          <soft_cfm>0.0</soft_cfm>
          <soft_erp>0.2</soft_erp>
          <kp>1000000000000.0</kp>
          <kd>1.0</kd>
          <max_vel>100.0</max_vel>
          <min_depth>0.001</min_depth>
        </ode>
      </contact>
    </surface>
  </collision>
</link>
```

### Friction and Contact Parameters

For humanoid robots, friction parameters are critical for realistic walking and manipulation:

| Parameter | Description | Typical Value for Humanoid |
|-----------|-------------|----------------------------|
| `mu` (static friction) | Resistance to sliding | 0.5-0.8 for feet on floor |
| `mu2` (dynamic friction) | Friction during sliding | Similar to mu |
| `restitution_coefficient` | Bounciness | 0.0-0.2 for stability |
| `max_vel` | Maximum contact velocity | 100.0 (default) |
| `min_depth` | Penetration depth | 0.001 (default) |

## 1.2 Sensor Simulation

### LiDAR Sensor Integration

LiDAR sensors are essential for humanoid navigation and mapping. Here's how to configure them in Gazebo:

```xml
<!-- LiDAR sensor configuration -->
<gazebo reference="lidar_link">
  <sensor name="lidar_front" type="ray">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>10</update_rate>
    <ray>
      <scan>
        <horizontal>
          <samples>360</samples>
          <resolution>1</resolution>
          <min_angle>-3.14159</min_angle>
          <max_angle>3.14159</max_angle>
        </horizontal>
      </scan>
      <range>
        <min>0.1</min>
        <max>10.0</max>
        <resolution>0.01</resolution>
      </range>
    </ray>
    <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
      <ros>
        <namespace>/humanoid_robot</namespace>
        <remapping>~/out:=scan</remapping>
      </ros>
      <output_type>sensor_msgs/LaserScan</output_type>
    </plugin>
  </sensor>
</gazebo>
```

### Depth Camera Simulation

Depth cameras provide 3D perception capabilities for humanoid robots:

```xml
<!-- Depth camera configuration -->
<gazebo reference="camera_link">
  <sensor name="depth_camera" type="depth">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>30</update_rate>
    <camera name="head">
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
      <noise>
        <type>gaussian</type>
        <mean>0.0</mean>
        <stddev>0.007</stddev>
      </noise>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
      <ros>
        <namespace>/humanoid_robot</namespace>
        <remapping>~/rgb/image_raw:=camera/color/image_raw</remapping>
        <remapping>~/depth/image_raw:=camera/depth/image_raw</remapping>
        <remapping>~/depth/camera_info:=camera/depth/camera_info</remapping>
      </ros>
      <camera_name>camera</camera_name>
      <frame_name>camera_optical_frame</frame_name>
    </plugin>
  </sensor>
</gazebo>
```

### IMU Sensor Simulation

IMU sensors are critical for humanoid balance and orientation:

```xml
<!-- IMU sensor configuration -->
<gazebo reference="imu_link">
  <sensor name="imu_sensor" type="imu">
    <always_on>true</always_on>
    <update_rate>100</update_rate>
    <visualize>false</visualize>
    <imu>
      <orientation>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.001</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.001</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.001</stddev>
          </noise>
        </z>
      </orientation>
      <angular_velocity>
        <x>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.001</stddev>
          </noise>
        </x>
        <y>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.001</stddev>
          </noise>
        </y>
        <z>
          <noise type="gaussian">
            <mean>0.0</mean>
            <stddev>0.001</stddev>
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
    <plugin name="imu_plugin" filename="libgazebo_ros_imu.so">
      <ros>
        <namespace>/humanoid_robot</namespace>
        <remapping>~/out:=imu/data</remapping>
      </ros>
      <frame_name>imu_link</frame_name>
      <initial_orientation_as_reference>false</initial_orientation_as_reference>
    </plugin>
  </sensor>
</gazebo>
```

### Common Gazebo Sensors Table

| Sensor Type | Plugin | ROS Message | Use Case |
|-------------|--------|-------------|----------|
| LiDAR | `libgazebo_ros_ray_sensor.so` | `sensor_msgs/LaserScan` | Navigation, mapping |
| RGB Camera | `libgazebo_ros_camera.so` | `sensor_msgs/Image` | Vision processing |
| Depth Camera | `libgazebo_ros_openni_kinect.so` | `sensor_msgs/Image` | 3D perception |
| IMU | `libgazebo_ros_imu.so` | `sensor_msgs/Imu` | Orientation, balance |
| GPS | `libgazebo_ros_gps.so` | `sensor_msgs/NavSatFix` | Global positioning |
| Force/Torque | `libgazebo_ros_ft_sensor.so` | `geometry_msgs/WrenchStamped` | Manipulation feedback |

## 1.3 Model Integration: URDF/Xacro to Gazebo

### Importing URDF Models into Gazebo

The integration of URDF models with Gazebo requires special Gazebo-specific tags:

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include other xacro files -->
  <xacro:include filename="$(find humanoid_description)/urdf/materials.xacro" />
  <xacro:include filename="$(find humanoid_description)/urdf/transmission_macros.xacro" />

  <!-- Properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="base_mass" value="10.0" />
  <xacro:property name="base_radius" value="0.2" />
  <xacro:property name="base_length" value="0.3" />

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder radius="${base_radius}" length="${base_length}"/>
      </geometry>
      <material name="blue_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="${base_radius}" length="${base_length}"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="${base_mass}"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.15"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="neck_joint" type="revolute">
    <parent link="base_link"/>
    <child link="head_link"/>
    <origin xyz="0 0 ${base_length/2 + 0.1}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="10" velocity="1"/>
  </joint>

  <link name="head_link">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="white_material"/>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.002" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Left Arm -->
  <joint name="left_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_upper_arm_link"/>
    <origin xyz="${base_radius + 0.05} 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="50" velocity="2"/>
  </joint>

  <link name="left_upper_arm_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
      <material name="gray_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm_link"/>
    <child link="left_lower_arm_link"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="30" velocity="2"/>
  </joint>

  <link name="left_lower_arm_link">
    <visual>
      <geometry>
        <cylinder radius="0.04" length="0.25"/>
      </geometry>
      <material name="gray_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.04" length="0.25"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.0005"/>
    </inertial>
  </link>

  <!-- Gazebo-specific tags for simulation -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/humanoid_robot</robotNamespace>
      <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
    </plugin>
  </gazebo>

  <!-- Gazebo material definitions -->
  <gazebo reference="base_link">
    <material>Gazebo/Blue</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>

  <gazebo reference="head_link">
    <material>Gazebo/White</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>

  <gazebo reference="left_upper_arm_link">
    <material>Gazebo/Grey</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>

  <gazebo reference="left_lower_arm_link">
    <material>Gazebo/Grey</material>
    <mu1>0.2</mu1>
    <mu2>0.2</mu2>
  </gazebo>

</robot>
```

### Xacro Macros for Gazebo Integration

Using Xacro macros to simplify Gazebo integration:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Gazebo material macro -->
  <xacro:macro name="gazebo_material" params="link color">
    <gazebo reference="${link}">
      <material>Gazebo/${color}</material>
      <mu1>0.2</mu1>
      <mu2>0.2</mu2>
    </gazebo>
  </xacro:macro>

  <!-- Gazebo transmission macro -->
  <xacro:macro name="gazebo_transmission" params="joint_name hardware_interface">
    <gazebo>
      <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
        <robotNamespace>/humanoid_robot</robotNamespace>
        <robotSimType>gazebo_ros_control/DefaultRobotHWSim</robotSimType>
      </plugin>
    </gazebo>
  </xacro:macro>

  <!-- Sensor mounting macro -->
  <xacro:macro name="mount_lidar" params="name parent_link xyz rpy">
    <joint name="${name}_joint" type="fixed">
      <parent link="${parent_link}"/>
      <child link="${name}_link"/>
      <origin xyz="${xyz}" rpy="${rpy}"/>
    </joint>

    <link name="${name}_link">
      <visual>
        <geometry>
          <box size="0.05 0.05 0.05"/>
        </geometry>
      </visual>
      <collision>
        <geometry>
          <box size="0.05 0.05 0.05"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.1"/>
        <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
      </inertial>
    </link>

    <gazebo reference="${name}_link">
      <sensor name="${name}" type="ray">
        <pose>0 0 0 0 0 0</pose>
        <visualize>true</visualize>
        <update_rate>10</update_rate>
        <ray>
          <scan>
            <horizontal>
              <samples>360</samples>
              <resolution>1</resolution>
              <min_angle>-3.14159</min_angle>
              <max_angle>3.14159</max_angle>
            </horizontal>
          </scan>
          <range>
            <min>0.1</min>
            <max>10.0</max>
            <resolution>0.01</resolution>
          </range>
        </ray>
        <plugin name="${name}_controller" filename="libgazebo_ros_ray_sensor.so">
          <ros>
            <namespace>/humanoid_robot</namespace>
            <remapping>~/out:=scan</remapping>
          </ros>
          <output_type>sensor_msgs/LaserScan</output_type>
        </plugin>
      </sensor>
    </gazebo>
  </xacro:macro>

</robot>
```

## 1.4 Environment Setup

### World File Configuration

Creating a world file for humanoid robot simulation:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_indoor">
    <!-- Include ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Include sun -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Physics engine -->
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>
          <sor>1.3</sor>
        </solver>
        <constraints>
          <cfm>0.0</cfm>
          <erp>0.2</erp>
          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <!-- Indoor environment -->
    <model name="room_walls">
      <pose>0 0 2.5 0 0 0</pose>
      <link name="wall1">
        <pose>-5 0 2.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.1 10 5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.1 10 5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>100</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>

      <link name="wall2">
        <pose>5 0 2.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.1 10 5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.1 10 5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>100</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>

      <link name="wall3">
        <pose>0 -5 2.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>10 0.1 5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>10 0.1 5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>100</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>

      <link name="wall4">
        <pose>0 5 2.5 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>10 0.1 5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>10 0.1 5</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.8 0.8 1</ambient>
            <diffuse>0.8 0.8 0.8 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>100</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Furniture for realistic environment -->
    <model name="table">
      <pose>2 2 0.4 0 0 0</pose>
      <link name="table_top">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 0.6 0.02</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 0.6 0.02</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.3 0.1 1</ambient>
            <diffuse>0.5 0.3 0.1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>20</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>
      <link name="leg1">
        <pose>0.4 0.2 -0.3 0 0 0</pose>
        <collision name="collision">
          <geometry>
            <box>
              <size>0.05 0.05 0.6</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.05 0.05 0.6</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.3 0.1 1</ambient>
            <diffuse>0.5 0.3 0.1 1</diffuse>
          </material>
        </visual>
        <inertial>
          <mass>2</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Lighting configuration -->
    <light name='directional_light' type='directional'>
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

  </world>
</sdf>
```

### Physics Parameters Effects Table

| Parameter | Effect on Humanoid Simulation | Recommended Value |
|-----------|-------------------------------|-------------------|
| `max_step_size` | Simulation accuracy vs speed | 0.001s for stability |
| `real_time_factor` | Speed relative to real time | 1.0 for real-time |
| `real_time_update_rate` | Physics update frequency | 1000Hz for accuracy |
| `contact_surface_layer` | Penetration tolerance | 0.001m for stability |
| `contact_max_correcting_vel` | Contact velocity limit | 100m/s (default) |
| `erp` | Error reduction parameter | 0.2 for stability |
| `cfm` | Constraint force mixing | 0.0 (default) |

## 1.5 Real-time Simulation and Control

### Simulation Control and Timing

Gazebo provides real-time simulation capabilities that can be controlled programmatically:

```python
#!/usr/bin/env python3
# simulation_control.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float32
from gazebo_msgs.srv import SetPhysicsProperties, GetPhysicsProperties
from gazebo_msgs.msg import LinkStates
import time


class SimulationController(Node):
    def __init__(self):
        super().__init__('simulation_controller')

        # Services for physics control
        self.set_physics_client = self.create_client(
            SetPhysicsProperties, '/gazebo/set_physics_properties')
        self.get_physics_client = self.create_client(
            GetPhysicsProperties, '/gazebo/get_physics_properties')

        # Publishers for simulation control
        self.pause_pub = self.create_publisher(Bool, '/gazebo/pause_physics', 10)
        self.unpause_pub = self.create_publisher(Bool, '/gazebo/unpause_physics', 10)

        # Subscriber for link states
        self.link_states_sub = self.create_subscription(
            LinkStates, '/gazebo/link_states', self.link_states_callback, 10)

        # Timer for simulation monitoring
        self.monitor_timer = self.create_timer(0.1, self.monitor_simulation)

        # Internal state
        self.simulation_paused = False
        self.link_states = None

        self.get_logger().info('Simulation controller initialized')

    def link_states_callback(self, msg):
        """Receive link states from Gazebo"""
        self.link_states = msg

    def pause_simulation(self):
        """Pause the simulation"""
        msg = Bool()
        msg.data = True
        self.pause_pub.publish(msg)
        self.simulation_paused = True
        self.get_logger().info('Simulation paused')

    def unpause_simulation(self):
        """Unpause the simulation"""
        msg = Bool()
        msg.data = True
        self.unpause_pub.publish(msg)
        self.simulation_paused = False
        self.get_logger().info('Simulation unpaused')

    def set_physics_properties(self, time_step=0.001, real_time_factor=1.0):
        """Set physics properties for the simulation"""
        while not self.set_physics_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for set physics properties service...')

        request = SetPhysicsProperties.Request()
        request.time_step = time_step
        request.max_update_rate = 1000.0  # 1/time_step
        request.gravity.x = 0.0
        request.gravity.y = 0.0
        request.gravity.z = -9.8

        # ODE solver parameters
        request.ode_config.sor_pgs_precon_iters = 0
        request.ode_config.sor_pgs_iters = 50
        request.ode_config.sor_pgs_w = 1.3
        request.ode_config.sor_pgs_rms_error_tol = 0.01
        request.ode_config.contact_surface_layer = 0.001
        request.ode_config.contact_max_correcting_vel = 100.0
        request.ode_config.cfm = 0.0
        request.ode_config.erp = 0.2
        request.ode_config.max_contacts = 20

        future = self.set_physics_client.call_async(request)
        future.add_done_callback(self.physics_set_callback)

    def physics_set_callback(self, future):
        """Handle physics properties set response"""
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('Physics properties updated successfully')
            else:
                self.get_logger().error(f'Failed to set physics properties: {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

    def monitor_simulation(self):
        """Monitor simulation performance"""
        if self.link_states:
            # Calculate simulation statistics
            num_links = len(self.link_states.name)
            self.get_logger().debug(f'Monitoring {num_links} links in simulation')


def main(args=None):
    rclpy.init(args=args)
    controller = SimulationController()

    # Set physics properties for humanoid simulation
    controller.set_physics_properties(time_step=0.001, real_time_factor=1.0)

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down simulation controller')
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Step-wise Control for Precise Simulation

```python
#!/usr/bin/env python3
# stepwise_control.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool
from gazebo_msgs.srv import StepPhysics
from geometry_msgs.msg import Twist


class StepWiseController(Node):
    def __init__(self):
        super().__init__('step_wise_controller')

        # Service client for stepping physics
        self.step_physics_client = self.create_client(StepPhysics, '/gazebo/step_physics')

        # Publisher for robot commands
        self.cmd_vel_pub = self.create_publisher(Twist, '/humanoid_robot/cmd_vel', 10)

        # Timer for step-wise control
        self.control_timer = self.create_timer(0.01, self.step_wise_control)  # 100Hz

        # Simulation step parameters
        self.time_step = 0.001  # 1ms per step
        self.steps_per_control_cycle = 10  # 10 steps per control cycle (10ms effective rate)
        self.step_counter = 0

        self.get_logger().info('Step-wise controller initialized')

    def step_wise_control(self):
        """Execute step-wise control"""
        # Send robot command
        cmd = Twist()
        cmd.linear.x = 0.5  # Move forward
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

        # Step physics simulation
        self.step_simulation()

    def step_simulation(self):
        """Step the physics simulation"""
        while not self.step_physics_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for step physics service...')

        request = StepPhysics.Request()
        request.max_step_size = self.time_step
        request.time_step = self.time_step

        future = self.step_physics_client.call_async(request)
        future.add_done_callback(self.step_callback)

    def step_callback(self, future):
        """Handle step completion"""
        try:
            response = future.result()
            if response.success:
                self.step_counter += 1
                if self.step_counter % 10 == 0:  # Log every 10 steps
                    self.get_logger().debug(f'Simulation stepped {self.step_counter} times')
            else:
                self.get_logger().error(f'Step failed: {response.status_message}')
        except Exception as e:
            self.get_logger().error(f'Step service call failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    controller = StepWiseController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down step-wise controller')
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 1.6 Plugin Usage for Sensors and Controllers

### Gazebo Plugin Architecture

```
Gazebo Plugin Architecture for Humanoid Robots
┌─────────────────────────────────────────────────────────────────┐
│                        Gazebo Simulator                         │
│  ┌─────────────────┐  ┌──────────────────┐  ┌─────────────────┐ │
│  │   Sensor        │  │   Controller     │  │   Communication │ │
│  │   Plugins       │  │   Plugins        │  │   Plugins       │ │
│  │ (LiDAR, IMU,   │  │ (Joint Control,  │  │ (ROS 2 Bridge,  │ │
│  │  Camera, etc.)  │  │  Diff Drive,     │  │  TF Publisher)  │ │
│  └─────────────────┘  │  Position Ctrl)   │  └─────────────────┘ │
│         │              └──────────────────┘         │           │
│         ▼                       │                   ▼           │
│  ┌─────────────────┐            │            ┌─────────────────┐ │
│  │   Sensor Data   │            │            │   ROS 2 Nodes   │ │
│  │   Generation    │            │            │   Interface     │ │
│  │                 │            │            │                 │ │
│  │   Realistic     │            │            │   Real-time     │ │
│  │   Simulation    │            │            │   Communication │ │
│  └─────────────────┘            │            └─────────────────┘ │
│                                 ▲                                │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │                    Robot Hardware Interface                 │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### Common Controller Plugins

```xml
<!-- Joint state publisher plugin -->
<gazebo>
  <plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
    <ros>
      <namespace>/humanoid_robot</namespace>
      <remapping>~/out:=joint_states</remapping>
    </ros>
    <update_rate>30</update_rate>
    <joint_name>joint1</joint_name>
    <joint_name>joint2</joint_name>
  </plugin>
</gazebo>

<!-- Differential drive controller plugin -->
<gazebo>
  <plugin name="diff_drive_controller" filename="libgazebo_ros_diff_drive.so">
    <ros>
      <namespace>/humanoid_robot</namespace>
      <remapping>cmd_vel:=cmd_vel</remapping>
      <remapping>odom:=odom</remapping>
    </ros>
    <update_rate>30</update_rate>
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.3</wheel_separation>
    <wheel_diameter>0.15</wheel_diameter>
    <max_wheel_torque>20</max_wheel_torque>
    <max_wheel_acceleration>1.0</max_wheel_acceleration>
    <odometry_frame>odom</odometry_frame>
    <robot_base_frame>base_link</robot_base_frame>
    <publish_odom>true</publish_odom>
    <publish_odom_tf>true</publish_odom_tf>
    <publish_wheel_tf>true</publish_wheel_tf>
  </plugin>
</gazebo>

<!-- Joint trajectory controller plugin -->
<gazebo>
  <plugin name="position_command_controller" filename="libgazebo_ros_joint_position.so">
    <robotNamespace>/humanoid_robot</robotNamespace>
    <jointName>shoulder_joint</jointName>
    <topicName>shoulder_position/command</topicName>
    <updateRate>100</updateRate>
    <alwaysOn>true</alwaysOn>
  </plugin>
</gazebo>
```

## 1.7 Hands-On Examples

### Example 1: Humanoid Walking Simulation with Collision Detection

```python
#!/usr/bin/env python3
# humanoid_walking_simulation.py

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist, PointStamped
from sensor_msgs.msg import LaserScan, Imu
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState
import numpy as np
import math


class HumanoidWalkingSimulator(Node):
    def __init__(self):
        super().__init__('humanoid_walking_simulator')

        # Publishers for robot control
        self.cmd_vel_pub = self.create_publisher(Twist, '/humanoid_robot/cmd_vel', 10)
        self.joint_traj_pub = self.create_publisher(JointTrajectory, '/humanoid_robot/joint_trajectory', 10)

        # Subscribers for sensor data
        self.scan_sub = self.create_subscription(LaserScan, '/humanoid_robot/scan', self.scan_callback, 10)
        self.imu_sub = self.create_subscription(Imu, '/humanoid_robot/imu/data', self.imu_callback, 10)

        # Service client for model state control
        self.model_state_client = self.create_client(SetModelState, '/gazebo/set_model_state')

        # Timer for walking control
        self.walk_timer = self.create_timer(0.05, self.walking_control)  # 20Hz walking control

        # Internal state
        self.scan_data = None
        self.imu_data = None
        self.obstacle_detected = False
        self.balance_ok = True
        self.walk_phase = 0.0  # Phase of walking gait

        self.get_logger().info('Humanoid walking simulator initialized')

    def scan_callback(self, msg):
        """Process laser scan for obstacle detection"""
        self.scan_data = msg

        if msg.ranges:
            # Check for obstacles in front of robot
            front_ranges = msg.ranges[len(msg.ranges)//2-30:len(msg.ranges)//2+30]  # Front 60 degrees
            min_distance = min([r for r in front_ranges if r > msg.range_min and r < msg.range_max], default=float('inf'))

            self.obstacle_detected = min_distance < 1.0  # 1 meter safety distance

    def imu_callback(self, msg):
        """Process IMU data for balance checking"""
        self.imu_data = msg

        # Check balance using IMU data
        roll = math.atan2(2*(msg.orientation.w*msg.orientation.x + msg.orientation.y*msg.orientation.z),
                         1 - 2*(msg.orientation.x**2 + msg.orientation.y**2))
        pitch = math.asin(2*(msg.orientation.w*msg.orientation.y - msg.orientation.z*msg.orientation.x))

        # Check if robot is tilted too much
        tilt_threshold = 0.3  # 17 degrees
        self.balance_ok = abs(roll) < tilt_threshold and abs(pitch) < tilt_threshold

    def walking_control(self):
        """Main walking control loop"""
        if not self.balance_ok:
            self.get_logger().warn('Robot is not balanced, stopping walk')
            self.stop_robot()
            return

        if self.obstacle_detected:
            self.get_logger().warn('Obstacle detected, stopping walk')
            self.stop_robot()
            return

        # Generate walking gait
        self.execute_walking_gait()

    def execute_walking_gait(self):
        """Execute walking gait pattern"""
        # Simple walking pattern based on phase
        self.walk_phase += 0.1  # Increment phase
        if self.walk_phase > 2 * math.pi:
            self.walk_phase = 0.0

        # Calculate joint positions for walking
        left_hip = 0.1 * math.sin(self.walk_phase)
        right_hip = 0.1 * math.sin(self.walk_phase + math.pi)
        left_knee = 0.05 * math.sin(self.walk_phase + math.pi/2)
        right_knee = 0.05 * math.sin(self.walk_phase + 3*math.pi/2)

        # Create joint trajectory
        trajectory = JointTrajectory()
        trajectory.joint_names = ['left_hip_joint', 'left_knee_joint', 'right_hip_joint', 'right_knee_joint']

        point = JointTrajectoryPoint()
        point.positions = [left_hip, left_knee, right_hip, right_knee]
        point.time_from_start = Duration(sec=0, nanosec=50000000)  # 50ms

        trajectory.points = [point]
        self.joint_traj_pub.publish(trajectory)

        # Send forward velocity command
        cmd = Twist()
        cmd.linear.x = 0.3  # Walk forward at 0.3 m/s
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

    def stop_robot(self):
        """Stop all robot motion"""
        # Stop linear and angular motion
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

        # Stop joint motion
        trajectory = JointTrajectory()
        trajectory.joint_names = ['left_hip_joint', 'left_knee_joint', 'right_hip_joint', 'right_knee_joint']

        point = JointTrajectoryPoint()
        point.positions = [0.0, 0.0, 0.0, 0.0]  # Return to neutral position
        point.time_from_start = Duration(sec=0, nanosec=10000000)  # 10ms

        trajectory.points = [point]
        self.joint_traj_pub.publish(trajectory)


def main(args=None):
    rclpy.init(args=args)
    simulator = HumanoidWalkingSimulator()

    try:
        rclpy.spin(simulator)
    except KeyboardInterrupt:
        simulator.get_logger().info('Shutting down humanoid walking simulator')
    finally:
        simulator.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 2: LiDAR Integration and Point Cloud Visualization

```python
#!/usr/bin/env python3
# lidar_integration.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, PointCloud2
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header
from geometry_msgs.msg import Point32
from visualization_msgs.msg import Marker, MarkerArray
import numpy as np


class LidarIntegrationNode(Node):
    def __init__(self):
        super().__init__('lidar_integration')

        # Subscriber for laser scan
        self.scan_sub = self.create_subscription(LaserScan, '/humanoid_robot/scan', self.scan_callback, 10)

        # Publishers for processed data
        self.pointcloud_pub = self.create_publisher(PointCloud2, '/humanoid_robot/lidar/pointcloud', 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/humanoid_robot/lidar/markers', 10)

        self.get_logger().info('LiDAR integration node initialized')

    def scan_callback(self, scan_msg):
        """Convert laser scan to point cloud and markers"""
        # Convert laser scan to Cartesian points
        points = []
        for i, range_val in enumerate(scan_msg.ranges):
            if scan_msg.range_min <= range_val <= scan_msg.range_max:
                angle = scan_msg.angle_min + i * scan_msg.angle_increment

                x = range_val * np.cos(angle)
                y = range_val * np.sin(angle)

                points.append([x, y, 0.0])  # Z=0 for 2D laser scan

        # Publish as PointCloud2
        header = Header()
        header.stamp = scan_msg.header.stamp
        header.frame_id = scan_msg.header.frame_id

        # Create PointCloud2 message
        fields = [
            point_cloud2.PointField(name='x', offset=0, datatype=point_cloud2.PointField.FLOAT32, count=1),
            point_cloud2.PointField(name='y', offset=4, datatype=point_cloud2.PointField.FLOAT32, count=1),
            point_cloud2.PointField(name='z', offset=8, datatype=point_cloud2.PointField.FLOAT32, count=1),
        ]

        pcl_msg = point_cloud2.create_cloud(header, fields, points)
        self.pointcloud_pub.publish(pcl_msg)

        # Create visualization markers
        marker_array = MarkerArray()

        for i, point in enumerate(points):
            marker = Marker()
            marker.header = header
            marker.ns = "lidar_points"
            marker.id = i
            marker.type = Marker.SPHERE
            marker.action = Marker.ADD
            marker.pose.position.x = point[0]
            marker.pose.position.y = point[1]
            marker.pose.position.z = point[2]
            marker.pose.orientation.w = 1.0
            marker.scale.x = 0.05
            marker.scale.y = 0.05
            marker.scale.z = 0.05
            marker.color.r = 1.0
            marker.color.g = 0.0
            marker.color.b = 0.0
            marker.color.a = 1.0

            marker_array.markers.append(marker)

        self.marker_pub.publish(marker_array)


def main(args=None):
    rclpy.init(args=args)
    node = LidarIntegrationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down LiDAR integration node')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 3: IMU and Depth Camera Data Integration

```python
#!/usr/bin/env python3
# sensor_integration_node.py

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, Image, CameraInfo
from geometry_msgs.msg import Vector3Stamped, PointStamped
from cv_bridge import CvBridge
import numpy as np
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class SensorIntegrationNode(Node):
    def __init__(self):
        super().__init__('sensor_integration')

        # Initialize CV bridge
        self.cv_bridge = CvBridge()

        # Subscribers
        self.imu_sub = self.create_subscription(Imu, '/humanoid_robot/imu/data', self.imu_callback, 10)
        self.depth_sub = self.create_subscription(Image, '/humanoid_robot/camera/depth/image_raw', self.depth_callback, 10)
        self.camera_info_sub = self.create_subscription(CameraInfo, '/humanoid_robot/camera/depth/camera_info', self.camera_info_callback, 10)

        # Publishers
        self.orientation_pub = self.create_publisher(Vector3Stamped, '/humanoid_robot/orientation', 10)
        self.centroid_pub = self.create_publisher(PointStamped, '/humanoid_robot/depth_centroid', 10)

        # Internal state
        self.imu_data = None
        self.depth_image = None
        self.camera_info = None
        self.latest_transform = None

        # TF buffer and listener
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        # Processing timer
        self.process_timer = self.create_timer(0.1, self.process_sensor_data)

        self.get_logger().info('Sensor integration node initialized')

    def imu_callback(self, msg):
        """Process IMU data"""
        self.imu_data = msg

    def depth_callback(self, msg):
        """Process depth image"""
        try:
            self.depth_image = self.cv_bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        except Exception as e:
            self.get_logger().error(f'Error converting depth image: {e}')

    def camera_info_callback(self, msg):
        """Process camera info"""
        self.camera_info = msg

    def process_sensor_data(self):
        """Process integrated sensor data"""
        if self.imu_data:
            # Extract orientation from IMU
            orientation_msg = Vector3Stamped()
            orientation_msg.header = self.imu_data.header
            orientation_msg.vector.x = self.imu_data.orientation.x
            orientation_msg.vector.y = self.imu_data.orientation.y
            orientation_msg.vector.z = self.imu_data.orientation.z
            self.orientation_pub.publish(orientation_msg)

        if self.depth_image is not None and self.camera_info is not None:
            # Process depth image to find closest point
            self.process_depth_image()

    def process_depth_image(self):
        """Process depth image to find closest object"""
        # Find minimum depth value (closest object)
        if self.depth_image.size > 0:
            valid_depths = self.depth_image[self.depth_image > 0]  # Remove invalid depths
            if valid_depths.size > 0:
                min_depth = np.min(valid_depths)

                # Find pixel coordinates of closest point
                y, x = np.where(self.depth_image == min_depth)
                if len(y) > 0 and len(x) > 0:
                    closest_y, closest_x = y[0], x[0]

                    # Convert pixel coordinates to 3D using camera intrinsics
                    if self.camera_info:
                        # Calculate 3D position using pinhole camera model
                        fx = self.camera_info.k[0]  # Focal length x
                        fy = self.camera_info.k[4]  # Focal length y
                        cx = self.camera_info.k[2]  # Principal point x
                        cy = self.camera_info.k[5]  # Principal point y

                        # Convert to 3D coordinates
                        z = min_depth  # Depth value
                        x_3d = (closest_x - cx) * z / fx
                        y_3d = (closest_y - cy) * z / fy

                        # Publish centroid
                        centroid_msg = PointStamped()
                        centroid_msg.header.stamp = self.get_clock().now().to_msg()
                        centroid_msg.header.frame_id = self.camera_info.header.frame_id
                        centroid_msg.point.x = x_3d
                        centroid_msg.point.y = y_3d
                        centroid_msg.point.z = z
                        self.centroid_pub.publish(centroid_msg)


def main(args=None):
    rclpy.init(args=args)
    node = SensorIntegrationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Shutting down sensor integration node')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Example 4: ROS 2 Launch Integration with Gazebo

```python
# launch/humanoid_gazebo_simulation.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time'
    )

    world_file = DeclareLaunchArgument(
        'world_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('humanoid_gazebo'),
            'worlds',
            'humanoid_indoor.world'
        ]),
        description='Path to the Gazebo world file'
    )

    robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='humanoid_robot',
        description='Name of the robot'
    )

    # Launch Gazebo with the specified world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('gazebo_ros'),
                'launch',
                'gazebo.launch.py'
            ])
        ]),
        launch_arguments={
            'world': LaunchConfiguration('world_file'),
            'verbose': 'false',
            'gui': 'true'
        }.items()
    )

    # Spawn the robot in Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', LaunchConfiguration('robot_name'),
            '-x', '0.0',
            '-y', '0.0',
            '-z', '1.0'
        ],
        output='screen'
    )

    # Robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'robot_description':
                PathJoinSubstitution([
                    FindPackageShare('humanoid_description'),
                    'urdf',
                    'humanoid_robot.urdf.xacro'
                ])
            }
        ],
        remappings=[
            ('/joint_states', [LaunchConfiguration('robot_name'), '/joint_states'])
        ]
    )

    # Launch the controller manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            PathJoinSubstitution([
                FindPackageShare('humanoid_bringup'),
                'config',
                'humanoid_controllers.yaml'
            ]),
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        remappings=[
            ('/joint_states', [LaunchConfiguration('robot_name'), '/joint_states'])
        ]
    )

    # Launch controller spawners
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    joint_trajectory_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_trajectory_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # Launch the perception and control nodes
    perception_node = Node(
        package='humanoid_perception',
        executable='lidar_integration',
        name='lidar_integration_node',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[
            ('/humanoid_robot/scan', [LaunchConfiguration('robot_name'), '/scan']),
        ]
    )

    control_node = Node(
        package='humanoid_control',
        executable='humanoid_walking_simulator',
        name='humanoid_walking_simulator',
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        remappings=[
            ('/humanoid_robot/cmd_vel', [LaunchConfiguration('robot_name'), '/cmd_vel']),
            ('/humanoid_robot/scan', [LaunchConfiguration('robot_name'), '/scan']),
            ('/humanoid_robot/imu/data', [LaunchConfiguration('robot_name'), '/imu/data']),
        ]
    )

    return LaunchDescription([
        use_sim_time,
        world_file,
        robot_name,
        gazebo,
        TimerAction(
            period=3.0,
            actions=[spawn_entity]
        ),
        robot_state_publisher,
        TimerAction(
            period=5.0,
            actions=[controller_manager]
        ),
        TimerAction(
            period=7.0,
            actions=[
                joint_state_broadcaster_spawner,
                joint_trajectory_controller_spawner
            ]
        ),
        TimerAction(
            period=9.0,
            actions=[perception_node]
        ),
        TimerAction(
            period=10.0,
            actions=[control_node]
        )
    ])
```

## 1.8 Data Flow Architecture

### Robot-Gazebo-ROS 2 Data Flow Diagram

```
Data Flow in Gazebo-ROS 2 Integration:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Robot URDF    │───▶│   Gazebo        │───▶│   ROS 2 Nodes   │
│   Model         │    │   Simulator     │    │                 │
│                 │    │                 │    │  Perception     │
│  (Physical     │    │  (Physics,      │    │  Processing     │
│   Properties)  │    │   Sensors)      │    │  Nodes          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Joint States  │───▶│  Sensor Data    │───▶│  Control        │
│   (Position,    │    │  (LiDAR, IMU,  │    │  Commands       │
│   Velocity)     │    │   Camera)       │    │  (Twist, Joint │
└─────────────────┘    └──────────────────┘    │   Trajectory)   │
         │                       │              └─────────────────┘
         ▼                       ▼                       │
┌─────────────────┐    ┌──────────────────┐              │
│  Gazebo        │◀───│  ROS 2          │◀───────────────┘
│  Plugins       │    │  Communication  │
│  (Controllers, │    │  (Topics,       │
│   Sensors)     │    │   Services)     │
└─────────────────┘    └──────────────────┘
```

### Sensor Placement and Data Pipeline

```
Sensor Data Pipeline:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Raw Sensor    │───▶│  Preprocessing   │───▶│  Perception     │
│   Data          │    │  & Filtering     │    │  Algorithms     │
│                 │    │                 │    │                 │
│  LiDAR: Scan   │    │  - Noise filter │    │  - Object       │
│  IMU: Acc/Gyro │    │  - Outlier rem. │    │    Detection    │
│  Camera: Image │    │  - Calibration  │    │  - SLAM         │
└─────────────────┘    └──────────────────┘    │  - Localization │
         │                       │              └─────────────────┘
         ▼                       ▼                       │
┌─────────────────┐    ┌──────────────────┐              │
│   Sensor        │───▶│  State          │───▶┌─────────────────┐
│   Fusion        │    │  Estimation     │    │  Behavior       │
│  (Kalman Filter│    │  (EKF, UKF)     │    │  Selection      │
│   Particle      │    │                 │    │  (FSM, BT)      │
│   Filter)       │    │  - Pose         │    │                 │
└─────────────────┘    │  - Velocity     │    │  - Walking      │
         │              │  - IMU Fusion   │    │  - Balancing    │
         ▼              └──────────────────┘    │  - Manipulation │
┌─────────────────┐              │              └─────────────────┘
│   Control       │◀─────────────┘
│   Generation    │
│  (Trajectory,   │
│   MPC, PID)     │
└─────────────────┘
```

## 1.9 Exercises

### Exercise 1: Physics Parameter Tuning
Experiment with different physics parameters in the Gazebo world file to observe their effects on humanoid robot simulation. Try adjusting `max_step_size`, `real_time_factor`, and contact parameters to achieve stable walking.

### Exercise 2: New Sensor Integration
Add a force/torque sensor to the humanoid robot's foot and simulate ground reaction forces during walking. Create the Gazebo plugin configuration and ROS 2 interface for the new sensor.

### Exercise 3: Custom Environment Creation
Design a custom Gazebo world with ramps, stairs, or obstacles that challenge the humanoid robot's locomotion capabilities. Include appropriate physics properties for realistic interaction.

### Exercise 4: Sensor Fusion Algorithm
Implement a simple sensor fusion algorithm that combines LiDAR and IMU data to improve robot localization in the presence of wheel slippage.

### Exercise 5: Dynamic Obstacle Simulation
Create a moving obstacle in the Gazebo world and implement collision avoidance behavior in the humanoid robot's control system.

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Physics Parameter Tuning</summary>

```xml
<!-- Example of a tuned world file with optimized physics parameters -->
<sdf version="1.7">
  <world name="humanoid_world_tuned">
    <!-- Physics engine with optimized parameters -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>  <!-- Smaller for better humanoid stability -->
      <real_time_factor>1.0</real_time_factor>  <!-- 1x real-time speed -->
      <real_time_update_rate>1000</real_time_update_rate>  <!-- Higher update rate -->

      <!-- Contact parameters optimized for humanoid simulation -->
      <ode>
        <solver>
          <type>quick</type>
          <iters>10</iters>  <!-- Increase for stability -->
          <sor>1.3</sor>
        </solver>
        <constraints>
          <cfm>0.000001</cfm>  <!-- Constraint Force Mixing -->
          <erp>0.2</erp>      <!-- Error Reduction Parameter -->
          <contact_max_correcting_vel>100.0</contact_max_correcting_vel>
          <contact_surface_layer>0.001</contact_surface_layer>
        </constraints>
      </ode>
    </physics>

    <!-- Include your robot model -->
    <include>
      <uri>model://humanoid_robot</uri>
      <pose>0 0 1.0 0 0 0</pose>  <!-- Starting position adjusted for proper ground contact -->
    </include>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Lighting -->
    <include>
      <uri>model://sun</uri>
    </include>
  </world>
</sdf>
```

### Key Physics Parameters for Humanoid Stability:
- `max_step_size`: Smaller values (0.001-0.005) provide better stability for humanoid robots with many joints
- `real_time_factor`: Set to 1.0 for real-time simulation, lower values for more stable computation
- `contact_max_correcting_vel`: Higher values allow faster contact corrections
- `contact_surface_layer`: Small positive value prevents excessive penetration

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: New Sensor Integration</summary>

```xml
<!-- Add force/torque sensor to humanoid robot's foot -->
<!-- In your URDF/Xacro file -->
<xacro:macro name="fts_plugin" params="name parent_link topic_name">
  <gazebo reference="${parent_link}">
    <sensor name="${name}" type="force_torque">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <force_torque>
        <frame>child</frame>
        <measure_direction>child_to_parent</measure_direction>
      </force_torque>
      <plugin name="ft_sensor_${name}" filename="libgazebo_ros_ft_sensor.so">
        <ros>
          <namespace>humanoid</namespace>
          <remapping>~/out:=${topic_name}</remapping>
        </ros>
        <frame_name>${parent_link}</frame_name>
      </plugin>
    </sensor>
  </gazebo>
</xacro:macro>

<!-- Use the macro to add FTS to feet -->
<xacro:fts_plugin name="left_foot_fts"
                  parent_link="left_foot_link"
                  topic_name="left_foot/forces"/>

<xacro:fts_plugin name="right_foot_fts"
                  parent_link="right_foot_link"
                  topic_name="right_foot/forces"/>
```

```python
#!/usr/bin/env python3
"""
Ground reaction force processing node
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import WrenchStamped
from std_msgs.msg import Float32MultiArray
from sensor_msgs.msg import JointState
import numpy as np

class GroundReactionForceNode(Node):
    def __init__(self):
        super().__init__('ground_reaction_force_node')

        # Subscribers for both feet force/torque sensors
        self.left_foot_sub = self.create_subscription(
            WrenchStamped, 'left_foot/forces', self.left_force_callback, 10)
        self.right_foot_sub = self.create_subscription(
            WrenchStamped, 'right_foot/forces', self.right_force_callback, 10)
        self.joint_state_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_state_callback, 10)

        # Publishers for processed force data
        self.zmp_pub = self.create_publisher(Float32MultiArray, 'zero_moment_point', 10)
        self.stability_pub = self.create_publisher(Float32MultiArray, 'stability_metrics', 10)

        # Internal state
        self.left_force = np.array([0.0, 0.0, 0.0])
        self.left_torque = np.array([0.0, 0.0, 0.0])
        self.right_force = np.array([0.0, 0.0, 0.0])
        self.right_torque = np.array([0.0, 0.0, 0.0])
        self.joint_positions = {}

        self.get_logger().info('Ground reaction force processor initialized')

    def left_force_callback(self, msg):
        """Process left foot force/torque data"""
        self.left_force = np.array([msg.wrench.force.x,
                                   msg.wrench.force.y,
                                   msg.wrench.force.z])
        self.left_torque = np.array([msg.wrench.torque.x,
                                    msg.wrench.torque.y,
                                    msg.wrench.torque.z])
        self.process_forces()

    def right_force_callback(self, msg):
        """Process right foot force/torque data"""
        self.right_force = np.array([msg.wrench.force.x,
                                    msg.wrench.force.y,
                                    msg.wrench.force.z])
        self.right_torque = np.array([msg.wrench.torque.x,
                                     msg.wrench.torque.y,
                                     msg.wrench.torque.z])
        self.process_forces()

    def joint_state_callback(self, msg):
        """Update joint positions"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]

    def process_forces(self):
        """Process ground reaction forces to determine stability"""
        # Calculate Zero Moment Point (ZMP) - simplified 2D
        total_force_z = self.left_force[2] + self.right_force[2]
        total_torque_x = self.left_torque[0] + self.right_torque[0]
        total_torque_y = self.left_torque[1] + self.right_torque[1]

        if abs(total_force_z) > 0.1:  # Avoid division by zero
            zmp_x = -total_torque_y / total_force_z
            zmp_y = total_torque_x / total_force_z

            # Publish ZMP
            zmp_msg = Float32MultiArray()
            zmp_msg.data = [zmp_x, zmp_y, total_force_z]
            self.zmp_pub.publish(zmp_msg)

            # Calculate stability metrics
            stability_msg = Float32MultiArray()
            # Check if ZMP is within support polygon (simplified)
            support_polygon_radius = 0.1  # Approximate foot size
            distance_from_center = np.sqrt(zmp_x**2 + zmp_y**2)
            stability_metric = max(0.0, 1.0 - distance_from_center/support_polygon_radius)

            stability_msg.data = [stability_metric, distance_from_center,
                                 self.left_force[2], self.right_force[2]]
            self.stability_pub.publish(stability_msg)

def main(args=None):
    rclpy.init(args=args)
    node = GroundReactionForceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Force processing node stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Custom Environment Creation</summary>

```xml
<!-- Custom world with ramps, stairs, and obstacles -->
<sdf version="1.7">
  <world name="humanoid_challenge_world">
    <!-- Physics engine -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>

    <!-- Sun light -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
      </attenuation>
      <direction>-0.2 0.5 -1.0</direction>
    </light>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Ramps -->
    <model name="ramp_1">
      <pose>-2 0 0 0 0 0</pose>
      <link name="ramp_link">
        <collision name="collision">
          <geometry>
            <mesh>
              <uri>file://ramp.dae</uri>
            </mesh>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <mesh>
              <uri>file://ramp.dae</uri>
            </mesh>
          </geometry>
        </visual>
        <inertial>
          <mass>100.0</mass>
          <inertia>
            <ixx>100.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>100.0</iyy>
            <iyz>0.0</iyz>
            <izz>100.0</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Stairs -->
    <model name="stairs">
      <pose>2 0 0 0 0 0</pose>
      <link name="stairs_base">
        <collision name="step_1">
          <pose>0 0 0.1 0 0 0</pose>
          <geometry>
            <box>
              <size>1.0 2.0 0.2</size>
            </box>
          </geometry>
        </collision>
        <collision name="step_2">
          <pose>0 0 0.2 0 0 0</pose>
          <geometry>
            <box>
              <size>1.0 2.0 0.2</size>
            </box>
          </geometry>
        </collision>
        <collision name="step_3">
          <pose>0 0 0.3 0 0 0</pose>
          <geometry>
            <box>
              <size>1.0 2.0 0.2</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1.0 2.0 0.6</size>
            </box>
          </geometry>
        </visual>
        <inertial>
          <mass>200.0</mass>
          <inertia>
            <ixx>200.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>200.0</iyy>
            <iyz>0.0</iyz>
            <izz>200.0</izz>
          </inertia>
        </inertial>
      </link>
    </model>

    <!-- Moving obstacles -->
    <model name="moving_obstacle">
      <pose>0 3 0.5 0 0 0</pose>
      <link name="obstacle_link">
        <collision name="collision">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>0.5 0.5 0.5</size>
            </box>
          </geometry>
          <material>
            <script>
              <uri>file://media/materials/scripts/gazebo.material</uri>
              <name>Gazebo/Red</name>
            </script>
          </material>
        </visual>
        <inertial>
          <mass>10.0</mass>
          <inertia>
            <ixx>1.0</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>1.0</iyy>
            <iyz>0.0</iyz>
            <izz>1.0</izz>
          </inertia>
        </inertial>
      </link>
      <!-- Model plugin for movement -->
      <plugin name="obstacle_controller" filename="libgazebo_ros_p3d.so">
        <always_on>true</always_on>
        <update_rate>100</update_rate>
        <body_name>obstacle_link</body_name>
        <topic_name>moving_obstacle/pose</topic_name>
        <gaussian_noise>0.0</gaussian_noise>
        <frame_name>world</frame_name>
      </plugin>
    </model>

    <!-- Include humanoid robot -->
    <include>
      <uri>model://humanoid_robot</uri>
      <pose>0 0 1.0 0 0 0</pose>
    </include>
  </world>
</sdf>
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: Sensor Fusion Algorithm</summary>

```python
#!/usr/bin/env python3
"""
LIDAR and IMU sensor fusion for improved localization
"""
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseWithCovarianceStamped, TwistWithCovarianceStamped
from std_msgs.msg import Float32
import numpy as np
from scipy.spatial.transform import Rotation as R
import math

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')

        # Subscribers
        self.lidar_sub = self.create_subscription(
            LaserScan, 'scan', self.lidar_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)

        # Publishers
        self.odom_pub = self.create_publisher(Odometry, 'fused_odom', 10)
        self.pose_pub = self.create_publisher(PoseWithCovarianceStamped, 'fused_pose', 10)

        # Internal state
        self.current_pose = np.array([0.0, 0.0, 0.0])  # x, y, theta
        self.current_velocity = np.array([0.0, 0.0, 0.0])  # vx, vy, vtheta
        self.current_angular_rates = np.array([0.0, 0.0, 0.0])  # roll_rate, pitch_rate, yaw_rate
        self.imu_orientation = np.array([0.0, 0.0, 0.0, 1.0])  # x, y, z, w quaternion

        # Covariance matrices (simplified)
        self.pose_covariance = np.eye(6) * 0.1  # Initial uncertainty
        self.twist_covariance = np.eye(6) * 0.1

        # Previous time for integration
        self.prev_time = self.get_clock().now()

        self.get_logger().info('Sensor fusion node initialized')

    def lidar_callback(self, msg):
        """Process LIDAR data for position correction"""
        # Extract features from LIDAR scan (simplified - in practice, use more sophisticated methods)
        ranges = np.array(msg.ranges)
        angles = np.array([msg.angle_min + i*msg.angle_increment for i in range(len(ranges))])

        # Filter valid ranges
        valid_mask = (ranges > msg.range_min) & (ranges < msg.range_max)
        valid_ranges = ranges[valid_mask]
        valid_angles = angles[valid_mask]

        # Find nearest obstacles in front, left, right
        front_mask = (valid_angles > -0.5) & (valid_angles < 0.5)
        left_mask = (valid_angles > 0.5) & (valid_angles < 1.0)
        right_mask = (valid_angles < -0.5) & (valid_angles > -1.0)

        front_distances = valid_ranges[front_mask] if np.any(front_mask) else [float('inf')]
        left_distances = valid_ranges[left_mask] if np.any(left_mask) else [float('inf')]
        right_distances = valid_ranges[right_mask] if np.any(right_mask) else [float('inf')]

        min_front = min(front_distances)
        min_left = min(left_distances)
        min_right = min(right_distances)

        # Use LIDAR features to correct pose estimate
        # This is a simplified approach - in practice, use scan matching or particle filters
        self.correct_pose_with_lidar(min_front, min_left, min_right)

    def imu_callback(self, msg):
        """Process IMU data for orientation and angular velocity"""
        # Update orientation from IMU
        self.imu_orientation = np.array([
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        ])

        # Convert quaternion to euler for easier processing
        euler = self.quaternion_to_euler(self.imu_orientation)
        roll, pitch, yaw = euler

        # Update angular velocities
        self.current_angular_rates = np.array([
            msg.angular_velocity.x,
            msg.angular_velocity.y,
            msg.angular_velocity.z
        ])

        # Integrate angular velocity to get position change (dead reckoning component)
        current_time = self.get_clock().now()
        dt = (current_time.nanoseconds - self.prev_time.nanoseconds) / 1e9
        self.prev_time = current_time

        if dt > 0:
            # Update pose based on IMU data
            self.current_pose[2] += self.current_angular_rates[2] * dt  # Change in yaw

            # Update covariance based on IMU reliability
            self.update_covariance_from_imu(dt)

        # Publish fused estimate
        self.publish_fused_estimate()

    def correct_pose_with_lidar(self, front_dist, left_dist, right_dist):
        """Correct pose estimate using LIDAR features"""
        # This is a simplified correction - in practice, use more sophisticated methods
        # like Extended Kalman Filter or Particle Filter

        # If we detect that we're closer to obstacles than expected, adjust position
        expected_front = 1.0  # Expected distance to wall in front
        expected_side = 0.5   # Expected distance to walls on sides

        # Calculate corrections
        front_correction = (expected_front - front_dist) * 0.1  # Proportional correction
        side_correction = ((expected_side - left_dist) + (expected_side - right_dist)) * 0.05

        # Apply corrections to position
        self.current_pose[0] += front_correction
        self.current_pose[1] += side_correction

        # Reduce uncertainty when LIDAR provides reliable measurements
        self.pose_covariance[:2, :2] *= 0.9  # Reduce position uncertainty

    def quaternion_to_euler(self, q):
        """Convert quaternion to euler angles"""
        w, x, y, z = q[3], q[0], q[1], q[2]

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return np.array([roll, pitch, yaw])

    def update_covariance_from_imu(self, dt):
        """Update pose covariance based on IMU integration"""
        # Increase uncertainty due to integration drift
        process_noise = np.diag([0.01, 0.01, 0.005]) * dt  # Position uncertainty growth
        self.pose_covariance[:3, :3] += process_noise

    def publish_fused_estimate(self):
        """Publish the fused pose estimate"""
        odom_msg = Odometry()
        odom_msg.header.stamp = self.get_clock().now().to_msg()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'

        # Set position
        odom_msg.pose.pose.position.x = self.current_pose[0]
        odom_msg.pose.pose.position.y = self.current_pose[1]
        odom_msg.pose.pose.position.z = 0.0

        # Set orientation from IMU
        odom_msg.pose.pose.orientation.x = self.imu_orientation[0]
        odom_msg.pose.pose.orientation.y = self.imu_orientation[1]
        odom_msg.pose.pose.orientation.z = self.imu_orientation[2]
        odom_msg.pose.pose.orientation.w = self.imu_orientation[3]

        # Set covariance
        odom_msg.pose.covariance = self.pose_covariance.flatten().tolist()
        odom_msg.twist.covariance = self.twist_covariance.flatten().tolist()

        self.odom_pub.publish(odom_msg)

        # Also publish as PoseWithCovarianceStamped
        pose_stamped = PoseWithCovarianceStamped()
        pose_stamped.header = odom_msg.header
        pose_stamped.pose = odom_msg.pose
        self.pose_pub.publish(pose_stamped)

def main(args=None):
    rclpy.init(args=args)
    node = SensorFusionNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sensor fusion node stopped')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Dynamic Obstacle Simulation</summary>

```python
#!/usr/bin/env python3
"""
Dynamic obstacle avoidance for humanoid robot
"""
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist, Point, PoseStamped
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import numpy as np
import math

class DynamicObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('dynamic_obstacle_avoidance')

        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_sub = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(
            Odometry, 'odom', self.odom_callback, 10)
        self.status_pub = self.create_publisher(String, 'robot_status', 10)

        # Parameters
        self.declare_parameter('safety_distance', 0.8)
        self.declare_parameter('avoidance_gain', 2.0)
        self.declare_parameter('approach_gain', 1.5)
        self.declare_parameter('rotation_gain', 1.0)

        self.safety_distance = self.get_parameter('safety_distance').value
        self.avoidance_gain = self.get_parameter('avoidance_gain').value
        self.approach_gain = self.get_parameter('approach_gain').value
        self.rotation_gain = self.get_parameter('rotation_gain').value

        # Robot state
        self.current_scan = None
        self.current_odom = None
        self.obstacle_vectors = []  # List of obstacle vectors (x, y, distance, angle)

        # Control timer
        self.control_timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('Dynamic obstacle avoidance node initialized')

    def scan_callback(self, msg):
        """Process laser scan for obstacle detection"""
        self.current_scan = msg

        # Process scan to identify obstacles
        self.detect_obstacles(msg)

    def odom_callback(self, msg):
        """Update robot odometry"""
        self.current_odom = msg

    def detect_obstacles(self, scan_msg):
        """Detect obstacles from laser scan"""
        ranges = np.array(scan_msg.ranges)
        angles = np.array([scan_msg.angle_min + i*scan_msg.angle_increment
                          for i in range(len(ranges))])

        # Filter valid ranges (within safety distance)
        valid_mask = (ranges > scan_msg.range_min) & (ranges < self.safety_distance) & (ranges < scan_msg.range_max)
        valid_ranges = ranges[valid_mask]
        valid_angles = angles[valid_mask]

        # Convert polar to cartesian coordinates (relative to robot)
        obstacle_vectors = []
        for r, theta in zip(valid_ranges, valid_angles):
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            obstacle_vectors.append((x, y, r, theta))

        self.obstacle_vectors = obstacle_vectors

    def control_loop(self):
        """Main control loop for obstacle avoidance"""
        if self.current_scan is None:
            return

        # Calculate avoidance command based on detected obstacles
        cmd = self.calculate_avoidance_command()

        # Publish command
        self.cmd_vel_pub.publish(cmd)

        # Publish status
        status_msg = String()
        status_msg.data = f'Obstacles detected: {len(self.obstacle_vectors)}, cmd: ({cmd.linear.x:.2f}, {cmd.angular.z:.2f})'
        self.status_pub.publish(status_msg)

    def calculate_avoidance_command(self):
        """Calculate avoidance command based on obstacles"""
        cmd = Twist()

        if not self.obstacle_vectors:
            # No obstacles detected, continue forward
            cmd.linear.x = 0.3  # Default forward speed
            cmd.angular.z = 0.0
            return cmd

        # Calculate repulsive forces from obstacles
        repulsive_force_x = 0.0
        repulsive_force_y = 0.0

        for obs_x, obs_y, distance, angle in self.obstacle_vectors:
            # Calculate repulsive force magnitude (stronger when closer)
            force_magnitude = self.avoidance_gain * (1.0/distance - 1.0/self.safety_distance) / (distance**2)

            # Calculate repulsive force direction (away from obstacle)
            force_x = -obs_x * force_magnitude
            force_y = -obs_y * force_magnitude

            repulsive_force_x += force_x
            repulsive_force_y += force_y

        # Calculate desired direction (try to move forward while avoiding obstacles)
        desired_x = self.approach_gain * 1.0  # Want to move forward
        desired_y = 0.0  # Stay centered laterally

        # Combine desired direction with obstacle avoidance
        total_x = desired_x + repulsive_force_x
        total_y = desired_y + repulsive_force_y

        # Convert to linear/angular commands
        cmd.linear.x = max(0.0, min(0.5, total_x))  # Forward speed limited
        cmd.angular.z = self.rotation_gain * math.atan2(total_y, total_x)  # Turning

        # Apply safety limits
        cmd.angular.z = max(-1.0, min(1.0, cmd.angular.z))

        return cmd

def main(args=None):
    rclpy.init(args=args)
    node = DynamicObstacleAvoidanceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Dynamic obstacle avoidance node stopped')
        # Stop robot on shutdown
        stop_cmd = Twist()
        node.cmd_vel_pub.publish(stop_cmd)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

## 1.10 Mini-Project: Humanoid Robot with LiDAR and IMU in Custom World

Create a complete simulation environment featuring:
1. A humanoid robot model with LiDAR and IMU sensors
2. A custom Gazebo world with furniture and obstacles
3. ROS 2 nodes for sensor data processing and robot control
4. Launch file that brings up the complete simulation system
5. Basic navigation and obstacle avoidance behaviors

The project should demonstrate:
- Proper URDF to Gazebo integration
- Realistic sensor simulation
- Physics-based interactions
- ROS 2 communication between simulation and control nodes
- Responsive robot behaviors based on sensor input

:::tip
Start with a simple world and robot model, then gradually add complexity. Test each component individually before integrating them into the full system.
:::

## 1.11 Chapter Summary

This chapter covered the fundamentals of Gazebo simulation for humanoid robots:

- **Physics Engine**: Understanding dynamics, gravity, collisions, and friction for realistic simulation
- **Sensor Simulation**: Configuring LiDAR, Depth Camera, IMU, and other humanoid sensors in Gazebo
- **Model Integration**: Importing URDF/Xacro models into Gazebo with proper plugin configuration
- **Environment Setup**: Creating world files with obstacles, lighting, and physics properties
- **Real-time Simulation**: Controlling simulation timing and step-wise execution
- **Plugin Usage**: Leveraging Gazebo plugins for sensors and controllers
- **Data Flow**: Understanding the flow of information between robot, simulation, and ROS 2 nodes

Gazebo provides a powerful platform for developing and testing humanoid robot applications in a safe, repeatable, and cost-effective environment. Proper configuration of physics, sensors, and control interfaces is essential for achieving realistic simulation results that transfer effectively to real hardware.