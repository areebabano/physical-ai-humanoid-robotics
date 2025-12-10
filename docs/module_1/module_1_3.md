---
title: "Module 1.3 - Chapter 3: ROS 2 Services and Actions"
sidebar_position: 3
---

# Module 1.3 - Chapter 3: ROS 2 Services and Actions

## 3.0 Introduction to Services and Actions

### Communication Patterns in ROS 2

ROS 2 provides three primary communication patterns for nodes to interact: topics (publish/subscribe), services (request/response), and actions (goal-based communication). While topics enable asynchronous communication for continuous data streams, services and actions provide synchronous and goal-oriented communication respectively for more complex interactions.

```
ROS 2 Communication Patterns
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    Topics       │    │   Services      │    │    Actions      │
│                 │    │                 │    │                 │
│  • Asynchronous │    │  • Synchronous  │    │  • Goal-oriented│
│  • Continuous   │    │  • Request/     │    │  • Feedback     │
│  • Many-to-many │    │    Response     │    │  • Long-running │
│  • Data streams │    │  • One-shot     │    │  • Cancelable   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### When to Use Services vs Actions

| Use Case | Communication Pattern | Reason |
|----------|----------------------|---------|
| Quick computations | Services | Fast, synchronous response |
| Sensor calibration | Services | Simple request-response |
| Long-running navigation | Actions | Need feedback and cancel |
| Robot arm control | Actions | Multi-step with progress |
| Parameter queries | Services | Immediate response needed |
| Complex manipulation | Actions | Goal-based with status |

## 3.1 ROS 2 Services: Request-Response Pattern

### Understanding ROS 2 Services

ROS 2 services implement a request-response communication pattern where a service client sends a request to a service server, which processes the request and returns a response. This pattern is ideal for operations that require a direct response and typically complete quickly.

```
Service Communication Flow
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Service Client  │───►│   Service       │───►│ Service Server  │
│                 │    │   Request       │    │                 │
│  Sends request  │    │   (Request msg) │    │ Processes       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        ▲                       │                       │
        │                       ▼                       │
        │                ┌─────────────────┐            │
        │                │   Service       │            │
        │                │   Response      │            │
        └────────────────│  (Response msg) │◄───────────┘
                         └─────────────────┘
```

### Service Definition (.srv Files)

Service definitions use the `.srv` file format with the request and response separated by `---`:

```xml
# In AddTwoInts.srv
int64 a
int64 b
---
int64 sum
```

The format is:
- Lines before `---` define request fields
- Lines after `---` define response fields

### Python Service Server Implementation

```python
# my_robot_package/calculator_service.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class CalculatorService(Node):
    def __init__(self):
        super().__init__('calculator_service')

        # Create a service server
        self.srv = self.create_service(
            AddTwoInts,
            'add_two_ints',
            self.add_two_ints_callback
        )

        self.get_logger().info('Calculator service ready')

    def add_two_ints_callback(self, request, response):
        """Process the request and set the response"""
        response.sum = request.a + request.b
        self.get_logger().info(f'Request: {request.a} + {request.b} = {response.sum}')
        return response

def main(args=None):
    rclpy.init(args=args)
    calculator_service = CalculatorService()
    rclpy.spin(calculator_service)
    calculator_service.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Python Service Client Implementation

```python
# my_robot_package/calculator_client.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class CalculatorClient(Node):
    def __init__(self):
        super().__init__('calculator_client')

        # Create a service client
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # Wait for service to be available
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        """Send a request to the service"""
        self.req.a = a
        self.req.b = b
        future = self.cli.call_async(self.req)
        return future

def main(args=None):
    rclpy.init(args=args)
    calculator_client = CalculatorClient()

    # Send request
    future = calculator_client.send_request(1, 2)

    # Spin until future is complete
    rclpy.spin_until_future_complete(calculator_client, future)

    response = future.result()
    calculator_client.get_logger().info(f'Result: {response.sum}')

    calculator_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Asynchronous Service Client

For non-blocking service calls, use asynchronous clients:

```python
# my_robot_package/async_calculator_client.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from rclpy.executors import MultiThreadedExecutor

class AsyncCalculatorClient(Node):
    def __init__(self):
        super().__init__('async_calculator_client')

        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # Timer to periodically check for service availability
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.req_count = 0

    def timer_callback(self):
        """Check if service is available and send requests"""
        if self.cli.service_is_ready():
            self.timer.cancel()
            self.send_async_request()

    def send_async_request(self):
        """Send an asynchronous request"""
        if self.req_count < 5:  # Send 5 requests
            request = AddTwoInts.Request()
            request.a = self.req_count
            request.b = self.req_count * 2

            future = self.cli.call_async(request)
            future.add_done_callback(self.response_callback)

            self.req_count += 1
            self.get_logger().info(f'Sent request {self.req_count}: {request.a} + {request.b}')

    def response_callback(self, future):
        """Handle response from service"""
        try:
            response = future.result()
            self.get_logger().info(f'Received response: {response.sum}')
            # Send next request
            self.send_async_request()
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')

def main(args=None):
    rclpy.init(args=args)
    async_client = AsyncCalculatorClient()

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

### C++ Service Server Implementation

```cpp
// src/calculator_service.cpp
#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>

class CalculatorService : public rclcpp::Node
{
public:
    CalculatorService() : Node("calculator_service")
    {
        // Create a service server
        service_ = this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_two_ints",
            std::bind(&CalculatorService::handle_request, this,
                     std::placeholders::_1, std::placeholders::_2));

        RCLCPP_INFO(this->get_logger(), "Calculator service ready");
    }

private:
    void handle_request(
        const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
        std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response)
    {
        response->sum = request->a + request->b;
        RCLCPP_INFO(this->get_logger(),
                   "Request: %ld + %ld = %ld",
                   request->a, request->b, response->sum);
    }

    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CalculatorService>());
    rclcpp::shutdown();
    return 0;
}
```

### Service Error Handling and Timeouts

