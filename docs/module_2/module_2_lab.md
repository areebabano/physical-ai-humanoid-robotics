---
title: "Module 2 Lab - Hands-On Simulation for Humanoid Robotics"
sidebar_position: 8
---

# Module 2 Lab - Hands-On Simulation for Humanoid Robotics

## Lab Overview

This lab provides hands-on experience with Gazebo simulation for humanoid robots. You will create a complete simulation environment, implement physics-based models, and integrate with ROS 2 for realistic humanoid robot simulation.

## Learning Objectives

By completing this lab, you will:
- Set up a complete Gazebo simulation environment for humanoid robots
- Create and configure URDF models for simulation
- Implement physics parameters for realistic behavior
- Integrate sensors in the simulation environment
- Connect simulation to ROS 2 for control and monitoring
- Test humanoid behaviors in simulation

## Prerequisites

- Completion of Module 1 and Module 2.1-2.2
- Gazebo installed (Fortress or Garden)
- ROS 2 environment properly configured
- Basic understanding of physics concepts
- Experience with URDF from Module 1.3

## Lab Duration

Estimated completion time: 5-7 hours

## Exercise 1: Setting Up the Simulation Environment

First, create a new ROS 2 package for simulation:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python humanoid_simulation
cd humanoid_simulation
```

Create the package structure:

```
humanoid_simulation/
├── launch/
│   ├── simulation.launch.py
│   └── robot_spawn.launch.py
├── models/
│   └── simple_humanoid/
│       ├── model.sdf
│       └── meshes/
├── worlds/
│   └── humanoid_world.sdf
├── config/
│   ├── controller_params.yaml
│   └── robot_properties.yaml
├── scripts/
│   └── simulation_test.py
├── package.xml
└── setup.py
```

### 1.1 Creating a Basic Humanoid Model

Create a simple humanoid model in SDF format. First, create the `models/simple_humanoid/model.sdf` file:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <model name="simple_humanoid">
    <!-- Model properties -->
    <static>false</static>
    <self_collide>false</self_collide>
    <enable_wind>false</enable_wind>

    <!-- Base link -->
    <link name="base_link">
      <pose>0 0 1.0 0 0 0</pose>
      <inertial>
        <mass>10.0</mass>
        <inertia>
          <ixx>0.1</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.1</iyy>
          <iyz>0.0</iyz>
          <izz>0.1</izz>
        </inertia>
      </inertial>

      <visual name="base_visual">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
        <material>
          <ambient>0.8 0.8 0.8 1</ambient>
          <diffuse>0.8 0.8 0.8 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="base_collision">
        <geometry>
          <box>
            <size>0.3 0.2 0.5</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Torso -->
    <link name="torso">
      <pose>0 0 0.3 0 0 0</pose>
      <inertial>
        <mass>5.0</mass>
        <inertia>
          <ixx>0.05</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.05</iyy>
          <iyz>0.0</iyz>
          <izz>0.05</izz>
        </inertia>
      </inertial>

      <visual name="torso_visual">
        <geometry>
          <box>
            <size>0.25 0.15 0.4</size>
          </box>
        </geometry>
        <material>
          <ambient>0.6 0.6 0.8 1</ambient>
          <diffuse>0.6 0.6 0.8 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="torso_collision">
        <geometry>
          <box>
            <size>0.25 0.15 0.4</size>
          </box>
        </geometry>
      </collision>
    </link>

    <!-- Joint connecting base to torso -->
    <joint name="base_torso_joint" type="revolute">
      <parent>base_link</parent>
      <child>torso</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>100</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>0 0 0.25 0 0 0</pose>
    </joint>

    <!-- Left leg -->
    <link name="left_thigh">
      <pose>0.1 0 0 0 0 0</pose>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.02</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.02</iyy>
          <iyz>0.0</iyz>
          <izz>0.02</izz>
        </inertia>
      </inertial>

      <visual name="left_thigh_visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.8 0.6 0.6 1</ambient>
          <diffuse>0.8 0.6 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="left_thigh_collision">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="left_hip_joint" type="revolute">
      <parent>base_link</parent>
      <child>left_thigh</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>50</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>0.1 0 -0.1 0 0 0</pose>
    </joint>

    <link name="left_shin">
      <pose>0.1 0 -0.2 0 0 0</pose>
      <inertial>
        <mass>1.5</mass>
        <inertia>
          <ixx>0.01</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.01</iyy>
          <iyz>0.0</iyz>
          <izz>0.01</izz>
        </inertia>
      </inertial>

      <visual name="left_shin_visual">
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.35</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.8 0.6 0.6 1</ambient>
          <diffuse>0.8 0.6 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="left_shin_collision">
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.35</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="left_knee_joint" type="revolute">
      <parent>left_thigh</parent>
      <child>left_shin</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>0.0</upper>
          <effort>50</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>0.1 0 -0.2 0 0 0</pose>
    </joint>

    <!-- Right leg (similar to left) -->
    <link name="right_thigh">
      <pose>-0.1 0 0 0 0 0</pose>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.02</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.02</iyy>
          <iyz>0.0</iyz>
          <izz>0.02</izz>
        </inertia>
      </inertial>

      <visual name="right_thigh_visual">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.8 0.6 0.6 1</ambient>
          <diffuse>0.8 0.6 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="right_thigh_collision">
        <geometry>
          <cylinder>
            <radius>0.05</radius>
            <length>0.4</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="right_hip_joint" type="revolute">
      <parent>base_link</parent>
      <child>right_thigh</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>50</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>-0.1 0 -0.1 0 0 0</pose>
    </joint>

    <link name="right_shin">
      <pose>-0.1 0 -0.2 0 0 0</pose>
      <inertial>
        <mass>1.5</mass>
        <inertia>
          <ixx>0.01</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.01</iyy>
          <iyz>0.0</iyz>
          <izz>0.01</izz>
        </inertia>
      </inertial>

      <visual name="right_shin_visual">
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.35</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.8 0.6 0.6 1</ambient>
          <diffuse>0.8 0.6 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="right_shin_collision">
        <geometry>
          <cylinder>
            <radius>0.04</radius>
            <length>0.35</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="right_knee_joint" type="revolute">
      <parent>right_thigh</parent>
      <child>right_shin</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>0.0</upper>
          <effort>50</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>-0.1 0 -0.2 0 0 0</pose>
    </joint>

    <!-- Left arm -->
    <link name="left_upper_arm">
      <pose>0.15 0 0.2 0 0 0</pose>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.005</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.005</iyy>
          <iyz>0.0</iyz>
          <izz>0.005</izz>
        </inertia>
      </inertial>

      <visual name="left_upper_arm_visual">
        <geometry>
          <cylinder>
            <radius>0.03</radius>
            <length>0.3</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.6 0.8 0.6 1</ambient>
          <diffuse>0.6 0.8 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="left_upper_arm_collision">
        <geometry>
          <cylinder>
            <radius>0.03</radius>
            <length>0.3</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="left_shoulder_joint" type="revolute">
      <parent>torso</parent>
      <child>left_upper_arm</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>30</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>0.15 0 0.1 0 0 0</pose>
    </joint>

    <link name="left_lower_arm">
      <pose>0.15 0 0.05 0 0 0</pose>
      <inertial>
        <mass>0.8</mass>
        <inertia>
          <ixx>0.003</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.003</iyy>
          <iyz>0.0</iyz>
          <izz>0.003</izz>
        </inertia>
      </inertial>

      <visual name="left_lower_arm_visual">
        <geometry>
          <cylinder>
            <radius>0.025</radius>
            <length>0.25</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.6 0.8 0.6 1</ambient>
          <diffuse>0.6 0.8 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="left_lower_arm_collision">
        <geometry>
          <cylinder>
            <radius>0.025</radius>
            <length>0.25</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="left_elbow_joint" type="revolute">
      <parent>left_upper_arm</parent>
      <child>left_lower_arm</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>20</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>0.15 0 -0.1 0 0 0</pose>
    </joint>

    <!-- Right arm -->
    <link name="right_upper_arm">
      <pose>-0.15 0 0.2 0 0 0</pose>
      <inertial>
        <mass>1.0</mass>
        <inertia>
          <ixx>0.005</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.005</iyy>
          <iyz>0.0</iyz>
          <izz>0.005</izz>
        </inertia>
      </inertial>

      <visual name="right_upper_arm_visual">
        <geometry>
          <cylinder>
            <radius>0.03</radius>
            <length>0.3</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.6 0.8 0.6 1</ambient>
          <diffuse>0.6 0.8 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="right_upper_arm_collision">
        <geometry>
          <cylinder>
            <radius>0.03</radius>
            <length>0.3</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="right_shoulder_joint" type="revolute">
      <parent>torso</parent>
      <child>right_upper_arm</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>30</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>-0.15 0 0.1 0 0 0</pose>
    </joint>

    <link name="right_lower_arm">
      <pose>-0.15 0 0.05 0 0 0</pose>
      <inertial>
        <mass>0.8</mass>
        <inertia>
          <ixx>0.003</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.003</iyy>
          <iyz>0.0</iyz>
          <izz>0.003</izz>
        </inertia>
      </inertial>

      <visual name="right_lower_arm_visual">
        <geometry>
          <cylinder>
            <radius>0.025</radius>
            <length>0.25</length>
          </cylinder>
        </geometry>
        <material>
          <ambient>0.6 0.8 0.6 1</ambient>
          <diffuse>0.6 0.8 0.6 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="right_lower_arm_collision">
        <geometry>
          <cylinder>
            <radius>0.025</radius>
            <length>0.25</length>
          </cylinder>
        </geometry>
      </collision>
    </link>

    <joint name="right_elbow_joint" type="revolute">
      <parent>right_upper_arm</parent>
      <child>right_lower_arm</child>
      <axis>
        <xyz>0 0 1</xyz>
        <limit>
          <lower>-1.57</lower>
          <upper>1.57</upper>
          <effort>20</effort>
          <velocity>1</velocity>
        </limit>
      </axis>
      <pose>-0.15 0 -0.1 0 0 0</pose>
    </joint>

    <!-- Head -->
    <link name="head">
      <pose>0 0 0.4 0 0 0</pose>
      <inertial>
        <mass>2.0</mass>
        <inertia>
          <ixx>0.01</ixx>
          <ixy>0.0</ixy>
          <ixz>0.0</ixz>
          <iyy>0.01</iyy>
          <iyz>0.0</iyz>
          <izz>0.01</izz>
        </inertia>
      </inertial>

      <visual name="head_visual">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
        <material>
          <ambient>0.9 0.9 0.9 1</ambient>
          <diffuse>0.9 0.9 0.9 1</diffuse>
          <specular>0.1 0.1 0.1 1</specular>
        </material>
      </visual>

      <collision name="head_collision">
        <geometry>
          <sphere>
            <radius>0.1</radius>
          </sphere>
        </geometry>
      </collision>
    </link>

    <joint name="neck_joint" type="revolute">
      <parent>torso</parent>
      <child>head</child>
      <axis>
        <xyz>0 1 0</xyz>
        <limit>
          <lower>-0.785</lower>
          <upper>0.785</upper>
          <effort>10</effort>
          <velocity>0.5</velocity>
        </limit>
      </axis>
      <pose>0 0 0.2 0 0 0</pose>
    </joint>
  </model>
</sdf>
```

