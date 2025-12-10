---
title: "Module 1.4 - Chapter 4: URDF Robot Modeling"
sidebar_position: 4
---

# Module 1.4 - Chapter 4: URDF Robot Modeling

## 4.0 Introduction to URDF

### What is URDF?

URDF (Unified Robot Description Format) is an XML-based format for representing robot models in the Robot Operating System (ROS). It serves as the standard way to describe a robot's physical and visual properties, including its links (rigid parts), joints (connections between links), and other components like sensors and actuators. URDF is essential for robot simulation, visualization, motion planning, and control.

```
URDF Structure Overview
┌─────────────────────────────────────────┐
│              Robot Model                │
│  ┌─────────────────────────────────┐    │
│  │           Links                 │    │
│  │  ┌─────────┐ ┌─────────┐      │    │
│  │  │ Visual  │ │ Inertial│      │    │
│  │  │         │ │         │      │    │
│  │  │Collision│ │Material │      │    │
│  │  └─────────┘ └─────────┘      │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │           Joints                │    │
│  │  ┌─────────┐ ┌─────────┐       │    │
│  │  │ Type    │ │ Limits  │       │    │
│  │  │         │ │         │       │    │
│  │  │Axis     │ │Origin   │       │    │
│  │  └─────────┘ └─────────┘       │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

URDF models are used by various ROS tools including:
- **RViz**: For visualization
- **Gazebo**: For physics simulation
- **MoveIt!**: For motion planning
- **TF**: For coordinate transformations

### URDF vs. Other Formats

| Format | Purpose | Advantages | Disadvantages |
|--------|---------|------------|---------------|
| URDF | Robot structure | Simple, widely supported | Limited for complex scenes |
| SDF | Simulation | More features for Gazebo | Complex for basic robots |
| Xacro | Macro expansion | Reusable, modular | Requires preprocessing |

:::note
URDF is specifically designed for describing individual robots, not entire environments or scenes.
:::

## 4.1 Link Elements: The Building Blocks of Robots

### Understanding Links

Links represent the rigid parts of a robot - the parts that don't move relative to themselves. Each link can have multiple properties that define how it appears, behaves, and interacts with the physical world.

### Link Structure

```xml
<link name="link_name">
  <!-- Visual properties for rendering -->
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="1 1 1"/>
    </geometry>
    <material name="red">
      <color rgba="1 0 0 1"/>
    </material>
  </visual>

  <!-- Collision properties for physics simulation -->
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <box size="1 1 1"/>
    </geometry>
  </collision>

  <!-- Inertial properties for dynamics -->
  <inertial>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <mass value="1.0"/>
    <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1"/>
  </inertial>
</link>
```

### Visual Elements

Visual elements define how a link appears in visualization tools like RViz and simulation environments. They include geometry, materials, and transformations.

```xml
<visual>
  <!-- Position and orientation relative to link frame -->
  <origin xyz="0 0 0.1" rpy="0 0 0"/>

  <!-- Geometry definition -->
  <geometry>
    <!-- Box geometry -->
    <box size="0.1 0.1 0.2"/>
    <!-- Alternative geometries: cylinder, sphere, mesh -->
  </geometry>

  <!-- Material definition -->
  <material name="blue_material">
    <color rgba="0 0 1 1"/>
    <!-- Or reference a material defined elsewhere -->
    <!-- <material name="predefined_material"/> -->
  </material>
</visual>
```

#### Visual Geometry Types

| Geometry Type | Parameters | Use Case |
|---------------|------------|----------|
| Box | `size="x y z"` | Simple rectangular shapes |
| Cylinder | `radius="r" length="l"` | Wheels, limbs |
| Sphere | `radius="r"` | Ball joints, spherical objects |
| Mesh | `filename="path" scale="x y z"` | Complex shapes |

### Collision Elements

Collision elements define the physical boundaries of a link for physics simulation. They can be simpler than visual elements for performance.

```xml
<collision>
  <!-- Often the same as visual but can be simplified -->
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <geometry>
    <!-- Often use simpler geometry than visual -->
    <cylinder radius="0.05" length="0.2"/>
  </geometry>