```python
# my_robot_package/robust_service_client.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from rclpy.qos import QoSProfile
import time

class RobustServiceClient(Node):
    def __init__(self):
        super().__init__('robust_service_client')

        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

        # Set up quality of service profile if needed
        qos_profile = QoSProfile(depth=10)

    def call_service_with_timeout(self, a, b, timeout_sec=5.0):
        """Call service with timeout handling"""
        try:
            # Wait for service with timeout
            if not self.cli.wait_for_service(timeout_sec=timeout_sec):
                self.get_logger().error('Service not available after waiting')
                return None

            # Create and send request
            request = AddTwoInts.Request()
            request.a = a
            request.b = b

            # Call service asynchronously
            future = self.cli.call_async(request)

            # Wait for response with timeout
            start_time = time.time()
            while not future.done():
                if time.time() - start_time > timeout_sec:
                    self.get_logger().error('Service call timed out')
                    return None
                rclpy.spin_once(self, timeout_sec=0.1)

            return future.result()

        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')
            return None

def main(args=None):
    rclpy.init(args=args)
    client = RobustServiceClient()

    # Call service with error handling
    response = client.call_service_with_timeout(10, 20)
    if response:
        client.get_logger().info(f'Result: {response.sum}')
    else:
        client.get_logger().error('Service call failed')

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 3.2 ROS 2 Actions: Goal-Based Communication

### Understanding ROS 2 Actions

Actions are designed for long-running tasks that require feedback, status updates, and the ability to be canceled. They follow a goal-based communication pattern with three main components: goals (what the client wants to achieve), feedback (ongoing status updates), and results (final outcome).

```
Action Communication Flow
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Action Client   │───►│   Action Goal   │───►│ Action Server   │
│                 │    │                 │    │                 │
│ Send goal       │    │ Goal accepted/  │    │ Process goal    │
└─────────────────┘    │ rejected        │    └─────────────────┘
        │               └─────────────────┘            │
        │                      │                       │
        │                      ▼                       │
        │              ┌─────────────────┐             │
        │              │   Action        │             │
        │              │   Feedback      │             │
        │              │  (intermediate   │             │
        │              │   status)       │◄────────────┘
        │              └─────────────────┘
        │                      │
        │                      ▼
        │              ┌─────────────────┐
        │              │   Action        │
        │              │   Result        │
        └─────────────►│  (final result) │
                       └─────────────────┘
```

### Action Definition (.action Files)

Action definitions use the `.action` file format with three sections separated by `---`:

```xml
# In Fibonacci.action
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

The format is:
- Lines before first `---` define goal fields
- Lines between `---` define result fields
- Lines after second `---` define feedback fields

### Python Action Server Implementation

```python
# my_robot_package/fibonacci_action_server.py
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')

        # Create an action server
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info('Fibonacci action server started')

    def goal_callback(self, goal_request):
        """Accept or reject a client request to begin an action"""
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject a client request to cancel an action"""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Execute the goal and provide feedback"""
        self.get_logger().info('Executing goal...')

        # Get the goal order
        order = goal_handle.request.order

        # Create feedback message
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        # Start the Fibonacci sequence
        if order == 0:
            result = Fibonacci.Result()
            result.sequence = [0]
            goal_handle.succeed()
            return result
        elif order == 1:
            result = Fibonacci.Result()
            result.sequence = [0, 1]
            goal_handle.succeed()
            return result

        # Generate the Fibonacci sequence with feedback
        for i in range(1, order):
            # Check if there's a cancel request
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = Fibonacci.Result()
                result.sequence = feedback_msg.partial_sequence
                self.get_logger().info('Goal canceled')
                return result

            # Provide feedback periodically
            if i % 2 == 0:  # Every 2nd iteration
                self.get_logger().info(f'Feedback: {feedback_msg.partial_sequence}')
                goal_handle.publish_feedback(feedback_msg)

            # Calculate next Fibonacci number
            next_num = feedback_msg.partial_sequence[-1] + feedback_msg.partial_sequence[-2]
            feedback_msg.partial_sequence.append(next_num)

        # Set final result
        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        self.get_logger().info(f'Result: {result.sequence}')

        return result

def main(args=None):
    rclpy.init(args=args)
    action_server = FibonacciActionServer()
    rclpy.spin(action_server)
    action_server.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Python Action Client Implementation

```python
# my_robot_package/fibonacci_action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')

        # Create an action client
        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )

    def send_goal(self, order):
        """Send a goal to the action server"""
        # Wait for action server
        self._action_client.wait_for_server()

        # Create goal
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        # Send goal and get future
        self._send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        """Handle goal response"""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """Handle feedback from action server"""
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback.partial_sequence}')

    def get_result_callback(self, future):
        """Handle result from action server"""
        result = future.result().result
        self.get_logger().info(f'Final result: {result.sequence}')

def main(args=None):
    rclpy.init(args=args)
    action_client = FibonacciActionClient()

    # Send a goal
    action_client.send_goal(10)

    rclpy.spin(action_client)
    action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Advanced Action Client with Cancellation

```python
# my_robot_package/advanced_action_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from example_interfaces.action import Fibonacci
import time

class AdvancedActionClient(Node):
    def __init__(self):
        super().__init__('advanced_action_client')

        self._action_client = ActionClient(
            self,
            Fibonacci,
            'fibonacci'
        )
        self.goal_handle = None

    def send_goal_async(self, order):
        """Send goal asynchronously"""
        self._action_client.wait_for_server()

        goal_msg = Fibonacci.Goal()
        goal_msg.order = order

        future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        future.add_done_callback(self.goal_response_callback)
        return future

    def goal_response_callback(self, future):
        """Handle goal response"""
        self.goal_handle = future.result()
        if not self.goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self._get_result_future = self.goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)

    def feedback_callback(self, feedback_msg):
        """Handle feedback"""
        self.get_logger().info(f'Feedback: {feedback_msg.feedback.partial_sequence}')

    def get_result_callback(self, future):
        """Handle result"""
        result = future.result().result
        status = future.result().status
        self.get_logger().info(f'Result: {result.sequence}, Status: {status}')

    def cancel_goal(self):
        """Cancel the current goal"""
        if self.goal_handle is not None:
            future = self.goal_handle.cancel_goal_async()
            future.add_done_callback(self.cancel_response_callback)

    def cancel_response_callback(self, future):
        """Handle cancel response"""
        cancel_response = future.result()
        self.get_logger().info(f'Cancel response: {cancel_response}')

def main(args=None):
    rclpy.init(args=args)
    action_client = AdvancedActionClient()

    # Send a goal
    action_client.send_goal_async(15)

    # Cancel the goal after 2 seconds
    def cancel_after_delay():
        time.sleep(2)
        action_client.get_logger().info('Canceling goal...')
        action_client.cancel_goal()

    import threading
    cancel_thread = threading.Thread(target=cancel_after_delay)
    cancel_thread.start()

    rclpy.spin(action_client)
    action_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### C++ Action Server Implementation

```cpp
// src/fibonacci_action_server.cpp
#include <rclcpp/rclcpp.hpp>
#include <rclcpp_action/rclcpp_action.hpp>
#include <example_interfaces/action/fibonacci.hpp>

class FibonacciActionServer : public rclcpp::Node
{
public:
    using Fibonacci = example_interfaces::action::Fibonacci;
    using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;

