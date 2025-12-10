---
title: "Module 1.5 - Chapter 5: Advanced rclpy"
sidebar_position: 5
---

# Module 1.5 - Chapter 5: Advanced rclpy

## 5.0 Introduction to Advanced rclpy Concepts

### What is Advanced rclpy?

Advanced rclpy encompasses the sophisticated features and patterns that enable developers to create complex, robust, and efficient ROS 2 nodes. While basic rclpy covers simple node creation and communication, advanced rclpy focuses on complex node architectures, advanced execution patterns, and sophisticated parameter management that are essential for building production-ready robotic applications.

```
Advanced rclpy Features Overview
┌─────────────────────────────────────────┐
│            Advanced rclpy               │
│  ┌─────────────────────────────────┐    │
│  │         Execution               │    │
│  │  ┌─────────┐ ┌─────────┐      │    │
│  │  │ Timers  │ │Executors│      │    │
│  │  │         │ │         │      │    │
│  │  │Callbacks│ │Groups   │      │    │
│  │  └─────────┘ └─────────┘      │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │        Parameters               │    │
│  │  ┌─────────┐ ┌─────────┐       │    │
│  │  │ Declare │ │ Dynamic │       │    │
│  │  │         │ │         │       │    │
│  │  │YAML Load│ │Updates  │       │    │
│  │  └─────────┘ └─────────┘       │    │
│  └─────────────────────────────────┘    │
│  ┌─────────────────────────────────┐    │
│  │        Error Handling           │    │
│  │  ┌─────────┐ ┌─────────┐       │    │
│  │  │Logging  │ │Recovery │       │    │
│  │  │         │ │         │       │    │
│  │  │QoS Tuning││Lifecycle│       │    │
│  │  └─────────┘ └─────────┘       │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

Advanced rclpy concepts are used by various ROS 2 tools and applications including:
- **Robot controllers**: For precise timing and coordination
- **Sensor fusion**: For handling multiple data streams
- **Motion planning**: For dynamic parameter adjustment
- **Simulation**: For realistic behavior modeling

### Advanced rclpy vs. Basic rclpy

| Feature | Basic rclpy | Advanced rclpy |
|---------|-------------|----------------|
| Node architecture | Simple nodes | Complex lifecycle management |
| Execution | Single-threaded | Multi-threaded executors |
| Callbacks | Basic subscriptions | Callback groups, reentrancy |
| Parameters | Static declaration | Dynamic updates, validation |
| Error handling | Basic try/catch | Recovery patterns, graceful degradation |

:::note
Advanced rclpy concepts are essential for building production-ready robotic applications that require high performance, reliability, and maintainability.
:::

## 5.1 Node Architecture in rclpy

### Understanding Node Architecture

In advanced rclpy applications, understanding node architecture is crucial for creating efficient and maintainable code. A node in ROS 2 is the basic unit of execution that can communicate with other nodes using topics, services, and actions.

### Node Lifecycle Management

Advanced nodes often need to handle different lifecycle states. The lifecycle provides hooks for initialization, configuration, activation, and cleanup.

```python
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle import LifecycleState
from rclpy.lifecycle import TransitionCallbackReturn


class LifecycleAdvancedNode(LifecycleNode):
    def __init__(self):
        super().__init__('lifecycle_advanced_node')
        self.declare_parameter('sensor_enabled', True)

    def on_configure(self, state):
        self.get_logger().info(f'Configuring node from state: {state}')
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, state):
        self.get_logger().info(f'Activating node from state: {state}')
        return TransitionCallbackReturn.SUCCESS

    def on_deactivate(self, state):
        self.get_logger().info(f'Deactivating node from state: {state}')
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, state):
        self.get_logger().info(f'Cleaning up node from state: {state}')
        return TransitionCallbackReturn.SUCCESS
```

:::tip
Use LifecycleNode when you need fine-grained control over the node's state transitions, especially in safety-critical robotic applications.
:::

## 5.2 Timers and Periodic Execution Patterns

### Basic Timer Implementation

Timers are essential for periodic execution in ROS 2 nodes. They allow you to execute code at regular intervals, which is particularly useful for sensor polling, control loops, and status updates.

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


class TimerNode(Node):
    def __init__(self):
        super().__init__('timer_node')
        self.publisher = self.create_publisher(Float64, 'timer_data', 10)
        self.timer_counter = 0

        # Create a timer that fires every 0.5 seconds (500ms)
        self.timer = self.create_timer(0.5, self.timer_callback)

    def timer_callback(self):
        msg = Float64()
        msg.data = float(self.timer_counter)
        self.publisher.publish(msg)
        self.get_logger().info(f'Timer published: {msg.data}')
        self.timer_counter += 1
```

### Multiple Timers with Different Frequencies

For complex robotic applications, you might need multiple timers running at different frequencies:

```python
class MultiTimerNode(Node):
    def __init__(self):
        super().__init__('multi_timer_node')

        # High frequency timer (100Hz) for control loops
        self.control_timer = self.create_timer(0.01, self.control_callback)

        # Medium frequency timer (10Hz) for status updates
        self.status_timer = self.create_timer(0.1, self.status_callback)

        # Low frequency timer (1Hz) for diagnostics
        self.diag_timer = self.create_timer(1.0, self.diag_callback)

        self.control_counter = 0
        self.status_counter = 0
        self.diag_counter = 0

    def control_callback(self):
        # High-frequency control logic
        self.control_counter += 1
        self.get_logger().debug(f'Control tick: {self.control_counter}')

    def status_callback(self):
        # Medium-frequency status updates
        self.status_counter += 1
        self.get_logger().info(f'Status tick: {self.status_counter}')

    def diag_callback(self):
        # Low-frequency diagnostic checks
        self.diag_counter += 1
        self.get_logger().info(f'Diagnostic tick: {self.diag_counter}')
```

### Timer-Based Sensor Polling

In robotics, timers are commonly used for sensor polling:

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import random


class SensorPollingNode(Node):
    def __init__(self):
        super().__init__('sensor_polling_node')
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)

        # Simulate sensor polling at 50Hz (20ms)
        self.polling_timer = self.create_timer(0.02, self.poll_sensors)

    def poll_sensors(self):
        """Simulate polling joint position sensors"""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = ['joint1', 'joint2', 'joint3']
        msg.position = [random.uniform(-3.14, 3.14) for _ in range(3)]
        msg.velocity = [random.uniform(-1.0, 1.0) for _ in range(3)]
        msg.effort = [random.uniform(-10.0, 10.0) for _ in range(3)]

        self.joint_pub.publish(msg)