</collision>
```

:::tip
Use simpler collision geometries (boxes, cylinders) instead of complex meshes for better simulation performance.
:::

### Inertial Elements

Inertial elements define the mass properties of a link, which are crucial for dynamics simulation and control.

```xml
<inertial>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <mass value="0.5"/>
  <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.005"/>
</inertial>
```

#### Inertia Tensor

The inertia tensor represents how mass is distributed in the link. For common shapes:

**Solid Box** (width w, height h, depth d, mass m):
```
ixx = m*(h² + d²)/12
iyy = m*(w² + d²)/12
izz = m*(w² + h²)/12
```

**Solid Cylinder** (radius r, height h, mass m):
```
ixx = iyy = m*(3*r² + h²)/12
izz = m*r²/2
```

**Solid Sphere** (radius r, mass m):
```
ixx = iyy = izz = 2*m*r²/5
```

## 4.2 Joint Types and Kinematic Structure

### Understanding Joints

Joints define the connections between links and specify how they can move relative to each other. Each joint has a type, parent link, child link, and optional limits.

### Joint Type Comparison

| Joint Type | DOF | Movement | Common Use | Limits |
|------------|-----|----------|------------|--------|
| Fixed | 0 | No movement | Rigid connections | N/A |
| Revolute | 1 | Single-axis rotation | Elbow, knee | Yes |
| Continuous | 1 | Unlimited rotation | Wheels | No |
| Prismatic | 1 | Linear movement | Slides | Yes |
| Planar | 2 | Movement in plane | Mobile platforms | No |
| Floating | 6 | 6 DOF | Simulated floating objects | No |

```
Joint Types Visualization
Fixed:      Revolute:     Continuous:    Prismatic:
  ┌─┐         ┌─┐            ┌─┐           ┌─┐
  │ │    ┌───►│ │◄───┐    ┌─┤ ├─┐       ┌─┼─┐
  └─┘    │    └─┘    │    │ └─┘ │       │   │
         │           │    └─────┘       └───┘
         └───────────┘                  │   │
                                      └───┘
```

### Joint Definition Structure

```xml
<joint name="joint_name" type="joint_type">
  <!-- Parent link (closer to robot base) -->
  <parent link="parent_link_name"/>

  <!-- Child link (further from robot base) -->
  <child link="child_link_name"/>

  <!-- Position and orientation of joint relative to parent -->
  <origin xyz="0 0 0.1" rpy="0 0 0"/>

  <!-- For revolute/prismatic joints: axis of rotation/translation -->
  <axis xyz="0 0 1"/>

  <!-- Joint limits (for revolute and prismatic joints) -->
  <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>

  <!-- Dynamics properties -->
  <dynamics damping="0.1" friction="0.01"/>
</joint>
```

### Joint Type Examples

#### Fixed Joint
```xml
<joint name="fixed_connection" type="fixed">
  <parent link="base_link"/>
  <child link="sensor_link"/>
  <origin xyz="0.1 0 0.05" rpy="0 0 0"/>
</joint>
```

#### Revolute Joint
```xml
<joint name="elbow_joint" type="revolute">
  <parent link="upper_arm"/>
  <child link="lower_arm"/>
  <origin xyz="0 0 0.3" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-2.0" upper="2.0" effort="50" velocity="2"/>
  <dynamics damping="1.0" friction="0.1"/>
</joint>
```

#### Continuous Joint
```xml
<joint name="wheel_joint" type="continuous">
  <parent link="chassis"/>
  <child link="wheel"/>
  <origin xyz="0.2 0 -0.1" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <dynamics damping="0.1"/>
</joint>
```

#### Prismatic Joint
```xml
<joint name="slider_joint" type="prismatic">
  <parent link="base"/>
  <child link="slider"/>
  <origin xyz="0 0 0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="0" upper="0.5" effort="100" velocity="0.5"/>
</joint>
```

### Robot Kinematic Structure

The kinematic structure of a robot is represented as a tree of links connected by joints, with a single base link at the root.

```
Humanoid Robot Kinematic Tree
         ┌─────────────┐
         │  base_link  │
         └──────┬──────┘
                │
         ┌──────▼──────┐
         │  torso_link │
         └──────┬──────┘
         ┌──────┴──────┐
    ┌────▼────┐    ┌───▼────┐
    │ head    │    │ pelvis │
    │ _link   │    │ _link  │
    └─────────┘    └────────┘
         │              │
    ┌────▼────┐    ┌────▼────┐
    │ left    │    │ left    │
    │ _arm    │    │ _leg    │
    │ _chain  │    │ _chain  │
    └─────────┘    └─────────┘
         │              │
    ┌────▼────┐    ┌────▼────┐
    │ right   │    │ right   │
    │ _arm    │    │ _leg    │
    │ _chain  │    │ _chain  │
    └─────────┘    └─────────┘