    FibonacciActionServer() : Node("fibonacci_action_server")
    {
        using namespace std::placeholders;

        // Create an action server
        this->action_server_ = rclcpp_action::create_server<Fibonacci>(
            this->get_node_base_interface(),
            this->get_node_clock_interface(),
            this->get_node_logging_interface(),
            this->get_node_waitables_interface(),
            "fibonacci",
            std::bind(&FibonacciActionServer::handle_goal, this, _1, _2),
            std::bind(&FibonacciActionServer::handle_cancel, this, _1),
            std::bind(&FibonacciActionServer::handle_accepted, this, _1)
        );

        RCLCPP_INFO(this->get_logger(), "Fibonacci action server started");
    }

private:
    rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;

    rclcpp_action::GoalResponse handle_goal(
        const rclcpp_action::GoalUUID & uuid,
        std::shared_ptr<const Fibonacci::Goal> goal)
    {
        RCLCPP_INFO(this->get_logger(), "Received goal request");
        (void)uuid;
        return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
    }

    rclcpp_action::CancelResponse handle_cancel(
        const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
        RCLCPP_INFO(this->get_logger(), "Received cancel request");
        (void)goal_handle;
        return rclcpp_action::CancelResponse::ACCEPT;
    }

    void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
        using namespace std::placeholders;
        // This needs to return quickly to avoid blocking the executor
        // So spin up a new thread
        std::thread{std::bind(&FibonacciActionServer::execute, this, _1), goal_handle}.detach();
    }

    void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
    {
        RCLCPP_INFO(this->get_logger(), "Executing goal...");

        // Get the goal order
        auto goal = goal_handle->get_goal();
        auto order = goal->order;

        // Create feedback
        auto feedback = std::make_shared<Fibonacci::Feedback>();
        feedback->partial_sequence = {0, 1};

        // Start the Fibonacci sequence
        if (order == 0) {
            auto result = std::make_shared<Fibonacci::Result>();
            result->sequence = {0};
            goal_handle->succeed(result);
            return;
        } else if (order == 1) {
            auto result = std::make_shared<Fibonacci::Result>();
            result->sequence = {0, 1};
            goal_handle->succeed(result);
            return;
        }

        // Generate the Fibonacci sequence with feedback
        for (int i = 1; i < order; ++i) {
            // Check if there's a cancel request
            if (goal_handle->is_canceling()) {
                auto result = std::make_shared<Fibonacci::Result>();
                result->sequence = feedback->partial_sequence;
                goal_handle->canceled(result);
                RCLCPP_INFO(this->get_logger(), "Goal canceled");
                return;
            }

            // Provide feedback periodically
            if (i % 2 == 0) {  // Every 2nd iteration
                RCLCPP_INFO(this->get_logger(), "Publishing feedback");
                goal_handle->publish_feedback(feedback);
            }

            // Calculate next Fibonacci number
            int next_num = feedback->partial_sequence.back() +
                          feedback->partial_sequence[feedback->partial_sequence.size() - 2];
            feedback->partial_sequence.push_back(next_num);
        }

        // Set final result
        goal_handle->succeed(std::make_shared<Fibonacci::Result>());
        goal_handle->get_result()->sequence = feedback->partial_sequence;
        RCLCPP_INFO(this->get_logger(), "Goal succeeded");
    }
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FibonacciActionServer>());
    rclcpp::shutdown();
    return 0;
}
```

## 3.3 Custom Service and Action Definitions

### Creating Custom Services

To create a custom service, define a `.srv` file in the `srv/` directory of your package:

```xml
# srv/CalculateDistance.srv
# Request fields
float64 x1
float64 y1
float64 x2
float64 y2
---
# Response fields
float64 distance
bool success
string message
```

Update your `package.xml` to include message generation:

```xml
<build_depend>message_generation</build_depend>
<exec_depend>message_runtime</exec_depend>
```

For Python packages, update your `setup.py`:

```python
from glob import glob
import os

package_name = 'my_robot_package'

setup(
    # ... other setup parameters ...
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        # Add this line to include service files
        (os.path.join('share', package_name, 'srv'), glob('srv/*.srv')),
    ],
    # ... rest of setup ...
)
```

For C++ packages, update your `CMakeLists.txt`:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "srv/CalculateDistance.srv"
  DEPENDENCIES builtin_interfaces std_msgs
)

ament_export_dependencies(rosidl_default_runtime)
```

### Creating Custom Actions

To create a custom action, define an `.action` file in the `action/` directory of your package:

```xml
# action/MoveArm.action
# Goal: desired joint positions
float64[] joint_positions
float64 timeout
---
# Result: success status
bool success
string message
---
# Feedback: current progress
float64[] current_joint_positions
float64[] joint_velocities
string status
```

Update your `package.xml`:

```xml
<build_depend>action_msgs</build_depend>
<exec_depend>action_msgs</exec_depend>
```

For Python packages, update your `setup.py`:

```python
data_files=[
    # ... other data files ...
    (os.path.join('share', package_name, 'action'), glob('action/*.action')),
],
```

For C++ packages, update your `CMakeLists.txt`:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/MoveArm.action"
  DEPENDENCIES builtin_interfaces std_msgs
)
```

### Using Custom Services and Actions

```python
# Using custom service
from my_robot_package.srv import CalculateDistance

class DistanceCalculator(Node):
    def __init__(self):
        super().__init__('distance_calculator')
        self.srv = self.create_service(
            CalculateDistance,
            'calculate_distance',
            self.distance_callback
        )

    def distance_callback(self, request, response):
        import math
        distance = math.sqrt((request.x2 - request.x1)**2 + (request.y2 - request.y1)**2)
        response.distance = distance
        response.success = True
        response.message = f'Distance calculated: {distance}'
        return response

# Using custom action
from my_robot_package.action import MoveArm

class ArmController(Node):
    def __init__(self):
        super().__init__('arm_controller')
        self._action_server = ActionServer(
            self,
            MoveArm,
            'move_arm',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )
```

## 3.4 Humanoid Robotics Applications

### Navigation Actions for Humanoid Robots

Humanoid robots require sophisticated navigation capabilities that benefit from action-based communication:

```python
# my_humonoid_robot/navigation_action.py
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from nav_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math