### 1.2 Creating a Simulation World

Create `worlds/humanoid_world.sdf`:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics engine -->
    <physics name="1ms" type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
      <real_time_update_rate>1000.0</real_time_update_rate>
      <gravity>0 0 -9.8</gravity>
    </physics>

    <!-- GUI configuration -->
    <gui fullscreen="0">
      <camera name="user_camera">
        <pose>5 -5 3 0 0.4 1.5707</pose>
        <view_controller>orbit</view_controller>
      </camera>
    </gui>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Simple floor with texture -->
    <model name="floor">
      <static>true</static>
      <link name="floor_link">
        <collision name="floor_collision">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>10 10</size>
            </plane>
          </geometry>
        </collision>
        <visual name="floor_visual">
          <geometry>
            <plane>
              <normal>0 0 1</normal>
              <size>10 10</size>
            </plane>
          </geometry>
          <material>
            <ambient>0.7 0.7 0.7 1</ambient>
            <diffuse>0.7 0.7 0.7 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
      </link>
    </model>

    <!-- Add obstacles for testing -->
    <model name="obstacle_1">
      <pose>2 0 0.5 0 0 0</pose>
      <link name="obstacle_link">
        <inertial>
          <mass>1.0</mass>
          <inertia>
            <ixx>0.1</ixx>
            <ixy>0.0</ixy>
            <ixz>0.0</ixz>
            <iyy>0.1</iyy>
            <iyz>0.0</iyz>
            <izz>0.1</izz>
          </inertia>
        </inertial>
        <visual name="obstacle_visual">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
          <material>
            <ambient>0.8 0.4 0.2 1</ambient>
            <diffuse>0.8 0.4 0.2 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
        <collision name="obstacle_collision">
          <geometry>
            <box>
              <size>0.5 0.5 1.0</size>
            </box>
          </geometry>
        </collision>
      </link>
    </model>

    <!-- Add a ramp for testing -->
    <model name="ramp">
      <pose>-2 0 0 0 0 0.785</pose>  <!-- 45-degree angle -->
      <link name="ramp_link">
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
        <visual name="ramp_visual">
          <geometry>
            <box>
              <size>2.0 1.0 0.2</size>
            </box>
          </geometry>
          <material>
            <ambient>0.5 0.5 0.7 1</ambient>
            <diffuse>0.5 0.5 0.7 1</diffuse>
            <specular>0.1 0.1 0.1 1</specular>
          </material>
        </visual>
        <collision name="ramp_collision">
          <geometry>
            <box>
              <size>2.0 1.0 0.2</size>
            </box>
          </geometry>
        </collision>
      </link>
    </model>

    <!-- Include the humanoid model -->
    <include>
      <uri>model://simple_humanoid</uri>
      <pose>0 0 1.0 0 0 0</pose>
    </include>
  </world>