```

:::tip
Choose timer frequencies appropriate for your application: high frequency (100Hz+) for control loops, medium frequency (10-50Hz) for sensor data, and low frequency (1-10Hz) for diagnostics and logging.
:::

## 5.3 Callback Types

### Understanding Callback Types

ROS 2 nodes handle different types of callbacks for various communication patterns.

### Subscription Callbacks

Subscription callbacks are triggered when a message is received on a topic:

```python
class SubscriptionNode(Node):
    def __init__(self):
        super().__init__('subscription_node')

        # Create subscription with custom QoS
        self.subscription = self.create_subscription(
            String,
            'chatter',
            self.subscription_callback,
            10  # QoS history depth
        )

        # Subscription with custom QoS profile
        from rclpy.qos import QoSProfile, QoSDurabilityPolicy, QoSHistoryPolicy
        qos_profile = QoSProfile(
            depth=10,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
            history=QoSHistoryPolicy.KEEP_LAST
        )

        self.durable_subscription = self.create_subscription(
            String,
            'durable_chatter',
            self.durable_callback,
            qos_profile
        )

    def subscription_callback(self, msg):
        self.get_logger().info(f'I heard: {msg.data}')

    def durable_callback(self, msg):
        self.get_logger().info(f'Durable message: {msg.data}')
```

### Service Callbacks

Service callbacks handle synchronous request-response communication:

```python
from example_interfaces.srv import AddTwoInts


class ServiceNode(Node):
    def __init__(self):
        super().__init__('service_node')

        # Create service server
        self.service = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Request: {request.a} + {request.b} = {response.sum}')
        return response
```

### Action Callbacks

Actions provide goal-based asynchronous communication with feedback:

```python
from rclpy.action import ActionServer
from rclpy.action import GoalResponse
from rclpy.action import CancelResponse
from example_interfaces.action import Fibonacci


class ActionNode(Node):
    def __init__(self):
        super().__init__('action_node')

        # Create action server
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

    def goal_callback(self, goal_request):
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1]
            )

            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Publishing feedback: {feedback_msg.sequence}')

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        self.get_logger().info(f'Returning result: {result.sequence}')

        return result
```

## 5.4 Multi-threaded vs Single-threaded Executors

### Understanding Executors

ROS 2 provides different executors for handling callbacks. Understanding the differences is crucial for performance optimization.

### Single-threaded Executor

The default executor processes callbacks sequentially in a single thread:

```
Single-threaded Executor Architecture:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Timer A       │    │  Subscription    │    │   Service       │
│   Callback      │    │  Callback        │    │   Callback      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                        │
         └───────────────────────┼────────────────────────┘
                                 │
                    ┌─────────────────┐
                    │  Single Thread  │
                    │   (Sequential   │
                    │   Execution)    │
                    └─────────────────┘
```

```python
import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node


def main():
    rclpy.init()

    node = Node('single_threaded_node')
    executor = SingleThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        rclpy.shutdown()
```

### Multi-threaded Executor

The multi-threaded executor can process callbacks concurrently using multiple threads:

```
Multi-threaded Executor Architecture:
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Timer A       │    │  Subscription    │    │   Service       │
│   Callback      │    │  Callback        │    │   Callback      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                        │
         ▼                       ▼                        ▼
    ┌──────────┐           ┌──────────┐            ┌──────────┐
    │ Thread 1 │           │ Thread 2 │            │ Thread 3 │
    │(Timer A) │           │(Subscr.) │            │(Service) │
    └──────────┘           └──────────┘            └──────────┘
```

```python
import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node


def main():
    rclpy.init()

    node = Node('multi_threaded_node')
    executor = MultiThreadedExecutor(num_threads=4)  # Use 4 threads
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        rclpy.shutdown()
```

## 5.5 Callback Groups

### Understanding Callback Groups

Callback groups allow you to control how callbacks are executed by the executor, providing fine-grained control over concurrency.

### Mutually Exclusive Callback Groups

Callbacks in mutually exclusive groups are executed one at a time, preventing race conditions:

```python
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from rclpy.node import Node


class ExclusiveCallbackNode(Node):
    def __init__(self):
        super().__init__('exclusive_callback_node')

        # Create mutually exclusive callback group
        self.exclusive_group = MutuallyExclusiveCallbackGroup()

        # Create timer in the exclusive group
        self.timer = self.create_timer(
            0.1,
            self.exclusive_timer_callback,
            callback_group=self.exclusive_group
        )

        # Create subscription in the same exclusive group
        self.subscription = self.create_subscription(
            String,
            'exclusive_topic',
            self.exclusive_subscription_callback,
            10,
            callback_group=self.exclusive_group
        )

        # Create another timer in default group (can run concurrently)
        self.normal_timer = self.create_timer(0.2, self.normal_timer_callback)

    def exclusive_timer_callback(self):
        self.get_logger().info('Exclusive timer callback')
        # This will not run concurrently with the subscription callback
        # since they're in the same mutually exclusive group

    def exclusive_subscription_callback(self, msg):
        self.get_logger().info(f'Exclusive subscription: {msg.data}')
        # This will not run concurrently with the timer callback
        # since they're in the same mutually exclusive group

    def normal_timer_callback(self):
        self.get_logger().info('Normal timer callback')
        # This can run concurrently with callbacks in the exclusive group
```

### Reentrant Callback Groups

Callbacks in reentrant groups can be executed concurrently:

```python
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.node import Node


class ReentrantCallbackNode(Node):
    def __init__(self):
        super().__init__('reentrant_callback_node')

        # Create reentrant callback group
        self.reentrant_group = ReentrantCallbackGroup()

        # Create multiple timers in the reentrant group
        self.timer1 = self.create_timer(
            0.1,
            self.reentrant_timer1_callback,
            callback_group=self.reentrant_group
        )

        self.timer2 = self.create_timer(
            0.15,
            self.reentrant_timer2_callback,
            callback_group=self.reentrant_group
        )

        # Create subscription in the same reentrant group
        self.subscription = self.create_subscription(
            String,
            'reentrant_topic',
            self.reentrant_subscription_callback,
            10,
            callback_group=self.reentrant_group
        )

    def reentrant_timer1_callback(self):
        self.get_logger().info('Reentrant timer 1 callback')
        # Can run concurrently with other callbacks in the same group

    def reentrant_timer2_callback(self):
        self.get_logger().info('Reentrant timer 2 callback')
        # Can run concurrently with other callbacks in the same group

    def reentrant_subscription_callback(self, msg):
        self.get_logger().info(f'Reentrant subscription: {msg.data}')
        # Can run concurrently with other callbacks in the same group
```

### Callback Groups Comparison Table

| Callback Group Type | Concurrent Execution | Use Case |
|---------------------|---------------------|----------|
| Mutually Exclusive | No - Sequential only | Protect shared resources, prevent race conditions |
| Reentrant | Yes - Parallel execution | Independent operations, maximum throughput |
| Default (None) | Executor dependent | General purpose, default behavior |

## 5.6 Parameters

### Understanding Parameters

ROS 2 parameters provide a way to configure nodes at runtime without recompiling.

### Declaring and Using Parameters

```python
from rclpy.node import Node
from rclpy.parameter import Parameter


