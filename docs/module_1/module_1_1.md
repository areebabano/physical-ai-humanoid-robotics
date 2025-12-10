---
id: module_1_1
title: "Module 1.1 - Chapter 1: ROS 2 Fundamentals"
sidebar_position: 1
---

# Module 1.1 - Chapter 1: ROS 2 Fundamentals

## 1.0 Introduction and Learning Objectives

### Chapter Overview

Robot Operating System 2 (ROS 2) represents a paradigm shift in robotics software development, providing a flexible framework for writing robot software. Unlike traditional monolithic approaches, ROS 2 embraces a distributed architecture that enables complex robot systems to be built from modular, reusable components. This chapter introduces the fundamental concepts that form the backbone of ROS 2, establishing the foundation for advanced robotics applications.

ROS 2 is not an operating system in the traditional sense, but rather a collection of libraries, tools, and conventions that facilitate communication between robot processes. Whether these processes run on a single machine or across multiple robots, ROS 2 provides the infrastructure for seamless coordination and data exchange.

### Learning Objectives

By the end of this chapter, you will be able to:

- Understand the architecture and design principles of ROS 2
- Create and manage ROS 2 nodes for robot applications
- Implement communication patterns using topics, services, and parameters
- Model robot kinematics using URDF (Unified Robot Description Format)
- Integrate Python with ROS 2 using the `rclpy` client library
- Design complete robot systems with sensors, perception, and control
- Apply best practices for debugging and error handling in ROS 2
- Build a complete running example that demonstrates all core concepts

## 1.1 ROS 2 Architecture Overview

### High-Level Architecture

ROS 2 employs a distributed architecture built on the Data Distribution Service (DDS) middleware. This design enables robust communication patterns while maintaining flexibility for various deployment scenarios.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Node A        │    │   DDS Middleware│    │   Node B        │
│                 │    │                 │    │                 │
│  Publisher      │◄──►│  Discovery &    │◄──►│  Subscriber     │
│  Service Server │    │  Communication  │    │  Service Client │
│  Action Server  │    │  Layer         │    │  Action Client  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Architectural Components

ROS 2 architecture consists of several layers that work together to provide a comprehensive robotics framework:

1. **Application Layer**: User-defined robot applications and algorithms
2. **Client Library Layer**: Language-specific APIs (rclpy, rclcpp)
3. **ROS Client Library Layer**: Common ROS interfaces
4. **Middleware Layer**: DDS implementation for communication
5. **Operating System Layer**: Underlying OS services

### Comparison: ROS 1 vs ROS 2

| Feature | ROS 1 | ROS 2 |
|---------|-------|-------|
| Communication | Custom TCP/UDP | DDS-based |
| Multi-machine | Master-dependent | Masterless |
| Real-time support | Limited | Full support |
| Security | None | Built-in security |
| QoS policies | Fixed | Configurable |
| Language support | Python, C++ | Python, C++, Java, etc. |
| Lifecycle management | Manual | Built-in |
| Time handling | ROS time only | System + ROS time |

## 1.2 Nodes: The Building Blocks of ROS 2

### Understanding Nodes

Nodes are the fundamental execution units in ROS 2. Each node represents a process that performs a specific computation or task within the robot system. Nodes are designed to be modular, allowing complex robot behaviors to emerge from the interaction of multiple specialized nodes.

### Node Creation and Lifecycle

Creating a basic ROS 2 node using `rclpy`:

```python
import rclpy
from rclpy.node import Node

class SimpleNode(Node):
    def __init__(self):
        # Initialize the node with a name
        super().__init__('simple_node')

        # Log a message to indicate node startup
        self.get_logger().info('Simple node has been initialized')

def main(args=None):
    # Initialize the ROS 2 client library
    rclpy.init(args=args)

    # Create an instance of the node
    node = SimpleNode()

    # Keep the node running
    rclpy.spin(node)

    # Clean up resources
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Node Lifecycle States

ROS 2 nodes can transition through several lifecycle states:

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Unconfigured│───►│   Inactive  │───►│    Active   │
│     (1)     │    │     (2)     │    │     (3)     │
└─────────────┘    └─────────────┘    └─────────────┘
        ▲                   │                   │
        │                   ▼                   ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Finalized │◄───│   Error     │◄───│   Shutdown  │
│     (6)     │    │     (5)     │    │     (4)     │
└─────────────┘    └─────────────┘    └─────────────┘
```

1. **Unconfigured**: Initial state after node creation
2. **Inactive**: After configuration but before activation
3. **Active**: Node is fully operational
4. **Shutdown**: Node is shutting down
5. **Error**: Node is in error state
6. **Finalized**: Node has been destroyed

### Advanced Node Features

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy
from rclpy.lifecycle import LifecycleNode, LifecycleState
from rclpy.lifecycle import TransitionCallbackReturn

class AdvancedNode(LifecycleNode):
    def __init__(self):
        super().__init__('advanced_node')

        # Define QoS profiles for different use cases
        self.qos_profile = QoSProfile(
            depth=10,
            reliability=ReliabilityPolicy.RELIABLE,
            history=HistoryPolicy.KEEP_LAST
        )

        self.get_logger().info('Advanced node created with lifecycle management')

    def on_configure(self, state):
        """Configure the node"""
        self.get_logger().info('Configuring node')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state):
        """Activate the node"""
        self.get_logger().info('Activating node')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state):
        """Deactivate the node"""
        self.get_logger().info('Deactivating node')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state):
        """Clean up the node"""
        self.get_logger().info('Cleaning up node')
        return TransitionCallbackReturn.SUCCESS

def main(args=None):
    rclpy.init(args=args)
    node = AdvancedNode()

    # For lifecycle nodes, use the lifecycle node executor
    from rclpy.executors import SingleThreadedExecutor
    executor = SingleThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.3 Topics: Publish-Subscribe Communication

### Topic Communication Model

