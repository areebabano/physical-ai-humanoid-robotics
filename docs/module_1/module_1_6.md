---
title: "Module 1.6 - Chapter 6: Integration & Applications"
sidebar_position: 6
---

# Module 1.6 - Chapter 6: Integration & Applications

## 6.0 Introduction to Full-Stack ROS 2 Integration

### What is Full-Stack Integration?

Full-stack ROS 2 integration involves combining all core ROS 2 concepts—nodes, topics, services, actions, URDF, packages, and rclpy—into complete, functional humanoid robotics applications. This chapter focuses on how to architect, build, and orchestrate complex robotic systems that leverage multiple ROS 2 components working together seamlessly.

```
Full-Stack ROS 2 Integration Overview
┌─────────────────────────────────────────────────────────────────┐
│                    ROS 2 Full-Stack System                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   Nodes     │  │   Topics    │  │  Services   │              │
│  │             │  │             │  │             │              │
│  │ Publishers  │◄─►│ Subscribers │◄─►│   Actions   │              │
│  │ Subscribers │  │ Publishers  │  │   Clients   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │                 │                 │                   │
│         ▼                 ▼                 ▼                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │   URDF      │  │   rclpy     │  │ Parameters  │              │
│  │   Models    │  │   Nodes     │  │ Management  │              │
│  │             │  │             │  │             │              │
│  │   Xacro     │  │   Launch    │  │   Files     │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│         │                 │                 │                   │
│         └─────────────────┼─────────────────┘                   │
│                           ▼                                     │
│                    ┌─────────────┐                              │
│                    │   System    │                              │
│                    │ Integration │                              │
│                    └─────────────┘                              │
└─────────────────────────────────────────────────────────────────┘
```

Full-stack integration is used in:
- **Humanoid robot control systems**: Coordinating multiple subsystems
- **Sensor fusion**: Combining data from various sensors
- **Motion planning**: Integrating path planning with execution
- **Simulation**: Connecting real and simulated components

### Integration vs. Individual Components

| Aspect | Individual Components | Full-Stack Integration |
|--------|----------------------|------------------------|
| Complexity | Low | High |
| Coordination | None required | Critical |
| Error handling | Local | System-wide |
| Performance | Component-specific | System-wide |
| Maintainability | Simple | Requires architecture |

:::note
Full-stack integration requires careful planning of data flow, error handling, and system architecture to ensure all components work together effectively.
:::

## 6.1 Combining Nodes, Topics, Services, and Actions

### Understanding Communication Methods

In a complete robotic system, different communication methods serve different purposes:

```python
# complete_robot_system.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from rclpy.action import ActionClient
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist, PoseStamped
from sensor_msgs.msg import JointState, LaserScan
from example_interfaces.srv import SetBool, Trigger
from example_interfaces.action import FollowJointTrajectory
import threading
import time


class CompleteRobotSystem(Node):
    def __init__(self):
        super().__init__('complete_robot_system')

        # QoS profile for reliable communication
        qos_profile = QoSProfile(depth=10, reliability=ReliabilityPolicy.RELIABLE)

        # Publishers for different purposes
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.status_pub = self.create_publisher(String, 'robot_status', 10)
        self.joint_cmd_pub = self.create_publisher(JointState, 'joint_commands', 10)

        # Subscribers for sensor data
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)
        self.joint_state_sub = self.create_subscription(JointState, 'joint_states', self.joint_state_callback, 10)

        # Service clients for specific operations
        self.safety_service = self.create_client(SetBool, 'safety_control')
        self.calibration_service = self.create_client(Trigger, 'calibrate_sensors')

        # Action client for complex tasks
        self.trajectory_client = ActionClient(self, FollowJointTrajectory, 'joint_trajectory')

        # Parameters for system configuration
        self.declare_parameter('safety_distance', 0.5)
        self.declare_parameter('control_frequency', 50)
        self.declare_parameter('operation_mode', 'autonomous')

        # Initialize system state
        self.safety_distance = self.get_parameter('safety_distance').value
        self.control_frequency = self.get_parameter('control_frequency').value
        self.operation_mode = self.get_parameter('operation_mode').value

        # System state variables
        self.obstacle_detected = False
        self.joint_states = JointState()
        self.robot_stopped = False

        # Control timer for main loop
        self.control_timer = self.create_timer(1.0/self.control_frequency, self.control_loop)

        # Service server for system commands
        self.system_service = self.create_service(
            Trigger, 'system_command', self.system_command_callback)

        self.get_logger().info('Complete robot system initialized')

    def scan_callback(self, msg):
        """Handle laser scan data using topic communication"""
        if msg.ranges:
            min_distance = min([r for r in msg.ranges if r > 0 and r < float('inf')], default=float('inf'))
            self.obstacle_detected = min_distance < self.safety_distance

            # Publish status update
            status_msg = String()
            status_msg.data = f'OBSTACLE_DISTANCE: {min_distance:.2f}m'
            self.status_pub.publish(status_msg)

    def joint_state_callback(self, msg):
        """Handle joint state updates"""
        self.joint_states = msg

    def control_loop(self):
        """Main control loop that integrates all communication methods"""
        if self.operation_mode == 'autonomous':
            self.autonomous_control()
        elif self.operation_mode == 'manual':
            self.manual_control()
        elif self.operation_mode == 'safety':
            self.safety_mode()

    def autonomous_control(self):
        """Autonomous control using all communication methods"""
        # Check for obstacles
        if self.obstacle_detected and not self.robot_stopped:
            self.stop_robot()
            self.get_logger().warn('Obstacle detected, stopping robot')
        else:
            # Send movement command
            cmd = Twist()
            cmd.linear.x = 0.5  # Move forward
            cmd.angular.z = 0.0
            self.cmd_vel_pub.publish(cmd)

    def manual_control(self):
        """Manual control mode"""
        # In manual mode, commands come from external sources
        # but we still monitor for safety
        if self.obstacle_detected and not self.robot_stopped:
            self.emergency_stop()

    def safety_mode(self):
        """Safety mode - robot is stopped"""
        self.stop_robot()

    def stop_robot(self):
        """Stop all robot motion"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
        self.robot_stopped = True

    async def emergency_stop(self):
        """Emergency stop using service communication"""
        if self.safety_service.wait_for_service(timeout_sec=1.0):
            request = SetBool.Request()
            request.data = True  # Enable safety stop
            future = self.safety_service.call_async(request)
            try:
                response = await future
                if response.success:
                    self.get_logger().info('Emergency stop activated via service')
                    self.operation_mode = 'safety'
                    self.stop_robot()
            except Exception as e:
                self.get_logger().error(f'Emergency stop service call failed: {e}')

    def send_trajectory_command(self, trajectory_points):
        """Send trajectory command using action communication"""
        if not self.trajectory_client.wait_for_server(timeout_sec=1.0):
            self.get_logger().error('Trajectory action server not available')
            return False

        goal_msg = FollowJointTrajectory.Goal()
        goal_msg.trajectory = trajectory_points

        send_goal_future = self.trajectory_client.send_goal_async(
            goal_msg,
            feedback_callback=self.trajectory_feedback_callback
        )
        send_goal_future.add_done_callback(self.trajectory_response_callback)
        return True

    def trajectory_feedback_callback(self, feedback_msg):
        """Handle trajectory execution feedback"""
        self.get_logger().info(f'Trajectory progress: {feedback_msg.feedback}')

    def trajectory_response_callback(self, future):
        """Handle trajectory goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Trajectory goal rejected')
            return
        self.get_logger().info('Trajectory goal accepted')
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(self.trajectory_result_callback)

    def trajectory_result_callback(self, future):
        """Handle trajectory execution result"""
        result = future.result().result
        status = future.result().status
        self.get_logger().info(f'Trajectory completed with status: {status}')

    async def system_command_callback(self, request, response):
        """Handle system commands using service communication"""
        try:
            if request.message == 'start':
                self.operation_mode = 'autonomous'
                self.robot_stopped = False
                response.success = True
                response.message = 'System started in autonomous mode'
            elif request.message == 'stop':
                self.operation_mode = 'safety'
                self.stop_robot()
                response.success = True
                response.message = 'System stopped'
            elif request.message == 'calibrate':
                # Use service to trigger calibration
                if self.calibration_service.wait_for_service(timeout_sec=1.0):
                    calib_request = Trigger.Request()
                    calib_future = self.calibration_service.call_async(calib_request)
                    calib_response = await calib_future
                    response.success = calib_response.success
                    response.message = calib_response.message
                else:
                    response.success = False
                    response.message = 'Calibration service not available'
            else:
                response.success = False
                response.message = f'Unknown command: {request.message}'
        except Exception as e:
            response.success = False
            response.message = f'Command failed: {str(e)}'

        return response


def main(args=None):
    rclpy.init(args=args)
    system = CompleteRobotSystem()

    try:
        rclpy.spin(system)
    except KeyboardInterrupt:
        system.get_logger().info('Shutting down complete robot system')
    finally:
        system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

### Communication Methods Comparison Table

| Method | Type | Use Case | Latency | Reliability | Example |
|--------|------|----------|---------|-------------|---------|
| Topics | Publish/Subscribe | Continuous data flow | Low | Best effort | Sensor data, commands |
| Services | Request/Response | One-time operations | Medium | Reliable | Calibration, activation |
| Actions | Goal-Based | Long-running tasks | High | Reliable | Navigation, trajectory |

## 6.2 Integrating URDF/Xacro Models with Controllers

### URDF Integration Pipeline

The integration of URDF models with controllers follows a specific pipeline:

```
URDF → Controllers → Nodes → Simulation/Real Robot
  ↓         ↓          ↓           ↓
Model   Control    ROS 2    Physical/
File    Logic     Nodes     Virtual
```

### Complete URDF with Controllers Example

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Include other xacro files -->
  <xacro:include filename="$(find humanoid_description)/urdf/materials.xacro" />
  <xacro:include filename="$(find humanoid_description)/urdf/transmissions.xacro" />
  <xacro:include filename="$(find humanoid_description)/urdf/gazebo.xacro" />

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
    <axis xyz="0 0 1"/>
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

  <!-- Right Arm -->
  <joint name="right_shoulder_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_upper_arm_link"/>
    <origin xyz="${-(base_radius + 0.05)} 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="50" velocity="2"/>
  </joint>

  <link name="right_upper_arm_link">
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

  <joint name="right_elbow_joint" type="revolute">
    <parent link="right_upper_arm_link"/>
    <child link="right_lower_arm_link"/>
    <origin xyz="0 0 -0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="30" velocity="2"/>
  </joint>

  <link name="right_lower_arm_link">
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

  <!-- Left Leg -->
  <joint name="left_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="left_thigh_link"/>
    <origin xyz="0 0.1 -0.15" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="2"/>
  </joint>

  <link name="left_thigh_link">
    <visual>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
      <material name="gray_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="left_knee_joint" type="revolute">
    <parent link="left_thigh_link"/>
    <child link="left_shin_link"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100" velocity="2"/>
  </joint>

  <link name="left_shin_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="gray_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Right Leg -->
  <joint name="right_hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="right_thigh_link"/>
    <origin xyz="0 -0.1 -0.15" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-M_PI/2}" upper="${M_PI/2}" effort="100" velocity="2"/>
  </joint>

  <link name="right_thigh_link">
    <visual>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
      <material name="gray_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.06" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="3.0"/>
      <inertia ixx="0.02" ixy="0.0" ixz="0.0" iyy="0.02" iyz="0.0" izz="0.002"/>
    </inertial>
  </link>

  <joint name="right_knee_joint" type="revolute">
    <parent link="right_thigh_link"/>
    <child link="right_shin_link"/>
    <origin xyz="0 0 -0.4" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="0" upper="${M_PI/2}" effort="100" velocity="2"/>
  </joint>

  <link name="right_shin_link">
    <visual>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
      <material name="gray_material"/>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.05" length="0.4"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.001"/>
    </inertial>
  </link>

  <!-- Gazebo plugins -->
  <gazebo>
    <plugin name="gazebo_ros_control" filename="libgazebo_ros_control.so">
      <robotNamespace>/humanoid_robot</robotNamespace>
    </plugin>
  </gazebo>

  <!-- Joint state publisher -->
  <gazebo>
    <plugin name="joint_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
      <ros>
        <remapping>~/out:=joint_states</remapping>
      </ros>
      <update_rate>30</update_rate>
    </plugin>
  </gazebo>

</robot>
```