class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values and descriptions
        self.declare_parameter('robot_name', 'robot1')
        self.declare_parameter('control_frequency', 50.0)
        self.declare_parameter('safety_threshold', 0.5)
        self.declare_parameter('motor_limits', [10.0, 15.0, 20.0])

        # Get parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.control_freq = self.get_parameter('control_frequency').value
        self.safety_threshold = self.get_parameter('safety_threshold').value
        self.motor_limits = self.get_parameter('motor_limits').value

        self.get_logger().info(f'Robot name: {self.robot_name}')
        self.get_logger().info(f'Control frequency: {self.control_freq} Hz')

    def update_parameters(self):
        """Update parameters at runtime"""
        new_params = [
            Parameter('control_frequency', Parameter.Type.DOUBLE, 100.0),
            Parameter('safety_threshold', Parameter.Type.DOUBLE, 0.7)
        ]

        for param in new_params:
            self.set_parameters([param])
```

### Parameter Descriptors

Parameters can have descriptors that define constraints and metadata:

```python
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterDescriptor
from rcl_interfaces.msg import FloatingPointRange


class ParameterDescriptorNode(Node):
    def __init__(self):
        super().__init__('parameter_descriptor_node')

        # Create descriptor with constraints
        frequency_descriptor = ParameterDescriptor()
        frequency_descriptor.description = 'Control loop frequency in Hz'
        frequency_descriptor.floating_point_range = [
            FloatingPointRange(from_value=1.0, to_value=1000.0)
        ]
        frequency_descriptor.read_only = False

        # Declare parameter with descriptor
        self.declare_parameter(
            'control_frequency',
            50.0,
            descriptor=frequency_descriptor
        )

        # Get the parameter value
        self.control_frequency = self.get_parameter('control_frequency').value
```

### Dynamic Parameter Updates

Nodes can respond to parameter changes at runtime:

```python
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult


class DynamicParameterNode(Node):
    def __init__(self):
        super().__init__('dynamic_parameter_node')

        # Declare parameters
        self.declare_parameter('kp', 1.0)
        self.declare_parameter('ki', 0.1)
        self.declare_parameter('kd', 0.05)

        # Set callback for parameter changes
        self.add_on_set_parameters_callback(self.parameters_callback)

        # Store current values
        self.kp = self.get_parameter('kp').value
        self.ki = self.get_parameter('ki').value
        self.kd = self.get_parameter('kd').value

    def parameters_callback(self, params):
        """Callback for parameter changes"""
        result = SetParametersResult()
        result.successful = True

        for param in params:
            if param.name == 'kp' and param.type_ == Parameter.Type.DOUBLE:
                if param.value < 0.0 or param.value > 10.0:
                    result.successful = False
                    result.reason = 'kp must be between 0.0 and 10.0'
                    break
                self.kp = param.value
                self.get_logger().info(f'Updated kp to: {self.kp}')

            elif param.name == 'ki' and param.type_ == Parameter.Type.DOUBLE:
                if param.value < 0.0 or param.value > 5.0:
                    result.successful = False
                    result.reason = 'ki must be between 0.0 and 5.0'
                    break
                self.ki = param.value
                self.get_logger().info(f'Updated ki to: {self.ki}')

            elif param.name == 'kd' and param.type_ == Parameter.Type.DOUBLE:
                if param.value < 0.0 or param.value > 2.0:
                    result.successful = False
                    result.reason = 'kd must be between 0.0 and 2.0'
                    break
                self.kd = param.value
                self.get_logger().info(f'Updated kd to: {self.kd}')

        return result
```

## 5.7 YAML-based Parameter Loading

### Understanding YAML Parameter Loading

Parameters can be loaded from YAML files, making it easy to configure nodes for different environments.

### Creating a Parameter YAML File

Create a file named `robot_params.yaml`:

```yaml
robot_controller:
  ros__parameters:
    robot_name: "humanoid_robot"
    control_frequency: 100.0
    safety_threshold: 0.5
    motor_limits:
      - 10.0
      - 15.0
      - 20.0
    pid_gains:
      kp: 2.0
      ki: 0.5
      kd: 0.1
    sensor_config:
      lidar_enabled: true
      camera_enabled: true
      imu_enabled: true
```

### Loading Parameters from YAML

```python
import rclpy
from rclpy.node import Node
import yaml
from ament_index_python.packages import get_package_share_directory
import os


class YAMLParameterNode(Node):
    def __init__(self):
        super().__init__('yaml_parameter_node')

        # Load parameters from YAML file
        config_dir = get_package_share_directory('my_robot_package')
        config_path = os.path.join(config_dir, 'config', 'robot_params.yaml')

        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)

        # Set parameters from YAML
        robot_params = config['robot_controller']['ros__parameters']
        for param_name, param_value in robot_params.items():
            self.declare_parameter(param_name, param_value)

        self.get_logger().info('Parameters loaded from YAML file')
```

### Loading Parameters via Launch Files

Parameters can also be loaded and set through ROS 2 launch files, which is often more convenient for complex deployments:

```python
# launch/robot_params_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments
    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='humanoid_robot',
        description='Name of the robot'
    )

    control_frequency_launch_arg = DeclareLaunchArgument(
        'control_frequency',
        default_value='100.0',
        description='Control loop frequency'
    )

    # Get launch configurations
    robot_name = LaunchConfiguration('robot_name')
    control_frequency = LaunchConfiguration('control_frequency')

    # Create the robot controller node with parameters
    robot_controller_node = Node(
        package='my_robot_package',
        executable='robot_controller',
        name='robot_controller',
        parameters=[
            {
                'robot_name': robot_name,
                'control_frequency': control_frequency,
                'safety_threshold': 0.5,
                'motor_limits': [10.0, 15.0, 20.0],
                'pid_gains': {
                    'kp': 2.0,
                    'ki': 0.5,
                    'kd': 0.1
                }
            }
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_name_launch_arg,
        control_frequency_launch_arg,
        robot_controller_node
    ])
```

You can also load parameters from YAML files directly in launch files:

```python
# launch/robot_with_yaml_params_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    # Get the path to the parameter file
    config = os.path.join(
        get_package_share_directory('my_robot_package'),
        'config',
        'robot_params.yaml'
    )

    # Create the robot controller node with parameters from YAML
    robot_controller_node = Node(
        package='my_robot_package',
        executable='robot_controller',
        name='robot_controller',
        parameters=[config],
        output='screen'
    )

    return LaunchDescription([
        robot_controller_node
    ])
```

And here's an example of how to pass parameters from launch to nodes with command line overrides:

```python
# launch/robot_with_override_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    # Get launch configurations with defaults
    robot_name = LaunchConfiguration('robot_name').perform(context)
    kp = LaunchConfiguration('kp').perform(context)

    controller_node = Node(
        package='my_robot_package',
        executable='robot_controller',
        name='robot_controller',
        parameters=[
            {
                'robot_name': robot_name,
                'balance.kp': float(kp),  # Override specific parameter
                'safety_mode': True
            }
        ],
        output='screen'
    )

    return [controller_node]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'robot_name',
            default_value='default_robot',
            description='Name of the robot'
        ),
        DeclareLaunchArgument(
            'kp',
            default_value='2.0',
            description='Proportional gain for balance controller'
        ),
        OpaqueFunction(function=launch_setup)
    ])