Topics implement the publish-subscribe pattern, enabling asynchronous communication between nodes. Publishers send messages to topics, while subscribers receive messages from topics. This decoupling allows for flexible system architectures where publishers and subscribers don't need to know about each other.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Publisher   │    │   Topic     │    │ Subscriber  │
│ Node        │───►│   /sensor   │───►│   Node      │
│             │    │   Data      │    │             │
└─────────────┘    └─────────────┘    └─────────────┘
                        │
                ┌─────────────┐
                │ Message     │
                │ Buffer      │
                └─────────────┘
```

### Publisher Implementation

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import time

class PublisherNode(Node):
    def __init__(self):
        super().__init__('publisher_node')

        # Create a publisher
        self.publisher = self.create_publisher(
            String,           # Message type
            'topic_name',     # Topic name
            10               # Queue size
        )

        # Create a timer to publish messages periodically
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.i = 0
        self.get_logger().info('Publisher node started')

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    publisher_node = PublisherNode()

    try:
        rclpy.spin(publisher_node)
    except KeyboardInterrupt:
        publisher_node.get_logger().info('Interrupted by user')
    finally:
        publisher_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Implementation

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SubscriberNode(Node):
    def __init__(self):
        super().__init__('subscriber_node')

        # Create a subscription
        self.subscription = self.create_subscription(
            String,           # Message type
            'topic_name',     # Topic name
            self.listener_callback,  # Callback function
            10               # Queue size
        )

        # Prevent unused variable warning
        self.subscription

        self.get_logger().info('Subscriber node started')

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    subscriber_node = SubscriberNode()

    try:
        rclpy.spin(subscriber_node)
    except KeyboardInterrupt:
        subscriber_node.get_logger().info('Interrupted by user')
    finally:
        subscriber_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Quality of Service (QoS) Settings

QoS policies control how messages are delivered between publishers and subscribers:

```python
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy, DurabilityPolicy

# Different QoS profiles for different use cases
SENSOR_QOS = QoSProfile(
    depth=10,
    reliability=ReliabilityPolicy.BEST_EFFORT,
    history=HistoryPolicy.KEEP_LAST,
    durability=DurabilityPolicy.VOLATILE
)

CRITICAL_QOS = QoSProfile(
    depth=1,
    reliability=ReliabilityPolicy.RELIABLE,
    history=HistoryPolicy.KEEP_ALL,
    durability=DurabilityPolicy.TRANSIENT_LOCAL
)

class QoSPublisherNode(Node):
    def __init__(self):
        super().__init__('qos_publisher_node')

        # Publisher with custom QoS for sensor data
        self.sensor_publisher = self.create_publisher(
            String, 'sensor_data', SENSOR_QOS
        )

        # Publisher with critical QoS for commands
        self.command_publisher = self.create_publisher(
            String, 'commands', CRITICAL_QOS
        )

        self.timer = self.create_timer(0.1, self.publish_data)

    def publish_data(self):
        # Publish sensor data
        sensor_msg = String()
        sensor_msg.data = f'Sensor reading: {self.get_clock().now().nanoseconds}'
        self.sensor_publisher.publish(sensor_msg)

        # Publish command data
        cmd_msg = String()
        cmd_msg.data = f'Command: {self.get_clock().now().nanoseconds}'
        self.command_publisher.publish(cmd_msg)
```

## 1.4 Services: Request-Response Communication

### Service Communication Model

Services provide synchronous request-response communication between nodes. A service client sends a request to a service server, which processes the request and returns a response. This pattern is ideal for operations that require a direct response.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│ Service     │    │   Service   │    │ Service     │
│ Client      │───►│   Name      │───►│ Server      │
│ Request     │    │   /add      │    │ Process     │
└─────────────┘    └─────────────┘    └─────────────┘
                        │
                ┌─────────────┐
                │ Request/    │
                │ Response    │
                │ Queue       │
                └─────────────┘
```

### Service Server Implementation

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')

        # Create a service server
        self.srv = self.create_service(
            AddTwoInts,           # Service type
            'add_two_ints',       # Service name
            self.add_two_ints_callback  # Callback function
        )

        self.get_logger().info('Service server started')

    def add_two_ints_callback(self, request, response):
        # Process the request and set the response
        response.sum = request.a + request.b

        self.get_logger().info(
            f'Request received: {request.a} + {request.b} = {response.sum}'
        )

        return response  # Return the response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()

    try:
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        minimal_service.get_logger().info('Service interrupted by user')
    finally:
        minimal_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client Implementation

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')

        # Create a service client
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # Wait for the service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        # Set the request parameters
        self.req.a = a
        self.req.b = b

        # Send the request asynchronously
        self.future = self.cli.call_async(self.req)

        # Wait for the response
        rclpy.spin_until_future_complete(self, self.future)

        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClient()

    # Send a request
    response = minimal_client.send_request(1, 2)

    minimal_client.get_logger().info(
        f'Result of {minimal_client.req.a} + {minimal_client.req.b} = {response.sum}'
    )

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Asynchronous Service Client

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class AsyncClient(Node):
    def __init__(self):
        super().__init__('async_client')

        # Create service client
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # Timer to periodically check for service availability
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.req_count = 0

    def timer_callback(self):
        if self.cli.service_is_ready():
            self.timer.cancel()
            self.send_async_request()

    def send_async_request(self):
        if self.req_count < 5:  # Send 5 requests
            request = AddTwoInts.Request()
            request.a = self.req_count
            request.b = self.req_count * 2

            future = self.cli.call_async(request)
            future.add_done_callback(self.response_callback)

            self.req_count += 1
            self.get_logger().info(f'Sent request {self.req_count}: {request.a} + {request.b}')

    def response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Received response: {response.sum}')
            # Send next request
            self.send_async_request()
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    async_client = AsyncClient()

    executor = MultiThreadedExecutor()
    executor.add_node(async_client)

    try:
        executor.spin()
    finally:
        async_client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.5 Parameters: Configuration and Runtime Control

### Parameter System Overview

Parameters provide a way to configure nodes at runtime without recompilation. They allow for dynamic adjustment of node behavior, making systems more flexible and easier to tune.