### Controller Configuration

```yaml
# config/humanoid_controllers.yaml
controller_manager:
  ros__parameters:
    update_rate: 100  # Hz

    joint_state_broadcaster:
      type: joint_state_broadcaster/JointStateBroadcaster

    left_arm_controller:
      type: position_controllers/JointTrajectoryController

    right_arm_controller:
      type: position_controllers/JointTrajectoryController

    left_leg_controller:
      type: position_controllers/JointTrajectoryController

    right_leg_controller:
      type: position_controllers/JointTrajectoryController

left_arm_controller:
  ros__parameters:
    joints:
      - left_shoulder_joint
      - left_elbow_joint
    interface_name: position

right_arm_controller:
  ros__parameters:
    joints:
      - right_shoulder_joint
      - right_elbow_joint
    interface_name: position

left_leg_controller:
  ros__parameters:
    joints:
      - left_hip_joint
      - left_knee_joint
    interface_name: position

right_leg_controller:
  ros__parameters:
    joints:
      - right_hip_joint
      - right_knee_joint
    interface_name: position
```

## 6.3 Launching Multi-Node Systems with ROS 2 Launch Files

### Multi-Node Launch Architecture

Creating launch files that orchestrate multiple nodes with proper parameter management:

```python
# launch/humanoid_robot.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessExit
import os


def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    robot_name = DeclareLaunchArgument(
        'robot_name',
        default_value='humanoid_robot',
        description='Name of the robot'
    )

    config_file = DeclareLaunchArgument(
        'config_file',
        default_value=PathJoinSubstitution([
            FindPackageShare('humanoid_bringup'),
            'config',
            'humanoid_controllers.yaml'
        ]),
        description='Path to controller configuration file'
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

    # Joint state publisher (for simulation)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        condition=IfCondition(LaunchConfiguration('use_sim_time'))
    )

    # Controller manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        parameters=[
            LaunchConfiguration('config_file'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        remappings=[
            ('/joint_states', [LaunchConfiguration('robot_name'), '/joint_states'])
        ]
    )

    # Spawn controllers
    spawn_joint_state_broadcaster = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    spawn_left_arm_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['left_arm_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    spawn_right_arm_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['right_arm_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    spawn_left_leg_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['left_leg_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    spawn_right_leg_controller = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['right_leg_controller'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
    )

    # Humanoid control node
    humanoid_control = Node(
        package='humanoid_control',
        executable='humanoid_control_node',
        name='humanoid_control',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'robot_name': LaunchConfiguration('robot_name')},
            {'control_frequency': 50},
            {'safety_distance': 0.5}
        ],
        remappings=[
            ('/cmd_vel', [LaunchConfiguration('robot_name'), '/cmd_vel']),
            ('/joint_commands', [LaunchConfiguration('robot_name'), '/joint_commands'])
        ]
    )

    # Sensor processing node
    sensor_processor = Node(
        package='humanoid_sensors',
        executable='sensor_processor',
        name='sensor_processor',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            {'sensor_timeout': 1.0}
        ]
    )

    # Add event handlers to ensure proper startup order
    load_joint_state_broadcaster = RegisterEventHandler(
        OnProcessExit(
            target_action=controller_manager,
            on_exit=[spawn_joint_state_broadcaster],
        )
    )

    load_left_arm_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_joint_state_broadcaster,
            on_exit=[spawn_left_arm_controller],
        )
    )

    load_right_arm_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_left_arm_controller,
            on_exit=[spawn_right_arm_controller],
        )
    )

    load_left_leg_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_right_arm_controller,
            on_exit=[spawn_left_leg_controller],
        )
    )

    load_right_leg_controller = RegisterEventHandler(
        OnProcessExit(
            target_action=spawn_left_leg_controller,
            on_exit=[spawn_right_leg_controller],
        )
    )

    return LaunchDescription([
        use_sim_time,
        robot_name,
        config_file,
        robot_state_publisher,
        joint_state_publisher,
        controller_manager,
        load_joint_state_broadcaster,
        load_left_arm_controller,
        load_right_arm_controller,
        load_left_leg_controller,
        load_right_leg_controller,
        humanoid_control,
        sensor_processor
    ])
```

### Advanced Launch File with Conditional Nodes

```python
# launch/humanoid_with_simulation.launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, GroupAction
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )

    launch_simulation = DeclareLaunchArgument(
        'launch_simulation',
        default_value='false',
        description='Launch Gazebo simulation'
    )

    launch_rviz = DeclareLaunchArgument(
        'launch_rviz',
        default_value='true',
        description='Launch RViz for visualization'
    )

    # Conditional groups
    simulation_group = GroupAction(
        condition=IfCondition(LaunchConfiguration('launch_simulation')),
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        FindPackageShare('gazebo_ros'),
                        'launch',
                        'gazebo.launch.py'
                    ])
                ])
            )
        ]
    )

    rviz_group = GroupAction(
        condition=IfCondition(LaunchConfiguration('launch_rviz')),
        actions=[
            Node(
                package='rviz2',
                executable='rviz2',
                name='rviz2',
                arguments=['-d', PathJoinSubstitution([
                    FindPackageShare('humanoid_bringup'),
                    'rviz',
                    'humanoid.rviz'
                ])],
                parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}]
            )
        ]
    )

    # Main robot launch (always runs)
    main_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('humanoid_bringup'),
                'launch',
                'humanoid_robot.launch.py'
            ])
        ]),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('use_sim_time')
        }.items()
    )

    return LaunchDescription([
        use_sim_time,
        launch_simulation,
        launch_rviz,
        simulation_group,
        rviz_group,
        main_launch
    ])
```

## 6.4 Parameter Management Across the System

### System-Wide Parameter Architecture

```python
# parameter_manager.py
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor, ParameterType
from rcl_interfaces.srv import ListParameters, GetParameters, SetParameters
import json
import yaml
from pathlib import Path


class ParameterManager(Node):
    def __init__(self):
        super().__init__('parameter_manager')

        # Declare system-wide parameters
        self.declare_parameter('robot_name', 'humanoid_robot')
        self.declare_parameter('system_mode', 'autonomous',
                              ParameterDescriptor(
                                  description='System operation mode',
                                  type=ParameterType.PARAMETER_STRING
                              ))
        self.declare_parameter('safety_limits.enabled', True)
        self.declare_parameter('safety_limits.max_velocity', 1.0)
        self.declare_parameter('safety_limits.max_torque', 50.0)
        self.declare_parameter('control.gains.kp', 1.0)
        self.declare_parameter('control.gains.ki', 0.1)
        self.declare_parameter('control.gains.kd', 0.05)

        # Parameter validation callback
        self.add_on_set_parameters_callback(self.parameters_callback)

        # Services for parameter management
        self.list_params_srv = self.create_service(
            ListParameters, 'list_system_parameters', self.list_parameters_callback)
        self.get_params_srv = self.create_service(
            GetParameters, 'get_system_parameters', self.get_parameters_callback)
        self.set_params_srv = self.create_service(
            SetParameters, 'set_system_parameters', self.set_parameters_callback)

        # Timer for parameter synchronization
        self.param_sync_timer = self.create_timer(1.0, self.synchronize_parameters)

        self.get_logger().info('Parameter manager initialized')

    def parameters_callback(self, params):
        """Validate parameters before accepting them"""
        from rcl_interfaces.msg import SetParametersResult

        result = SetParametersResult()
        result.successful = True

        for param in params:
            # Validate safety limits
            if param.name.startswith('safety_limits.'):
                if param.name == 'safety_limits.max_velocity':
                    if param.value <= 0 or param.value > 5.0:
                        result.successful = False
                        result.reason = 'Max velocity must be between 0 and 5.0 m/s'
                        return result
                elif param.name == 'safety_limits.max_torque':
                    if param.value <= 0 or param.value > 100.0:
                        result.successful = False
                        result.reason = 'Max torque must be between 0 and 100.0 Nm'
                        return result

            # Validate control gains
            elif param.name.startswith('control.gains.'):
                if param.value < 0 or param.value > 10.0:
                    result.successful = False
                    result.reason = 'Control gains must be between 0 and 10.0'
                    return result

        return result

    def list_parameters_callback(self, request, response):
        """List all system parameters"""
        all_params = self.list_parameters([])
        response.result.names = all_params.result.names
        response.result.prefixes = all_params.result.prefixes
        return response

    def get_parameters_callback(self, request, response):
        """Get specific parameters"""
        param_values = self.get_parameters(request.names)
        response.values = [param.get_parameter_value() for param in param_values]
        return response

    def set_parameters_callback(self, request, response):
        """Set parameters through service call"""
        from rcl_interfaces.msg import SetParametersResult

        # Convert service request to parameter objects
        parameters = []
        for param in request.parameters:
            parameters.append(rclpy.parameter.Parameter(
                name=param.name,
                value=param.value
            ))

        # Set parameters
        result = self.set_parameters(parameters)
        response.results = [SetParametersResult(successful=r.successful, reason=r.reason) for r in result]
        return response

    def synchronize_parameters(self):
        """Synchronize parameters across the system"""
        # This could publish parameter updates to other nodes
        # or save parameters to a configuration file
        pass

    def save_parameters_to_file(self, filename):
        """Save current parameters to a YAML file"""
        params = {}
        for param_name in self.get_parameter_names():
            param_value = self.get_parameter(param_name).value
            # Create nested dictionary structure from parameter names
            keys = param_name.split('.')
            current = params
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = param_value

        with open(filename, 'w') as f:
            yaml.dump(params, f, default_flow_style=False)

    def load_parameters_from_file(self, filename):
        """Load parameters from a YAML file"""
        with open(filename, 'r') as f:
            params = yaml.safe_load(f)

        # Flatten nested parameters
        def flatten_params(d, parent_key='', sep='.'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_params(v, new_key, sep=sep).items())
                else:
                    items.append((new_key, v))
            return dict(items)

        flattened = flatten_params(params)

        # Set parameters
        parameters = []
        for name, value in flattened.items():
            parameters.append(rclpy.parameter.Parameter(name, value))

        self.set_parameters(parameters)


def main(args=None):
    rclpy.init(args=args)
    param_manager = ParameterManager()

    try:
        rclpy.spin(param_manager)
    except KeyboardInterrupt:
        param_manager.get_logger().info('Shutting down parameter manager')
    finally:
        param_manager.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 6.5 Event-Driven Architecture and Real-Time Callbacks

### Event-Driven System Design

```python
# event_driven_system.py
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String, Bool, Float32
from sensor_msgs.msg import JointState, LaserScan
from geometry_msgs.msg import Twist
from example_interfaces.srv import Trigger, SetBool
from threading import Lock
import time
import asyncio