```

## 5.8 Error Handling, Exceptions, and Debugging Tools

### Understanding Error Handling

Proper error handling is essential for robust robotic applications.

### Exception Handling in Callbacks

```python
import traceback
from rclpy.node import Node


class ErrorHandlingNode(Node):
    def __init__(self):
        super().__init__('error_handling_node')

        self.subscription = self.create_subscription(
            String,
            'unsafe_topic',
            self.unsafe_callback,
            10
        )

        self.timer = self.create_timer(1.0, self.safe_timer_callback)

    def unsafe_callback(self, msg):
        """Callback with potential exceptions"""
        try:
            # Process the message
            processed_data = self.process_message(msg.data)
            self.get_logger().info(f'Processed: {processed_data}')
        except ValueError as e:
            self.get_logger().error(f'Value error in callback: {e}')
        except TypeError as e:
            self.get_logger().error(f'Type error in callback: {e}')
        except Exception as e:
            self.get_logger().error(f'Unexpected error in callback: {e}')
            self.get_logger().error(traceback.format_exc())

    def process_message(self, data):
        """Simulate processing that might fail"""
        if not isinstance(data, str):
            raise TypeError('Expected string data')
        if len(data) == 0:
            raise ValueError('Empty string not allowed')
        return data.upper()

    def safe_timer_callback(self):
        """Timer callback with error handling"""
        try:
            result = self.perform_calculation()
            self.get_logger().info(f'Calculation result: {result}')
        except Exception as e:
            self.get_logger().error(f'Timer callback failed: {e}')
            # Continue execution instead of crashing

    def perform_calculation(self):
        """Simulate calculation that might fail"""
        import random
        if random.random() < 0.1:  # 10% chance of failure
            raise RuntimeError('Calculation failed randomly')
        return random.random()
```

### Custom Exception Handling

```python
from rclpy.exceptions import ParameterNotDeclaredException


class CustomErrorHandlingNode(Node):
    def __init__(self):
        super().__init__('custom_error_handling_node')

        # Handle parameter declaration safely
        try:
            self.declare_parameter('critical_param', 1.0)
        except Exception as e:
            self.get_logger().error(f'Failed to declare parameter: {e}')
            # Set a default value
            self.critical_param = 1.0

        self.timer = self.create_timer(0.1, self.check_parameters)

    def check_parameters(self):
        """Check if parameters are available"""
        try:
            param_value = self.get_parameter('critical_param').value
            self.get_logger().debug(f'Critical param: {param_value}')
        except ParameterNotDeclaredException:
            self.get_logger().warn('Parameter not declared, using default')
            # Handle the missing parameter case
```

## 5.9 Logging, QoS Tuning, Lifecycle Considerations

### Advanced Logging

```python
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy


class LoggingNode(Node):
    def __init__(self):
        super().__init__('logging_node')

        # Set up different logging levels
        self.get_logger().set_level(rclpy.logging.LoggingSeverity.INFO)

        # Create publisher with custom QoS
        qos_profile = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE
        )

        self.publisher = self.create_publisher(String, 'log_topic', qos_profile)

        # Log different severity levels
        self.get_logger().debug('Debug message - detailed info')
        self.get_logger().info('Info message - normal operation')
        self.get_logger().warn('Warning message - potential issue')
        self.get_logger().error('Error message - recoverable error')
        self.get_logger().fatal('Fatal message - unrecoverable error')

        self.timer = self.create_timer(1.0, self.periodic_logging)

    def periodic_logging(self):
        """Periodic logging with context"""
        try:
            # Simulate some work
            result = self.do_work()
            self.get_logger().info(f'Work completed successfully: {result}')
        except Exception as e:
            self.get_logger().error(f'Work failed: {str(e)}')
            import traceback
            self.get_logger().error(f'Traceback: {traceback.format_exc()}')

    def do_work(self):
        """Simulate work that might fail"""
        import random
        if random.random() < 0.05:  # 5% chance of failure
            raise RuntimeError('Work failed randomly')
        return f'Result_{random.randint(1, 100)}'
```

### QoS Tuning

Quality of Service (QoS) profiles can be tuned for different use cases:

```python
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSDurabilityPolicy
from rclpy.qos import QoSHistoryPolicy, QoSLivelinessPolicy


class QoSNode(Node):
    def __init__(self):
        super().__init__('qos_node')

        # Different QoS profiles for different data types

        # For sensor data (real-time, may lose some messages)
        sensor_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=5,  # Only keep the last 5 messages
            reliability=QoSReliabilityPolicy.BEST_EFFORT,  # Accept some message loss
            durability=QoSDurabilityPolicy.VOLATILE
        )

        # For critical commands (must be delivered)
        cmd_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,
            reliability=QoSReliabilityPolicy.RELIABLE,  # Ensure delivery
            durability=QoSDurabilityPolicy.VOLATILE
        )

        # For configuration data (transient local)
        config_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,
            reliability=QoSReliabilityPolicy.RELIABLE,
            durability=QoSDurabilityPolicy.TRANSIENT_LOCAL  # Keep until received
        )

        # Create publishers with different QoS
        self.sensor_pub = self.create_publisher(String, 'sensor_data', sensor_qos)
        self.cmd_pub = self.create_publisher(String, 'cmd_vel', cmd_qos)
        self.config_pub = self.create_publisher(String, 'config', config_qos)

        # Start publishing with different QoS profiles
        self.sensor_timer = self.create_timer(0.01, self.publish_sensor_data)  # 100Hz
        self.cmd_timer = self.create_timer(0.1, self.publish_cmd_data)  # 10Hz
        self.config_timer = self.create_timer(1.0, self.publish_config_data)  # 1Hz

    def publish_sensor_data(self):
        msg = String()
        msg.data = f'Sensor data at {self.get_clock().now().nanoseconds}'
        self.sensor_pub.publish(msg)

    def publish_cmd_data(self):
        msg = String()
        msg.data = f'Command at {self.get_clock().now().nanoseconds}'
        self.cmd_pub.publish(msg)

    def publish_config_data(self):
        msg = String()
        msg.data = f'Config at {self.get_clock().now().nanoseconds}'
        self.config_pub.publish(msg)