```

:::warning
URDF only supports tree structures, not closed loops. For closed-loop mechanisms, you need to use additional tools or approximate with multiple trees.
:::

## 4.3 Materials and Mesh Files

### Material Definition

Materials define the visual appearance of links, including color and texture.

```xml
<!-- Define materials at the top of the URDF file -->
<material name="red">
  <color rgba="1 0 0 1"/>
</material>

<material name="blue">
  <color rgba="0 0 1 0.8"/>
</material>

<material name="metal">
  <color rgba="0.7 0.7 0.7 1"/>
  <texture filename="package://my_robot/meshes/metal_texture.png"/>
</material>

<!-- Use materials in visual elements -->
<visual>
  <geometry>
    <box size="0.1 0.1 0.1"/>
  </geometry>
  <material name="red"/>
</visual>
```

### Mesh Files

Complex robot geometries are often defined using 3D mesh files (STL, DAE, OBJ, etc.).

```xml
<visual>
  <geometry>
    <mesh filename="package://my_robot/meshes/complex_part.dae" scale="1 1 1"/>
  </geometry>
  <material name="robot_gray"/>
</visual>

<collision>
  <!-- Use simplified collision mesh for performance -->
  <geometry>
    <mesh filename="package://my_robot/meshes/complex_part_collision.stl"/>
  </geometry>
</collision>
```

#### Mesh File Best Practices

- Use **DAE (Collada)** format for best compatibility
- Include **collision-optimized versions** of meshes
- Use **relative paths** with `package://` prefix
- **Scale appropriately** for your robot's size

## 4.4 Xacro: XML Macros for URDF

### Introduction to Xacro

Xacro (XML Macros) is a macro language for XML that allows you to create more modular and maintainable URDF files. It provides features like variables, macros, and mathematical expressions.

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="xacro_robot">

  <!-- Define properties -->
  <xacro:property name="M_PI" value="3.1415926535897931" />
  <xacro:property name="wheel_radius" value="0.1" />
  <xacro:property name="wheel_width" value="0.05" />

  <!-- Define a macro for creating wheels -->
  <xacro:macro name="wheel" params="prefix parent x y z">
    <joint name="${prefix}_wheel_joint" type="continuous">
      <parent link="${parent}"/>
      <child link="${prefix}_wheel"/>
      <origin xyz="${x} ${y} ${z}" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
    </joint>

    <link name="${prefix}_wheel">
      <visual>
        <origin rpy="${M_PI/2} 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </visual>
      <collision>
        <origin rpy="${M_PI/2} 0 0"/>
        <geometry>
          <cylinder radius="${wheel_radius}" length="${wheel_width}"/>
        </geometry>
      </collision>
      <inertial>
        <mass value="0.5"/>
        <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.001" iyz="0.0" izz="0.002"/>
      </inertial>
    </link>
  </xacro:macro>

  <!-- Use the macro to create wheels -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.15"/>
      </geometry>
    </visual>
  </link>

  <!-- Create wheels using the macro -->
  <xacro:wheel prefix="front_left" parent="base_link" x="0.15" y="0.1" z="-0.05"/>
  <xacro:wheel prefix="front_right" parent="base_link" x="0.15" y="-0.1" z="-0.05"/>
  <xacro:wheel prefix="back_left" parent="base_link" x="-0.15" y="0.1" z="-0.05"/>
  <xacro:wheel prefix="back_right" parent="base_link" x="-0.15" y="-0.1" z="-0.05"/>