class EventDrivenSystem(Node):
    def __init__(self):
        super().__init__('event_driven_system')

        # Create callback groups for different event types
        self.safety_group = MutuallyExclusiveCallbackGroup()  # Safety events must be exclusive
        self.sensor_group = ReentrantCallbackGroup()         # Sensor events can run in parallel
        self.control_group = ReentrantCallbackGroup()        # Control events can run in parallel

        # Safety-critical subscribers (must be processed exclusively)
        self.emergency_stop_sub = self.create_subscription(
            Bool,
            'emergency_stop',
            self.emergency_stop_callback,
            1,
            callback_group=self.safety_group
        )

        # Sensor subscribers (can be processed in parallel)
        self.scan_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10,
            callback_group=self.sensor_group
        )

        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10,
            callback_group=self.sensor_group
        )

        # Control subscribers (can be processed in parallel)
        self.cmd_vel_sub = self.create_subscription(
            Twist,
            'cmd_vel',
            self.cmd_vel_callback,
            10,
            callback_group=self.control_group
        )

        # Publishers
        self.cmd_pub = self.create_publisher(Twist, 'cmd_vel_out', 10)
        self.status_pub = self.create_publisher(String, 'system_status', 10)
        self.event_pub = self.create_publisher(String, 'system_events', 10)

        # Services
        self.reset_service = self.create_service(
            Trigger, 'reset_system', self.reset_callback)
        self.enable_service = self.create_service(
            SetBool, 'enable_system', self.enable_callback)

        # Event queues and locks
        self.event_queue = []
        self.event_lock = Lock()
        self.system_enabled = True
        self.emergency_stopped = False

        # Event processing timer
        self.event_timer = self.create_timer(0.01, self.process_events)

        # Real-time performance monitoring
        self.last_callback_time = time.time()
        self.callback_interval = 0.01  # 100 Hz for critical callbacks

        self.get_logger().info('Event-driven system initialized')

    def emergency_stop_callback(self, msg):
        """Safety-critical callback - runs exclusively"""
        if msg.data:
            self.emergency_stopped = True
            self.system_enabled = False
            self.publish_event('EMERGENCY_STOP_ACTIVATED')
            self.get_logger().fatal('EMERGENCY STOP ACTIVATED')

            # Stop all motion
            stop_cmd = Twist()
            self.cmd_pub.publish(stop_cmd)
        else:
            self.emergency_stopped = False
            self.publish_event('EMERGENCY_STOP_DEACTIVATED')

    def scan_callback(self, msg):
        """Sensor callback - can run in parallel with other sensor callbacks"""
        if not self.system_enabled or self.emergency_stopped:
            return

        # Process laser scan data
        if msg.ranges:
            min_distance = min([r for r in msg.ranges if r > 0 and r < float('inf')], default=float('inf'))

            # Publish obstacle distance
            distance_msg = Float32()
            distance_msg.data = min_distance
            self.get_publisher('obstacle_distance').publish(distance_msg)

            # Check for obstacles
            if min_distance < 0.5:  # 50cm safety distance
                self.publish_event('OBSTACLE_DETECTED', {'distance': min_distance})

        # Check timing for real-time performance
        current_time = time.time()
        if current_time - self.last_callback_time > self.callback_interval * 2:
            self.get_logger().warn(f'Scan callback timing violation: {current_time - self.last_callback_time:.3f}s')
        self.last_callback_time = current_time

    def joint_state_callback(self, msg):
        """Joint state callback - can run in parallel"""
        if not self.system_enabled or self.emergency_stopped:
            return

        # Process joint states
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                # Check for joint limits
                if abs(msg.position[i]) > 3.14:  # Joint limit check
                    self.publish_event('JOINT_LIMIT_EXCEEDED', {
                        'joint': name,
                        'position': msg.position[i]
                    })

    def cmd_vel_callback(self, msg):
        """Command callback - can run in parallel"""
        if not self.system_enabled or self.emergency_stopped:
            # Still accept commands for logging but don't execute
            self.publish_event('COMMAND_IGNORED_DUE_TO_SAFETY')
            return

        # Apply command if system is enabled
        self.cmd_pub.publish(msg)
        self.publish_event('COMMAND_EXECUTED')

    def process_events(self):
        """Process system events in the main thread"""
        with self.event_lock:
            events_to_process = self.event_queue.copy()
            self.event_queue.clear()

        for event in events_to_process:
            self.handle_system_event(event)

    def publish_event(self, event_type, data=None):
        """Thread-safe event publishing"""
        event_msg = String()
        event_msg.data = f'{event_type}: {data if data else ""}'

        with self.event_lock:
            self.event_queue.append({
                'type': event_type,
                'data': data,
                'timestamp': time.time()
            })

        self.event_pub.publish(event_msg)

    def handle_system_event(self, event):
        """Handle a system event"""
        event_type = event['type']
        data = event['data']
        timestamp = event['timestamp']

        if event_type == 'EMERGENCY_STOP_ACTIVATED':
            self.status_pub.publish(String(data='EMERGENCY_STOP'))
        elif event_type == 'OBSTACLE_DETECTED':
            if data and data.get('distance', float('inf')) < 0.3:  # 30cm
                self.publish_event('OBSTACLE_TOO_CLOSE')
        elif event_type == 'JOINT_LIMIT_EXCEEDED':
            self.get_logger().warn(f'Joint limit exceeded: {data}')

    def reset_callback(self, request, response):
        """Reset system service"""
        if self.emergency_stopped:
            response.success = False
            response.message = 'Cannot reset while emergency stop is active'
            return response

        self.system_enabled = True
        self.publish_event('SYSTEM_RESET')
        response.success = True
        response.message = 'System reset successfully'
        return response

    def enable_callback(self, request, response):
        """Enable/disable system service"""
        if request.data and self.emergency_stopped:
            response.success = False
            response.message = 'Cannot enable system while emergency stop is active'
            return response

        self.system_enabled = request.data
        status = 'ENABLED' if request.data else 'DISABLED'
        self.status_pub.publish(String(data=status))
        self.publish_event(f'SYSTEM_{status}')

        response.success = True
        response.message = f'System {status.lower()}'
        return response


def main(args=None):
    rclpy.init(args=args)
    system = EventDrivenSystem()

    # Use multi-threaded executor to handle callbacks in parallel
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(system)

    try:
        executor.spin()
    except KeyboardInterrupt:
        system.get_logger().info('Shutting down event-driven system')
    finally:
        system.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 6.6 Building Modular Humanoid Control Pipelines

### Modular Control Architecture

```python
# modular_control_pipeline.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String, Float32MultiArray
from geometry_msgs.msg import Twist, Pose, Point
from sensor_msgs.msg import JointState, Imu
from builtin_interfaces.msg import Duration
from control_msgs.msg import JointTrajectoryControllerState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from humanoid_interfaces.msg import HumanoidState, HumanoidCommand
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Optional
import threading


@dataclass
class JointLimits:
    """Joint limits data structure"""
    min_position: float
    max_position: float
    max_velocity: float
    max_effort: float


class JointController(Node):
    """Modular joint controller component"""
    def __init__(self, joint_name: str, limits: JointLimits):
        super().__init__(f'{joint_name}_controller')

        self.joint_name = joint_name
        self.limits = limits

        # Publishers and subscribers
        self.command_pub = self.create_publisher(
            JointTrajectory, f'{joint_name}/command', 10)
        self.state_sub = self.create_subscription(
            JointTrajectoryControllerState, f'{joint_name}/state',
            self.state_callback, 10)

        # Internal state
        self.current_position = 0.0
        self.target_position = 0.0
        self.current_velocity = 0.0

        # Control timer
        self.control_timer = self.create_timer(0.01, self.control_loop)

        self.get_logger().info(f'Joint controller for {joint_name} initialized')

    def state_callback(self, msg):
        """Update joint state"""
        if self.joint_name in msg.joint_names:
            idx = msg.joint_names.index(self.joint_name)
            if idx < len(msg.actual.positions):
                self.current_position = msg.actual.positions[idx]
            if idx < len(msg.actual.velocities):
                self.current_velocity = msg.actual.velocities[idx]

    def set_target_position(self, position: float):
        """Set target position for the joint"""
        # Apply position limits
        position = max(self.limits.min_position, min(self.limits.max_position, position))
        self.target_position = position

    def control_loop(self):
        """Joint control loop"""
        # Simple PD controller
        error = self.target_position - self.current_position
        velocity_cmd = min(max(error * 2.0, -self.limits.max_velocity), self.limits.max_velocity)

        # Create trajectory command
        trajectory = JointTrajectory()
        trajectory.joint_names = [self.joint_name]

        point = JointTrajectoryPoint()
        point.positions = [self.target_position]
        point.velocities = [velocity_cmd]
        point.time_from_start = Duration(sec=0, nanosec=10000000)  # 10ms

        trajectory.points = [point]
        self.command_pub.publish(trajectory)


class SensorFusionNode(Node):
    """Modular sensor fusion component"""
    def __init__(self):
        super().__init__('sensor_fusion')

        # Subscribers for different sensors
        self.joint_state_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_state_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)

        # Publisher for fused state
        self.fused_state_pub = self.create_publisher(
            HumanoidState, 'fused_state', 10)

        # Internal state
        self.joint_states = JointState()
        self.imu_data = Imu()
        self.fused_state = HumanoidState()

        # Fusion timer
        self.fusion_timer = self.create_timer(0.02, self.fusion_loop)

        self.get_logger().info('Sensor fusion node initialized')

    def joint_state_callback(self, msg):
        """Process joint state data"""
        self.joint_states = msg
        self.update_fused_state()

    def imu_callback(self, msg):
        """Process IMU data"""
        self.imu_data = msg
        self.update_fused_state()

    def update_fused_state(self):
        """Update fused state with latest sensor data"""
        # Update joint positions
        self.fused_state.joint_positions = list(self.joint_states.position)
        self.fused_state.joint_velocities = list(self.joint_states.velocity)

        # Update IMU data
        self.fused_state.imu_orientation = self.imu_data.orientation
        self.fused_state.imu_angular_velocity = self.imu_data.angular_velocity
        self.fused_state.imu_linear_acceleration = self.imu_data.linear_acceleration

    def fusion_loop(self):
        """Fusion processing loop"""
        # Publish fused state
        self.fused_state.header.stamp = self.get_clock().now().to_msg()
        self.fused_state.header.frame_id = 'base_link'
        self.fused_state_pub.publish(self.fused_state)


class BalanceController(Node):
    """Modular balance controller component"""
    def __init__(self):
        super().__init__('balance_controller')

        # Subscribers
        self.state_sub = self.create_subscription(
            HumanoidState, 'fused_state', self.state_callback, 10)

        # Publishers
        self.balance_cmd_pub = self.create_publisher(
            HumanoidCommand, 'balance_commands', 10)

        # Internal state
        self.current_state = HumanoidState()
        self.balance_enabled = True

        # Balance control timer
        self.balance_timer = self.create_timer(0.01, self.balance_control)

        self.get_logger().info('Balance controller initialized')

    def state_callback(self, msg):
        """Update current state"""
        self.current_state = msg

    def balance_control(self):
        """Balance control algorithm"""
        if not self.balance_enabled:
            return

        # Simple balance control based on IMU data
        roll = self.current_state.imu_orientation.x
        pitch = self.current_state.imu_orientation.y

        # Calculate balance correction
        roll_correction = -roll * 0.5  # PD-like control
        pitch_correction = -pitch * 0.5

        # Create balance command
        cmd = HumanoidCommand()
        cmd.header.stamp = self.get_clock().now().to_msg()
        cmd.command_type = 'BALANCE'
        cmd.parameters = [roll_correction, pitch_correction]

        self.balance_cmd_pub.publish(cmd)


class GaitController(Node):
    """Modular gait controller component"""
    def __init__(self):
        super().__init__('gait_controller')

        # Subscribers
        self.cmd_sub = self.create_subscription(
            Twist, 'cmd_vel', self.velocity_command_callback, 10)
        self.state_sub = self.create_subscription(
            HumanoidState, 'fused_state', self.state_callback, 10)

        # Publishers
        self.trajectory_pub = self.create_publisher(
            JointTrajectory, 'gait_trajectories', 10)

        # Internal state
        self.desired_velocity = Twist()
        self.current_state = HumanoidState()
        self.gait_enabled = False

        # Gait timer
        self.gait_timer = self.create_timer(0.05, self.gait_generation)

        self.get_logger().info('Gait controller initialized')

    def velocity_command_callback(self, msg):
        """Handle velocity commands"""
        self.desired_velocity = msg
        self.gait_enabled = (abs(msg.linear.x) > 0.01 or abs(msg.angular.z) > 0.01)

    def state_callback(self, msg):
        """Update current state"""
        self.current_state = msg

    def gait_generation(self):
        """Generate gait trajectories"""
        if not self.gait_enabled:
            return

        # Simple walking gait pattern
        trajectory = JointTrajectory()
        trajectory.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'right_hip_joint', 'right_knee_joint'
        ]

        # Generate trajectory points based on desired velocity
        points = []
        for i in range(10):  # 10 points for one gait cycle
            point = JointTrajectoryPoint()

            # Simple oscillating pattern for walking
            phase = (i / 10.0) * 2 * np.pi
            left_hip_pos = 0.1 * np.sin(phase)
            left_knee_pos = 0.05 * np.sin(phase + np.pi/2)
            right_hip_pos = 0.1 * np.sin(phase + np.pi)
            right_knee_pos = 0.05 * np.sin(phase + 3*np.pi/2)

            # Scale by desired velocity
            scale = min(1.0, max(0.1, self.desired_velocity.linear.x))
            left_hip_pos *= scale
            left_knee_pos *= scale
            right_hip_pos *= scale
            right_knee_pos *= scale

            point.positions = [left_hip_pos, left_knee_pos, right_hip_pos, right_knee_pos]
            point.time_from_start = Duration(sec=0, nanosec=int((i+1) * 50000000))  # 50ms intervals

            points.append(point)

        trajectory.points = points
        self.trajectory_pub.publish(trajectory)


class HumanoidControlPipeline(Node):
    """Main pipeline that orchestrates all modular components"""
    def __init__(self):
        super().__init__('humanoid_control_pipeline')

        # Initialize modular components
        self.joint_limits = {
            'left_hip_joint': JointLimits(-1.57, 1.57, 2.0, 50.0),
            'left_knee_joint': JointLimits(0, 1.57, 2.0, 50.0),
            'right_hip_joint': JointLimits(-1.57, 1.57, 2.0, 50.0),
            'right_knee_joint': JointLimits(0, 1.57, 2.0, 50.0),
            'left_shoulder_joint': JointLimits(-1.57, 1.57, 2.0, 30.0),
            'left_elbow_joint': JointLimits(-1.57, 1.57, 2.0, 30.0),
        }

        # Create modular components
        self.joint_controllers = {}
        for joint_name, limits in self.joint_limits.items():
            self.joint_controllers[joint_name] = JointController(joint_name, limits)

        self.sensor_fusion = SensorFusionNode()
        self.balance_controller = BalanceController()
        self.gait_controller = GaitController()

        # System control services
        self.enable_service = self.create_service(
            String, 'enable_pipeline', self.enable_pipeline_callback)

        self.pipeline_enabled = True

        self.get_logger().info('Humanoid control pipeline initialized')

    def enable_pipeline_callback(self, request, response):
        """Enable/disable the entire pipeline"""
        if request.data == 'enable':
            self.pipeline_enabled = True
            response.data = 'Pipeline enabled'
        elif request.data == 'disable':
            self.pipeline_enabled = False
            response.data = 'Pipeline disabled'
        else:
            response.data = 'Unknown command, use "enable" or "disable"'

        return response


def main(args=None):
    rclpy.init(args=args)
    pipeline = HumanoidControlPipeline()

    try:
        rclpy.spin(pipeline)
    except KeyboardInterrupt:
        pipeline.get_logger().info('Shutting down humanoid control pipeline')
    finally:
        pipeline.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 6.7 Data Flow and Control Flow in Robotics Applications

### Data and Control Flow Architecture

```
Data Flow Architecture:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Sensors       │───▶│  Perception      │───▶│   Decision      │
│ (IMU, LIDAR,    │    │  Processing      │    │   Making        │
│  Cameras, etc.) │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Filtering     │───▶│ State Estimation │───▶│  Behavior       │
│   & Preprocessing│    │   & Fusion      │    │   Selection     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Control       │───▶│  Trajectory      │───▶│   Actuation     │
│   Generation    │    │   Planning       │    │   Commands      │
└─────────────────┘    └──────────────────┘    └─────────────────┘