### Parameter Declaration and Usage

```python
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterType

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'my_robot')
        self.declare_parameter('max_velocity', 1.0)
        self.declare_parameter('min_velocity', 0.1)
        self.declare_parameter('control_frequency', 50)
        self.declare_parameter('debug_mode', False)

        # Access parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.min_velocity = self.get_parameter('min_velocity').value
        self.control_frequency = self.get_parameter('control_frequency').value
        self.debug_mode = self.get_parameter('debug_mode').value

        self.get_logger().info(f'Node configured with robot name: {self.robot_name}')
        self.get_logger().info(f'Velocity limits: {self.min_velocity} to {self.max_velocity}')
        self.get_logger().info(f'Control frequency: {self.control_frequency} Hz')
        self.get_logger().info(f'Debug mode: {self.debug_mode}')

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Parameter node interrupted by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Parameter Validation and Callbacks

```python
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node

class ValidatedParameterNode(Node):
    def __init__(self):
        super().__init__('validated_parameter_node')

        # Declare parameters
        self.declare_parameter('threshold', 1.0)
        self.declare_parameter('max_velocity', 2.0)
        self.declare_parameter('robot_name', 'default_robot')

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.parameters_callback)

        # Initialize parameter values
        self.threshold = self.get_parameter('threshold').value
        self.max_velocity = self.get_parameter('max_velocity').value
        self.robot_name = self.get_parameter('robot_name').value

        self.get_logger().info('Parameter validation node started')

    def parameters_callback(self, parameters):
        """Validate parameter changes"""
        for param in parameters:
            if param.name == 'threshold' and param.value <= 0:
                self.get_logger().warn(f'Invalid threshold value: {param.value}')
                return SetParametersResult(successful=False)

            if param.name == 'max_velocity' and (param.value <= 0 or param.value > 10.0):
                self.get_logger().warn(f'Invalid max_velocity value: {param.value}')
                return SetParametersResult(successful=False)

            if param.name == 'robot_name' and not isinstance(param.value, str):
                self.get_logger().warn(f'Invalid robot_name type: {type(param.value)}')
                return SetParametersResult(successful=False)

        # Update local values if validation passes
        for param in parameters:
            if param.name == 'threshold':
                self.threshold = param.value
            elif param.name == 'max_velocity':
                self.max_velocity = param.value
            elif param.name == 'robot_name':
                self.robot_name = param.value

        self.get_logger().info('Parameters updated successfully')
        return SetParametersResult(successful=True)

def main(args=None):
    rclpy.init(args=args)
    node = ValidatedParameterNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Parameter node interrupted by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.6 URDF: Unified Robot Description Format

### URDF Overview

URDF (Unified Robot Description Format) is an XML-based format for representing robot models. It describes a robot's physical and visual properties, including links, joints, and other components. URDF is essential for robot simulation, visualization, and control.

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Links define the rigid parts of the robot -->
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
      <inertia ixx="1.0" ixy="0.0" ixz="0.0" iyy="1.0" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Joints define how links connect -->
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
</robot>
```

### Humanoid Robot URDF Example

```xml
<?xml version="1.0"?>
<robot name="humanoid_robot">
  <!-- Main body -->
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
  <joint name="left_shoulder_joint" type="revolute">
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

  <!-- Sensors in URDF -->
  <joint name="camera_joint" type="fixed">
    <parent link="head"/>
    <child link="camera_link"/>
    <origin xyz="0.05 0 0.05" rpy="0 0 0"/>
  </joint>

  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.02"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <inertial>
      <mass value="0.1"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Gazebo plugin for camera -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="camera_sensor">
      <pose>0 0 0 0 0 0</pose>
      <visualize>true</visualize>
      <update_rate>30</update_rate>
      <camera name="head">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.01</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <remapping>~/image_raw:=camera/image_raw</remapping>
          <remapping>~/camera_info:=camera/camera_info</remapping>
        </ros>
      </plugin>
    </sensor>
  </gazebo>
</robot>
```

### URDF Joint Types and Applications

| Joint Type | Description | Application | Range |
|------------|-------------|-------------|-------|
| Fixed | No movement | Rigid connections | N/A |
| Revolute | Single-axis rotation | Elbow, knee joints | Limited |
| Continuous | Unlimited rotation | Wheels, continuous rotation | Unlimited |
| Prismatic | Linear movement | Linear actuators | Limited |
| Planar | Movement in plane | Mobile platforms | Limited |
| Floating | 6 DOF | Simulated floating objects | Unlimited |

## 1.7 Python Integration with rclpy

### rclpy Overview

rclpy is the Python client library for ROS 2, providing a Python API for creating ROS 2 nodes, publishers, subscribers, services, and actions. It serves as the bridge between Python applications and the ROS 2 ecosystem.

### Basic rclpy Structure

```python
import rclpy
from rclpy.node import Node

class MyROSNode(Node):
    def __init__(self):
        # Initialize the node
        super().__init__('node_name')

        # Initialize ROS components here
        # - Publishers
        # - Subscribers
        # - Services
        # - Parameters
        # - Timers

        self.get_logger().info('Node initialized')

def main(args=None):
    # Initialize ROS
    rclpy.init(args=args)

    # Create node
    node = MyROSNode()

    # Spin the node (keep it running)
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node interrupted')
    finally:
        # Cleanup
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Advanced rclpy Features