</robot>
```

### Xacro vs URDF Comparison

| Feature | URDF | Xacro |
|---------|------|-------|
| Variables | No | Yes |
| Macros | No | Yes |
| Math expressions | No | Yes |
| Reusability | Low | High |
| Complexity | Simple | Moderate |
| Processing | Direct | Preprocessing required |

### Xacro Advanced Features

#### Conditional Statements
```xml
<xacro:macro name="conditional_part" params="include_sensor:=false">
  <xacro:if value="$(arg include_sensor)">
    <link name="sensor_link">
      <visual>
        <geometry>
          <box size="0.02 0.02 0.02"/>
        </geometry>
      </visual>
    </link>
  </xacro:if>
</xacro:macro>
```

#### Mathematical Expressions
```xml
<xacro:property name="length" value="0.5" />
<xacro:property name="volume" value="${length * length * length}" />
<xacro:property name="mass" value="${volume * 1000}" />  <!-- 1000 kg/m³ density -->
```

## 4.5 Frames, Transformations, and Coordinate Systems

### Coordinate System Conventions

ROS uses the right-handed coordinate system where:
- **X**: Forward (or toward the front of the robot)
- **Y**: Left (or toward the left of the robot)
- **Z**: Up (or toward the sky)

```
ROS Coordinate System
        Z (Up)
        │
        │
        └─────── Y (Left)
       ╱
      ╱
     X (Forward)
```

### Frame Relationships

Each link has its own coordinate frame, and joints define the transformation between parent and child frames.

```xml
<!-- Transformation from parent frame to joint frame -->
<joint name="arm_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <!-- Position of joint origin relative to parent frame -->
  <origin xyz="0 0.2 0.5" rpy="0 0 0"/>
  <!-- Joint axis in child frame coordinates -->
  <axis xyz="0 1 0"/>
</joint>
```

### URDF vs Collision vs Visual Comparison

| Element | Purpose | Performance | Detail |
|---------|---------|-------------|--------|
| Visual | Rendering/Visualization | Lower | High |
| Collision | Physics Simulation | Higher | Lower |
| Inertial | Dynamics | Fixed | Physics-specific |

```
Visual vs Collision vs Inertial
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Visual       │    │   Collision     │    │    Inertial     │
│   (Rendering)   │    │  (Physics)      │    │  (Dynamics)     │
│                 │    │                 │    │                 │
│  Detailed mesh  │    │  Simplified     │    │  Mathematical   │
│  textures,      │    │  geometry       │    │  model only     │
│  colors         │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 4.6 Minimal URDF Example

### Simple Robot Model

Here's a complete minimal URDF robot with basic links and joints:

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link (root of the robot) -->
  <link name="base_link">
    <visual>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder length="0.6" radius="0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.4" ixy="0.0" ixz="0.0" iyy="0.4" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Right leg -->
  <joint name="base_to_right_leg" type="fixed">
    <parent link="base_link"/>
    <child link="right_leg"/>
    <origin xyz="0 -0.23 0.25"/>
  </joint>

  <link name="right_leg">
    <visual>
      <geometry>
        <box size="0.6 0.1 0.2"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.6 0.1 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>

  <!-- Left leg -->
  <joint name="base_to_left_leg" type="fixed">
    <parent link="base_link"/>
    <child link="left_leg"/>
    <origin xyz="0 0.23 0.25"/>
  </joint>

  <link name="left_leg">
    <visual>
      <geometry>
        <box size="0.6 0.1 0.2"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.6 0.1 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
    </inertial>
  </link>
</robot>
```

## 4.7 Humanoid Robot URDF Examples

### Basic Humanoid Structure

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.5" iyz="0.0" izz="0.5"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.25"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="skin">
        <color rgba="0.8 0.6 0.4 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.02"/>
    </inertial>
  </link>

  <!-- Left Arm -->
  <joint name="left_shoulder_pitch" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.2 0 0.1"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="20" velocity="1"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.3"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 0.15"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 0.3"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="15" velocity="1"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <geometry>
        <cylinder radius="0.04" length="0.25"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.04" length="0.25"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0.125"/>
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.0005"/>
    </inertial>
  </link>

  <!-- Left Leg -->
  <joint name="left_hip_joint" type="revolute">
    <parent link="torso"/>
    <child link="left_thigh"/>
    <origin xyz="-0.1 -0.1 -0.25"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="30" velocity="1"/>
  </joint>

  <link name="left_thigh">
    <visual>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 -0.2"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh"/>
    <child link="left_shin"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="1.57" effort="30" velocity="1"/>
  </joint>

  <link name="left_shin">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 -0.2"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

</robot>
```