Control Flow Architecture:
┌─────────────────┐
│  Main Control   │
│   Loop (100Hz)  │
└─────────┬───────┘
          │
    ┌─────▼─────┐
    │  State    │
    │  Machine  │
    └─────┬─────┘
          │
    ┌─────▼─────┐    ┌─────────────┐
    │ Behavior  │───▶│ Subsystem   │
    │ Selector  │    │ Controllers │
    └───────────┘    └─────────────┘
```

### Implementation of Data and Control Flow

```python
# data_control_flow.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String, Bool, Float32
from sensor_msgs.msg import JointState, Imu, LaserScan
from geometry_msgs.msg import Twist, PoseStamped
from nav_msgs.msg import Odometry
from builtin_interfaces.msg import Time
import numpy as np
import threading
from enum import Enum
from dataclasses import dataclass
from typing import Dict, Any, Optional


class RobotState(Enum):
    """Robot state machine states"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    CALIBRATING = "calibrating"
    STANDBY = "standby"
    WALKING = "walking"
    BALANCING = "balancing"
    EMERGENCY_STOP = "emergency_stop"
    SHUTDOWN = "shutdown"


@dataclass
class RobotData:
    """Container for robot data"""
    timestamp: Time
    joint_states: Optional[JointState] = None
    imu_data: Optional[Imu] = None
    laser_scan: Optional[LaserScan] = None
    odometry: Optional[Odometry] = None
    pose: Optional[PoseStamped] = None
    velocity_command: Optional[Twist] = None
    system_status: str = "unknown"
    safety_status: bool = True


class DataProcessor(Node):
    """Handles data processing and filtering"""
    def __init__(self):
        super().__init__('data_processor')

        # Subscribers for raw sensor data
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)
        self.joint_sub = self.create_subscription(JointState, 'joint_states', self.joint_callback, qos)
        self.imu_sub = self.create_subscription(Imu, 'imu/data', self.imu_callback, qos)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos)
        self.odom_sub = self.create_subscription(Odometry, 'odom', self.odom_callback, qos)

        # Publishers for processed data
        self.filtered_imu_pub = self.create_publisher(Imu, 'filtered_imu', 10)
        self.processed_scan_pub = self.create_publisher(LaserScan, 'processed_scan', 10)
        self.joint_status_pub = self.create_publisher(String, 'joint_status', 10)

        # Internal data storage
        self.raw_data = RobotData(timestamp=self.get_clock().now().to_msg())
        self.filtered_data = RobotData(timestamp=self.get_clock().now().to_msg())

        # Filters and processing
        self.imu_filter = IMUFilter()
        self.scan_filter = ScanFilter()

        # Processing timer
        self.process_timer = self.create_timer(0.01, self.process_data)

        self.get_logger().info('Data processor initialized')

    def joint_callback(self, msg):
        """Process joint state data"""
        self.raw_data.joint_states = msg
        self.check_joint_limits()

    def imu_callback(self, msg):
        """Process IMU data"""
        self.raw_data.imu_data = msg
        # Apply filtering
        filtered_imu = self.imu_filter.update(msg)
        self.filtered_data.imu_data = filtered_imu
        self.filtered_imu_pub.publish(filtered_imu)

    def scan_callback(self, msg):
        """Process laser scan data"""
        self.raw_data.laser_scan = msg
        # Apply filtering
        processed_scan = self.scan_filter.update(msg)
        self.filtered_data.laser_scan = processed_scan
        self.processed_scan_pub.publish(processed_scan)

    def odom_callback(self, msg):
        """Process odometry data"""
        self.raw_data.odometry = msg

    def check_joint_limits(self):
        """Check if joints are within safe limits"""
        if self.raw_data.joint_states:
            status_msg = String()
            safe = True
            for i, pos in enumerate(self.raw_data.joint_states.position):
                if abs(pos) > 3.0:  # Example limit
                    safe = False
                    break
            status_msg.data = "SAFE" if safe else "JOINT_LIMIT_EXCEEDED"
            self.joint_status_pub.publish(status_msg)

    def process_data(self):
        """Main data processing loop"""
        # Update timestamp
        self.filtered_data.timestamp = self.get_clock().now().to_msg()

        # Additional processing can be added here
        pass


class StateEstimator(Node):
    """Estimates robot state based on sensor data"""
    def __init__(self):
        super().__init__('state_estimator')

        # Subscribers for processed data
        self.filtered_imu_sub = self.create_subscription(Imu, 'filtered_imu', self.imu_callback, 10)
        self.joint_state_sub = self.create_subscription(JointState, 'joint_states', self.joint_callback, 10)

        # Publisher for estimated state
        self.estimated_state_pub = self.create_publisher(HumanoidState, 'estimated_state', 10)

        # Internal state
        self.estimated_state = HumanoidState()
        self.com_estimator = CenterOfMassEstimator()
        self.pose_estimator = PoseEstimator()

        # Estimation timer
        self.estimation_timer = self.create_timer(0.01, self.estimate_state)

        self.get_logger().info('State estimator initialized')

    def imu_callback(self, msg):
        """Update state with IMU data"""
        self.estimated_state.imu_orientation = msg.orientation
        self.estimated_state.imu_angular_velocity = msg.angular_velocity
        self.estimated_state.imu_linear_acceleration = msg.linear_acceleration

    def joint_callback(self, msg):
        """Update state with joint data"""
        self.estimated_state.joint_positions = list(msg.position)
        self.estimated_state.joint_velocities = list(msg.velocity)
        self.estimated_state.joint_names = list(msg.name)

    def estimate_state(self):
        """Estimate complete robot state"""
        # Estimate center of mass
        com = self.com_estimator.estimate(
            self.estimated_state.joint_positions,
            self.estimated_state.joint_names
        )

        # Estimate pose and balance
        pose = self.pose_estimator.estimate(
            self.estimated_state.imu_orientation,
            com
        )

        # Update estimated state
        self.estimated_state.center_of_mass = com
        self.estimated_state.pose = pose

        # Publish estimated state
        self.estimated_state.header.stamp = self.get_clock().now().to_msg()
        self.estimated_state.header.frame_id = 'base_link'
        self.estimated_state_pub.publish(self.estimated_state)


class BehaviorSelector(Node):
    """Selects robot behavior based on current state"""
    def __init__(self):
        super().__init__('behavior_selector')

        # Subscribers
        self.state_sub = self.create_subscription(HumanoidState, 'estimated_state', self.state_callback, 10)
        self.command_sub = self.create_subscription(String, 'behavior_command', self.command_callback, 10)

        # Publishers
        self.behavior_pub = self.create_publisher(String, 'selected_behavior', 10)
        self.control_cmd_pub = self.create_publisher(Twist, 'behavior_control', 10)

        # Internal state
        self.current_state = HumanoidState()
        self.current_behavior = "IDLE"
        self.desired_behavior = "IDLE"
        self.robot_state = RobotState.IDLE

        # Behavior selection timer
        self.behavior_timer = self.create_timer(0.1, self.select_behavior)

        self.get_logger().info('Behavior selector initialized')

    def state_callback(self, msg):
        """Update with current robot state"""
        self.current_state = msg
        # Update robot state based on conditions
        self.update_robot_state()

    def command_callback(self, msg):
        """Handle behavior commands"""
        self.desired_behavior = msg.data

    def update_robot_state(self):
        """Update robot state based on current conditions"""
        # Check if robot is balanced
        roll = self.current_state.imu_orientation.x
        pitch = self.current_state.imu_orientation.y
        tilt_magnitude = np.sqrt(roll**2 + pitch**2)

        if tilt_magnitude > 1.0:  # Too tilted
            self.robot_state = RobotState.EMERGENCY_STOP
        elif self.current_state.center_of_mass.z < 0.1:  # COM too low
            self.robot_state = RobotState.BALANCING
        else:
            self.robot_state = RobotState.STANDBY

    def select_behavior(self):
        """Select behavior based on state and commands"""
        new_behavior = "IDLE"

        if self.robot_state == RobotState.EMERGENCY_STOP:
            new_behavior = "EMERGENCY_STOP"
        elif self.robot_state == RobotState.BALANCING:
            new_behavior = "BALANCING"
        elif self.desired_behavior == "WALK":
            new_behavior = "WALKING"
        elif self.desired_behavior == "STAND":
            new_behavior = "STANDBY"
        elif self.desired_behavior == "BALANCE":
            new_behavior = "BALANCING"

        if new_behavior != self.current_behavior:
            self.current_behavior = new_behavior
            # Publish selected behavior
            behavior_msg = String()
            behavior_msg.data = new_behavior
            self.behavior_pub.publish(behavior_msg)

            # Publish appropriate control command based on behavior
            cmd = Twist()
            if new_behavior == "WALKING":
                cmd.linear.x = 0.5  # Move forward
            elif new_behavior == "BALANCING":
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0  # Maintain balance
            elif new_behavior == "EMERGENCY_STOP":
                cmd.linear.x = 0.0
                cmd.angular.z = 0.0  # Stop immediately

            self.control_cmd_pub.publish(cmd)


class ControlFlowManager(Node):
    """Manages the overall control flow of the system"""
    def __init__(self):
        super().__init__('control_flow_manager')

        # Initialize system components
        self.data_processor = DataProcessor()
        self.state_estimator = StateEstimator()
        self.behavior_selector = BehaviorSelector()

        # System state
        self.system_initialized = False
        self.system_enabled = True

        # System control services
        self.init_service = self.create_service(
            String, 'initialize_system', self.initialize_system_callback)
        self.enable_service = self.create_service(
            String, 'enable_system', self.enable_system_callback)

        # System status publisher
        self.status_pub = self.create_publisher(String, 'system_status', 10)

        # System monitoring timer
        self.monitor_timer = self.create_timer(1.0, self.monitor_system)

        self.get_logger().info('Control flow manager initialized')

    def initialize_system_callback(self, request, response):
        """Initialize the system"""
        if request.data == 'start':
            self.system_initialized = True
            response.data = 'System initialized successfully'
        else:
            response.data = 'Unknown initialization command'

        return response

    def enable_system_callback(self, request, response):
        """Enable/disable the system"""
        if request.data == 'enable':
            self.system_enabled = True
            response.data = 'System enabled'
        elif request.data == 'disable':
            self.system_enabled = False
            response.data = 'System disabled'
        else:
            response.data = 'Unknown command, use "enable" or "disable"'

        return response

    def monitor_system(self):
        """Monitor system health and status"""
        status_msg = String()
        if not self.system_initialized:
            status_msg.data = "SYSTEM_NOT_INITIALIZED"
        elif not self.system_enabled:
            status_msg.data = "SYSTEM_DISABLED"
        else:
            status_msg.data = "SYSTEM_RUNNING"

        self.status_pub.publish(status_msg)


def main(args=None):
    rclpy.init(args=args)
    manager = ControlFlowManager()

    try:
        rclpy.spin(manager)
    except KeyboardInterrupt:
        manager.get_logger().info('Shutting down control flow manager')
    finally:
        manager.destroy_node()
        rclpy.shutdown()


# Supporting classes
class IMUFilter:
    """Simple IMU data filter"""
    def __init__(self):
        self.alpha = 0.1  # Low-pass filter coefficient
        self.filtered_orientation = None

    def update(self, imu_msg):
        """Update filter with new IMU data"""
        if self.filtered_orientation is None:
            self.filtered_orientation = imu_msg.orientation
        else:
            # Simple low-pass filter
            self.filtered_orientation.x = (1 - self.alpha) * self.filtered_orientation.x + \
                                         self.alpha * imu_msg.orientation.x
            self.filtered_orientation.y = (1 - self.alpha) * self.filtered_orientation.y + \
                                         self.alpha * imu_msg.orientation.y
            self.filtered_orientation.z = (1 - self.alpha) * self.filtered_orientation.z + \
                                         self.alpha * imu_msg.orientation.z
            self.filtered_orientation.w = (1 - self.alpha) * self.filtered_orientation.w + \
                                         self.alpha * imu_msg.orientation.w

        # Create new message with filtered data
        filtered_msg = Imu()
        filtered_msg.header = imu_msg.header
        filtered_msg.orientation = self.filtered_orientation
        filtered_msg.angular_velocity = imu_msg.angular_velocity  # Use raw angular velocity
        filtered_msg.linear_acceleration = imu_msg.linear_acceleration  # Use raw acceleration
        return filtered_msg


class ScanFilter:
    """Simple laser scan filter"""
    def __init__(self):
        self.min_range = 0.1
        self.max_range = 10.0

    def update(self, scan_msg):
        """Update filter with new scan data"""
        # Filter out invalid ranges
        filtered_ranges = []
        for r in scan_msg.ranges:
            if r >= self.min_range and r <= self.max_range:
                filtered_ranges.append(r)
            else:
                filtered_ranges.append(float('inf'))  # Use infinity for invalid ranges

        # Create new message with filtered data
        filtered_msg = LaserScan()
        filtered_msg.header = scan_msg.header
        filtered_msg.angle_min = scan_msg.angle_min
        filtered_msg.angle_max = scan_msg.angle_max
        filtered_msg.angle_increment = scan_msg.angle_increment
        filtered_msg.time_increment = scan_msg.time_increment
        filtered_msg.scan_time = scan_msg.scan_time
        filtered_msg.range_min = self.min_range
        filtered_msg.range_max = self.max_range
        filtered_msg.ranges = filtered_ranges
        filtered_msg.intensities = scan_msg.intensities if scan_msg.intensities else []
        return filtered_msg


class CenterOfMassEstimator:
    """Estimates center of mass based on joint positions"""
    def __init__(self):
        # Simple model: assume fixed masses for each link
        self.link_masses = {
            'base_link': 10.0,
            'left_leg': 5.0,
            'right_leg': 5.0,
            'torso': 8.0,
            'head': 2.0
        }

    def estimate(self, joint_positions, joint_names):
        """Estimate center of mass"""
        # This is a simplified estimation
        # In practice, you would use forward kinematics and actual robot model
        com = Point()
        com.x = 0.0
        com.y = 0.0
        com.z = 0.8  # Approximate height
        return com


class PoseEstimator:
    """Estimates robot pose"""
    def estimate(self, imu_orientation, center_of_mass):
        """Estimate pose based on IMU and COM"""
        # Simplified pose estimation
        pose = Pose()
        pose.orientation = imu_orientation
        pose.position = center_of_mass
        return pose


if __name__ == '__main__':
    main()
```

## 6.8 High-Level Modules in Humanoid Robot Stack

### Humanoid Robot Stack Architecture

| Module | Function | ROS 2 Components | Purpose |
|--------|----------|------------------|---------|
| Perception | Sensor data processing | Nodes, Topics, TF | Environment understanding |
| State Estimation | Robot state calculation | Nodes, Services, Parameters | Position, velocity, balance |
| Planning | Motion planning | Action servers, Services | Path and trajectory planning |
| Control | Low-level control | Controllers, Topics | Joint control, stabilization |
| Behavior | High-level behaviors | State machines, Services | Walking, standing, gestures |
| Safety | Safety monitoring | Services, Parameters | Emergency stop, limits |
| Simulation | Robot simulation | Gazebo, RViz | Testing and development |

## 6.9 Example: Humanoid Head Controller

### Complete Head Control System

```python
# head_controller.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from std_msgs.msg import String
from sensor_msgs.msg import JointState
from geometry_msgs.msg import PointStamped, Vector3Stamped
from builtin_interfaces.msg import Duration
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from humanoid_interfaces.srv import SetHeadPose, GetHeadPose
import numpy as np
import math


class HeadController(Node):
    def __init__(self):
        super().__init__('head_controller')

        # Joint names for head
        self.head_joints = ['neck_pan_joint', 'neck_tilt_joint']

        # Publishers
        self.joint_cmd_pub = self.create_publisher(
            JointTrajectory, 'head_controller/joint_trajectory', 10)

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_state_callback, 10)

        # Services
        self.set_pose_srv = self.create_service(
            SetHeadPose, 'set_head_pose', self.set_head_pose_callback)
        self.get_pose_srv = self.create_service(
            GetHeadPose, 'get_head_pose', self.get_head_pose_callback)

        # Parameters
        self.declare_parameter('max_pan_speed', 1.0)
        self.declare_parameter('max_tilt_speed', 1.0)
        self.declare_parameter('pan_limits', [-1.57, 1.57])
        self.declare_parameter('tilt_limits', [-0.78, 0.78])

        # Internal state
        self.current_joint_positions = {}
        self.current_joint_velocities = {}
        self.target_pan = 0.0
        self.target_tilt = 0.0

        # Control timer
        self.control_timer = self.create_timer(0.02, self.control_loop)

        self.get_logger().info('Head controller initialized')

    def joint_state_callback(self, msg):
        """Update current joint states"""
        for i, name in enumerate(msg.name):
            if name in self.head_joints and i < len(msg.position):
                self.current_joint_positions[name] = msg.position[i]
            if name in self.head_joints and i < len(msg.velocity):
                self.current_joint_velocities[name] = msg.velocity[i]

    def set_head_pose_callback(self, request, response):
        """Set head pose service"""
        try:
            # Apply limits
            pan_limits = self.get_parameter('pan_limits').value
            tilt_limits = self.get_parameter('tilt_limits').value

            pan = max(pan_limits[0], min(pan_limits[1], request.pan))
            tilt = max(tilt_limits[0], min(tilt_limits[1], request.tilt))

            # Set target positions
            self.target_pan = pan
            self.target_tilt = tilt

            # Send trajectory command
            self.send_trajectory_command(pan, tilt)

            response.success = True
            response.message = f'Head pose set to pan: {pan:.3f}, tilt: {tilt:.3f}'
        except Exception as e:
            response.success = False
            response.message = f'Error setting head pose: {str(e)}'

        return response

    def get_head_pose_callback(self, request, response):
        """Get head pose service"""
        try:
            # Get current positions
            pan = self.current_joint_positions.get('neck_pan_joint', 0.0)
            tilt = self.current_joint_positions.get('neck_tilt_joint', 0.0)

            response.pan = pan
            response.tilt = tilt
            response.success = True
            response.message = f'Current head pose - pan: {pan:.3f}, tilt: {tilt:.3f}'
        except Exception as e:
            response.success = False
            response.message = f'Error getting head pose: {str(e)}'
            response.pan = 0.0
            response.tilt = 0.0

        return response

    def send_trajectory_command(self, pan_pos, tilt_pos):
        """Send trajectory command to head joints"""
        trajectory = JointTrajectory()
        trajectory.joint_names = self.head_joints

        point = JointTrajectoryPoint()
        point.positions = [pan_pos, tilt_pos]
        point.velocities = [0.0, 0.0]  # Let controller handle velocities
        point.time_from_start = Duration(sec=0, nanosec=100000000)  # 100ms

        trajectory.points = [point]
        self.joint_cmd_pub.publish(trajectory)

    def control_loop(self):
        """Main control loop"""
        # This could implement more sophisticated control algorithms
        # For now, we rely on the trajectory controller
        pass


def main(args=None):
    rclpy.init(args=args)
    controller = HeadController()

    try:
        rclpy.spin(controller)
    except KeyboardInterrupt:
        controller.get_logger().info('Shutting down head controller')
    finally:
        controller.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 6.10 Example: Sensor Processing with Decision Node

### Integrated Sensor and Decision System

```python
# sensor_decision_system.py
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy
from std_msgs.msg import String, Bool, Float32
from sensor_msgs.msg import LaserScan, Image, CameraInfo
from geometry_msgs.msg import Twist, PointStamped
from visualization_msgs.msg import Marker, MarkerArray
from builtin_interfaces.msg import Time
import numpy as np
import cv2
from cv2 import cv2 as cv
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge
import threading
from typing import List, Tuple


class SensorProcessingNode(Node):
    def __init__(self):
        super().__init__('sensor_processing')

        # QoS profile
        qos = QoSProfile(depth=10, reliability=ReliabilityPolicy.BEST_EFFORT)

        # Subscribers
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, qos)
        self.image_sub = self.create_subscription(Image, 'camera/image_raw', self.image_callback, qos)

        # Publishers
        self.obstacle_pub = self.create_publisher(Float32, 'obstacle_distance', 10)
        self.target_pub = self.create_publisher(PointStamped, 'detected_target', 10)
        self.decision_pub = self.create_publisher(String, 'sensor_decision', 10)
        self.marker_pub = self.create_publisher(MarkerArray, 'sensor_markers', 10)

        # Internal state
        self.latest_scan = None
        self.latest_image = None
        self.cv_bridge = CvBridge()

        # Processing timer
        self.process_timer = self.create_timer(0.1, self.process_sensors)

        self.get_logger().info('Sensor processing node initialized')

    def scan_callback(self, msg):
        """Process laser scan data"""
        self.latest_scan = msg

    def image_callback(self, msg):
        """Process camera image"""
        self.latest_image = msg

    def process_sensors(self):
        """Process sensor data and make decisions"""
        decisions = []

        # Process laser scan for obstacles
        if self.latest_scan:
            obstacle_info = self.process_laser_scan(self.latest_scan)
            if obstacle_info['distance'] < 1.0:  # Obstacle within 1 meter
                decisions.append(f"OBSTACLE_DETECTED_{obstacle_info['distance']:.2f}m")

        # Process camera image for targets
        if self.latest_image:
            target_info = self.process_camera_image(self.latest_image)
            if target_info['found']:
                decisions.append(f"TARGET_DETECTED_{target_info['x']:.2f}_{target_info['y']:.2f}")

        # Publish decisions
        for decision in decisions:
            decision_msg = String()
            decision_msg.data = decision
            self.decision_pub.publish(decision_msg)

    def process_laser_scan(self, scan_msg) -> dict:
        """Process laser scan data to detect obstacles"""
        if not scan_msg.ranges:
            return {'distance': float('inf'), 'angle': 0.0}

        # Find minimum distance
        valid_ranges = [r for r in scan_msg.ranges if r > scan_msg.range_min and r < scan_msg.range_max]
        if not valid_ranges:
            return {'distance': float('inf'), 'angle': 0.0}

        min_distance = min(valid_ranges)
        min_idx = scan_msg.ranges.index(min_distance)
        angle = scan_msg.angle_min + min_idx * scan_msg.angle_increment

        # Publish obstacle distance
        distance_msg = Float32()
        distance_msg.data = min_distance
        self.obstacle_pub.publish(distance_msg)

        # Create visualization marker
        marker = Marker()
        marker.header = scan_msg.header
        marker.ns = "obstacles"
        marker.id = 0
        marker.type = Marker.SPHERE
        marker.action = Marker.ADD
        marker.pose.position.x = min_distance * np.cos(angle)
        marker.pose.position.y = min_distance * np.sin(angle)
        marker.pose.position.z = 0.0
        marker.pose.orientation.w = 1.0
        marker.scale.x = 0.1
        marker.scale.y = 0.1
        marker.scale.z = 0.1
        marker.color.r = 1.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        marker_array = MarkerArray()
        marker_array.markers.append(marker)
        self.marker_pub.publish(marker_array)

        return {'distance': min_distance, 'angle': angle}

    def process_camera_image(self, image_msg) -> dict:
        """Process camera image to detect targets (simplified example)"""
        try:
            # Convert ROS image to OpenCV
            cv_image = self.cv_bridge.imgmsg_to_cv2(image_msg, "bgr8")

            # Simple color-based target detection (red object)
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # Define range for red color
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red, upper_red)

            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red, upper_red)

            mask = mask1 + mask2

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Find largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                if cv2.contourArea(largest_contour) > 100:  # Minimum area threshold
                    # Get center of contour
                    M = cv2.moments(largest_contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])

                        # Convert to normalized coordinates (-1 to 1)
                        height, width = cv_image.shape[:2]
                        norm_x = (2.0 * cx / width) - 1.0
                        norm_y = (2.0 * cy / height) - 1.0

                        # Publish target
                        target_msg = PointStamped()
                        target_msg.header = image_msg.header
                        target_msg.point.x = norm_x
                        target_msg.point.y = norm_y
                        target_msg.point.z = 0.0  # Depth not available from 2D image
                        self.target_pub.publish(target_msg)

                        return {'found': True, 'x': norm_x, 'y': norm_y}

        except Exception as e:
            self.get_logger().error(f'Error processing image: {e}')

        return {'found': False, 'x': 0.0, 'y': 0.0}


def main(args=None):
    rclpy.init(args=args)
    processor = SensorProcessingNode()

    try:
        rclpy.spin(processor)
    except KeyboardInterrupt:
        processor.get_logger().info('Shutting down sensor processing node')
    finally:
        processor.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 6.11 Integration Checklist

### Complete Integration Checklist

| Component | Status | Notes |
|-----------|--------|-------|
| **Nodes** | | |
| All nodes properly initialized | ☐ | Check node constructors |
| Node names are unique | ☐ | Verify no naming conflicts |
| Nodes have proper cleanup | ☐ | Check destroy_node methods |
| **Topics** | | |
| Publishers/subscribers created | ☐ | Verify all topic connections |
| QoS profiles appropriate | ☐ | Match reliability needs |
| Topic names follow conventions | ☐ | Use consistent naming |
| **Services** | | |
| Service servers available | ☐ | Check service availability |
| Service clients wait for service | ☐ | Implement proper waiting |
| Service interfaces consistent | ☐ | Match .srv definitions |
| **Actions** | | |
| Action servers created | ☐ | Verify action server setup |
| Action clients properly configured | ☐ | Check goal handling |
| Feedback and result handling | ☐ | Implement complete flow |
| **URDF/Xacro** | | |
| Robot model defined | ☐ | Complete kinematic chain |
| Inertial properties set | ☐ | Accurate mass and inertia |
| Visual/collision geometry | ☐ | Proper shapes defined |
| Gazebo plugins included | ☐ | Simulation integration |
| **Parameters** | | |
| All parameters declared | ☐ | Use declare_parameter |
| Parameter validation implemented | ☐ | Check on_set callback |
| Default values provided | ☐ | Ensure defaults exist |
| **Launch Files** | | |
| All required nodes included | ☐ | Verify complete system |
| Proper startup ordering | ☐ | Use event handlers if needed |
| Parameter files loaded | ☐ | Include config files |
| **Safety** | | |
| Emergency stops implemented | ☐ | Safety-critical systems |
| Joint limits enforced | ☐ | Position and velocity limits |
| Collision detection | ☐ | Check for self-collisions |

## 6.12 Exercises

### Exercise 1: Simple Humanoid Head Controller
Create a node that controls a humanoid robot's head using topics and services. The node should:
- Subscribe to joint states
- Provide a service to set head pan and tilt angles
- Publish joint trajectory commands to move the head
- Include parameter validation for joint limits

### Exercise 2: Sensor Processing Node
Design a sensor processing node that:
- Subscribes to laser scan and camera data
- Processes both sensor streams simultaneously
- Publishes processed information (obstacles, targets)
- Uses callback groups to manage concurrent processing

### Exercise 3: Launch File Integration
Create a launch file that:
- Starts URDF model with robot_state_publisher
- Launches controller manager with joint trajectory controllers
- Includes parameter files for system configuration
- Sets up proper remapping for multi-robot systems

### Exercise 4: Multi-Node rclpy System
Build a system with:
- At least 3 interconnected nodes
- Use of topics, services, and actions
- Proper callback group management
- System-wide parameter coordination

### Exercise 5: Safety Integration
Implement a safety system that:
- Monitors multiple sensor inputs
- Implements emergency stop functionality
- Uses services for safety state management
- Integrates with the main control system

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Simple Humanoid Head Controller</summary>

```python
# head_controller_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
from example_interfaces.srv import SetBool
from std_msgs.msg import String

class HeadControllerNode(Node):
    def __init__(self):
        super().__init__('head_controller_node')

        # Publishers
        self.joint_traj_pub = self.create_publisher(JointTrajectory, 'head_controller/joint_trajectory', 10)

        # Subscribers
        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10
        )

        # Service server for head control
        self.head_control_srv = self.create_service(
            SetBool,  # Using SetBool as a simple service, but in practice would create custom service
            'set_head_angles',
            self.set_head_angles_callback
        )

        # Internal state
        self.current_joint_states = JointState()
        self.head_joints = ['head_pan_joint', 'head_tilt_joint']

        # Declare parameters with validation
        self.declare_parameter('head.pan_limit_min', -1.57)
        self.declare_parameter('head.pan_limit_max', 1.57)
        self.declare_parameter('head.tilt_limit_min', -0.78)
        self.declare_parameter('head.tilt_limit_max', 0.78)

        self.get_logger().info('Head controller node initialized')

    def joint_state_callback(self, msg):
        """Update current joint states"""
        self.current_joint_states = msg
        self.get_logger().debug(f'Updated joint states with {len(msg.name)} joints')

    def set_head_angles_callback(self, request, response):
        """Handle head angle setting service request"""
        try:
            # In practice, we would have a custom service with angle parameters
            # For this example, we'll simulate based on request data
            if request.data:  # If True, set to neutral position
                pan_angle = 0.0
                tilt_angle = 0.0
            else:  # If False, set to a default look-forward position
                pan_angle = 0.0
                tilt_angle = 0.1

            # Validate joint limits
            pan_limit_min = self.get_parameter('head.pan_limit_min').value
            pan_limit_max = self.get_parameter('head.pan_limit_max').value
            tilt_limit_min = self.get_parameter('head.tilt_limit_min').value
            tilt_limit_max = self.get_parameter('head.tilt_limit_max').value

            if not (pan_limit_min <= pan_angle <= pan_limit_max):
                response.success = False
                response.message = f'Pan angle {pan_angle} out of range [{pan_limit_min}, {pan_limit_max}]'
                self.get_logger().error(response.message)
                return response

            if not (tilt_limit_min <= tilt_angle <= tilt_limit_max):
                response.success = False
                response.message = f'Tilt angle {tilt_angle} out of range [{tilt_limit_min}, {tilt_limit_max}]'
                self.get_logger().error(response.message)
                return response

            # Create and publish joint trajectory command
            traj_msg = JointTrajectory()
            traj_msg.joint_names = self.head_joints
            point = JointTrajectoryPoint()
            point.positions = [pan_angle, tilt_angle]
            point.time_from_start = Duration(sec=0, nanosec=500000000)  # 500ms
            traj_msg.points = [point]

            self.joint_traj_pub.publish(traj_msg)

            response.success = True
            response.message = f'Head angles set to pan: {pan_angle}, tilt: {tilt_angle}'
            self.get_logger().info(response.message)

        except Exception as e:
            response.success = False
            response.message = f'Error setting head angles: {str(e)}'
            self.get_logger().error(response.message)

        return response

def main(args=None):
    rclpy.init(args=args)

    node = HeadControllerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Head controller node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Sensor Processing Node</summary>

```python
# sensor_processing_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Image
from std_msgs.msg import String
from rclpy.callback_groups import ReentrantCallbackGroup
import numpy as np
from cv_bridge import CvBridge

class SensorProcessingNode(Node):
    def __init__(self):
        super().__init__('sensor_processing_node')

        # Create callback groups for concurrent processing
        self.sensor_callback_group = ReentrantCallbackGroup()

        # Subscribers for different sensor types
        self.laser_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10,
            callback_group=self.sensor_callback_group
        )

        self.camera_sub = self.create_subscription(
            Image,
            'camera/image_raw',
            self.camera_callback,
            10,
            callback_group=self.sensor_callback_group
        )

        # Publishers for processed information
        self.obstacle_pub = self.create_publisher(String, 'obstacles_detected', 10)
        self.target_pub = self.create_publisher(String, 'targets_detected', 10)

        # Internal state
        self.latest_scan = None
        self.latest_image = None
        self.cv_bridge = CvBridge()

        self.get_logger().info('Sensor processing node initialized')

    def laser_callback(self, msg):
        """Process laser scan data concurrently"""
        self.latest_scan = msg

        # Process scan for obstacles
        obstacles = self.process_laser_scan(msg)

        if obstacles:
            obstacle_msg = String()
            obstacle_msg.data = f'Obstacles detected at distances: {[round(d, 2) for d in obstacles[:5]]}'  # First 5 obstacles
            self.obstacle_pub.publish(obstacle_msg)
            self.get_logger().info(f'Laser processing: {obstacle_msg.data}')

    def camera_callback(self, msg):
        """Process camera data concurrently"""
        self.latest_image = msg

        # Process image for targets
        targets = self.process_camera_image(msg)

        if targets:
            target_msg = String()
            target_msg.data = f'Targets detected: {len(targets)} objects'
            self.target_pub.publish(target_msg)
            self.get_logger().info(f'Camera processing: {target_msg.data}')

    def process_laser_scan(self, scan_msg):
        """Process laser scan to detect obstacles"""
        obstacles = []
        for i, range_val in enumerate(scan_msg.ranges):
            if scan_msg.range_min < range_val < scan_msg.range_max and range_val < 1.0:  # Within 1 meter
                angle = scan_msg.angle_min + i * scan_msg.angle_increment
                obstacles.append((range_val, angle))

        return obstacles

    def process_camera_image(self, image_msg):
        """Process camera image to detect targets (simplified)"""
        try:
            # Convert ROS image to OpenCV
            cv_image = self.cv_bridge.imgmsg_to_cv2(image_msg, "bgr8")

            # Simple color-based detection (detect red objects)
            hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

            # Define range for red color
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red, upper_red)

            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            mask2 = cv2.inRange(hsv, lower_red, upper_red)

            mask = mask1 + mask2

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Filter contours by area to avoid noise
            targets = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # Minimum area threshold
                    # Get bounding box
                    x, y, w, h = cv2.boundingRect(contour)
                    targets.append({'bbox': (x, y, w, h), 'area': area})

            return targets

        except Exception as e:
            self.get_logger().error(f'Error processing camera image: {e}')
            return []

def main(args=None):
    rclpy.init(args=args)

    node = SensorProcessingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sensor processing node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Launch File Integration</summary>

```python
# launch/robot_system_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, RegisterEventHandler
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time if true'
    )

    robot_namespace = DeclareLaunchArgument(
        'robot_namespace',
        default_value='humanoid_robot',
        description='Robot namespace for multi-robot systems'
    )

    # Get launch configurations
    use_sim_time_config = LaunchConfiguration('use_sim_time')
    robot_namespace_config = LaunchConfiguration('robot_namespace')

    # URDF model and robot state publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_namespace_config,
        parameters=[
            {'use_sim_time': use_sim_time_config},
            {'robot_description':
                PathJoinSubstitution([
                    FindPackageShare('humanoid_description'),
                    'urdf',
                    'humanoid_robot.urdf.xacro'
                ])
            }
        ],
        remappings=[
            ('/joint_states', [robot_namespace_config, '/joint_states']),
            ('/tf', [robot_namespace_config, '/tf']),
            ('/tf_static', [robot_namespace_config, '/tf_static'])
        ]
    )

    # Joint state publisher (for simulation)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        namespace=robot_namespace_config,
        parameters=[
            {'use_sim_time': use_sim_time_config},
            {'source_list': ['joint_states']}
        ],
        condition=IfCondition(use_sim_time_config)
    )

    # Controller manager
    controller_manager = Node(
        package='controller_manager',
        executable='ros2_control_node',
        name='controller_manager',
        namespace=robot_namespace_config,
        parameters=[
            PathJoinSubstitution([
                FindPackageShare('humanoid_control'),
                'config',
                'controllers.yaml'
            ]),
            {'use_sim_time': use_sim_time_config}
        ],
        remappings=[
            ('/joint_states', [robot_namespace_config, '/joint_states'])
        ]
    )

    # Head controller spawner
    head_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['head_controller'],
        namespace=robot_namespace_config,
        parameters=[{'use_sim_time': use_sim_time_config}]
    )

    # Joint state broadcaster spawner
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        namespace=robot_namespace_config,
        parameters=[{'use_sim_time': use_sim_time_config}]
    )

    # Event handler to ensure proper startup order
    load_head_controller = RegisterEventHandler(
        OnProcessStart(
            target_action=joint_state_broadcaster_spawner,
            on_start=[head_controller_spawner],
        )
    )

    # Main robot controller node
    robot_controller = Node(
        package='humanoid_control',
        executable='robot_controller_node',
        name='robot_controller',
        namespace=robot_namespace_config,
        parameters=[
            PathJoinSubstitution([
                FindPackageShare('humanoid_control'),
                'config',
                'robot_params.yaml'
            ]),
            {'use_sim_time': use_sim_time_config},
            {'robot_namespace': robot_namespace_config}
        ],
        remappings=[
            ('/cmd_vel', [robot_namespace_config, '/cmd_vel']),
            ('/joint_commands', [robot_namespace_config, '/joint_commands'])
        ],
        output='screen'
    )

    # Sensor processing node
    sensor_processor = Node(
        package='humanoid_sensors',
        executable='sensor_processing_node',
        name='sensor_processor',
        namespace=robot_namespace_config,
        parameters=[
            {'use_sim_time': use_sim_time_config}
        ],
        remappings=[
            ('/scan', [robot_namespace_config, '/scan']),
            ('/camera/image_raw', [robot_namespace_config, '/camera/image_raw'])
        ],
        output='screen'
    )

    return LaunchDescription([
        use_sim_time,
        robot_namespace,
        robot_state_publisher,
        joint_state_publisher,
        controller_manager,
        joint_state_broadcaster_spawner,
        load_head_controller,
        robot_controller,
        sensor_processor
    ])
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: Multi-Node rclpy System</summary>

```python
# multi_node_system_example.py
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from std_msgs.msg import String, Bool
from geometry_msgs.msg import Twist
from example_interfaces.srv import SetBool, Trigger
from example_interfaces.action import Fibonacci
from rclpy.action import ActionServer, ActionClient

class CentralCoordinatorNode(Node):
    def __init__(self):
        super().__init__('central_coordinator')

        # Create callback groups
        self.safety_group = MutuallyExclusiveCallbackGroup()
        self.communication_group = ReentrantCallbackGroup()

        # Publishers
        self.status_pub = self.create_publisher(String, 'system_status', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers
        self.emergency_stop_sub = self.create_subscription(
            Bool,
            'emergency_stop',
            self.emergency_stop_callback,
            10,
            callback_group=self.safety_group
        )

        self.system_alert_sub = self.create_subscription(
            String,
            'system_alerts',
            self.alert_callback,
            10,
            callback_group=self.communication_group
        )

        # Services
        self.control_service = self.create_service(
            SetBool,
            'system_control',
            self.system_control_callback,
            callback_group=self.safety_group
        )

        self.health_check_service = self.create_service(
            Trigger,
            'health_check',
            self.health_check_callback,
            callback_group=self.communication_group
        )

        # Parameters
        self.declare_parameter('system_enabled', True)
        self.declare_parameter('control_frequency', 50.0)
        self.declare_parameter('safety_timeout', 1.0)

        # Internal state
        self.system_enabled = self.get_parameter('system_enabled').value
        self.safety_timeout = self.get_parameter('safety_timeout').value
        self.last_heartbeat = self.get_clock().now()

        # Timer for system coordination
        control_frequency = self.get_parameter('control_frequency').value
        self.coordination_timer = self.create_timer(
            1.0/control_frequency,
            self.coordination_loop,
            callback_group=self.communication_group
        )

        self.get_logger().info('Central coordinator node initialized')

    def emergency_stop_callback(self, msg):
        """Handle emergency stop with highest priority"""
        if msg.data:
            self.system_enabled = False
            # Stop all motion
            stop_cmd = Twist()
            self.cmd_vel_pub.publish(stop_cmd)
            self.get_logger().fatal('EMERGENCY STOP ACTIVATED')
        else:
            self.system_enabled = True
            self.get_logger().info('System re-enabled after emergency stop')

    def alert_callback(self, msg):
        """Handle system alerts"""
        self.get_logger().warn(f'System alert received: {msg.data}')

    def system_control_callback(self, request, response):
        """Handle system control requests"""
        if request.data:
            self.system_enabled = True
            response.success = True
            response.message = 'System enabled'
        else:
            self.system_enabled = False
            # Stop robot if disabling
            stop_cmd = Twist()
            self.cmd_vel_pub.publish(stop_cmd)
            response.success = True
            response.message = 'System disabled'

        return response

    def health_check_callback(self, request, response):
        """Handle health check requests"""
        response.success = True
        response.message = f'System healthy, enabled: {self.system_enabled}'
        return response

    def coordination_loop(self):
        """Main coordination loop"""
        if not self.system_enabled:
            return

        # Publish system status
        status_msg = String()
        status_msg.data = f'Coordinated system running, time: {self.get_clock().now().nanoseconds}'
        self.status_pub.publish(status_msg)

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion')

        # Publishers
        self.fused_data_pub = self.create_publisher(String, 'fused_sensor_data', 10)

        # Subscribers for different sensors
        self.laser_sub = self.create_subscription(String, 'laser_processed', self.laser_cb, 10)
        self.camera_sub = self.create_subscription(String, 'camera_processed', self.camera_cb, 10)
        self.imu_sub = self.create_subscription(String, 'imu_processed', self.imu_cb, 10)

        # Internal state
        self.sensor_data = {'laser': None, 'camera': None, 'imu': None}

        self.get_logger().info('Sensor fusion node initialized')

    def laser_cb(self, msg):
        self.sensor_data['laser'] = msg.data

    def camera_cb(self, msg):
        self.sensor_data['camera'] = msg.data

    def imu_cb(self, msg):
        self.sensor_data['imu'] = msg.data

    def fuse_data(self):
        """Fuse sensor data"""
        if all(self.sensor_data.values()):
            fused_msg = String()
            fused_msg.data = f"Fused: laser={self.sensor_data['laser']}, camera={self.sensor_data['camera']}, imu={self.sensor_data['imu']}"
            self.fused_data_pub.publish(fused_msg)

class NavigationNode(Node):
    def __init__(self):
        super().__init__('navigation_node')

        # Action server for navigation
        self.nav_action_server = ActionServer(
            self,
            Fibonacci,  # Using Fibonacci as example, would use NavigateToPose in real system
            'navigate_action',
            self.nav_execute_callback
        )

        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.goal_sub = self.create_subscription(String, 'navigation_goals', self.goal_callback, 10)

        self.get_logger().info('Navigation node initialized')

    def nav_execute_callback(self, goal_handle):
        """Execute navigation action"""
        self.get_logger().info('Executing navigation goal...')

        # Simulate navigation execution
        result = Fibonacci.Result()
        result.sequence = [0, 1, 1, 2, 3, 5, 8, 13]  # Example sequence

        goal_handle.succeed()
        return result

    def goal_callback(self, msg):
        """Handle navigation goals"""
        self.get_logger().info(f'Navigation goal received: {msg.data}')

class ParameterManagementNode(Node):
    def __init__(self):
        super().__init__('parameter_management')

        # Declare parameters
        self.declare_parameter('global_config.nav_frequency', 10.0)
        self.declare_parameter('global_config.control_gain', 1.0)
        self.declare_parameter('global_config.safety_margin', 0.5)

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.param_validation_callback)

        self.get_logger().info('Parameter management node initialized')

    def param_validation_callback(self, params):
        """Validate parameter changes"""
        from rcl_interfaces.msg import SetParametersResult
        result = SetParametersResult()
        result.successful = True

        for param in params:
            if param.name == 'global_config.nav_frequency':
                if param.value <= 0 or param.value > 100:
                    result.successful = False
                    result.reason = 'Navigation frequency must be between 0 and 100 Hz'
                    return result

        return result

def main(args=None):
    rclpy.init(args=args)

    # Create nodes
    coordinator = CentralCoordinatorNode()
    sensor_fusion = SensorFusionNode()
    navigation = NavigationNode()
    params = ParameterManagementNode()

    # Create multi-threaded executor
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(coordinator)
    executor.add_node(sensor_fusion)
    executor.add_node(navigation)
    executor.add_node(params)

    try:
        executor.spin()
    except KeyboardInterrupt:
        coordinator.get_logger().info('Multi-node system interrupted by user')
    finally:
        coordinator.destroy_node()
        sensor_fusion.destroy_node()
        navigation.destroy_node()
        params.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Safety Integration</summary>

```python
# safety_integration_node.py
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from sensor_msgs.msg import LaserScan, Imu, JointState
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Twist
from example_interfaces.srv import SetBool, Trigger
import numpy as np
import threading
import time

class SafetyIntegrationNode(Node):
    def __init__(self):
        super().__init__('safety_integration')

        # Create safety-critical callback group
        self.safety_group = MutuallyExclusiveCallbackGroup()

        # Publishers for safety states
        self.emergency_stop_pub = self.create_publisher(Bool, 'emergency_stop', 10)
        self.safety_status_pub = self.create_publisher(String, 'safety_status', 10)
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers for monitoring sensors
        self.laser_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_monitor_callback,
            10
        )

        self.imu_sub = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_monitor_callback,
            10
        )

        self.joint_state_sub = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_monitor_callback,
            10
        )

        # Services for safety management
        self.emergency_stop_service = self.create_service(
            SetBool,
            'emergency_stop_service',
            self.emergency_stop_service_callback,
            callback_group=self.safety_group
        )

        self.safety_enable_service = self.create_service(
            SetBool,
            'safety_enable_service',
            self.safety_enable_service_callback,
            callback_group=self.safety_group
        )

        self.safety_reset_service = self.create_service(
            Trigger,
            'safety_reset_service',
            self.safety_reset_service_callback,
            callback_group=self.safety_group
        )

        # Parameters for safety thresholds
        self.declare_parameter('safety.obstacle_distance_threshold', 0.3)  # 30cm
        self.declare_parameter('safety.tilt_angle_threshold', 0.5)       # ~28 degrees
        self.declare_parameter('safety.joint_limit_threshold', 0.1)      # 0.1 rad from limit
        self.declare_parameter('safety.motion_timeout', 5.0)             # 5 seconds

        # Internal safety state
        self.safety_enabled = True
        self.emergency_stop_active = False
        self.obstacle_detected = False
        self.excessive_tilt = False
        self.joint_limits_violated = False
        self.motion_timeout = False
        self.last_motion_time = time.time()

        # Lock for thread safety
        self.safety_lock = threading.Lock()

        # Timer for safety monitoring
        self.safety_timer = self.create_timer(0.1, self.safety_monitor_loop)

        self.get_logger().info('Safety integration system initialized')

    def laser_monitor_callback(self, msg):
        """Monitor laser scan for obstacles"""
        if not self.safety_enabled or self.emergency_stop_active:
            return

        # Check for obstacles within safety threshold
        safety_dist = self.get_parameter('safety.obstacle_distance_threshold').value
        valid_ranges = [r for r in msg.ranges if msg.range_min < r < msg.range_max]

        if valid_ranges and min(valid_ranges) < safety_dist:
            with self.safety_lock:
                self.obstacle_detected = True
                self.get_logger().warn(f'Obstacle detected within safety distance: {min(valid_ranges):.2f}m')
        else:
            with self.safety_lock:
                self.obstacle_detected = False

    def imu_monitor_callback(self, msg):
        """Monitor IMU for excessive tilt"""
        if not self.safety_enabled or self.emergency_stop_active:
            return

        # Convert quaternion to Euler angles to check tilt
        orientation = msg.orientation
        w, x, y, z = orientation.w, orientation.x, orientation.y, orientation.z

        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        pitch = np.arcsin(sinp)

        # Check if tilt exceeds threshold
        tilt_threshold = self.get_parameter('safety.tilt_angle_threshold').value
        tilt_magnitude = np.sqrt(roll**2 + pitch**2)

        with self.safety_lock:
            if tilt_magnitude > tilt_threshold:
                self.excessive_tilt = True
                self.get_logger().warn(f'Excessive tilt detected: {np.degrees(tilt_magnitude):.2f} degrees')
            else:
                self.excessive_tilt = False

    def joint_monitor_callback(self, msg):
        """Monitor joint states for limit violations"""
        if not self.safety_enabled or self.emergency_stop_active:
            return

        # In a real system, we would have joint limits defined
        # For this example, we'll use arbitrary limits
        joint_limit_threshold = self.get_parameter('safety.joint_limit_threshold').value
        critical_joints = ['left_hip_joint', 'right_hip_joint', 'left_knee_joint', 'right_knee_joint']

        limit_violated = False
        for i, joint_name in enumerate(msg.name):
            if joint_name in critical_joints and i < len(msg.position):
                position = msg.position[i]
                # Example: assume joint limits of ±2.0 radians
                if abs(position) > (2.0 - joint_limit_threshold):
                    limit_violated = True
                    self.get_logger().warn(f'Joint limit approaching for {joint_name}: {position:.3f} rad')

        with self.safety_lock:
            self.joint_limits_violated = limit_violated

    def safety_monitor_loop(self):
        """Main safety monitoring loop"""
        if not self.safety_enabled:
            return

        with self.safety_lock:
            # Check for any safety violations
            any_violation = (
                self.obstacle_detected or
                self.excessive_tilt or
                self.joint_limits_violated or
                self.motion_timeout
            )

            if any_violation and not self.emergency_stop_active:
                self.activate_emergency_stop()
            elif not any_violation and self.emergency_stop_active:
                # Conditions are safe again, but we don't automatically resume
                # Safety reset must be done manually
                pass

            # Publish safety status
            status_msg = String()
            status_msg.data = f"Safety: enabled={self.safety_enabled}, emergency={self.emergency_stop_active}, " \
                             f"obstacle={self.obstacle_detected}, tilt={self.excessive_tilt}, " \
                             f"joints_violated={self.joint_limits_violated}, timeout={self.motion_timeout}"
            self.safety_status_pub.publish(status_msg)

    def activate_emergency_stop(self):
        """Activate emergency stop"""
        self.emergency_stop_active = True
        self.get_logger().fatal('EMERGENCY STOP ACTIVATED - Safety violation detected!')

        # Stop all motion immediately
        stop_cmd = Twist()
        self.cmd_vel_pub.publish(stop_cmd)

        # Publish emergency stop signal
        emergency_msg = Bool()
        emergency_msg.data = True
        self.emergency_stop_pub.publish(emergency_msg)

    def deactivate_emergency_stop(self):
        """Deactivate emergency stop"""
        self.emergency_stop_active = False
        self.get_logger().info('Emergency stop deactivated')

    def emergency_stop_service_callback(self, request, response):
        """Handle emergency stop service requests"""
        if request.data:
            self.activate_emergency_stop()
            response.success = True
            response.message = 'Emergency stop activated'
        else:
            self.deactivate_emergency_stop()
            response.success = True
            response.message = 'Emergency stop deactivated'

        return response

    def safety_enable_service_callback(self, request, response):
        """Handle safety enable/disable requests"""
        self.safety_enabled = request.data
        if request.data:
            response.success = True
            response.message = 'Safety system enabled'
            self.get_logger().info('Safety system enabled')
        else:
            response.success = True
            response.message = 'Safety system disabled - USE WITH CAUTION!'
            self.get_logger().warn('Safety system disabled - USE WITH CAUTION!')

        return response

    def safety_reset_service_callback(self, request, response):
        """Handle safety reset requests"""
        if self.emergency_stop_active:
            # Reset is only allowed by service, not automatically
            self.deactivate_emergency_stop()
            response.success = True
            response.message = 'Safety system reset - manual confirmation required'
            self.get_logger().info('Safety system reset via service call')
        else:
            response.success = True
            response.message = 'No emergency stop active, nothing to reset'

        return response

def main(args=None):
    rclpy.init(args=args)

    node = SafetyIntegrationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Safety integration node interrupted by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

## 6.13 Capstone Mini-Project: Multi-Node Humanoid Control System

Build a complete multi-node humanoid control system that includes:

1. **URDF Model**: Create a humanoid robot model with head, arms, and legs
2. **Topics**: Implement sensor data topics (joint states, IMU, laser scan)
3. **Services**: Create services for system control (calibration, mode switching)
4. **Actions**: Implement actions for complex behaviors (walking, gesture execution)
5. **Parameters**: Set up system-wide parameter management
6. **Launch System**: Create comprehensive launch files
7. **Safety System**: Include emergency stop and safety monitoring

The system should demonstrate:
- Proper node organization and communication
- Integration of all ROS 2 concepts
- Real-time performance characteristics
- Safety and error handling
- Modular design principles

:::tip
Start with a simple system and gradually add complexity. Test each component individually before integrating them into the full system.
:::

## 6.14 Chapter Summary

This chapter covered the integration of all core ROS 2 concepts into complete humanoid robotics applications:

- **System Architecture**: Combining nodes, topics, services, and actions into working systems
- **URDF Integration**: Connecting robot models with controllers and simulation
- **Launch Systems**: Orchestrating multi-node systems with proper parameter management
- **Parameter Management**: Coordinating configuration across the entire system
- **Event-Driven Architecture**: Building responsive, real-time callback systems
- **Modular Design**: Creating maintainable, reusable control pipelines
- **Data Flow**: Managing information flow through the system
- **Humanoid Applications**: Specialized considerations for humanoid robot systems

The integration of these components creates robust, maintainable, and scalable robotic applications that can perform complex tasks in real-world environments. Success in integration requires careful attention to system architecture, proper error handling, and thorough testing of all component interactions.