</sdf>
```

## Exercise 2: Creating ROS 2 Integration

Create a controller interface to connect the simulation to ROS 2. First, create a URDF version of the robot that includes ROS 2 control interfaces:

Create `models/simple_humanoid/model.urdf`:

```xml
<?xml version="1.0" ?>
<robot name="simple_humanoid" xmlns:xacro="http://www.ros.org/wiki/xacro">
  <!-- Base link -->
  <link name="base_link">
    <inertial>
      <mass value="10.0" />
      <origin xyz="0 0 0" rpy="0 0 0" />
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
    </inertial>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="0.3 0.2 0.5" />
      </geometry>
      <material name="gray">
        <color rgba="0.8 0.8 0.8 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="0.3 0.2 0.5" />
      </geometry>
    </collision>
  </link>

  <!-- Torso -->
  <link name="torso">
    <inertial>
      <mass value="5.0" />
      <origin xyz="0 0 0" rpy="0 0 0" />
      <inertia ixx="0.05" ixy="0.0" ixz="0.0" iyy="0.05" iyz="0.0" izz="0.05" />
    </inertial>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="0.25 0.15 0.4" />
      </geometry>
      <material name="blue">
        <color rgba="0.6 0.6 0.8 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <box size="0.25 0.15 0.4" />
      </geometry>
    </collision>
  </link>

  <!-- Joint connecting base to torso -->
  <joint name="base_torso_joint" type="revolute">
    <parent link="base_link" />
    <child link="torso" />
    <origin xyz="0 0 0.25" rpy="0 0 0" />
    <axis xyz="0 0 1" />
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1" />
  </joint>

  <!-- Left leg -->
  <link name="left_thigh">
    <inertial>
      <mass value="2.0" />
      <origin xyz="0 0 -0.2" rpy="0 0 0" />
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.02" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.05" length="0.4" />
      </geometry>
      <material name="red">
        <color rgba="0.8 0.6 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.05" length="0.4" />
      </geometry>
    </collision>
  </link>

  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link" />
    <child link="left_thigh" />
    <origin xyz="0.1 0 -0.1" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1" />
  </joint>

  <link name="left_shin">
    <inertial>
      <mass value="1.5" />
      <origin xyz="0 0 -0.175" rpy="0 0 0" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.175" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.04" length="0.35" />
      </geometry>
      <material name="red">
        <color rgba="0.8 0.6 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.175" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.04" length="0.35" />
      </geometry>
    </collision>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh" />
    <child link="left_shin" />
    <origin xyz="0 0 -0.4" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="0.0" effort="50" velocity="1" />
  </joint>

  <!-- Right leg -->
  <link name="right_thigh">
    <inertial>
      <mass value="2.0" />
      <origin xyz="0 0 -0.2" rpy="0 0 0" />
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.02" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.05" length="0.4" />
      </geometry>
      <material name="red">
        <color rgba="0.8 0.6 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.2" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.05" length="0.4" />
      </geometry>
    </collision>
  </link>

  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link" />
    <child link="right_thigh" />
    <origin xyz="-0.1 0 -0.1" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1" />
  </joint>

  <link name="right_shin">
    <inertial>
      <mass value="1.5" />
      <origin xyz="0 0 -0.175" rpy="0 0 0" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.175" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.04" length="0.35" />
      </geometry>
      <material name="red">
        <color rgba="0.8 0.6 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.175" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.04" length="0.35" />
      </geometry>
    </collision>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_thigh" />
    <child link="right_shin" />
    <origin xyz="0 0 -0.4" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="0.0" effort="50" velocity="1" />
  </joint>

  <!-- Left arm -->
  <link name="left_upper_arm">
    <inertial>
      <mass value="1.0" />
      <origin xyz="0 0 -0.15" rpy="0 0 0" />
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.005" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.03" length="0.3" />
      </geometry>
      <material name="green">
        <color rgba="0.6 0.8 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.03" length="0.3" />
      </geometry>
    </collision>
  </link>

  <joint name="left_shoulder_joint" type="revolute">
    <parent link="torso" />
    <child link="left_upper_arm" />
    <origin xyz="0.15 0 0.1" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="1.57" effort="30" velocity="1" />
  </joint>

  <link name="left_lower_arm">
    <inertial>
      <mass value="0.8" />
      <origin xyz="0 0 -0.125" rpy="0 0 0" />
      <inertia ixx="0.003" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.003" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.125" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.025" length="0.25" />
      </geometry>
      <material name="green">
        <color rgba="0.6 0.8 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.125" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.025" length="0.25" />
      </geometry>
    </collision>
  </link>

  <joint name="left_elbow_joint" type="revolute">
    <parent link="left_upper_arm" />
    <child link="left_lower_arm" />
    <origin xyz="0 0 -0.3" rpy="0 0 0" />
    <axis xyz="0 0 1" />
    <limit lower="-1.57" upper="1.57" effort="20" velocity="1" />
  </joint>

  <!-- Right arm -->
  <link name="right_upper_arm">
    <inertial>
      <mass value="1.0" />
      <origin xyz="0 0 -0.15" rpy="0 0 0" />
      <inertia ixx="0.005" ixy="0.0" ixz="0.0" iyy="0.005" iyz="0.0" izz="0.005" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.03" length="0.3" />
      </geometry>
      <material name="green">
        <color rgba="0.6 0.8 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.15" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.03" length="0.3" />
      </geometry>
    </collision>
  </link>

  <joint name="right_shoulder_joint" type="revolute">
    <parent link="torso" />
    <child link="right_upper_arm" />
    <origin xyz="-0.15 0 0.1" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-1.57" upper="1.57" effort="30" velocity="1" />
  </joint>

  <link name="right_lower_arm">
    <inertial>
      <mass value="0.8" />
      <origin xyz="0 0 -0.125" rpy="0 0 0" />
      <inertia ixx="0.003" ixy="0.0" ixz="0.0" iyy="0.003" iyz="0.0" izz="0.003" />
    </inertial>

    <visual>
      <origin xyz="0 0 -0.125" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.025" length="0.25" />
      </geometry>
      <material name="green">
        <color rgba="0.6 0.8 0.6 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 -0.125" rpy="1.57 0 0" />
      <geometry>
        <cylinder radius="0.025" length="0.25" />
      </geometry>
    </collision>
  </link>

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm" />
    <child link="right_lower_arm" />
    <origin xyz="0 0 -0.3" rpy="0 0 0" />
    <axis xyz="0 0 1" />
    <limit lower="-1.57" upper="1.57" effort="20" velocity="1" />
  </joint>

  <!-- Head -->
  <link name="head">
    <inertial>
      <mass value="2.0" />
      <origin xyz="0 0 0" rpy="0 0 0" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>

    <visual>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <sphere radius="0.1" />
      </geometry>
      <material name="white">
        <color rgba="0.9 0.9 0.9 1" />
      </material>
    </visual>

    <collision>
      <origin xyz="0 0 0" rpy="0 0 0" />
      <geometry>
        <sphere radius="0.1" />
      </geometry>
    </collision>
  </link>

  <joint name="neck_joint" type="revolute">
    <parent link="torso" />
    <child link="head" />
    <origin xyz="0 0 0.2" rpy="0 0 0" />
    <axis xyz="0 1 0" />
    <limit lower="-0.785" upper="0.785" effort="10" velocity="0.5" />
  </joint>

  <!-- ROS2 Control interface -->
  <ros2_control name="GazeboSystem" type="system">
    <hardware>
      <plugin>gazebo_ros2_control/GazeboSystem</plugin>
    </hardware>

    <joint name="left_hip_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="left_knee_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="right_hip_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="right_knee_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="left_shoulder_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="left_elbow_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="right_shoulder_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="right_elbow_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>

    <joint name="neck_joint">
      <command_interface name="position"/>
      <command_interface name="velocity"/>
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>
  </ros2_control>

  <!-- Gazebo plugin for ROS control -->
  <gazebo>
    <plugin filename="libgazebo_ros2_control.so" name="gazebo_ros2_control">
      <parameters>$(find humanoid_simulation)/config/controller_params.yaml</parameters>
    </plugin>
  </gazebo>