```python
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
import threading

class AdvancedRCLPYNode(Node):
    def __init__(self):
        super().__init__('advanced_rclpy_node')

        # Create different callback groups
        self.reentrant_group = ReentrantCallbackGroup()
        self.mutually_exclusive_group = MutuallyExclusiveCallbackGroup()

        # Publishers
        self.status_publisher = self.create_publisher(String, 'status', 10)

        # Subscribers with different callback groups
        self.fast_subscriber = self.create_subscription(
            String,
            'fast_topic',
            self.fast_callback,
            10,
            callback_group=self.reentrant_group
        )

        self.sensor_subscriber = self.create_subscription(
            LaserScan,
            'laser_scan',
            self.sensor_callback,
            10,
            callback_group=self.mutually_exclusive_group
        )

        # Timer
        self.status_timer = self.create_timer(
            1.0,
            self.status_callback,
            callback_group=self.reentrant_group
        )

        # Shared data with thread safety
        self.lock = threading.Lock()
        self.sensor_data = None
        self.status_counter = 0

        self.get_logger().info('Advanced rclpy node initialized')

    def fast_callback(self, msg):
        """Callback that can run concurrently"""
        with self.lock:
            self.status_counter += 1
            self.get_logger().info(f'Fast callback: {msg.data} (#{self.status_counter})')

    def sensor_callback(self, msg):
        """Callback that runs exclusively"""
        with self.lock:
            self.sensor_data = msg.ranges
            self.get_logger().info(f'Sensor callback: {len(msg.ranges)} ranges received')

    def status_callback(self):
        """Status timer callback"""
        with self.lock:
            status_msg = String()
            status_msg.data = f'Node status: {self.status_counter} fast callbacks processed'
            self.status_publisher.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    node = AdvancedRCLPYNode()

    # Use multi-threaded executor for callback groups
    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Advanced node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.8 Real Robot Scenario: Sensor → Perception → Control

### Complete Robot System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sensor        │    │   Perception    │    │   Control       │
│   Node          │───►│   Node          │───►│   Node          │
│                 │    │                 │    │                 │
│ • Laser Scanner │    │ • Obstacle      │    │ • Path Planner  │
│ • Camera        │    │   Detection     │    │ • Motion Ctrl   │
│ • IMU           │    │ • Object Rec.   │    │ • Safety Ctrl   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Sensor Data   │    │   Processed     │    │   Control       │
│   Topics        │    │   Information   │    │   Commands      │
│   (ROS 2)       │    │   (ROS 2)       │    │   (ROS 2)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Example: Obstacle Avoidance System

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32
import numpy as np

class ObstacleAvoidanceNode(Node):
    def __init__(self):
        super().__init__('obstacle_avoidance_node')

        # Parameters for obstacle detection
        self.declare_parameter('safety_distance', 0.5)
        self.declare_parameter('linear_velocity', 0.5)
        self.declare_parameter('angular_velocity', 0.5)

        self.safety_distance = self.get_parameter('safety_distance').value
        self.linear_velocity = self.get_parameter('linear_velocity').value
        self.angular_velocity = self.get_parameter('angular_velocity').value

        # Subscribers
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        # Publishers
        self.cmd_publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10
        )

        self.obstacle_publisher = self.create_publisher(
            Float32,
            'obstacle_distance',
            10
        )

        # Internal state
        self.obstacle_detected = False
        self.min_distance = float('inf')

        self.get_logger().info('Obstacle avoidance node initialized')

    def scan_callback(self, msg):
        """Process laser scan data for obstacle detection"""
        # Filter out invalid ranges
        valid_ranges = [r for r in msg.ranges if r > 0 and r < float('inf')]

        if valid_ranges:
            self.min_distance = min(valid_ranges)
            self.obstacle_detected = self.min_distance < self.safety_distance

            # Publish obstacle distance
            obstacle_msg = Float32()
            obstacle_msg.data = self.min_distance
            self.obstacle_publisher.publish(obstacle_msg)

            # Generate control command
            self.generate_control_command()

    def generate_control_command(self):
        """Generate velocity commands based on obstacle detection"""
        cmd = Twist()

        if self.obstacle_detected:
            # Obstacle detected - stop and turn
            cmd.linear.x = 0.0
            cmd.angular.z = self.angular_velocity
            self.get_logger().info(f'Obstacle detected at {self.min_distance:.2f}m, turning')
        else:
            # Clear path - move forward
            cmd.linear.x = self.linear_velocity
            cmd.angular.z = 0.0
            self.get_logger().info(f'Path clear, moving forward at {self.linear_velocity}m/s')

        # Publish command
        self.cmd_publisher.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = ObstacleAvoidanceNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Obstacle avoidance node interrupted')
    finally:
        # Stop the robot before shutting down
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        node.cmd_publisher.publish(cmd)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.9 Humanoid Robot Example: Sensors, Joints, and ROS Interfaces

### Humanoid Robot Architecture

```
                    ┌─────────────────┐
                    │   ROS Control   │
                    │   Interface     │
                    └─────────┬───────┘
                              │
    ┌─────────────────────────┼─────────────────────────┐
    │                         │                         │