class HumanoidNavigationAction(Node):
    def __init__(self):
        super().__init__('humanoid_navigation_action')

        # Create action server
        self._action_server = ActionServer(
            self,
            NavigateToPose,
            'navigate_to_pose',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        # Publishers and subscribers
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, 'scan', self.scan_callback, 10)

        # Internal state
        self.current_scan = None
        self.current_pose = None  # Would come from localization
        self.navigation_active = False

    def goal_callback(self, goal_request):
        """Validate navigation goal"""
        # Check if goal is valid (not in obstacle, reachable, etc.)
        goal_x = goal_request.pose.pose.position.x
        goal_y = goal_request.pose.pose.position.y

        # Simple validation - check if goal is not too close to obstacles
        if self.current_scan and self.is_goal_blocked(goal_x, goal_y):
            self.get_logger().warn('Navigation goal is blocked by obstacles')
            return GoalResponse.REJECT
        else:
            self.get_logger().info(f'Accepting navigation goal: ({goal_x}, {goal_y})')
            return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Handle cancel request"""
        self.get_logger().info('Canceling navigation goal')
        return CancelResponse.ACCEPT

    def scan_callback(self, msg):
        """Update current scan data"""
        self.current_scan = msg

    def is_goal_blocked(self, goal_x, goal_y):
        """Check if path to goal is blocked"""
        if not self.current_scan:
            return False  # No scan data, assume clear

        # Simple check - if goal is within current scan range and has obstacles
        # In real implementation, this would use path planning
        return False

    def execute_callback(self, goal_handle):
        """Execute navigation goal"""
        self.get_logger().info('Starting navigation to goal')
        self.navigation_active = True

        # Get goal position
        goal_pose = goal_handle.request.pose.pose
        target_x = goal_pose.position.x
        target_y = goal_pose.position.y
        target_theta = 2 * math.atan2(goal_pose.orientation.z, goal_pose.orientation.w)

        # Navigation feedback
        feedback_msg = NavigateToPose.Feedback()

        # Simple navigation loop (in real implementation, use path planner)
        while self.navigation_active:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.stop_robot()
                result = NavigateToPose.Result()
                result.result = 0  # Canceled
                return result

            # Calculate distance to goal
            if self.current_pose:  # Would come from localization
                current_x = self.current_pose.position.x
                current_y = self.current_pose.position.y
                distance_to_goal = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)

                # Update feedback
                feedback_msg.current_pose = PoseStamped()  # Would be current pose
                feedback_msg.distance_remaining = distance_to_goal
                goal_handle.publish_feedback(feedback_msg)

                # Check if goal reached
                if distance_to_goal < 0.1:  # 10cm tolerance
                    goal_handle.succeed()
                    self.stop_robot()
                    result = NavigateToPose.Result()
                    result.result = 1  # Succeeded
                    return result

            # Publish velocity command (simplified)
            cmd = Twist()
            # Navigation logic would go here
            self.cmd_vel_pub.publish(cmd)

            # Sleep to control loop rate
            self.get_clock().sleep_for(rclpy.duration.Duration(seconds=0.1))

        # If we exit the loop without succeeding
        self.stop_robot()
        result = NavigateToPose.Result()
        result.result = 0  # Failed
        return result

    def stop_robot(self):
        """Stop robot movement"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidNavigationAction()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Manipulation Actions for Humanoid Arms

Humanoid robots with manipulator arms need complex manipulation actions:

```python
# my_humonoid_robot/manipulation_action.py
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math

class HumanoidManipulationAction(Node):
    def __init__(self):
        super().__init__('humanoid_manipulation_action')

        # Create action server
        self._action_server = ActionServer(
            self,
            FollowJointTrajectory,
            'arm_controller/follow_joint_trajectory',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        # Joint command publisher
        self.joint_cmd_pub = self.create_publisher(
            JointTrajectory,
            'arm_controller/joint_trajectory',
            10
        )

        # Internal state
        self.current_joint_positions = {}
        self.manipulation_active = False

    def goal_callback(self, goal_request):
        """Validate manipulation goal"""
        # Check if trajectory is valid
        trajectory = goal_request.trajectory

        if len(trajectory.points) == 0:
            self.get_logger().warn('Empty trajectory received')
            return GoalResponse.REJECT

        # Check if joint names are valid for this robot
        expected_joints = ['left_shoulder_pitch', 'left_shoulder_roll', 'left_elbow_yaw',
                          'left_elbow_pitch', 'left_wrist_roll', 'left_wrist_pitch']

        if set(trajectory.joint_names) != set(expected_joints):
            self.get_logger().warn('Invalid joint names in trajectory')
            return GoalResponse.REJECT

        self.get_logger().info('Accepting manipulation goal')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Handle cancel request"""
        self.get_logger().info('Canceling manipulation goal')
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle):
        """Execute manipulation goal"""
        self.get_logger().info('Starting manipulation execution')
        self.manipulation_active = True

        # Get trajectory
        trajectory = goal_handle.request.trajectory

        # Execute trajectory point by point
        for i, point in enumerate(trajectory.points):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result = FollowJointTrajectory.Result()
                result.error_code = FollowJointTrajectory.Result.PATH_TOLERANCE_VIOLATED
                return result

            # Create joint trajectory message
            joint_msg = JointTrajectory()
            joint_msg.joint_names = trajectory.joint_names
            joint_msg.points = [point]

            # Publish trajectory point
            self.joint_cmd_pub.publish(joint_msg)

            # Wait for execution (in real implementation, monitor actual position)
            time_to_wait = point.time_from_start.sec + point.time_from_start.nanosec / 1e9
            self.get_clock().sleep_for(rclpy.duration.Duration(seconds=time_to_wait))

            # Provide feedback
            feedback_msg = FollowJointTrajectory.Feedback()
            feedback_msg.joint_names = trajectory.joint_names
            feedback_msg.actual.positions = point.positions  # Simplified
            feedback_msg.desired = point
            goal_handle.publish_feedback(feedback_msg)

        # Check if all points were executed successfully
        goal_handle.succeed()
        result = FollowJointTrajectory.Result()
        result.error_code = FollowJointTrajectory.Result.SUCCESSFUL
        self.get_logger().info('Manipulation completed successfully')

        return result

def main(args=None):
    rclpy.init(args=args)
    node = HumanoidManipulationAction()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service-Based Robot Control

For immediate robot control commands, services are appropriate:

```python
# my_humonoid_robot/robot_control_service.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Bool, Float64MultiArray
from geometry_msgs.msg import Twist
from my_humonoid_robot.srv import RobotControlCommand