</robot>
```

## Exercise 3: Creating Controller Configuration

Create `config/controller_params.yaml`:

```yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    left_leg_controller:
      type: position_controllers/JointGroupPositionController

    right_leg_controller:
      type: position_controllers/JointGroupPositionController

    left_arm_controller:
      type: position_controllers/JointGroupPositionController

    right_arm_controller:
      type: position_controllers/JointGroupPositionController

    head_controller:
      type: position_controllers/JointGroupPositionController

left_leg_controller:
  ros__parameters:
    joints:
      - left_hip_joint
      - left_knee_joint

right_leg_controller:
  ros__parameters:
    joints:
      - right_hip_joint
      - right_knee_joint

left_arm_controller:
  ros__parameters:
    joints:
      - left_shoulder_joint
      - left_elbow_joint

right_arm_controller:
  ros__parameters:
    joints:
      - right_shoulder_joint
      - right_elbow_joint

head_controller:
  ros__parameters:
    joints:
      - neck_joint
```

## Exercise 4: Creating Launch Files

Create `launch/simulation.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    world_name = LaunchConfiguration('world_name', default='humanoid_world')
    headless = LaunchConfiguration('headless', default='false')

    # Paths
    pkg_gazebo_ros = FindPackageShare('gazebo_ros')
    pkg_humanoid_simulation = FindPackageShare('humanoid_simulation')

    # Gazebo launch
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([pkg_gazebo_ros, 'launch', 'gazebo.launch.py'])
        ]),
        launch_arguments={
            'world': PathJoinSubstitution([pkg_humanoid_simulation, 'worlds', world_name]),
            'verbose': 'false',
            'gui': [IfCondition(headless), 'false', 'true'],
        }.items()
    )

    # Robot state publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {'use_sim_time': use_sim_time},
            {'robot_description': PathJoinSubstitution([
                pkg_humanoid_simulation, 'models', 'simple_humanoid', 'model.urdf'
            ])}
        ]
    )

    # Spawn entity node
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description',
            '-entity', 'simple_humanoid',
            '-x', '0',
            '-y', '0',
            '-z', '1.0',
            '-R', '0',
            '-P', '0',
            '-Y', '0'
        ],
        output='screen'
    )

    # Controller manager
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    left_leg_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['left_leg_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    right_leg_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['right_leg_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    left_arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['left_arm_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    right_arm_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['right_arm_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    head_controller_spawner = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['head_controller'],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    # RViz2 node
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', PathJoinSubstitution([
            pkg_humanoid_simulation, 'config', 'simulation.rviz'
        ])],
        parameters=[{'use_sim_time': use_sim_time}],
        condition=IfCondition(LaunchConfiguration('rviz', default='true'))
    )

    # Create launch description
    ld = LaunchDescription()

    # Add launch arguments
    ld.add_action(DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock if true'
    ))

    ld.add_action(DeclareLaunchArgument(
        'world_name',
        default_value='humanoid_world.sdf',
        description='Choose one of the world files from `/humanoid_simulation/worlds`'
    ))

    ld.add_action(DeclareLaunchArgument(
        'headless',
        default_value='false',
        description='Run Gazebo headless without GUI'
    ))

    ld.add_action(DeclareLaunchArgument(
        'rviz',
        default_value='true',
        description='Open RViz2'
    ))

    # Add actions
    ld.add_action(gazebo)
    ld.add_action(robot_state_publisher)
    ld.add_action(spawn_entity)

    # Add controller spawners
    ld.add_action(joint_state_broadcaster_spawner)
    ld.add_action(left_leg_controller_spawner)
    ld.add_action(right_leg_controller_spawner)
    ld.add_action(left_arm_controller_spawner)
    ld.add_action(right_arm_controller_spawner)
    ld.add_action(head_controller_spawner)

    # Optionally add RViz
    ld.add_action(rviz)

    return ld