```

## 5.10 Robotics-Focused Context Examples

### Using Timers for Sensor Polling in Humanoid Robots

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Vector3
import time


class HumanoidSensorNode(Node):
    def __init__(self):
        super().__init__('humanoid_sensor_node')

        # Publishers for different sensor types
        self.joint_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.imu_pub = self.create_publisher(Imu, 'imu_data', 10)

        # Timers for different sensor polling rates
        # Joint state polling at 100Hz (10ms)
        self.joint_timer = self.create_timer(0.01, self.poll_joint_sensors)

        # IMU polling at 200Hz (5ms) for balance control
        self.imu_timer = self.create_timer(0.005, self.poll_imu_sensors)

        # Initialize sensor data
        self.joint_names = [
            'left_hip', 'left_knee', 'left_ankle',
            'right_hip', 'right_knee', 'right_ankle',
            'left_shoulder', 'left_elbow', 'right_shoulder', 'right_elbow'
        ]

        self.get_logger().info('Humanoid sensor node initialized')

    def poll_joint_sensors(self):
        """Poll joint position, velocity, and effort sensors"""
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = self.joint_names

        # Simulate reading from actual hardware
        import random
        msg.position = [random.uniform(-1.57, 1.57) for _ in self.joint_names]
        msg.velocity = [random.uniform(-2.0, 2.0) for _ in self.joint_names]
        msg.effort = [random.uniform(-50.0, 50.0) for _ in self.joint_names]

        self.joint_pub.publish(msg)

    def poll_imu_sensors(self):
        """Poll IMU for balance and orientation"""
        msg = Imu()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        # Simulate IMU readings
        import random
        msg.orientation.x = random.uniform(-0.1, 0.1)
        msg.orientation.y = random.uniform(-0.1, 0.1)
        msg.orientation.z = random.uniform(-0.1, 0.1)
        msg.orientation.w = 1.0  # Normalize

        # Angular velocity (for balance control)
        msg.angular_velocity.x = random.uniform(-0.5, 0.5)
        msg.angular_velocity.y = random.uniform(-0.5, 0.5)
        msg.angular_velocity.z = random.uniform(-0.1, 0.1)

        # Linear acceleration
        msg.linear_acceleration.x = random.uniform(-9.8, 9.8)
        msg.linear_acceleration.y = random.uniform(-9.8, 9.8)
        msg.linear_acceleration.z = random.uniform(8.0, 11.0)  # Gravity + movement

        self.imu_pub.publish(msg)
```

### Using Callback Groups for Humanoid Motor Controllers

```python
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from std_msgs.msg import Float64MultiArray
from control_msgs.msg import JointTrajectoryControllerState


class HumanoidMotorControllerNode(Node):
    def __init__(self):
        super().__init__('humanoid_motor_controller')

        # Create callback groups for different controller types
        self.safety_group = MutuallyExclusiveCallbackGroup()  # Safety checks must be exclusive
        self.motor_group = ReentrantCallbackGroup()  # Motor commands can run in parallel

        # Safety critical subscribers (must be processed exclusively)
        self.safety_sub = self.create_subscription(
            String,
            'safety_status',
            self.safety_callback,
            1,
            callback_group=self.safety_group
        )

        # Motor command subscribers (can be processed in parallel)
        self.left_leg_sub = self.create_subscription(
            Float64MultiArray,
            'left_leg_commands',
            self.left_leg_callback,
            10,
            callback_group=self.motor_group
        )

        self.right_leg_sub = self.create_subscription(
            Float64MultiArray,
            'right_leg_commands',
            self.right_leg_callback,
            10,
            callback_group=self.motor_group
        )

        self.left_arm_sub = self.create_subscription(
            Float64MultiArray,
            'left_arm_commands',
            self.left_arm_callback,
            10,
            callback_group=self.motor_group
        )

        self.right_arm_sub = self.create_subscription(
            Float64MultiArray,
            'right_arm_commands',
            self.right_arm_callback,
            10,
            callback_group=self.motor_group
        )

        # Publishers for motor states
        self.state_pub = self.create_publisher(JointTrajectoryControllerState, 'motor_states', 10)

        # Motor position tracking
        self.motor_positions = {
            'left_leg': [0.0] * 6,
            'right_leg': [0.0] * 6,
            'left_arm': [0.0] * 7,
            'right_arm': [0.0] * 7
        }

    def safety_callback(self, msg):
        """Safety callback - runs exclusively"""
        self.get_logger().info(f'Safety status: {msg.data}')
        # Perform safety checks that must not be interrupted
        if msg.data == 'EMERGENCY_STOP':
            self.emergency_stop()
        elif msg.data == 'SAFE_TO_OPERATE':
            self.resume_operation()

    def left_leg_callback(self, msg):
        """Left leg motor command - can run in parallel"""
        self.motor_positions['left_leg'] = list(msg.data)
        self.get_logger().debug(f'Left leg updated: {msg.data}')

    def right_leg_callback(self, msg):
        """Right leg motor command - can run in parallel"""
        self.motor_positions['right_leg'] = list(msg.data)
        self.get_logger().debug(f'Right leg updated: {msg.data}')

    def left_arm_callback(self, msg):
        """Left arm motor command - can run in parallel"""
        self.motor_positions['left_arm'] = list(msg.data)
        self.get_logger().debug(f'Left arm updated: {msg.data}')

    def right_arm_callback(self, msg):
        """Right arm motor command - can run in parallel"""
        self.motor_positions['right_arm'] = list(msg.data)
        self.get_logger().debug(f'Right arm updated: {msg.data}')

    def emergency_stop(self):
        """Stop all motors immediately"""
        self.get_logger().fatal('EMERGENCY STOP ACTIVATED')
        # Implementation would send stop commands to all motors

    def resume_operation(self):
        """Resume normal operation"""
        self.get_logger().info('Resuming normal operation')
```

### Parameter Tuning for Balance, Gait, and Sensor Calibration

```python
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor, FloatingPointRange
from rcl_interfaces.msg import IntegerRange


class HumanoidParameterNode(Node):
    def __init__(self):
        super().__init__('humanoid_parameters')

        # Balance control parameters
        balance_descriptor = ParameterDescriptor()
        balance_descriptor.description = 'Balance control parameters for humanoid'
        balance_descriptor.floating_point_range = [FloatingPointRange(from_value=0.0, to_value=10.0)]

        self.declare_parameter('balance.kp', 2.5, balance_descriptor)
        self.declare_parameter('balance.ki', 0.1, balance_descriptor)
        self.declare_parameter('balance.kd', 0.5, balance_descriptor)
        self.declare_parameter('balance.max_torque', 50.0, balance_descriptor)

        # Gait parameters
        gait_descriptor = ParameterDescriptor()
        gait_descriptor.description = 'Gait generation parameters'
        gait_descriptor.floating_point_range = [FloatingPointRange(from_value=0.1, to_value=5.0)]

        self.declare_parameter('gait.step_height', 0.1, gait_descriptor)
        self.declare_parameter('gait.step_length', 0.3, gait_descriptor)
        self.declare_parameter('gait.step_duration', 1.0, gait_descriptor)
        self.declare_parameter('gait.swing_speed', 2.0, gait_descriptor)

        # Sensor calibration parameters
        cal_descriptor = ParameterDescriptor()
        cal_descriptor.description = 'Sensor calibration offsets'

        self.declare_parameter('calibration.imu_offset.x', 0.0, cal_descriptor)
        self.declare_parameter('calibration.imu_offset.y', 0.0, cal_descriptor)
        self.declare_parameter('calibration.imu_offset.z', 0.0, cal_descriptor)
        self.declare_parameter('calibration.encoder_offsets', [0.0] * 20, cal_descriptor)

        # Set callback for parameter changes
        self.add_on_set_parameters_callback(self.parameters_callback)

        self.get_logger().info('Humanoid parameters initialized')

    def parameters_callback(self, params):
        """Handle parameter updates with validation"""
        from rcl_interfaces.msg import SetParametersResult

        result = SetParametersResult()
        result.successful = True

        for param in params:
            # Validate balance parameters
            if param.name.startswith('balance.'):
                if param.type_ == Parameter.Type.DOUBLE and (param.value < 0.0 or param.value > 10.0):
                    result.successful = False
                    result.reason = f'Balance parameter {param.name} out of range [0.0, 10.0]'
                    break

            # Validate gait parameters
            elif param.name.startswith('gait.'):
                if param.name.endswith('step_duration') and param.value < 0.1:
                    result.successful = False
                    result.reason = f'Gait parameter {param.name} must be >= 0.1'
                    break
                elif param.name.endswith('step_height') and (param.value < 0.0 or param.value > 0.5):
                    result.successful = False
                    result.reason = f'Gait parameter {param.name} out of range [0.0, 0.5]'
                    break

        return result
```