┌───▼───┐               ┌─────▼─────┐             ┌─────▼─────┐
│ Sensors│               │   Joints  │             │  Control  │
│       │               │           │             │   Logic   │
│ • IMU │               │ • Neck    │             │ • Balance │
│ • LIDAR│              │ • Arms    │             │ • Walk    │
│ • Camera│             │ • Legs    │             │ • Gesture │
│ • Force│              │ • Grippers│             │ • Safety  │
└───────┘               └───────────┘             └─────────┘
```

### Humanoid Robot Control Node

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Float64MultiArray
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import math

class HumanoidRobotController(Node):
    def __init__(self):
        super().__init__('humanoid_controller')

        # Parameters
        self.declare_parameter('control_frequency', 100)
        self.declare_parameter('balance_threshold', 0.1)

        self.control_frequency = self.get_parameter('control_frequency').value
        self.balance_threshold = self.get_parameter('balance_threshold').value

        # Subscribers for sensor data
        self.imu_subscriber = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
            10
        )

        self.joint_state_subscriber = self.create_subscription(
            JointState,
            'joint_states',
            self.joint_state_callback,
            10
        )

        # Publishers for control commands
        self.joint_command_publisher = self.create_publisher(
            JointTrajectory,
            'joint_trajectory',
            10
        )

        self.com_velocity_publisher = self.create_publisher(
            Twist,
            'com_velocity',
            10
        )

        # Timer for control loop
        self.control_timer = self.create_timer(
            1.0 / self.control_frequency,
            self.control_loop
        )

        # Internal state
        self.imu_data = None
        self.joint_positions = {}
        self.joint_velocities = {}

        self.get_logger().info('Humanoid robot controller initialized')

    def imu_callback(self, msg):
        """Process IMU data for balance control"""
        self.imu_data = {
            'orientation': msg.orientation,
            'angular_velocity': msg.angular_velocity,
            'linear_acceleration': msg.linear_acceleration
        }

        # Check balance
        roll, pitch, yaw = self.quaternion_to_euler(
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        )

        if abs(pitch) > self.balance_threshold:
            self.get_logger().warn(f'Balance threshold exceeded: pitch = {pitch:.3f}')

    def joint_state_callback(self, msg):
        """Update joint state information"""
        for i, name in enumerate(msg.name):
            if i < len(msg.position):
                self.joint_positions[name] = msg.position[i]
            if i < len(msg.velocity):
                self.joint_velocities[name] = msg.velocity[i]

    def control_loop(self):
        """Main control loop for humanoid robot"""
        if self.imu_data is None:
            return

        # Generate joint trajectory for walking
        trajectory = self.generate_walk_trajectory()
        self.joint_command_publisher.publish(trajectory)

        # Publish center of mass velocity
        com_vel = Twist()
        com_vel.linear = Vector3(x=0.1, y=0.0, z=0.0)  # Walking forward
        com_vel.angular = Vector3(x=0.0, y=0.0, z=0.0)  # No rotation
        self.com_velocity_publisher.publish(com_vel)

    def generate_walk_trajectory(self):
        """Generate walking trajectory for humanoid robot"""
        trajectory = JointTrajectory()
        trajectory.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint'
        ]

        point = JointTrajectoryPoint()

        # Simple walking pattern - in a real system this would be more complex
        time_from_start = self.get_clock().now().nanoseconds / 1e9

        # Generate walking motion for each joint
        for i, joint_name in enumerate(trajectory.joint_names):
            # Oscillating motion for walking
            amplitude = 0.1 if 'hip' in joint_name else 0.05
            frequency = 0.5
            phase = i * math.pi / 3  # Phase offset for coordination

            position = amplitude * math.sin(2 * math.pi * frequency * time_from_start + phase)
            point.positions.append(position)
            point.velocities.append(0.0)  # Velocity control
            point.accelerations.append(0.0)  # Acceleration control

        point.time_from_start.sec = 0
        point.time_from_start.nanosec = int(1e9 / self.control_frequency)  # 10ms

        trajectory.points.append(point)
        return trajectory

    def quaternion_to_euler(self, x, y, z, w):
        """Convert quaternion to Euler angles"""
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)  # Use 90 degrees if out of range
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidRobotController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Humanoid controller interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.10 Complete Running Example: Publisher + Subscriber + Service

### Project Structure

```
humanoid_robot_project/
├── CMakeLists.txt
├── package.xml
├── setup.py
├── setup.cfg
├── resource/humanoid_robot_project
├── humanoid_robot_project/
│   ├── __init__.py
│   ├── publisher_node.py
│   ├── subscriber_node.py
│   ├── service_node.py
│   └── robot_controller.py
└── launch/
    └── complete_system.launch.py