```

## Exercise 5: Creating a Simulation Test Script

Create `scripts/simulation_test.py`:

```python
#!/usr/bin/env python3

"""
Simulation test script for humanoid robot
Tests various simulation scenarios and robot behaviors
"""

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from builtin_interfaces.msg import Duration
from controller_manager_msgs.srv import SwitchController
import time
import math


class SimulationTestNode(Node):
    def __init__(self):
        super().__init__('simulation_test_node')

        # Publishers
        self.joint_cmd_pub = self.create_publisher(
            JointState, '/joint_commands', 10
        )
        self.status_pub = self.create_publisher(
            String, '/simulation_status', 10
        )

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )

        # Service clients
        self.controller_switch_client = self.create_client(
            SwitchController, '/controller_manager/switch_controller'
        )

        # Wait for services
        self.get_logger().info('Waiting for controller manager...')
        self.controller_switch_client.wait_for_service()

        # Robot state
        self.joint_positions = {}
        self.joint_velocities = {}
        self.joint_efforts = {}

        # Test sequence
        self.test_sequence = [
            self.test_standing_pose,
            self.test_arm_movement,
            self.test_leg_movement,
            self.test_head_movement,
            self.test_balancing,
        ]
        self.current_test = 0

        # Timer for test execution
        self.test_timer = self.create_timer(0.1, self.run_tests)
        self.test_step = 0
        self.test_start_time = time.time()

        self.get_logger().info('Simulation test node initialized')

    def joint_state_callback(self, msg):
        """Update joint state information"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]
            if i < len(msg.velocity):
                self.joint_velocities[name] = msg.velocity[i]
            if i < len(msg.effort):
                self.joint_efforts[name] = msg.effort[i]

    def run_tests(self):
        """Run the test sequence"""
        if self.current_test < len(self.test_sequence):
            test_func = self.test_sequence[self.current_test]
            if test_func():
                self.current_test += 1
                self.test_step = 0
                self.test_start_time = time.time()
                self.get_logger().info(f'Completed test {self.current_test}, moving to next')
        else:
            self.test_timer.cancel()
            self.get_logger().info('All tests completed successfully')

    def send_joint_commands(self, joint_positions):
        """Send joint position commands"""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(joint_positions.keys())
        msg.position = list(joint_positions.values())

        self.joint_cmd_pub.publish(msg)

    def switch_controllers(self, start_controllers, stop_controllers):
        """Switch controllers on/off"""
        request = SwitchController.Request()
        request.start_controllers = start_controllers
        request.stop_controllers = stop_controllers
        request.strictness = SwitchController.Request.BEST_EFFORT

        future = self.controller_switch_client.call_async(request)
        return future

    def test_standing_pose(self):
        """Test standing pose - move to neutral standing position"""
        # Define standing pose (simplified)
        standing_pose = {
            'left_hip_joint': 0.0,
            'left_knee_joint': 0.0,
            'right_hip_joint': 0.0,
            'right_knee_joint': 0.0,
            'left_shoulder_joint': 0.0,
            'left_elbow_joint': 0.0,
            'right_shoulder_joint': 0.0,
            'right_elbow_joint': 0.0,
            'neck_joint': 0.0
        }

        if self.test_step < 100:  # 10 seconds at 10 Hz
            self.send_joint_commands(standing_pose)
            self.test_step += 1

            # Publish status
            if self.test_step % 50 == 0:  # Every 5 seconds
                status_msg = String()
                status_msg.data = f'Standing pose test: {self.test_step}/100'
                self.status_pub.publish(status_msg)

            return False
        else:
            return True

    def test_arm_movement(self):
        """Test arm movement patterns"""
        t = time.time() - self.test_start_time

        if t < 5.0:  # 5 seconds of arm waving
            # Wave arms in a coordinated pattern
            left_arm_pos = math.sin(t * 2) * 0.5
            right_arm_pos = math.sin(t * 2 + math.pi) * 0.5

            arm_pose = {
                'left_shoulder_joint': left_arm_pos,
                'left_elbow_joint': -left_arm_pos * 0.7,
                'right_shoulder_joint': right_arm_pos,
                'right_elbow_joint': -right_arm_pos * 0.7
            }

            self.send_joint_commands(arm_pose)

            status_msg = String()
            status_msg.data = f'Arm movement test: {t:.1f}s'
            self.status_pub.publish(status_msg)

            return False
        else:
            return True

    def test_leg_movement(self):
        """Test leg movement patterns"""
        t = time.time() - self.test_start_time

        if t < 6.0:  # 6 seconds of leg movement
            # Simple leg movement (not walking, just testing joints)
            left_leg_pos = math.sin(t * 1.5) * 0.3
            right_leg_pos = math.sin(t * 1.5 + math.pi) * 0.3

            leg_pose = {
                'left_hip_joint': left_leg_pos,
                'left_knee_joint': -abs(left_leg_pos) * 0.8,
                'right_hip_joint': right_leg_pos,
                'right_knee_joint': -abs(right_leg_pos) * 0.8
            }

            self.send_joint_commands(leg_pose)

            status_msg = String()
            status_msg.data = f'Leg movement test: {t:.1f}s'
            self.status_pub.publish(status_msg)

            return False
        else:
            return True

    def test_head_movement(self):
        """Test head/neck movement"""
        t = time.time() - self.test_start_time

        if t < 4.0:  # 4 seconds of head movement
            # Look left and right
            head_pos = math.sin(t * 1.0) * 0.5

            head_pose = {
                'neck_joint': head_pos
            }

            self.send_joint_commands(head_pose)

            status_msg = String()
            status_msg.data = f'Head movement test: {t:.1f}s'
            self.status_pub.publish(status_msg)

            return False
        else:
            return True

    def test_balancing(self):
        """Test basic balancing behavior"""
        # Move back to standing position
        standing_pose = {
            'left_hip_joint': 0.0,
            'left_knee_joint': 0.0,
            'right_hip_joint': 0.0,
            'right_knee_joint': 0.0,
            'left_shoulder_joint': 0.0,
            'left_elbow_joint': 0.0,
            'right_shoulder_joint': 0.0,
            'right_elbow_joint': 0.0,
            'neck_joint': 0.0
        }

        if self.test_step < 50:  # 5 seconds at 10 Hz
            self.send_joint_commands(standing_pose)
            self.test_step += 1

            status_msg = String()
            status_msg.data = f'Balancing test: {self.test_step}/50'
            self.status_pub.publish(status_msg)

            return False
        else:
            return True


def main(args=None):
    rclpy.init(args=args)

    node = SimulationTestNode()

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

## Exercise 6: Creating a Controller Node

Create `scripts/controller_node.py`:

```python
#!/usr/bin/env python3

"""
Controller node for humanoid robot simulation
Implements basic control algorithms for humanoid behaviors
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from builtin_interfaces.msg import Duration
from controller_manager_msgs.srv import SwitchController
import numpy as np
import math
import time