### Comparison Tables

#### QoS Profiles Comparison Table

| Profile | Reliability | Durability | History | Use Case |
|---------|-------------|------------|---------|----------|
| Sensor Data | BEST_EFFORT | VOLATILE | KEEP_LAST | Real-time sensor streams where some data loss is acceptable |
| Command Data | RELIABLE | VOLATILE | KEEP_LAST | Robot commands where delivery is critical |
| Configuration | RELIABLE | TRANSIENT_LOCAL | KEEP_LAST | Configuration parameters that must be retained |
| Diagnostic | BEST_EFFORT | VOLATILE | KEEP_ALL | Diagnostic data where all information is valuable |

#### Timer vs Async Patterns Comparison Table

| Pattern | Complexity | Concurrency | Error Handling | Use Case |
|---------|------------|-------------|----------------|----------|
| Timer-based | Low | Limited by executor | Sequential in single-threaded | Control loops, sensor polling |
| Async callbacks | High | High (with proper groups) | Concurrent | High-throughput applications |
| Mixed approach | Medium | Balanced | Flexible | Complex robotic systems |

## 5.11 Exercises

1. **Timer Synchronization**: Create a node with three timers running at different frequencies (10Hz, 25Hz, 50Hz) that must coordinate their execution to avoid conflicts when accessing shared resources.

2. **Callback Group Optimization**: Design a sensor fusion node that uses different callback groups to ensure sensor data processing doesn't interfere with safety-critical callbacks.

3. **Parameter Validation**: Implement a parameter validation system that checks for physically impossible values (e.g., negative motor speeds, impossible joint angles) before applying them to a robot.

4. **QoS Selection**: For a humanoid robot performing a balancing task, determine the appropriate QoS settings for IMU data, joint commands, and diagnostic information, explaining your choices.

5. **Multi-threaded Executor Design**: Create a multi-threaded executor configuration for a humanoid robot with 8 different sensor types and 4 actuator groups, ensuring that safety-critical operations are isolated from other processing.

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Timer Synchronization</summary>

```python
# timer_synchronization_example.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import threading
import time

class TimerSynchronizationNode(Node):
    def __init__(self):
        super().__init__('timer_synchronization_node')

        # Publisher for synchronized data
        self.sync_publisher = self.create_publisher(String, 'synchronized_data', 10)

        # Shared resource with lock
        self.shared_resource = {'counter': 0, 'last_updated': 0}
        self.resource_lock = threading.Lock()

        # Create timers with different frequencies
        self.timer_10hz = self.create_timer(0.1, self.timer_10hz_callback)   # 10Hz
        self.timer_25hz = self.create_timer(0.04, self.timer_25hz_callback)  # 25Hz
        self.timer_50hz = self.create_timer(0.02, self.timer_50hz_callback)  # 50Hz

        self.get_logger().info('Timer synchronization node initialized')

    def timer_10hz_callback(self):
        """10Hz timer callback - lowest priority"""
        with self.resource_lock:
            self.shared_resource['counter'] += 1
            self.shared_resource['last_updated'] = time.time()
            self.get_logger().debug(f'10Hz timer updated counter to: {self.shared_resource["counter"]}')

    def timer_25hz_callback(self):
        """25Hz timer callback - medium priority"""
        with self.resource_lock:
            # Perform coordinated update
            current_counter = self.shared_resource['counter']
            self.shared_resource['counter'] = current_counter * 1.1  # Example processing
            self.get_logger().debug(f'25Hz timer processed counter: {self.shared_resource["counter"]}')

    def timer_50hz_callback(self):
        """50Hz timer callback - highest priority"""
        with self.resource_lock:
            # High-frequency update with minimal processing
            self.shared_resource['counter'] += 0.1
            msg = String()
            msg.data = f'Sync data: counter={self.shared_resource["counter"]:.1f}, time={self.shared_resource["last_updated"]:.3f}'
            self.sync_publisher.publish(msg)
            self.get_logger().debug(f'50Hz timer published: {msg.data}')

def main(args=None):
    rclpy.init(args=args)

    node = TimerSynchronizationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Timer synchronization node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Callback Group Optimization</summary>

```python
# sensor_fusion_optimization.py
import rclpy
from rclpy.node import Node
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from sensor_msgs.msg import LaserScan, Imu, JointState
from std_msgs.msg import Bool
from builtin_interfaces.msg import Time

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')

        # Create callback groups
        self.safety_group = MutuallyExclusiveCallbackGroup()  # Safety-critical callbacks
        self.sensor_group = ReentrantCallbackGroup()         # Regular sensor processing
        self.fusion_group = ReentrantCallbackGroup()         # Fusion processing

        # Safety-critical subscriber (runs in exclusive group)
        self.emergency_stop_sub = self.create_subscription(
            Bool,
            'emergency_stop',
            self.emergency_stop_callback,
            1,
            callback_group=self.safety_group
        )

        # Sensor subscribers (run in reentrant group)
        self.laser_sub = self.create_subscription(
            LaserScan,
            'scan',
            self.laser_callback,
            10,
            callback_group=self.sensor_group
        )

        self.imu_sub = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
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

        # Fusion processing timer (runs in fusion group)
        self.fusion_timer = self.create_timer(
            0.02,  # 50Hz fusion
            self.fusion_processing,
            callback_group=self.fusion_group
        )

        # Internal state
        self.latest_laser = None
        self.latest_imu = None
        self.latest_joints = None
        self.emergency_stop_active = False

        self.get_logger().info('Sensor fusion node with optimized callback groups initialized')

    def emergency_stop_callback(self, msg):
        """Safety-critical callback - runs exclusively"""
        self.emergency_stop_active = msg.data
        if self.emergency_stop_active:
            self.get_logger().fatal('EMERGENCY STOP ACTIVATED')
            # Implement emergency stop logic here

    def laser_callback(self, msg):
        """Laser scan processing - can run concurrently with other sensors"""
        self.latest_laser = msg
        self.get_logger().debug(f'Laser data received with {len(msg.ranges)} ranges')

    def imu_callback(self, msg):
        """IMU processing - can run concurrently with other sensors"""
        self.latest_imu = msg
        self.get_logger().debug('IMU data received')

    def joint_state_callback(self, msg):
        """Joint state processing - can run concurrently with other sensors"""
        self.latest_joints = msg
        self.get_logger().debug(f'Joint state received with {len(msg.position)} joints')

    def fusion_processing(self):
        """Fusion processing - can run concurrently but separately from sensors"""
        if not all([self.latest_laser, self.latest_imu, self.latest_joints]):
            return

        # Perform sensor fusion
        # Example: combine laser and IMU data for better localization
        fused_data = self.perform_sensor_fusion(
            self.latest_laser,
            self.latest_imu,
            self.latest_joints
        )

        self.get_logger().info(f'Sensor fusion completed: {len(fused_data)} fused elements')

    def perform_sensor_fusion(self, laser_data, imu_data, joint_data):
        """Perform actual sensor fusion (simplified example)"""
        # In a real system, this would implement sophisticated fusion algorithms
        # For example: Kalman filtering, particle filtering, or neural networks
        return [len(laser_data.ranges), imu_data.orientation.x, len(joint_data.position)]