class RobotControlService(Node):
    def __init__(self):
        super().__init__('robot_control_service')

        # Service server
        self.control_srv = self.create_service(
            RobotControlCommand,
            'robot_control',
            self.control_callback
        )

        # Publishers for different control types
        self.cmd_vel_pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.joint_cmd_pub = self.create_publisher(Float64MultiArray, 'joint_commands', 10)
        self.emergency_stop_pub = self.create_publisher(Bool, 'emergency_stop', 10)

        # Robot state
        self.robot_enabled = True

    def control_callback(self, request, response):
        """Handle robot control commands"""
        command_type = request.command_type
        params = request.parameters

        try:
            if command_type == 'MOVE_LINEAR':
                self.move_linear(params)
                response.success = True
                response.message = 'Linear movement command sent'

            elif command_type == 'ROTATE':
                self.rotate(params)
                response.success = True
                response.message = 'Rotation command sent'

            elif command_type == 'SET_JOINT_POSITIONS':
                self.set_joint_positions(params)
                response.success = True
                response.message = 'Joint position command sent'

            elif command_type == 'EMERGENCY_STOP':
                self.emergency_stop()
                response.success = True
                response.message = 'Emergency stop activated'

            elif command_type == 'ENABLE_ROBOT':
                self.enable_robot()
                response.success = True
                response.message = 'Robot enabled'

            elif command_type == 'DISABLE_ROBOT':
                self.disable_robot()
                response.success = True
                response.message = 'Robot disabled'

            else:
                response.success = False
                response.message = f'Unknown command type: {command_type}'

        except Exception as e:
            response.success = False
            response.message = f'Command failed: {str(e)}'
            self.get_logger().error(f'Control command error: {e}')

        return response

    def move_linear(self, params):
        """Move robot linearly"""
        cmd = Twist()
        cmd.linear.x = params[0] if len(params) > 0 else 0.0
        cmd.linear.y = params[1] if len(params) > 1 else 0.0
        cmd.linear.z = params[2] if len(params) > 2 else 0.0
        self.cmd_vel_pub.publish(cmd)

    def rotate(self, params):
        """Rotate robot"""
        cmd = Twist()
        cmd.angular.z = params[0] if len(params) > 0 else 0.0
        self.cmd_vel_pub.publish(cmd)

    def set_joint_positions(self, params):
        """Set joint positions"""
        cmd = Float64MultiArray()
        cmd.data = params
        self.joint_cmd_pub.publish(cmd)

    def emergency_stop(self):
        """Activate emergency stop"""
        stop_msg = Bool()
        stop_msg.data = True
        self.emergency_stop_pub.publish(stop_msg)
        self.robot_enabled = False

    def enable_robot(self):
        """Enable robot"""
        self.robot_enabled = True

    def disable_robot(self):
        """Disable robot"""
        cmd = Twist()
        cmd.linear.x = 0.0
        cmd.angular.z = 0.0
        self.cmd_vel_pub.publish(cmd)
        self.robot_enabled = False

def main(args=None):
    rclpy.init(args=args)
    node = RobotControlService()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## 3.5 Launch Files for Services and Actions

### Launch File with Services and Actions

```python
# launch/services_actions_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='humonoid_robot',
        description='Name of the robot'
    )

    # Service server node
    calculator_service = Node(
        package='my_humonoid_robot',
        executable='calculator_service',
        name='calculator_service',
        parameters=[
            {'robot_name': LaunchConfiguration('robot_name')}
        ],
        output='screen'
    )

    # Action server node
    navigation_action = Node(
        package='my_humonoid_robot',
        executable='navigation_action',
        name='navigation_action',
        parameters=[
            {'robot_name': LaunchConfiguration('robot_name')}
        ],
        output='screen'
    )

    # Action server for manipulation
    manipulation_action = Node(
        package='my_humonoid_robot',
        executable='manipulation_action',
        name='manipulation_action',
        parameters=[
            {'robot_name': LaunchConfiguration('robot_name')}
        ],
        output='screen'
    )

    # Robot control service
    robot_control_service = Node(
        package='my_humonoid_robot',
        executable='robot_control_service',
        name='robot_control_service',
        parameters=[
            {'robot_name': LaunchConfiguration('robot_name')}
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_name_launch_arg,

        LogInfo(msg=['Starting services and actions for: ', LaunchConfiguration('robot_name')]),

        calculator_service,
        navigation_action,
        manipulation_action,
        robot_control_service,
    ])
```

## 3.6 Best Practices for Humanoid Robotics

### Service and Action Package Structure

```
my_humonoid_robot/
├── CMakeLists.txt
├── package.xml
├── srv/
│   ├── RobotControlCommand.srv
│   └── SensorCalibration.srv
├── action/
│   ├── MoveArm.action
│   └── Walk.action
├── my_humonoid_robot/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── robot_control_service.py
│   │   └── sensor_calibration_service.py
│   ├── actions/
│   │   ├── __init__.py
│   │   ├── navigation_action.py
│   │   └── manipulation_action.py
│   └── utils/
│       ├── __init__.py
│       └── robot_helpers.py
├── launch/
│   ├── services_launch.py
│   └── actions_launch.py
└── config/
    └── robot_params.yaml
```

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Service name | lowercase with underscores | `robot_control`, `sensor_calibration` |
| Action name | lowercase with underscores | `navigate_to_pose`, `move_arm` |
| Service types | CamelCase | `RobotControlCommand`, `SensorCalibration` |
| Action types | CamelCase | `NavigateToPose`, `MoveArm` |

:::tip
Use descriptive names that clearly indicate the purpose of the service or action. For humanoid robots, include the robot part in the name when relevant (e.g., `left_arm_move`, `right_leg_control`).
:::

### Reliability Patterns

1. **Timeout Handling**: Always implement timeouts for service calls
2. **Graceful Degradation**: Handle service/action unavailability gracefully
3. **State Management**: Maintain consistent state across service/action calls
4. **Error Recovery**: Implement retry mechanisms for critical operations

## 3.7 Chapter Summary

This chapter has covered the essential concepts of ROS 2 services and actions:

1. **Services**: Request-response communication for synchronous operations
2. **Actions**: Goal-based communication for long-running tasks with feedback
3. **Custom Definitions**: Creating `.srv` and `.action` files for specific needs
4. **Implementation**: Python and C++ examples for servers and clients
5. **Humanoid Applications**: Navigation, manipulation, and control use cases
6. **Best Practices**: Proper error handling, naming conventions, and architecture

Services are ideal for quick, synchronous operations that return a result, while actions are designed for complex, long-running tasks that require ongoing feedback and the ability to be canceled. Both patterns are essential for building robust humanoid robot systems.

## 3.8 Exercises

### Exercise 1: Basic Service Implementation (Beginner)
Create a service that takes two 3D points (x, y, z coordinates) and returns the Euclidean distance between them. Implement both the service server and client in Python.

### Exercise 2: Action Server (Intermediate)
Implement an action server that simulates a humanoid robot walking to a specified location. The action should provide feedback on the robot's progress and allow cancellation.

### Exercise 3: Service with Error Handling (Intermediate)
Create a service that performs robot calibration with proper error handling, timeouts, and validation of input parameters.

### Exercise 4: Multi-Goal Action Client (Advanced)
Implement an action client that can send multiple goals to a navigation action server and manage them concurrently, handling completion, cancellation, and errors for each goal.

### Exercise 5: Custom Action Definition (Advanced)
Define a custom action for humanoid robot balance control that includes goal (desired pose), feedback (current stability metrics), and result (success/failure with reason).

## 3.9 Mini-Project: Action-Based Humanoid Arm Controller

Create a complete action-based humanoid arm controller system that includes:

- A custom action definition for arm manipulation tasks
- An action server that manages joint trajectory execution
- An action client that demonstrates various arm movements
- Proper error handling, feedback, and cancellation support
- Integration with robot simulation (if available)
- Launch files for starting the complete system
- Unit tests for the action server

The system should be able to execute complex arm movements with real-time feedback on progress, handle interruptions gracefully, and provide detailed results upon completion. The action should support various types of movements such as reaching, grasping, and waving, with appropriate safety checks and joint limits enforcement.

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Basic Service Implementation</summary>

```python
# distance_calculator_service.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts  # We'll reuse this for simplicity, or create custom
from geometry_msgs.msg import Point

class DistanceCalculatorService(Node):
    def __init__(self):
        super().__init__('distance_calculator_service')

        # Create a service to calculate Euclidean distance between two 3D points
        self.srv = self.create_service(
            AddTwoInts,  # In practice, you'd create a custom service for 3D points
            'calculate_distance_3d',
            self.calculate_distance_callback
        )

        self.get_logger().info('Distance calculator service ready')

    def calculate_distance_callback(self, request, response):
        # For this example, we'll simulate 3D points using the available AddTwoInts
        # In practice, you'd create a custom service like Calculate3DDistance.srv
        # with fields for x1, y1, z1, x2, y2, z2

        # Calculate Euclidean distance: sqrt((x2-x1)² + (y2-y1)² + (z2-z1)²)
        # Using request.a and request.b as x1 and x2 coordinates for this example
        # A real implementation would use a custom service definition

        # Simulate calculating distance between (0,0,0) and (request.a, request.b, 1)
        dx = request.a - 0.0  # x2 - x1
        dy = request.b - 0.0  # y2 - y1
        dz = 1.0 - 0.0        # z2 - z1 (fixed for example)

        distance = (dx*dx + dy*dy + dz*dz)**0.5
        response.sum = distance  # Using sum field to return distance

        self.get_logger().info(f'Calculated distance: {distance:.3f}')
        return response

def main(args=None):
    rclpy.init(args=args)

    distance_service = DistanceCalculatorService()

    try:
        rclpy.spin(distance_service)
    except KeyboardInterrupt:
        distance_service.get_logger().info('Service interrupted by user')
    finally:
        distance_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

```python
# distance_calculator_client.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class DistanceCalculatorClient(Node):
    def __init__(self):
        super().__init__('distance_calculator_client')

        # Create client
        self.cli = self.create_client(AddTwoInts, 'calculate_distance_3d')

        # Wait for service
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for distance calculation service...')

        self.req = AddTwoInts.Request()

    def send_request(self, x1, y1, z1, x2, y2, z2):
        # For this example, we'll use x1, y1 as request.a, request.b
        # A real implementation would use a custom service
        self.req.a = x2  # Using as x2 coordinate
        self.req.b = y2  # Using as y2 coordinate
        # z coordinates would be handled differently in a real implementation

        self.future = self.cli.call_async(self.req)
        return self.future

def main(args=None):
    rclpy.init(args=args)

    client = DistanceCalculatorClient()

    # Send request to calculate distance between (0,0,0) and (3,4,1)
    future = client.send_request(0.0, 0.0, 0.0, 3.0, 4.0, 1.0)

    # Wait for response
    rclpy.spin_until_future_complete(client, future)

    if future.result() is not None:
        response = future.result()
        distance = response.sum  # The distance value
        client.get_logger().info(f'Result: Distance = {distance:.3f}')
    else:
        client.get_logger().error('Exception while calling service: %r' % future.exception())

    client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

For a complete implementation with a custom service, you would create a custom service file:

```xml
# srv/Calculate3DDistance.srv
# Request
float64 x1
float64 y1
float64 z1
float64 x2
float64 y2
float64 z2
---
# Response
float64 distance
bool success
string message
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Action Server Implementation</summary>

```python
# humanoid_navigation_action.py
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped, Point
from nav_msgs.action import NavigateToPose  # Using standard action for navigation
import math
import time