class HumanoidControllerNode(Node):
    def __init__(self):
        super().__init__('humanoid_controller_node')

        # Publishers
        self.joint_cmd_pub = self.create_publisher(
            JointState, '/joint_commands', 10
        )
        self.status_pub = self.create_publisher(
            String, '/controller_status', 10
        )

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, '/joint_states', self.joint_state_callback, 10
        )
        self.cmd_vel_sub = self.create_subscription(
            Twist, '/cmd_vel', self.cmd_vel_callback, 10
        )
        self.behavior_sub = self.create_subscription(
            String, '/behavior_command', self.behavior_callback, 10
        )

        # Robot state
        self.current_positions = {}
        self.current_velocities = {}
        self.current_efforts = {}
        self.desired_positions = {}
        self.desired_velocities = {}

        # Controller parameters
        self.kp = 100.0  # Proportional gain
        self.kd = 10.0   # Derivative gain
        self.control_freq = 100  # Hz
        self.dt = 1.0 / self.control_freq

        # Behavior state
        self.current_behavior = 'idle'
        self.cmd_vel = Twist()

        # Timer for control loop
        self.control_timer = self.create_timer(
            self.dt, self.control_loop
        )

        # Initialize desired positions to current positions
        self.initialize_positions()

        self.get_logger().info('Humanoid controller node initialized')

    def initialize_positions(self):
        """Initialize desired positions to neutral pose"""
        joint_names = [
            'left_hip_joint', 'left_knee_joint', 'right_hip_joint', 'right_knee_joint',
            'left_shoulder_joint', 'left_elbow_joint', 'right_shoulder_joint', 'right_elbow_joint',
            'neck_joint'
        ]

        neutral_positions = [0.0] * len(joint_names)

        for name, pos in zip(joint_names, neutral_positions):
            self.desired_positions[name] = pos
            self.desired_velocities[name] = 0.0

    def joint_state_callback(self, msg):
        """Update current joint state"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.current_positions[name] = msg.position[i]
            if i < len(msg.velocity):
                self.current_velocities[name] = msg.velocity[i]
            if i < len(msg.effort):
                self.current_efforts[name] = msg.effort[i]

    def cmd_vel_callback(self, msg):
        """Update velocity command"""
        self.cmd_vel = msg

    def behavior_callback(self, msg):
        """Update behavior command"""
        self.current_behavior = msg.data
        self.get_logger().info(f'Switching to behavior: {self.current_behavior}')

    def control_loop(self):
        """Main control loop"""
        # Based on current behavior, update desired positions
        self.update_behavior_targets()

        # Apply PD control
        self.apply_pd_control()

        # Publish commands
        self.publish_joint_commands()

        # Publish status
        self.publish_status()

    def update_behavior_targets(self):
        """Update desired positions based on current behavior"""
        t = time.time()

        if self.current_behavior == 'idle':
            # Stay in neutral position
            pass
        elif self.current_behavior == 'wave':
            # Wave arms
            left_arm_pos = math.sin(t * 2) * 0.5
            right_arm_pos = math.sin(t * 2 + math.pi) * 0.5

            self.desired_positions['left_shoulder_joint'] = left_arm_pos
            self.desired_positions['left_elbow_joint'] = -abs(left_arm_pos) * 0.7
            self.desired_positions['right_shoulder_joint'] = right_arm_pos
            self.desired_positions['right_elbow_joint'] = -abs(right_arm_pos) * 0.7
        elif self.current_behavior == 'look_around':
            # Look left and right
            head_pos = math.sin(t * 0.5) * 0.5
            self.desired_positions['neck_joint'] = head_pos
        elif self.current_behavior == 'dance':
            # Simple dance movement
            left_leg_pos = math.sin(t * 1.5) * 0.3
            right_leg_pos = math.sin(t * 1.5 + math.pi) * 0.3
            left_arm_pos = math.sin(t * 2 + math.pi/2) * 0.4
            right_arm_pos = math.sin(t * 2) * 0.4

            self.desired_positions['left_hip_joint'] = left_leg_pos
            self.desired_positions['right_hip_joint'] = right_leg_pos
            self.desired_positions['left_shoulder_joint'] = left_arm_pos
            self.desired_positions['right_shoulder_joint'] = right_arm_pos
        else:
            # Default to neutral position
            for joint in self.desired_positions:
                self.desired_positions[joint] = 0.0

    def apply_pd_control(self):
        """Apply PD control to compute joint efforts"""
        # For simplicity, we'll just send position commands
        # In a real implementation, you would compute efforts based on position/velocity errors
        pass

    def publish_joint_commands(self):
        """Publish joint commands"""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(self.desired_positions.keys())
        msg.position = list(self.desired_positions.values())

        self.joint_cmd_pub.publish(msg)

    def publish_status(self):
        """Publish controller status"""
        status_msg = String()
        status_msg.data = f'Behavior: {self.current_behavior}, Joints: {len(self.current_positions)}'
        self.status_pub.publish(status_msg)

    def switch_behavior(self, behavior_name):
        """Switch to a specific behavior"""
        self.current_behavior = behavior_name
        self.get_logger().info(f'Switched to behavior: {behavior_name}')


def main(args=None):
    rclpy.init(args=args)

    node = HumanoidControllerNode()

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

## Exercise 7: Running the Simulation

### 7.1 Building the Package

```bash
cd ~/ros2_ws
colcon build --packages-select humanoid_simulation
source install/setup.bash
```

### 7.2 Launching the Simulation

```bash
# Launch the simulation with the humanoid robot
ros2 launch humanoid_simulation simulation.launch.py

# In another terminal, send behavior commands
ros2 topic pub /behavior_command std_msgs/String "data: 'wave'"
ros2 topic pub /behavior_command std_msgs/String "data: 'look_around'"
ros2 topic pub /behavior_command std_msgs/String "data: 'dance'"
```

### 7.3 Running the Test Script

```bash
# Run the simulation test
ros2 run humanoid_simulation simulation_test.py
```

## Exercise 8: Advanced Physics Configuration

Create `config/physics_params.yaml` for advanced physics tuning:

```yaml
# Physics parameters for humanoid simulation
gazebo:
  physics:
    # Solver parameters
    solver_type: "ode"  # Options: ode, bullet, dart
    ode_solver_type: "quick"  # Options: world, quick
    iters: 1000           # Number of iterations
    sor: 0.8              # Successive Over Relaxation parameter

    # Step size and real-time parameters
    max_step_size: 0.001  # Maximum simulation step size (seconds)
    real_time_update_rate: 1000.0  # Hz
    real_time_factor: 1.0  # Real-time factor (1.0 = real-time)

    # Gravity
    gravity_x: 0.0
    gravity_y: 0.0
    gravity_z: -9.8

    # Constraints
    min_step_size: 0.0001
    max_contacts: 20

    # Contact parameters
    cfm: 0.000001         # Constraint Force Mixing
    erp: 0.2              # Error Reduction Parameter

    # Joint limits enforcement
    enforce_joint_limits: true

    # Friction parameters
    friction_model: "bullet"
    mu1: 1.0              # Primary friction coefficient
    mu2: 1.0              # Secondary friction coefficient
    fdir1: [0, 0, 0]      # Primary friction direction
```

## Lab Report Requirements

After completing all exercises, prepare a lab report that includes:

1. **Simulation Environment Setup**: Document your Gazebo environment configuration
2. **Robot Model Design**: Explain your humanoid model design choices
3. **Physics Parameters**: Discuss how physics parameters affect robot behavior
4. **Controller Implementation**: Document your control algorithms
5. **Testing Results**: Include simulation test results and observations
6. **Challenges Faced**: Any issues encountered and how you resolved them
7. **Performance Analysis**: Compare simulation vs. expected real-world behavior

## Assessment Criteria

Your lab will be assessed based on:
- Proper simulation environment setup
- Realistic humanoid model creation
- Effective ROS 2 integration
- Functional control systems
- Comprehensive testing and validation
- Quality of documentation and code

## Next Steps

Upon successful completion of this lab, you should have a working simulation environment with a humanoid robot model, physics configuration, and basic control systems. This foundation will be essential as you progress through the subsequent modules, where you'll build upon these concepts to create increasingly sophisticated simulation scenarios and integrate with perception and AI systems.