def main(args=None):
    rclpy.init(args=args)

    node = SensorFusionNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sensor fusion node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Parameter Validation System</summary>

```python
# parameter_validation_system.py
import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import SetParametersResult, ParameterDescriptor, ParameterType
from rcl_interfaces.srv import GetParameters, SetParameters
import math

class ParameterValidationNode(Node):
    def __init__(self):
        super().__init__('parameter_validation_node')

        # Declare parameters with validation
        self.declare_parameter('motor.speed_limit', 1.0,
                              ParameterDescriptor(
                                  type=ParameterType.PARAMETER_DOUBLE,
                                  description='Maximum motor speed (must be positive)',
                                  floating_point_range=[{"from_value": 0.0, "to_value": 10.0, "step": 0.01}]
                              ))

        self.declare_parameter('joints.max_angle', 1.57,
                              ParameterDescriptor(
                                  type=ParameterType.PARAMETER_DOUBLE,
                                  description='Maximum joint angle in radians (must be between 0 and PI)',
                                  floating_point_range=[{"from_value": 0.0, "to_value": math.pi, "step": 0.01}]
                              ))

        self.declare_parameter('safety.timeout', 5.0,
                              ParameterDescriptor(
                                  type=ParameterType.PARAMETER_DOUBLE,
                                  description='Safety timeout in seconds (must be positive)',
                                  floating_point_range=[{"from_value": 0.1, "to_value": 60.0, "step": 0.1}]
                              ))

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.validate_parameters)

        # Get initial parameter values
        self.motor_speed_limit = self.get_parameter('motor.speed_limit').value
        self.joint_max_angle = self.get_parameter('joints.max_angle').value
        self.safety_timeout = self.get_parameter('safety.timeout').value

        self.get_logger().info(f'Parameter validation node initialized with:')
        self.get_logger().info(f'  Motor speed limit: {self.motor_speed_limit}')
        self.get_logger().info(f'  Joint max angle: {self.joint_max_angle}')
        self.get_logger().info(f'  Safety timeout: {self.safety_timeout}')

    def validate_parameters(self, parameters):
        """Validate parameters before they are set"""
        result = SetParametersResult()
        result.successful = True

        for param in parameters:
            if param.name == 'motor.speed_limit':
                if param.value <= 0 or param.value > 10.0:
                    result.successful = False
                    result.reason = f'Motor speed limit must be positive and <= 10.0, got {param.value}'
                    self.get_logger().error(result.reason)
                    return result

            elif param.name == 'joints.max_angle':
                if param.value < 0 or param.value > math.pi:
                    result.successful = False
                    result.reason = f'Joint max angle must be between 0 and PI, got {param.value}'
                    self.get_logger().error(result.reason)
                    return result

            elif param.name == 'safety.timeout':
                if param.value <= 0 or param.value > 60.0:
                    result.successful = False
                    result.reason = f'Safety timeout must be between 0.1 and 60.0, got {param.value}'
                    self.get_logger().error(result.reason)
                    return result

        # Update internal values if validation passes
        for param in parameters:
            if param.name == 'motor.speed_limit':
                self.motor_speed_limit = param.value
            elif param.name == 'joints.max_angle':
                self.joint_max_angle = param.value
            elif param.name == 'safety.timeout':
                self.safety_timeout = param.value

        self.get_logger().info(f'Parameters validated and updated successfully')
        return result

def main(args=None):
    rclpy.init(args=args)

    node = ParameterValidationNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Parameter validation node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: QoS Selection for Balancing Robot</summary>

```python
# qos_balancing_example.py
from rclpy.qos import QoSProfile, QoSHistoryPolicy, QoSReliabilityPolicy, QoSDurabilityPolicy
from rclpy.node import Node
import rclpy

class QoSBalancingNode(Node):
    def __init__(self):
        super().__init__('qos_balancing_node')

        # Define appropriate QoS profiles for balancing task

        # IMU data - critical for balance, needs reliability and minimal latency
        self.imu_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,  # Only keep latest - old IMU data is useless for balance
            reliability=QoSReliabilityPolicy.RELIABLE,  # Must be delivered for safety
            durability=QoSDurabilityPolicy.VOLATILE,
            deadline=(0, 10000000),  # 10ms deadline (100Hz)
            lifespan=(0, 50000000)   # 50ms lifespan
        )

        # Joint commands - safety-critical, must be delivered reliably
        self.joint_cmd_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1,  # Only latest command matters - avoid old commands
            reliability=QoSReliabilityPolicy.RELIABLE,  # Critical for safety
            durability=QoSDurabilityPolicy.VOLATILE,
            deadline=(0, 5000000),   # 5ms deadline (200Hz control)
            lifespan=(0, 10000000)   # 10ms lifespan
        )

        # Diagnostic information - less critical, can tolerate some loss
        self.diag_qos = QoSProfile(
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=10,  # Keep more diagnostic messages for analysis
            reliability=QoSReliabilityPolicy.BEST_EFFORT,  # Diagnostics can be lost occasionally
            durability=QoSDurabilityPolicy.VOLATILE
        )

        # Create publishers with appropriate QoS
        self.imu_sub = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
            self.imu_qos
        )

        self.joint_cmd_pub = self.create_publisher(
            JointTrajectory,
            'joint_trajectory',
            self.joint_cmd_qos
        )

        self.diag_pub = self.create_publisher(
            DiagnosticArray,
            'diagnostics',
            self.diag_qos
        )

        self.get_logger().info('QoS balancing node initialized with appropriate profiles')

    def imu_callback(self, msg):
        """Process IMU data for balance control - must be timely and reliable"""
        # Balance control algorithm using IMU data
        self.process_balance_control(msg)

    def process_balance_control(self, imu_msg):
        """Implement balance control algorithm"""
        # In a real system, this would implement PID controllers or other balancing algorithms
        # based on IMU readings to maintain humanoid robot balance
        pass