## 4.8 Loading URDF in RViz and Gazebo

### Loading in RViz

To visualize your URDF in RViz, you need to publish it using the `robot_state_publisher`:

```bash
# Launch the robot state publisher
ros2 run robot_state_publisher robot_state_publisher --ros-args -p robot_description:='$(cat your_robot.urdf)'

# Or use a launch file
ros2 launch your_package robot_description.launch.py
```

### Gazebo Integration

For Gazebo simulation, you need to add Gazebo-specific plugins and controller configurations:

```xml
<!-- Add Gazebo plugins for simulation -->
<gazebo>
  <plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
    <ros>
      <namespace>/robot</namespace>
      <remapping>~/out:=joint_states</remapping>
    </ros>
    <update_rate>30</update_rate>
  </plugin>
</gazebo>

<!-- Controller Manager Plugin for ros2_control -->
<gazebo>
  <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
    <parameters_filename>ros2_controllers.yaml</parameters_filename>
    <robot_namespace>/</robot_namespace>
  </plugin>
</gazebo>

<!-- For each link that needs physics properties -->
<gazebo reference="base_link">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
</gazebo>
```

### ROS 2 Controller Configuration

To properly control a humanoid robot, you need to define controller configurations. Here's an example controller configuration file:

```yaml
# ros2_controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    # Joint trajectory controllers for different parts of the robot
    left_arm_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    right_arm_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    left_leg_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    right_leg_controller:
      type: joint_trajectory_controller/JointTrajectoryController

    head_controller:
      type: joint_trajectory_controller/JointTrajectoryController

# Left Arm Controller Configuration
left_arm_controller:
  ros__parameters:
    joints:
      - left_shoulder_pitch
      - left_shoulder_roll
      - left_shoulder_yaw
      - left_elbow
      - left_wrist_yaw
      - left_wrist_pitch
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity

# Right Arm Controller Configuration
right_arm_controller:
  ros__parameters:
    joints:
      - right_shoulder_pitch
      - right_shoulder_roll
      - right_shoulder_yaw
      - right_elbow
      - right_wrist_yaw
      - right_wrist_pitch
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity

# Left Leg Controller Configuration
left_leg_controller:
  ros__parameters:
    joints:
      - left_hip_yaw
      - left_hip_roll
      - left_hip_pitch
      - left_knee
      - left_ankle_pitch
      - left_ankle_roll
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity

# Right Leg Controller Configuration
right_leg_controller:
  ros__parameters:
    joints:
      - right_hip_yaw
      - right_hip_roll
      - right_hip_pitch
      - right_knee
      - right_ankle_pitch
      - right_ankle_roll
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity

# Head Controller Configuration
head_controller:
  ros__parameters:
    joints:
      - head_pan
      - head_tilt
    command_interfaces:
      - position
    state_interfaces:
      - position
      - velocity
```

### Complete Humanoid Robot URDF with Controllers

Here's a more complete example that includes controller interfaces in the URDF:

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include gazebo plugins -->
  <gazebo>
    <plugin name="gazebo_ros2_control" filename="libgazebo_ros2_control.so">
      <parameters_filename>config/ros2_controllers.yaml</parameters_filename>
      <robot_namespace>/</robot_namespace>
    </plugin>
  </gazebo>

  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
      <material name="gray">
        <color rgba="0.5 0.5 0.5 1.0"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="5.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.2" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.1"/>
  </joint>

  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.2 0.6"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.3 0.2 0.6"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0.3"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.5" iyz="0.0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Left Hip Joint -->
  <joint name="left_hip_yaw" type="revolute">
    <parent link="torso"/>
    <child link="left_thigh"/>
    <origin xyz="-0.05 -0.15 -0.3"/>
    <axis xyz="0 0 1"/>
    <limit lower="-0.5" upper="0.5" effort="100" velocity="2"/>
    <dynamics damping="1.0" friction="0.1"/>
  </joint>

  <link name="left_thigh">
    <visual>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <origin xyz="0 0 -0.2"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Left Knee Joint -->
  <joint name="left_knee" type="revolute">
    <parent link="left_thigh"/>
    <child link="left_shin"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="2.5" effort="100" velocity="2"/>
    <dynamics damping="1.0" friction="0.1"/>
  </joint>

  <link name="left_shin">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="green">
        <color rgba="0 1 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 -0.2"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Left Ankle Joint -->
  <joint name="left_ankle_pitch" type="revolute">
    <parent link="left_shin"/>
    <child link="left_foot"/>
    <origin xyz="0 0 -0.4"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.5" upper="0.5" effort="50" velocity="1"/>
    <dynamics damping="0.5" friction="0.05"/>
  </joint>

  <link name="left_foot">
    <visual>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.2 0.1 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.001" ixy="0.0" ixz="0.0" iyy="0.002" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="neck_joint" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.3"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.0" upper="1.0" effort="10" velocity="1"/>
    <dynamics damping="0.5" friction="0.05"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
      <material name="skin">
        <color rgba="0.8 0.6 0.4 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.1"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.004" ixy="0.0" ixz="0.0" iyy="0.004" iyz="0.0" izz="0.004"/>
    </inertial>
  </link>