```

### Publisher Node (sensor_simulator.py)

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String
import random
import math

class SensorSimulatorNode(Node):
    def __init__(self):
        super().__init__('sensor_simulator')

        # Publishers
        self.scan_publisher = self.create_publisher(LaserScan, 'scan', 10)
        self.status_publisher = self.create_publisher(String, 'robot_status', 10)

        # Timer for sensor simulation
        self.timer = self.create_timer(0.1, self.publish_sensor_data)

        self.get_logger().info('Sensor simulator node started')

    def publish_sensor_data(self):
        """Simulate sensor data publishing"""
        # Create laser scan message
        scan_msg = LaserScan()
        scan_msg.header.stamp = self.get_clock().now().to_msg()
        scan_msg.header.frame_id = 'laser_frame'

        # Laser scan parameters
        scan_msg.angle_min = -math.pi / 2  # -90 degrees
        scan_msg.angle_max = math.pi / 2   # 90 degrees
        scan_msg.angle_increment = math.pi / 180  # 1 degree
        scan_msg.time_increment = 0.0
        scan_msg.scan_time = 0.1
        scan_msg.range_min = 0.1
        scan_msg.range_max = 10.0

        # Generate simulated ranges (with some obstacles)
        num_scans = int((scan_msg.angle_max - scan_msg.angle_min) / scan_msg.angle_increment) + 1
        ranges = []

        for i in range(num_scans):
            angle = scan_msg.angle_min + i * scan_msg.angle_increment

            # Simulate different distances based on angle (creating "walls")
            if -0.5 < angle < 0.5:  # Front of robot
                distance = 2.0 + random.uniform(-0.2, 0.2)  # Clear path
            elif angle < -0.5:  # Left side
                distance = 1.5 + random.uniform(-0.1, 0.1)  # Wall on left
            else:  # Right side
                distance = 3.0 + random.uniform(-0.3, 0.3)  # Wall on right

            ranges.append(distance)

        scan_msg.ranges = ranges
        scan_msg.intensities = [1.0] * len(ranges)  # All intensities the same

        # Publish scan data
        self.scan_publisher.publish(scan_msg)

        # Publish status
        status_msg = String()
        status_msg.data = f'Simulating sensor data - Min distance: {min(ranges):.2f}m'
        self.status_publisher.publish(status_msg)

def main(args=None):
    rclpy.init(args=args)
    node = SensorSimulatorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sensor simulator interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Node (data_processor.py)

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from std_msgs.msg import String, Float32
import numpy as np

class DataProcessorNode(Node):
    def __init__(self):
        super().__init__('data_processor')

        # Subscribers
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            'scan',
            self.scan_callback,
            10
        )

        self.status_subscriber = self.create_subscription(
            String,
            'robot_status',
            self.status_callback,
            10
        )

        # Publishers
        self.obstacle_publisher = self.create_publisher(Float32, 'obstacle_distance', 10)
        self.analysis_publisher = self.create_publisher(String, 'data_analysis', 10)

        self.get_logger().info('Data processor node started')

    def scan_callback(self, msg):
        """Process laser scan data"""
        # Filter valid ranges
        valid_ranges = [r for r in msg.ranges if 0 < r < msg.range_max]

        if valid_ranges:
            min_distance = min(valid_ranges)
            max_distance = max(valid_ranges)
            avg_distance = sum(valid_ranges) / len(valid_ranges)

            # Publish obstacle distance
            obstacle_msg = Float32()
            obstacle_msg.data = min_distance
            self.obstacle_publisher.publish(obstacle_msg)

            # Analyze data and publish analysis
            analysis_msg = String()
            analysis_msg.data = (
                f'Scan Analysis - Min: {min_distance:.2f}m, '
                f'Max: {max_distance:.2f}m, '
                f'Avg: {avg_distance:.2f}m, '
                f'Points: {len(valid_ranges)}'
            )
            self.analysis_publisher.publish(analysis_msg)

            self.get_logger().info(f'Processed scan: {analysis_msg.data}')

    def status_callback(self, msg):
        """Process status messages"""
        self.get_logger().info(f'Status: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = DataProcessorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Data processor interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Node (robot_control_service.py)

```python
from example_interfaces.srv import Trigger, SetBool
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class RobotControlService(Node):
    def __init__(self):
        super().__init__('robot_control_service')

        # Services
        self.emergency_stop_service = self.create_service(
            Trigger,
            'emergency_stop',
            self.emergency_stop_callback
        )

        self.navigation_control_service = self.create_service(
            SetBool,
            'navigation_control',
            self.navigation_control_callback
        )

        # Publisher for status updates
        self.status_publisher = self.create_publisher(String, 'service_status', 10)

        # Internal state
        self.navigation_enabled = True

        self.get_logger().info('Robot control service started')

    def emergency_stop_callback(self, request, response):
        """Handle emergency stop request"""
        self.get_logger().warn('EMERGENCY STOP REQUESTED!')

        # In a real system, this would send stop commands to all actuators
        response.success = True
        response.message = 'Emergency stop executed'

        # Publish status
        status_msg = String()
        status_msg.data = 'EMERGENCY STOP: All systems halted'
        self.status_publisher.publish(status_msg)

        return response

    def navigation_control_callback(self, request, response):
        """Handle navigation enable/disable request"""
        self.navigation_enabled = request.data

        if self.navigation_enabled:
            response.success = True
            response.message = 'Navigation enabled'
            status_msg = String()
            status_msg.data = 'Navigation: ENABLED'
        else:
            response.success = True
            response.message = 'Navigation disabled'
            status_msg = String()
            status_msg.data = 'Navigation: DISABLED'

        self.status_publisher.publish(status_msg)
        self.get_logger().info(f'Navigation control: {request.data}')

        return response

def main(args=None):
    rclpy.init(args=args)
    service_node = RobotControlService()

    try:
        rclpy.spin(service_node)
    except KeyboardInterrupt:
        service_node.get_logger().info('Service node interrupted')
    finally:
        service_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Launch File (complete_system.launch.py)

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    # Declare launch arguments
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation time'
    )

    # Sensor simulator node
    sensor_simulator = Node(
        package='humanoid_robot_project',
        executable='sensor_simulator',
        name='sensor_simulator',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ]
    )

    # Data processor node
    data_processor = Node(
        package='humanoid_robot_project',
        executable='data_processor',
        name='data_processor',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ]
    )

    # Robot control service
    robot_control_service = Node(
        package='humanoid_robot_project',
        executable='robot_control_service',
        name='robot_control_service',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ]
    )

    return LaunchDescription([
        use_sim_time,
        sensor_simulator,
        data_processor,
        robot_control_service
    ])
```

## 1.11 Best Practices, Common Errors, and Debugging

### Best Practices

#### 1. Node Design Principles
- **Single Responsibility**: Each node should have one primary function
- **Modularity**: Design nodes to be reusable and independent
- **Error Handling**: Implement comprehensive error handling
- **Resource Management**: Properly clean up resources in `destroy_node()`

#### 2. Communication Best Practices
- **Appropriate QoS**: Choose QoS settings based on data criticality
- **Topic Naming**: Use descriptive, consistent topic names
- **Message Design**: Keep messages simple and well-documented
- **Rate Limiting**: Don't publish at unnecessarily high rates

#### 3. Parameter Management
- **Validation**: Always validate parameter values
- **Documentation**: Document all parameters with defaults
- **Type Safety**: Use appropriate parameter types
- **Dynamic Reconfiguration**: Support runtime parameter changes

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Node not found | Package not built/installed | Run `colcon build` and source setup.bash |
| Topic not connected | Publisher/subscriber mismatch | Check topic names and message types |
| Service timeout | Service not available | Verify service is running and name is correct |
| Parameter not found | Parameter not declared | Declare parameter before accessing |
| Memory leak | Not destroying nodes properly | Always call `destroy_node()` |
| Thread safety | Shared data without synchronization | Use locks for shared data access |

### Debugging Techniques

#### 1. Logging and Monitoring
```python
# Use different log levels appropriately
self.get_logger().debug('Detailed debug information')
self.get_logger().info('General information')
self.get_logger().warn('Warning message')
self.get_logger().error('Error occurred')
self.get_logger().fatal('Fatal error')
```

#### 2. Command Line Debugging Tools
```bash
# Check available topics
ros2 topic list

# Echo topic data
ros2 topic echo /topic_name

# Check node status
ros2 node list
ros2 node info node_name

# Call services
ros2 service call /service_name service_type "{request: data}"