class HumanoidNavigationAction(Node):
    def __init__(self):
        super().__init__('humanoid_navigation_action')

        # Create action server
        self._action_server = ActionServer(
            self,
            NavigateToPose,
            'humanoid_navigate_to_pose',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        self.get_logger().info('Humanoid navigation action server started')

    def goal_callback(self, goal_request):
        """Accept or reject a goal."""
        self.get_logger().info('Received goal request')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject a cancel request."""
        self.get_logger().info('Received cancel request')
        return CancelResponse.ACCEPT

    async def execute_callback(self, goal_handle):
        """Execute the goal."""
        self.get_logger().info('Executing goal...')

        # Get target pose from goal
        target_pose = goal_handle.request.pose.pose
        target_x = target_pose.position.x
        target_y = target_pose.position.y

        # Create feedback message
        feedback_msg = NavigateToPose.Feedback()
        feedback_msg.current_pose.header.stamp = self.get_clock().now().to_msg()
        feedback_msg.current_pose.pose = target_pose  # Simplified - in reality this would be current position

        # Calculate initial distance
        current_x, current_y = 0.0, 0.0  # Starting at origin for simulation
        initial_distance = math.sqrt((target_x - current_x)**2 + (target_y - current_y)**2)

        # Simulate navigation progress
        for i in range(0, 101, 5):  # Progress from 0 to 100%
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                result = NavigateToPose.Result()
                result.result = 0  # Canceled
                return result

            # Update feedback
            progress_percentage = i / 100.0
            feedback_msg.progress = progress_percentage
            feedback_msg.distance_remaining = initial_distance * (1 - progress_percentage)

            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f'Navigation progress: {i}%')

            # Simulate movement by sleeping
            time.sleep(0.1)

        # Goal succeeded
        goal_handle.succeed()
        result = NavigateToPose.Result()
        result.result = 1  # Success
        self.get_logger().info('Goal succeeded')

        return result

def main(args=None):
    rclpy.init(args=args)

    navigation_action_server = HumanoidNavigationAction()

    try:
        rclpy.spin(navigation_action_server)
    except KeyboardInterrupt:
        navigation_action_server.get_logger().info('Action server interrupted by user')
    finally:
        navigation_action_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Service with Error Handling</summary>

```python
# robot_calibration_service.py
import rclpy
from rclpy.node import Node
from example_interfaces.srv import Trigger  # Using Trigger as simple service
from rcl_interfaces.msg import SetParametersResult
import random

class RobotCalibrationService(Node):
    def __init__(self):
        super().__init__('robot_calibration_service')

        # Create calibration service
        self.srv = self.create_service(
            Trigger,
            'robot_calibration',
            self.calibration_callback
        )

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.parameters_callback)

        # Declare calibration parameters
        self.declare_parameter('calibration_timeout', 30.0)
        self.declare_parameter('calibration_accuracy_threshold', 0.01)

        self.get_logger().info('Robot calibration service ready')

    def parameters_callback(self, parameters):
        """Validate parameter changes."""
        from rcl_interfaces.msg import SetParametersResult

        result = SetParametersResult()
        result.successful = True

        for param in parameters:
            if param.name == 'calibration_timeout':
                if param.value <= 0 or param.value > 300:  # Max 5 minutes
                    result.successful = False
                    result.reason = 'Calibration timeout must be between 0 and 300 seconds'
                    return result
            elif param.name == 'calibration_accuracy_threshold':
                if param.value <= 0 or param.value > 1.0:
                    result.successful = False
                    result.reason = 'Calibration accuracy threshold must be between 0 and 1.0'
                    return result

        return result

    def calibration_callback(self, request, response):
        """Handle calibration request with error handling."""
        try:
            timeout = self.get_parameter('calibration_timeout').value
            accuracy_threshold = self.get_parameter('calibration_accuracy_threshold').value

            self.get_logger().info(f'Starting calibration with timeout {timeout}s')

            # Simulate calibration process
            success = self.perform_calibration(timeout, accuracy_threshold)

            if success:
                response.success = True
                response.message = 'Calibration completed successfully'
                self.get_logger().info('Calibration completed successfully')
            else:
                response.success = False
                response.message = 'Calibration failed to meet accuracy requirements'
                self.get_logger().error('Calibration failed')

        except Exception as e:
            response.success = False
            response.message = f'Calibration failed with exception: {str(e)}'
            self.get_logger().error(f'Calibration exception: {e}')

        return response

    def perform_calibration(self, timeout, accuracy_threshold):
        """Simulate robot calibration process."""
        import time
        start_time = time.time()

        # Simulate calibration steps
        steps = ['sensor_alignment', 'joint_zeroing', 'imu_calibration', 'accuracy_check']

        for step in steps:
            if time.time() - start_time > timeout:
                self.get_logger().error('Calibration timed out')
                return False

            self.get_logger().info(f'Performing calibration step: {step}')
            time.sleep(1)  # Simulate time for each step

            # Simulate potential failure (10% chance)
            if random.random() < 0.1:
                self.get_logger().error(f'Calibration failed at step: {step}')
                return False

        # Check if accuracy is within threshold
        achieved_accuracy = random.uniform(0.001, 0.05)  # Random accuracy
        if achieved_accuracy > accuracy_threshold:
            self.get_logger().warn(f'Calibration accuracy {achieved_accuracy} exceeds threshold {accuracy_threshold}')
            return False

        return True

def main(args=None):
    rclpy.init(args=args)

    calibration_service = RobotCalibrationService()

    try:
        rclpy.spin(calibration_service)
    except KeyboardInterrupt:
        calibration_service.get_logger().info('Calibration service interrupted by user')
    finally:
        calibration_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: Multi-Goal Action Client</summary>

```python
# multi_goal_navigation_client.py
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose  # Using navigation action
from std_msgs.msg import String
import threading
import time
from enum import Enum

class GoalState(Enum):
    PENDING = "pending"
    ACTIVE = "active"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"

class MultiGoalNavigationClient(Node):
    def __init__(self):
        super().__init__('multi_goal_navigation_client')

        # Create action client
        self._action_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Goals management
        self.goals = {}
        self.next_goal_id = 0

        # Publisher for status updates
        self.status_pub = self.create_publisher(String, 'multi_goal_status', 10)

        self.get_logger().info('Multi-goal navigation client initialized')

    def send_goal_async(self, x, y, theta=0.0):
        """Send a goal asynchronously and return goal handle."""
        # Wait for action server
        if not self._action_client.wait_for_server(timeout_sec=5.0):
            self.get_logger().error('Action server not available')
            return None

        # Create goal message
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = x
        goal_msg.pose.pose.position.y = y
        goal_msg.pose.pose.position.z = 0.0

        # Convert theta to quaternion
        import math
        goal_msg.pose.pose.orientation.z = math.sin(theta / 2.0)
        goal_msg.pose.pose.orientation.w = math.cos(theta / 2.0)

        # Send goal
        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )

        # Assign a unique ID to this goal
        goal_id = self.next_goal_id
        self.next_goal_id += 1

        # Store goal info
        self.goals[goal_id] = {
            'future': send_goal_future,
            'goal_msg': goal_msg,
            'state': GoalState.PENDING,
            'start_time': time.time()
        }

        send_goal_future.add_done_callback(lambda future: self.goal_response_callback(future, goal_id))

        self.get_logger().info(f'Sent goal {goal_id} to ({x}, {y})')
        return goal_id

    def goal_response_callback(self, future, goal_id):
        """Handle goal response."""
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info(f'Goal {goal_id} rejected')
            self.goals[goal_id]['state'] = GoalState.FAILED
            return

        self.get_logger().info(f'Goal {goal_id} accepted')
        self.goals[goal_id]['state'] = GoalState.ACTIVE
        self.goals[goal_id]['handle'] = goal_handle

        # Get result
        get_result_future = goal_handle.get_result_async()
        get_result_future.add_done_callback(lambda future: self.result_callback(future, goal_id))

    def feedback_callback(self, feedback_msg):
        """Handle feedback."""
        # This would be enhanced to associate feedback with specific goals
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')

    def result_callback(self, future, goal_id):
        """Handle action result."""
        result = future.result().result
        status = future.result().status

        if status == 3:  # GoalStatus.SUCCEEDED
            self.goals[goal_id]['state'] = GoalState.SUCCEEDED
            self.get_logger().info(f'Goal {goal_id} succeeded')
        else:
            self.goals[goal_id]['state'] = GoalState.FAILED
            self.get_logger().info(f'Goal {goal_id} failed with status: {status}')

    def cancel_goal(self, goal_id):
        """Cancel a specific goal."""
        if goal_id not in self.goals or self.goals[goal_id]['state'] != GoalState.ACTIVE:
            self.get_logger().warn(f'Cannot cancel goal {goal_id}, not active')
            return False

        goal_handle = self.goals[goal_id]['handle']
        future = goal_handle.cancel_goal_async()
        future.add_done_callback(lambda future: self.cancel_response_callback(future, goal_id))

        self.get_logger().info(f'Cancelling goal {goal_id}')
        return True

    def cancel_response_callback(self, future, goal_id):
        """Handle cancel response."""
        cancel_response = future.result()
        self.goals[goal_id]['state'] = GoalState.CANCELED
        self.get_logger().info(f'Goal {goal_id} cancelled')

    def get_goals_status(self):
        """Get status of all goals."""
        status_msg = String()
        status_str = ""
        for goal_id, goal_info in self.goals.items():
            status_str += f"Goal {goal_id}: {goal_info['state'].value}; "
        status_msg.data = status_str
        self.status_pub.publish(status_msg)
        return status_str

def main(args=None):
    rclpy.init(args=args)

    client = MultiGoalNavigationClient()

    # Send multiple goals
    goal_ids = []
    goals = [(1.0, 1.0), (2.0, 0.0), (0.0, -1.0), (-1.0, 1.0)]

    for i, (x, y) in enumerate(goals):
        goal_id = client.send_goal_async(x, y)
        if goal_id is not None:
            goal_ids.append(goal_id)
        time.sleep(0.5)  # Delay between goals

    # Monitor goals
    try:
        while any(client.goals[gid]['state'] in [GoalState.PENDING, GoalState.ACTIVE] for gid in goal_ids):
            status = client.get_goals_status()
            client.get_logger().info(f'Goals status: {status}')
            time.sleep(2.0)
            rclpy.spin_once(client, timeout_sec=0.1)
    except KeyboardInterrupt:
        client.get_logger().info('Client interrupted by user')
    finally:
        client.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Custom Action Definition</summary>

First, let's define the custom action file:

```xml
# action/BalanceControl.action
# Goal: Desired pose and balance parameters
float64[] target_pose  # [x, y, z, roll, pitch, yaw]
float64 max_lean_angle
float64 balance_threshold
duration max_duration
---
# Result: Success/failure with reason
bool success
string message
float64 final_stability_score
---
# Feedback: Current stability metrics
float64[] current_pose  # [x, y, z, roll, pitch, yaw]
float64 stability_score
float64 lean_angle
string status_message
```

```python
# balance_control_action_server.py
import rclpy
from rclpy.action import ActionServer, CancelResponse, GoalResponse
from rclpy.node import Node
from my_robot_interfaces.action import BalanceControl  # Custom action
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Imu
import math
import time

class BalanceControlActionServer(Node):
    def __init__(self):
        super().__init__('balance_control_action_server')

        # Create action server
        self._action_server = ActionServer(
            self,
            BalanceControl,
            'balance_control',
            execute_callback=self.execute_callback,
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback
        )

        # Subscribe to IMU data for balance feedback
        self.imu_sub = self.create_subscription(
            Imu,
            'imu/data',
            self.imu_callback,
            10
        )

        # Internal state
        self.current_imu_data = None
        self.balance_active = False

        self.get_logger().info('Balance control action server started')

    def goal_callback(self, goal_request):
        """Accept or reject a goal."""
        # Validate goal parameters
        if goal_request.max_lean_angle <= 0 or goal_request.max_lean_angle > math.pi/2:
            self.get_logger().warn('Invalid max_lean_angle in goal')
            return GoalResponse.REJECT

        if goal_request.balance_threshold <= 0:
            self.get_logger().warn('Invalid balance_threshold in goal')
            return GoalResponse.REJECT

        self.get_logger().info('Accepted balance control goal')
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle):
        """Accept or reject a cancel request."""
        self.get_logger().info('Received balance control cancel request')
        return CancelResponse.ACCEPT

    def imu_callback(self, msg):
        """Update current IMU data."""
        self.current_imu_data = msg

    def calculate_stability_score(self):
        """Calculate current stability based on IMU data."""
        if not self.current_imu_data:
            return 0.0  # Unknown stability

        # Extract roll and pitch from orientation (simplified)
        quat = self.current_imu_data.orientation
        import tf_transformations
        euler = tf_transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
        roll, pitch, yaw = euler

        # Stability score: 1.0 is perfectly stable, 0.0 is unstable
        max_angle = math.radians(15)  # Consider stable if within 15 degrees
        roll_score = max(0, 1 - abs(roll) / max_angle)
        pitch_score = max(0, 1 - abs(pitch) / max_angle)

        return min(roll_score, pitch_score)

    async def execute_callback(self, goal_handle):
        """Execute the balance control goal."""
        self.get_logger().info('Executing balance control goal...')
        self.balance_active = True

        # Create feedback message
        feedback_msg = BalanceControl.Feedback()
        result = BalanceControl.Result()

        start_time = time.time()
        max_duration = goal_handle.request.max_duration.sec + goal_handle.request.max_duration.nanosec / 1e9

        while self.balance_active:
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                result.success = False
                result.message = 'Balance control canceled'
                result.final_stability_score = 0.0
                self.balance_active = False
                self.get_logger().info('Balance control canceled')
                return result

            # Calculate current stability
            stability_score = self.calculate_stability_score()
            feedback_msg.stability_score = stability_score

            # Calculate current lean angle (magnitude of roll and pitch)
            if self.current_imu_data:
                quat = self.current_imu_data.orientation
                import tf_transformations
                euler = tf_transformations.euler_from_quaternion([quat.x, quat.y, quat.z, quat.w])
                roll, pitch, _ = euler
                lean_angle = math.sqrt(roll**2 + pitch**2)
                feedback_msg.lean_angle = lean_angle
            else:
                feedback_msg.lean_angle = 0.0

            # Check if we've achieved balance
            if stability_score >= goal_handle.request.balance_threshold:
                feedback_msg.status_message = "Balanced achieved"
                goal_handle.succeed()
                result.success = True
                result.message = "Balance control successful"
                result.final_stability_score = stability_score
                self.balance_active = False
                self.get_logger().info('Balance control succeeded')
                return result

            # Check for excessive lean
            if feedback_msg.lean_angle > goal_handle.request.max_lean_angle:
                feedback_msg.status_message = "Excessive lean detected"
                goal_handle.abort()
                result.success = False
                result.message = f"Excessive lean: {feedback_msg.lean_angle:.3f} > {goal_handle.request.max_lean_angle:.3f}"
                result.final_stability_score = stability_score
                self.balance_active = False
                self.get_logger().error('Balance control failed - excessive lean')
                return result

            # Check for timeout
            if time.time() - start_time > max_duration:
                feedback_msg.status_message = "Timeout reached"
                goal_handle.abort()
                result.success = False
                result.message = f"Balance control timed out after {max_duration:.1f}s"
                result.final_stability_score = stability_score
                self.balance_active = False
                self.get_logger().info('Balance control timed out')
                return result

            # Publish feedback
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().debug(f'Balance feedback: score={stability_score:.3f}, lean={feedback_msg.lean_angle:.3f}')

            # Small delay to prevent busy waiting
            time.sleep(0.05)

        # If we exit the loop without succeeding
        result.success = False
        result.message = "Balance control terminated unexpectedly"
        result.final_stability_score = 0.0
        return result

def main(args=None):
    rclpy.init(args=args)

    server = BalanceControlActionServer()

    try:
        rclpy.spin(server)
    except KeyboardInterrupt:
        server.get_logger().info('Balance control server interrupted by user')
    finally:
        server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>