</robot>
```

### Controller Launch and Management

To launch and manage controllers, you'll need launch files:

```python
# launch/humanoid_controllers_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.events.lifecycle import ChangedState
from launch.event_handlers import OnProcessExit, OnStateTransition

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation time if true'
    )

    # Controller manager
    control_node = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            'path/to/ros2_controllers.yaml'
        ],
        output='screen'
    )

    # Joint state broadcaster spawner
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # Individual controller spawners
    left_arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['left_arm_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    right_arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['right_arm_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    left_leg_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['left_leg_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    right_leg_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['right_leg_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    head_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['head_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # Event handlers to ensure proper startup order
    load_joint_state_broadcaster = RegisterEventHandler(
        OnProcessExit(
            target_action=control_node,
            on_exit=[joint_state_broadcaster_spawner],
        )
    )

    load_left_arm_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=joint_state_broadcaster_spawner,
            on_exit=[left_arm_controller_spawner],
        )
    )

    load_right_arm_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=left_arm_controller_spawner,
            on_exit=[right_arm_controller_spawner],
        )
    )

    load_left_leg_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=right_arm_controller_spawner,
            on_exit=[left_leg_controller_spawner],
        )
    )

    load_right_leg_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=left_leg_controller_spawner,
            on_exit=[right_leg_controller_spawner],
        )
    )

    load_head_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=right_leg_controller_spawner,
            on_exit=[head_controller_spawner],
        )
    )

    return LaunchDescription([
        use_sim_time,
        control_node,
        load_joint_state_broadcaster,
        load_left_arm_controller,
        load_right_arm_controller,
        load_left_leg_controller,
        load_right_leg_controller,
        load_head_controller
    ])
```

### Control Theory Integration

For humanoid robots, understanding control theory is essential for proper controller implementation:

| Controller Type | Use Case | Advantages | Disadvantages |
|-----------------|----------|------------|---------------|
| Position Control | Precise joint positioning | Accurate positioning, simple | May cause oscillations |
| Velocity Control | Smooth motion control | Smooth transitions | Requires integration for position |
| Effort/Torque Control | Force control, compliant motion | Direct force control | Complex tuning |
| PID Control | Feedback control | Well-understood, stable | Requires tuning |
| Model Predictive Control | Complex multi-variable systems | Optimal control, constraints | Computationally intensive |

#### PID Controller Implementation Example

```python
class PIDController:
    def __init__(self, kp, ki, kd, dt):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.dt = dt  # Time step

        self.prev_error = 0.0
        self.integral = 0.0

    def compute(self, error):
        # Proportional term
        p_term = self.kp * error

        # Integral term
        self.integral += error * self.dt
        i_term = self.ki * self.integral

        # Derivative term
        derivative = (error - self.prev_error) / self.dt
        d_term = self.kd * derivative

        # Store current error for next iteration
        self.prev_error = error

        # Compute output
        output = p_term + i_term + d_term
        return output