# List parameters
ros2 param list
ros2 param get node_name param_name
```

#### 3. Debugging Node Example
```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DebuggingNode(Node):
    def __init__(self):
        super().__init__('debugging_node')

        # Enable debug logging
        self.get_logger().set_level(10)  # DEBUG level

        self.publisher = self.create_publisher(String, 'debug_topic', 10)
        self.subscription = self.create_subscription(
            String, 'input_topic', self.debug_callback, 10
        )

        self.get_logger().debug('Debugging node initialized')

    def debug_callback(self, msg):
        """Debug callback with detailed logging"""
        self.get_logger().debug(f'Received message: {msg.data}')

        # Process message
        processed_msg = String()
        processed_msg.data = f'Processed: {msg.data}'

        self.get_logger().debug(f'Publishing: {processed_msg.data}')
        self.publisher.publish(processed_msg)

def main(args=None):
    rclpy.init(args=args)
    node = DebuggingNode()

    try:
        rclpy.spin(node)
    except Exception as e:
        node.get_logger().fatal(f'Fatal error: {e}')
        raise
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 1.12 Chapter Summary

This chapter has provided a comprehensive introduction to ROS 2 fundamentals, covering the essential components that form the foundation of any ROS 2-based robot system:

1. **Architecture**: Understanding the distributed nature of ROS 2 built on DDS middleware
2. **Nodes**: Creating and managing the fundamental execution units
3. **Topics**: Implementing publish-subscribe communication patterns
4. **Services**: Using request-response communication for synchronous operations
5. **Parameters**: Configuring nodes at runtime without recompilation
6. **URDF**: Modeling robot kinematics and physical properties
7. **rclpy Integration**: Connecting Python applications with ROS 2
8. **Real-World Applications**: Building complete robot systems
9. **Humanoid Robotics**: Special considerations for humanoid robot development
10. **Complete Examples**: Running systems with multiple integrated components

The concepts learned in this chapter form the building blocks for more advanced ROS 2 development, including actions, launch files, testing, and deployment strategies covered in subsequent chapters.

## 1.13 Exercises

### Exercise 1: Basic Node Creation (Beginner)
Create a ROS 2 node that publishes the current time in seconds since epoch to a topic called "current_time". The node should publish a message every 0.5 seconds.

### Exercise 2: Topic Communication (Beginner)
Create a publisher that sends random numbers between 0 and 100 to a topic, and a subscriber that receives these numbers and prints whether they are even or odd.

### Exercise 3: Service Implementation (Intermediate)
Implement a service that takes two integers as input and returns their greatest common divisor. Create both the service server and a client that tests the service with various inputs.

### Exercise 4: Parameter Validation (Intermediate)
Create a node that declares parameters for robot dimensions (width, length, height) and includes validation to ensure all values are positive. Add a parameter callback to validate changes at runtime.

### Exercise 5: URDF Modeling (Intermediate)
Create a URDF file for a simple robot with a base, two wheels, and a camera. Include visual and collision properties for each link, as well as appropriate joints connecting the components.

### Exercise 6: Multi-Node Communication (Advanced)
Design a system with three nodes: a sensor node that publishes random sensor data, a processing node that analyzes the data and determines if it's within normal ranges, and an alert node that publishes warnings when anomalies are detected.

### Exercise 7: Quality of Service (Advanced)
Implement a publisher-subscriber pair where the publisher sends critical control commands with high QoS reliability and durability settings, and another publisher-subscriber pair for sensor data with best-effort QoS settings.

### Exercise 8: Humanoid Robot Joints (Advanced)
Create a URDF model for a simplified humanoid robot with at least 12 joints (head, arms, legs), and implement a node that simulates joint position commands using JointState messages.

## 1.14 Mini-Projects

### Mini-Project 1: Robot Patrol System (Medium Difficulty)
Design and implement a complete robot patrol system that:
- Uses laser scan data to detect obstacles
- Plans a patrol route around obstacles
- Publishes robot status and location
- Implements emergency stop functionality
- Uses parameters to configure patrol behavior
- Includes a launch file to start all nodes

### Mini-Project 2: Humanoid Robot Arm Controller (Hard Difficulty)
Create a comprehensive humanoid robot arm control system that:
- Models a 6-DOF arm in URDF with proper kinematic chains
- Implements inverse kinematics for end-effector positioning
- Creates a control node that accepts Cartesian position goals
- Publishes joint trajectories to move the arm
- Includes safety limits and collision avoidance
- Provides both position and velocity control interfaces
- Implements a complete launch system with visualization

### Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Basic Node Creation</summary>

```python
# time_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import time

class TimePublisherNode(Node):
    def __init__(self):
        super().__init__('time_publisher')
        self.publisher = self.create_publisher(Float64, 'current_time', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = Float64()
        msg.data = time.time()  # Current time in seconds since epoch
        self.publisher.publish(msg)
        self.get_logger().info(f'Published time: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = TimePublisherNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Topic Communication</summary>

```python
# random_number_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import random

class RandomNumberPublisher(Node):
    def __init__(self):
        super().__init__('random_number_publisher')
        self.publisher = self.create_publisher(Int32, 'random_numbers', 10)
        self.timer = self.create_timer(1.0, self.publish_random_number)

    def publish_random_number(self):
        msg = Int32()
        msg.data = random.randint(0, 100)
        self.publisher.publish(msg)
        self.get_logger().info(f'Published random number: {msg.data}')

# even_odd_subscriber.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenOddSubscriber(Node):
    def __init__(self):
        super().__init__('even_odd_subscriber')
        self.subscription = self.create_subscription(
            Int32,
            'random_numbers',
            self.listener_callback,
            10)
        self.subscription  # Prevent unused variable warning

    def listener_callback(self, msg):
        number = msg.data
        if number % 2 == 0:
            self.get_logger().info(f'{number} is EVEN')
        else:
            self.get_logger().info(f'{number} is ODD')