def main(args=None):
    rclpy.init(args=args)

    node = QoSBalancingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('QoS balancing node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Multi-threaded Executor Design</summary>

```python
# multitheaded_executor_design.py
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup, ReentrantCallbackGroup
from sensor_msgs.msg import LaserScan, Imu, JointState, CameraInfo
from sensor_msgs.msg import Image, MagneticField, Temperature, FluidPressure
from geometry_msgs.msg import Twist, Vector3
from std_msgs.msg import Float64MultiArray
from control_msgs.msg import JointTrajectoryControllerState

class ExecutorDesignNode(Node):
    def __init__(self):
        super().__init__('executor_design_node')

        # Create callback groups for different priorities
        self.safety_critical_group = MutuallyExclusiveCallbackGroup()
        self.actuator_control_group = MutuallyExclusiveCallbackGroup()
        self.high_freq_sensors_group = ReentrantCallbackGroup()
        self.low_freq_sensors_group = ReentrantCallbackGroup()

        # 8 Sensor Types (example publishers - in real system these would be subscribers)
        self.lidar_pub = self.create_publisher(LaserScan, 'lidar_scan', 10)
        self.imu_pub = self.create_publisher(Imu, 'imu_data', 10)
        self.camera_pub = self.create_publisher(Image, 'camera_image', 10)
        self.joint_states_pub = self.create_publisher(JointState, 'joint_states', 10)
        self.magnetic_field_pub = self.create_publisher(MagneticField, 'magnetic_field', 10)
        self.pressure_pub = self.create_publisher(FluidPressure, 'pressure', 10)
        self.temperature_pub = self.create_publisher(Temperature, 'temperature', 10)
        self.encoders_pub = self.create_publisher(Float64MultiArray, 'encoders', 10)

        # 4 Actuator Groups
        self.arm_controller_pub = self.create_publisher(JointTrajectoryControllerState, 'arm_controller', 10)
        self.leg_controller_pub = self.create_publisher(JointTrajectoryControllerState, 'leg_controller', 10)
        self.head_controller_pub = self.create_publisher(JointTrajectoryControllerState, 'head_controller', 10)
        self.base_controller_pub = self.create_publisher(JointTrajectoryControllerState, 'base_controller', 10)

        # Timers for different sensor/actuator frequencies
        self.lidar_timer = self.create_timer(0.05, self.publish_lidar_data)  # 20Hz
        self.imu_timer = self.create_timer(0.001, self.publish_imu_data)     # 1000Hz (safety critical)
        self.camera_timer = self.create_timer(0.1, self.publish_camera_data)  # 10Hz
        self.joint_timer = self.create_timer(0.01, self.publish_joint_data)   # 100Hz

        # Safety timer (runs in safety group)
        self.safety_timer = self.create_timer(
            0.005,  # 200Hz for safety checks
            self.safety_check,
            callback_group=self.safety_critical_group
        )

        # Actuator control timers (run in actuator group)
        self.arm_control_timer = self.create_timer(
            0.01,  # 100Hz
            self.control_arm_actuators,
            callback_group=self.actuator_control_group
        )
        self.leg_control_timer = self.create_timer(
            0.01,  # 100Hz
            self.control_leg_actuators,
            callback_group=self.actuator_control_group
        )

        self.get_logger().info('Multi-threaded executor design node initialized')

    def publish_lidar_data(self):
        """Publish simulated lidar data"""
        # Simulate lidar publishing
        pass

    def publish_imu_data(self):
        """Publish simulated IMU data - safety critical"""
        # Simulate IMU publishing at high frequency
        pass

    def publish_camera_data(self):
        """Publish simulated camera data"""
        # Simulate camera publishing
        pass

    def publish_joint_data(self):
        """Publish simulated joint state data"""
        # Simulate joint state publishing
        pass

    def safety_check(self):
        """Safety check that runs in exclusive group"""
        # Perform safety checks with high priority
        self.get_logger().debug('Safety check performed')

    def control_arm_actuators(self):
        """Control arm actuators - runs in actuator group"""
        # Control arm actuators
        pass

    def control_leg_actuators(self):
        """Control leg actuators - runs in actuator group"""
        # Control leg actuators
        pass

def main(args=None):
    rclpy.init(args=args)

    # Create node
    node = ExecutorDesignNode()

    # Create multi-threaded executor with appropriate number of threads
    # Using 6 threads: 1 for safety, 1 for actuators, 4 for general processing
    executor = MultiThreadedExecutor(num_threads=6)
    executor.add_node(node)

    try:
        executor.spin()
    except KeyboardInterrupt:
        node.get_logger().info('Multi-threaded executor design node interrupted')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

## 5.12 Mini-Project: Multi-threaded Sensor Node with Dynamic Parameters

Build a multi-threaded sensor node that:

1. Implements at least 3 different sensor types (IMU, joint encoders, force sensors)
2. Uses appropriate callback groups to ensure safety-critical sensors are processed with priority
3. Supports dynamic parameter updates for sensor calibration and filtering
4. Includes proper error handling and logging
5. Uses different QoS profiles appropriate for each sensor type
6. Implements a parameter file loader for different robot configurations

The node should be able to handle sensor failures gracefully and continue operating with reduced functionality.

:::tip
When implementing the multi-threaded sensor node, consider using a ReentrantCallbackGroup for non-critical sensors and a MutuallyExclusiveCallbackGroup for safety-critical sensors like emergency stops or collision detection.
:::

## 5.13 Chapter Summary

This chapter covered advanced rclpy concepts essential for building robust robotic applications:

- **Node Architecture**: Understanding how to structure complex nodes with proper lifecycle management
- **Timers**: Using timers for periodic execution patterns, especially important for control loops and sensor polling
- **Callback Types**: Handling different communication patterns (subscriptions, services, actions) with appropriate error handling
- **Executors**: Choosing between single-threaded and multi-threaded executors based on performance requirements
- **Callback Groups**: Using mutually exclusive and reentrant groups to control concurrency and prevent race conditions
- **Parameters**: Managing runtime configuration with validation and dynamic updates
- **YAML Loading**: Using configuration files for different deployment scenarios
- **Error Handling**: Implementing robust error handling in robotic applications
- **QoS Tuning**: Selecting appropriate Quality of Service profiles for different data types
- **Robotics Context**: Applying these concepts specifically to humanoid robotics applications

These advanced concepts are crucial for developing production-ready robotic applications that are both performant and reliable.