# Example usage in a humanoid robot controller
class HumanoidJointController:
    def __init__(self, joint_name):
        self.joint_name = joint_name
        self.pid_controller = PIDController(kp=2.0, ki=0.1, kd=0.05, dt=0.01)
        self.target_position = 0.0
        self.current_position = 0.0

    def update(self, target_pos, current_pos):
        self.target_position = target_pos
        self.current_position = current_pos

        error = self.target_position - self.current_position
        control_output = self.pid_controller.compute(error)

        return control_output
```

## 4.9 Best Practices for Humanoid Robot URDFs

### 1. Proper Mass Distribution

```xml
<!-- Calculate realistic inertial properties -->
<link name="torso">
  <!-- Use CAD software to calculate actual inertial properties -->
  <inertial>
    <mass value="15.0"/>
    <origin xyz="0 0 0.1"/>
    <inertia ixx="0.8" ixy="0.0" ixz="0.0" iyy="0.8" iyz="0.0" izz="1.2"/>
  </inertial>
</link>
```

### 2. Hierarchical Organization

```
Humanoid URDF Organization
├── base_link (pelvis)
├── torso
│   ├── head
│   ├── left_arm
│   │   ├── left_upper_arm
│   │   └── left_lower_arm
│   └── right_arm
│       ├── right_upper_arm
│       └── right_lower_arm
└── legs
    ├── left_leg
    │   ├── left_thigh
    │   ├── left_shin
    │   └── left_foot
    └── right_leg
        ├── right_thigh
        ├── right_shin
        └── right_foot
```

### 3. Joint Limit Considerations

```xml
<!-- Set realistic joint limits based on human anatomy -->
<joint name="left_shoulder_pitch" type="revolute">
  <limit lower="-2.0" upper="2.0" effort="50" velocity="2"/>
</joint>
```

### 4. Collision Optimization

```xml
<!-- Use simplified collision geometries for performance -->
<collision>
  <!-- Instead of complex mesh, use multiple simple shapes -->
  <geometry>
    <cylinder radius="0.05" length="0.3"/>
  </geometry>
</collision>
```

:::tip
For humanoid robots, pay special attention to the center of mass location and ensure it's properly positioned for stable walking.
:::

## 4.10 Chapter Summary

This chapter covered the essential aspects of URDF robot modeling:

1. **URDF Fundamentals**: Understanding links, joints, and the XML structure
2. **Link Elements**: Visual, collision, and inertial properties
3. **Joint Types**: Fixed, revolute, continuous, prismatic, planar, and floating joints
4. **Xacro**: Macro language for modular and reusable URDFs
5. **Coordinate Systems**: Frame relationships and transformations
6. **Humanoid Applications**: Special considerations for humanoid robot modeling
7. **Best Practices**: Proper mass distribution, collision optimization, and organization

URDF is fundamental to robot simulation, visualization, and control. Proper URDF modeling ensures accurate physics simulation and effective robot control, especially critical for complex humanoid robots with multiple degrees of freedom.

## 4.11 Exercises

### Exercise 1: Basic URDF Creation (Beginner)
Create a simple URDF file for a mobile robot with a base, two wheels, and a caster. Include visual, collision, and inertial properties for each link.

### Exercise 2: Joint Types (Beginner)
Create a URDF with all six joint types (fixed, revolute, continuous, prismatic, planar, floating) and explain the use case for each.

### Exercise 3: Xacro Macros (Intermediate)
Create a Xacro file that defines a macro for a robot arm with 3 joints, then instantiate two arms (left and right) with different positions.

### Exercise 4: Humanoid Leg (Intermediate)
Model a humanoid leg with hip, knee, and ankle joints, including proper inertial properties and realistic joint limits.

### Exercise 5: Collision Optimization (Advanced)
Take a complex robot model and create an optimized version with simplified collision geometries while maintaining simulation accuracy.

## 4.12 Mini-Project: Simple Humanoid URDF

Create a complete humanoid robot URDF model that includes:

- A torso with proper inertial properties
- A head connected with a neck joint
- Two arms (left and right) with shoulder, elbow, and wrist joints
- Two legs (left and right) with hip, knee, and ankle joints
- Use Xacro for modularity and reusability
- Include proper materials and visual properties
- Add Gazebo plugins for simulation
- Validate the URDF using `check_urdf` tool

The model should be suitable for basic simulation and visualization in RViz and Gazebo, with realistic joint limits and mass properties appropriate for a humanoid robot.