def main(args=None):
    rclpy.init(args=args)

    publisher_node = RandomNumberPublisher()
    subscriber_node = EvenOddSubscriber()

    executor = rclpy.executors.MultiThreadedExecutor()
    executor.add_node(publisher_node)
    executor.add_node(subscriber_node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        publisher_node.get_logger().info('Nodes stopped by user')
    finally:
        publisher_node.destroy_node()
        subscriber_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Service Implementation</summary>

```python
# greatest_common_divisor.srv
int64 a
int64 b
---
int64 result
```

```python
# gcd_service_server.py
import rclpy
from rclpy.node import Node
from your_interfaces.srv import GreatestCommonDivisor  # You'll need to create this service

def gcd(a, b):
    """Calculate greatest common divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return abs(a)

class GCDServiceserver(Node):
    def __init__(self):
        super().__init__('gcd_service_server')
        self.srv = self.create_service(
            GreatestCommonDivisor,
            'calculate_gcd',
            self.gcd_callback)

    def gcd_callback(self, request, response):
        result = gcd(request.a, request.b)
        response.result = result
        self.get_logger().info(f'GCD of {request.a} and {request.b} is {result}')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = GCDServiceserver()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Service server stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```python
# gcd_service_client.py
import rclpy
from rclpy.node import Node
from your_interfaces.srv import GreatestCommonDivisor

class GCDClientNode(Node):
    def __init__(self):
        super().__init__('gcd_client_node')
        self.client = self.create_client(GreatestCommonDivisor, 'calculate_gcd')

        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for GCD service...')

    def send_request(self, a, b):
        request = GreatestCommonDivisor.Request()
        request.a = a
        request.b = b

        future = self.client.call_async(request)
        return future

def main(args=None):
    rclpy.init(args=args)
    client_node = GCDClientNode()

    # Test with various inputs
    test_cases = [(48, 18), (100, 25), (17, 13), (1000, 350)]

    for a, b in test_cases:
        future = client_node.send_request(a, b)

        # Wait for response
        rclpy.spin_until_future_complete(client_node, future)
        response = future.result()

        if response:
            client_node.get_logger().info(f'GCD({a}, {b}) = {response.result}')
        else:
            client_node.get_logger().error('Failed to get response')

    client_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: Parameter Validation</summary>

```python
# parameter_validation_node.py
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor, ParameterType
from rcl_interfaces.srv import SetParameters

class ParameterValidationNode(Node):
    def __init__(self):
        super().__init__('parameter_validation_node')

        # Declare parameters with validation
        self.declare_parameter('robot_width', 1.0,
                              ParameterDescriptor(type=ParameterType.PARAMETER_DOUBLE,
                                                description='Width of the robot (must be positive)'))
        self.declare_parameter('robot_length', 1.0,
                              ParameterDescriptor(type=ParameterType.PARAMETER_DOUBLE,
                                                description='Length of the robot (must be positive)'))
        self.declare_parameter('robot_height', 1.0,
                              ParameterDescriptor(type=ParameterType.PARAMETER_DOUBLE,
                                                description='Height of the robot (must be positive)'))

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.parameter_callback)

        # Get initial values
        self.width = self.get_parameter('robot_width').value
        self.length = self.get_parameter('robot_length').value
        self.height = self.get_parameter('robot_height').value

        self.get_logger().info(f'Initial robot dimensions: {self.width} x {self.length} x {self.height}')

    def parameter_callback(self, params):
        """Validate that all dimension parameters are positive"""
        from rcl_interfaces.msg import SetParametersResult

        result = SetParametersResult()
        result.successful = True

        for param in params:
            if param.name in ['robot_width', 'robot_length', 'robot_height']:
                if param.type_ != ParameterType.PARAMETER_DOUBLE:
                    result.successful = False
                    result.reason = f'Parameter {param.name} must be a double'
                    return result

                if param.value <= 0:
                    result.successful = False
                    result.reason = f'Parameter {param.name} must be positive, got {param.value}'
                    return result

        return result

def main(args=None):
    rclpy.init(args=args)
    node = ParameterValidationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Parameter validation node stopped by user')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: URDF Modeling</summary>

```xml
<?xml version="1.0"?>
<robot name="simple_robot">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
      <material name="blue">
        <color rgba="0 0 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.3 0.2"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.5" ixy="0.0" ixz="0.0" iyy="0.8" iyz="0.0" izz="1.0"/>
    </inertial>
  </link>

  <!-- Left wheel -->
  <joint name="left_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="left_wheel"/>
    <origin xyz="0.2 -0.15 -0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <link name="left_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Right wheel -->
  <joint name="right_wheel_joint" type="continuous">
    <parent link="base_link"/>
    <child link="right_wheel"/>
    <origin xyz="0.2 0.15 -0.1" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
  </joint>

  <link name="right_wheel">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
      <material name="black">
        <color rgba="0 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.005"/>
    </inertial>
  </link>

  <!-- Camera -->
  <joint name="camera_joint" type="fixed">
    <parent link="base_link"/>
    <child link="camera_link"/>
    <origin xyz="0.25 0 0.1" rpy="0 0 0"/>
  </joint>

  <link name="camera_link">
    <visual>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <box size="0.05 0.05 0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="0.1"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.0001" ixy="0.0" ixz="0.0" iyy="0.0001" iyz="0.0" izz="0.0001"/>
    </inertial>
  </link>

  <!-- Gazebo plugin for the camera -->
  <gazebo reference="camera_link">
    <sensor type="camera" name="camera_sensor">
      <pose>0 0 0 0 0 0</pose>
      <visualize>true</visualize>
      <update_rate>30</update_rate>
      <camera name="head">
        <horizontal_fov>1.3962634</horizontal_fov>
        <image>
          <width>640</width>
          <height>480</height>
          <format>R8G8B8</format>
        </image>
        <clip>
          <near>0.01</near>
          <far>100</far>
        </clip>
      </camera>
      <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
        <ros>
          <remapping>~/image_raw:=camera/image_raw</remapping>
          <remapping>~/camera_info:=camera/camera_info</remapping>
        </ros>
      </plugin>
    </sensor>
  </gazebo>
</robot>
```

</details>

These exercises and mini-projects progressively build complexity and integrate multiple ROS 2 concepts, providing hands-on experience with the fundamental building blocks of robot systems.