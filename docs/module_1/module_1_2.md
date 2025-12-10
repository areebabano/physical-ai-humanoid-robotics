---
title: "Module 1.2 - Chapter 2: ROS 2 Packages"
sidebar_position: 2
---

# Module 1.2 - Chapter 2: ROS 2 Packages

## 2.0 Introduction to ROS 2 Packages

### What is a ROS 2 Package?

A ROS 2 package is the fundamental unit of code organization in the Robot Operating System 2 (ROS 2) framework. It represents a modular, self-contained software component that encapsulates related functionality, resources, and dependencies. Packages serve as the building blocks of complex robotic applications, enabling developers to create reusable, maintainable, and scalable robot software systems.

The package concept in ROS 2 extends beyond simple code organization. It encompasses:
- Source code (Python, C++, etc.)
- Launch files for system orchestration
- Configuration files and parameters
- Message, service, and action definitions
- Documentation and tests
- Dependencies and build instructions

```
┌─────────────────────────────────────────┐
│              ROS 2 Package              │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │   Source    │  │   Launch Files   │  │
│  │    Code     │  │                  │  │
│  │  (Python/   │  │  (Python-based)  │  │
│  │   C++)      │  │                  │  │
│  └─────────────┘  └──────────────────┘  │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Config/    │  │   Dependencies   │  │
│  │ Parameters  │  │                  │  │
│  │   (YAML)    │  │  (package.xml)   │  │
│  │             │  │                  │  │
│  └─────────────┘  └──────────────────┘  │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Message/   │  │   Build System   │  │
│  │  Service/   │  │ (CMakeLists.txt, │  │
│  │   Action    │  │   setup.py)      │  │
│  │ Definitions │  │                  │  │
│  └─────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
```

### Package Philosophy

The package system in ROS 2 embodies several key design principles:

1. **Modularity**: Each package focuses on a specific functionality or capability
2. **Reusability**: Packages can be shared across different robot projects
3. **Maintainability**: Clear boundaries make code easier to maintain
4. **Scalability**: Systems can grow by adding new packages
5. **Dependency Management**: Clear declaration of required packages

## 2.1 Package Directory Structure

### Standard Package Layout

A typical ROS 2 package follows a standardized directory structure that promotes consistency across the ROS ecosystem:

```
my_robot_package/
├── CMakeLists.txt              # Build configuration for C++ packages
├── package.xml                 # Package metadata and dependencies
├── setup.py                    # Python package build configuration
├── setup.cfg                   # Additional Python build configuration
├── my_robot_package/           # Main Python package directory
│   ├── __init__.py            # Python package initialization
│   ├── my_node.py             # Example Python node
│   ├── my_service.py          # Example service implementation
│   └── my_action.py           # Example action implementation
├── launch/                     # Launch files directory
│   ├── robot_launch.py        # Main robot launch file
│   ├── navigation_launch.py   # Navigation-specific launch file
│   └── config_launch.py       # Configuration launch file
├── config/                     # Configuration files directory
│   ├── params.yaml            # Parameter configuration
│   ├── sensors.yaml           # Sensor configuration
│   └── controllers.yaml       # Controller configuration
├── src/                        # C++ source files (if applicable)
│   ├── my_node.cpp            # C++ node implementation
│   └── my_library.cpp         # C++ library implementation
├── include/                    # C++ header files (if applicable)
│   └── my_robot_package/
│       ├── my_node.hpp        # C++ header file
│       └── my_library.hpp     # C++ library header
├── test/                       # Test files directory
│   ├── test_my_node.py        # Node unit tests
│   └── test_services.py       # Service integration tests
├── msg/                        # Custom message definitions
│   ├── MyMessage.msg          # Custom message definition
│   └── AnotherMessage.msg     # Another custom message
├── srv/                        # Custom service definitions
│   └── MyService.srv          # Custom service definition
├── action/                     # Custom action definitions
│   └── MyAction.action        # Custom action definition
├── meshes/                     # 3D mesh files (for URDF)
├── urdf/                       # URDF robot description files
└── resource/                   # Additional resources
```

### Key Directories Explained

| Directory | Purpose | Contents |
|-----------|---------|----------|
| `launch/` | Launch files | Python files for node orchestration |
| `config/` | Configuration | YAML files for parameters and settings |
| `msg/`, `srv/`, `action/` | Message definitions | Custom message/service/action files |
| `src/`, `include/` | C++ code | C++ source and header files |
| `test/` | Test files | Unit and integration tests |

:::note
The directory structure may vary depending on the package type (Python-only, C++-only, or mixed). Not all directories are required for every package.
:::

## 2.2 package.xml: The Package Manifest

### Understanding package.xml

The `package.xml` file serves as the package manifest, containing metadata about the package including its name, version, description, maintainers, license, and dependencies. This file is crucial for the ROS 2 build system and package management.

### Complete package.xml Example

```xml
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_robot_package</name>
  <version>1.0.0</version>
  <description>
    A comprehensive package for humanoid robot control and perception.
    This package provides essential functionality for robot navigation,
    sensor processing, and high-level control in humanoid robotics applications.
  </description>
  <maintainer email="robotics@example.com">Robotics Team</maintainer>
  <license>Apache License 2.0</license>

  <url type="website">https://github.com/robotics/my_robot_package</url>
  <url type="bugtracker">https://github.com/robotics/my_robot_package/issues</url>
  <url type="repository">https://github.com/robotics/my_robot_package</repository>

  <author email="developer@example.com">Robot Developer</author>

  <!-- Build tool dependencies -->
  <buildtool_depend>ament_cmake</buildtool_depend>
  <buildtool_depend>ament_python</buildtool_depend>

  <!-- Build dependencies -->
  <build_depend>rclpy</build_depend>
  <build_depend>std_msgs</build_depend>
  <build_depend>sensor_msgs</build_depend>
  <build_depend>geometry_msgs</build_depend>
  <build_depend>nav_msgs</build_depend>
  <build_depend>message_generation</build_depend>

  <!-- Execution dependencies -->
  <exec_depend>rclpy</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>nav_msgs</exec_depend>
  <exec_depend>message_runtime</exec_depend>

  <!-- Test dependencies -->
  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <!-- Export information -->
  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

### Field-by-Field Explanation

#### Essential Fields

- **`<name>`**: The unique identifier for the package. Must be lowercase with underscores.
- **`<version>`**: Package version following semantic versioning (MAJOR.MINOR.PATCH).
- **`<description>`**: A comprehensive description of the package functionality.
- **`<maintainer>`**: Contact information for the package maintainer.
- **`<license>`**: The license under which the package is distributed.

#### Dependency Types

```
package.xml Dependencies
├── buildtool_depend: Build system dependencies
├── build_depend: Dependencies required for building
├── exec_depend: Dependencies required for execution
├── test_depend: Dependencies required for testing
└── depend: Combined build and execution dependency
```

:::tip
Use `<depend>` instead of separate `<build_depend>` and `<exec_depend>` when the same package is needed for both building and execution.
:::

## 2.3 CMakeLists.txt for C++ Packages

### CMake Configuration Overview

For C++ packages, the `CMakeLists.txt` file provides build instructions to the CMake build system. This file defines how source files are compiled, linked, and installed.

### Complete CMakeLists.txt Example

```cmake
cmake_minimum_required(VERSION 3.8)
project(my_robot_package)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(message_generation REQUIRED)

# Define custom messages
add_message_files(
  FILES
  CustomMessage.msg
)

add_service_files(
  FILES
  CustomService.srv
)

add_action_files(
  FILES
  CustomAction.action
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
  sensor_msgs
)

# Create a library
add_library(my_robot_library
  src/my_robot_library.cpp
)

target_include_directories(my_robot_library
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>
)
target_compile_features(my_robot_library PUBLIC c_std_99 cxx_std_17)

ament_target_dependencies(my_robot_library
  PUBLIC
    rclcpp
    std_msgs
    sensor_msgs
    geometry_msgs
)

# Create an executable node
add_executable(my_robot_node
  src/my_robot_node.cpp
)

target_include_directories(my_robot_node
  PRIVATE
    include
)

ament_target_dependencies(my_robot_node
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
  nav_msgs
)

# Install targets
install(TARGETS
  my_robot_library
  my_robot_node
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  include/
  DESTINATION include
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(ament_cmake)
ament_export_include_directories(include)
ament_export_libraries(my_robot_library)
ament_package()
```

### Key CMake Components

1. **Project Definition**: Sets the project name and minimum CMake version
2. **Dependency Finding**: Locates required ROS 2 packages
3. **Message Generation**: Defines custom messages, services, and actions
4. **Library/Executable Creation**: Compiles source files into libraries/executables
5. **Target Dependencies**: Links required packages to targets
6. **Installation**: Specifies where to install files
7. **Export Information**: Makes the package available to others

## 2.4 Python Package Structure for rclpy

### Python Package Organization

Python packages in ROS 2 follow Python packaging conventions while integrating with the ROS 2 build system.

### setup.py Configuration

```python
from setuptools import find_packages, setup

package_name = 'my_robot_package'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            ['launch/robot_launch.py']),
        ('share/' + package_name + '/config',
            ['config/params.yaml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robotics Team',
    maintainer_email='robotics@example.com',
    description='A comprehensive package for humanoid robot control and perception',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'my_robot_node = my_robot_package.my_robot_node:main',
            'sensor_processor = my_robot_package.sensor_processor:main',
            'path_planner = my_robot_package.path_planner:main',
        ],
    },
)
```

### Python Node Structure

```python
# my_robot_package/my_robot_node.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from my_robot_package.srv import CustomService

class MyRobotNode(Node):
    def __init__(self):
        super().__init__('my_robot_node')

        # Publishers
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 10)

        # Subscribers
        self.scan_subscriber = self.create_subscription(
            LaserScan, 'scan', self.scan_callback, 10)

        # Services
        self.service = self.create_service(
            CustomService, 'custom_service', self.service_callback)

        # Parameters
        self.declare_parameter('robot_name', 'my_robot')
        self.declare_parameter('linear_velocity', 0.5)

        # Timers
        self.control_timer = self.create_timer(0.1, self.control_loop)

        self.get_logger().info('My Robot Node initialized')

    def scan_callback(self, msg):
        """Process laser scan data"""
        # Implementation here
        pass

    def service_callback(self, request, response):
        """Handle service requests"""
        # Implementation here
        return response

    def control_loop(self):
        """Main control loop"""
        # Implementation here
        pass

def main(args=None):
    rclpy.init(args=args)
    node = MyRobotNode()
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

## 2.5 Creating Packages Using ros2 pkg create

### Package Creation Commands

The `ros2 pkg create` command provides a convenient way to create new packages with proper structure and configuration files.

#### Python Package Creation

```bash
# Create a Python package
ros2 pkg create --build-type ament_python my_robot_package

# Create with dependencies
ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs sensor_msgs my_robot_package
```

#### C++ Package Creation

```bash
# Create a C++ package
ros2 pkg create --build-type ament_cmake my_robot_cpp_package

# Create with dependencies
ros2 pkg create --build-type ament_cmake --dependencies rclcpp std_msgs sensor_msgs my_robot_cpp_package
```

### Complete Package Creation Example

```
$ ros2 pkg create --build-type ament_python --dependencies rclpy std_msgs sensor_msgs geometry_msgs my_humonoid_controller
going to create a new package
  package name: my_humonoid_controller
  destination directory: /path/to/workspace/src
  package format: 3
  version: 0.0.0
  description: A package for humanoid robot control
  maintainer: ['Robot Developer <developer@example.com>']
  licenses: ['Apache License 2.0']
  build type: ament_python
  dependencies: ['rclpy', 'std_msgs', 'sensor_msgs', 'geometry_msgs']
  python version: 3
Creating package.xml
Creating setup.py
Creating setup.cfg
Creating MANIFEST.in
Creating my_humonoid_controller/__init__.py
Creating test/test_copyright.py
Creating test/test_flake8.py
Creating test/test_pep257.py
Creating my_humonoid_controller/my_humonoid_controller.py
Successfully created package 'my_humonoid_controller'
```

### Post-Creation Configuration

After creating a package, you typically need to:

1. Update `package.xml` with proper metadata
2. Modify `setup.py` for Python packages
3. Implement your nodes and functionality
4. Add launch files and configuration
5. Create tests

## 2.6 Launch Files: Python Launch System

### Launch File Architecture

Launch files in ROS 2 are Python scripts that orchestrate the startup of multiple nodes with specific configurations. They provide a flexible way to manage complex robot systems.

```
Launch System Architecture
┌─────────────────────────────────────────┐
│           Launch File                   │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────┐  │
│  │   Node A    │  │   Parameters     │  │
│  │             │  │                  │  │
│  └─────────────┘  │  (YAML files)    │  │
│                   │                  │  │
│  ┌─────────────┐  └──────────────────┘  │
│  │   Node B    │  ┌──────────────────┐  │
│  │             │  │   Remappings     │  │
│  └─────────────┘  │                  │  │
│                   │  (topic renaming) │  │
│  ┌─────────────┐  └──────────────────┘  │
│  │   Node C    │  ┌──────────────────┐  │
│  │             │  │   Conditions     │  │
│  └─────────────┘  │                  │  │
│                   │  (if/else logic) │  │
│  ┌─────────────┐  └──────────────────┘  │
│  │   Timer     │                        │
│  │   Actions   │                        │
│  └─────────────┘                        │
└─────────────────────────────────────────┘
```

### Basic Launch File Structure

```python
# launch/robot_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration, TextSubstitution
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='my_robot',
        description='Name of the robot'
    )

    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation time'
    )

    return LaunchDescription([
        # Launch arguments
        robot_name_launch_arg,
        use_sim_time_launch_arg,

        # Log startup information
        LogInfo(
            msg=['Starting robot with name: ', LaunchConfiguration('robot_name')]
        ),

        # Robot controller node
        Node(
            package='my_robot_package',
            executable='my_robot_node',
            name='robot_controller',
            parameters=[
                {'robot_name': LaunchConfiguration('robot_name')},
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'linear_velocity': 0.5},
                {'angular_velocity': 0.3},
            ],
            remappings=[
                ('/cmd_vel', [LaunchConfiguration('robot_name'), '/cmd_vel']),
                ('/scan', [LaunchConfiguration('robot_name'), '/scan']),
            ],
            output='screen'
        ),

        # Sensor processor node
        Node(
            package='my_robot_package',
            executable='sensor_processor',
            name='sensor_processor',
            parameters=[
                {'use_sim_time': LaunchConfiguration('use_sim_time')},
                {'sensor_range': 10.0},
            ],
            output='screen'
        ),
    ])
```

### Advanced Launch File Features

```python
# launch/advanced_robot_launch.py
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    LogInfo,
    TimerAction,
    IncludeLaunchDescription
)
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

def generate_launch_description():
    # Launch arguments
    debug_mode_launch_arg = DeclareLaunchArgument(
        'debug',
        default_value='false',
        description='Enable debug mode'
    )

    use_navigation_launch_arg = DeclareLaunchArgument(
        'use_navigation',
        default_value='true',
        description='Launch navigation stack'
    )

    # Robot controller node
    robot_controller = Node(
        package='my_robot_package',
        executable='my_robot_node',
        name='robot_controller',
        parameters=[
            {'debug_mode': LaunchConfiguration('debug')},
        ],
        output='screen',
        respawn=True,  # Restart if node crashes
        respawn_delay=2.0
    )

    # Navigation nodes (only if enabled)
    navigation_nodes = Node(
        package='nav2_bringup',
        executable='nav2_world',
        name='navigation_stack',
        condition=IfCondition(LaunchConfiguration('use_navigation')),
        parameters=[
            FindPackageShare('nav2_bringup').find('nav2_bringup') + '/params/nav2_params.yaml'
        ],
        output='screen'
    )

    # Debug tools (only if debug mode enabled)
    debug_node = Node(
        package='my_robot_package',
        executable='debug_tool',
        name='debug_tool',
        condition=IfCondition(LaunchConfiguration('debug')),
        output='screen'
    )

    return LaunchDescription([
        debug_mode_launch_arg,
        use_navigation_launch_arg,

        # Launch nodes
        robot_controller,
        navigation_nodes,
        debug_node,

        # Log startup message
        LogInfo(
            msg=['Robot system starting with debug mode: ', LaunchConfiguration('debug')]
        ),
    ])
```

### Launch File Best Practices

:::tip
Use launch arguments to make your launch files flexible and reusable across different configurations and environments.
:::

:::note
Launch files should be placed in the `launch/` directory of your package and follow the naming convention `*.launch.py`.
:::

## 2.7 Parameters and YAML Configuration

### Parameter System Overview

Parameters in ROS 2 provide a flexible way to configure nodes at runtime without recompilation. They can be set through launch files, command line, or YAML configuration files.

### YAML Parameter Files

```yaml
# config/params.yaml
my_robot_package:
  ros__parameters:
    robot_name: "my_humonoid_robot"
    control_frequency: 50
    linear_velocity_limit: 1.0
    angular_velocity_limit: 1.5
    safety:
      collision_threshold: 0.5
      emergency_stop_enabled: true
      max_acceleration: 2.0
    sensors:
      laser_scan:
        range_min: 0.1
        range_max: 10.0
        update_rate: 10.0
      camera:
        resolution: [640, 480]
        frame_rate: 30
    navigation:
      global_frame: "map"
      robot_frame: "base_link"
      planner_frequency: 5.0
      controller_frequency: 20.0
      recovery_enabled: true
      recovery_behaviors:
        - name: "spin"
          type: "nav2_recoveries/Spin"
        - name: "backup"
          type: "nav2_recoveries/BackUp"
```

### Loading Parameters in Launch Files

```python
# launch/parameterized_launch.py
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
import os

def generate_launch_description():
    # Get parameter file path
    params_file = PathJoinSubstitution([
        FindPackageShare('my_robot_package'),
        'config',
        'params.yaml'
    ])

    return LaunchDescription([
        Node(
            package='my_robot_package',
            executable='my_robot_node',
            name='robot_controller',
            parameters=[params_file],
            output='screen'
        ),

        # Alternative: Load from file path directly
        Node(
            package='my_robot_package',
            executable='sensor_processor',
            name='sensor_processor',
            parameters=[os.path.join(
                FindPackageShare('my_robot_package').find('my_robot_package'),
                'config',
                'sensors.yaml'
            )],
            output='screen'
        )
    ])
```

### Parameter Validation in Nodes

```python
# my_robot_package/parameter_node.py
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node

class ParameterNode(Node):
    def __init__(self):
        super().__init__('parameter_node')

        # Declare parameters with default values
        self.declare_parameter('robot_name', 'default_robot')
        self.declare_parameter('control_frequency', 50)
        self.declare_parameter('linear_velocity_limit', 1.0)

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.parameters_callback)

        # Initialize with current parameter values
        self.update_parameters()

    def parameters_callback(self, parameters):
        """Validate parameter changes"""
        for param in parameters:
            if param.name == 'control_frequency':
                if param.value <= 0 or param.value > 1000:
                    return SetParametersResult(successful=False)

            if param.name == 'linear_velocity_limit':
                if param.value <= 0 or param.value > 5.0:
                    return SetParametersResult(successful=False)

        # Update local values if validation passes
        self.update_parameters()
        return SetParametersResult(successful=True)

    def update_parameters(self):
        """Update local variables from parameter values"""
        self.robot_name = self.get_parameter('robot_name').value
        self.control_frequency = self.get_parameter('control_frequency').value
        self.linear_velocity_limit = self.get_parameter('linear_velocity_limit').value

def main(args=None):
    rclpy.init(args=args)
    node = ParameterNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

## 2.8 Integration in Humanoid Robotics Systems

### Humanoid Robot Package Architecture

Humanoid robotics systems require specialized package organization to handle the complexity of multiple sensors, actuators, and control systems.

```
Humanoid Robot Package Hierarchy
┌─────────────────────────────────────────┐
│           Main Robot Package            │
├─────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Perception │  │   Navigation     │  │
│  │   Package   │  │    Package       │  │
│  │             │  │                  │  │
│  │ • Vision    │  │ • Path Planning  │  │
│  │ • IMU       │  │ • Local Planner  │  │
│  │ • Force     │  │ • Global Planner │  │
│  └─────────────┘  └──────────────────┘  │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │  Control    │  │   Simulation     │  │
│  │   Package   │  │    Package       │  │
│  │             │  │                  │  │
│  │ • Balance   │  │ • Gazebo Models  │  │
│  │ • Walk      │  │ • Physics Config │  │
│  │ • Gesture   │  │ • Sensors        │  │
│  └─────────────┘  └──────────────────┘  │
└─────────────────────────────────────────┘
```

### Example Humanoid Robot Package

```python
# my_humonoid_robot/my_humonoid_controller.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import math

class HumonoidController(Node):
    def __init__(self):
        super().__init__('humonoid_controller')

        # Joint state publisher
        self.joint_state_publisher = self.create_publisher(
            JointState, 'joint_states', 10)

        # Joint command publisher
        self.joint_command_publisher = self.create_publisher(
            JointTrajectory, 'joint_trajectory', 10)

        # IMU subscriber
        self.imu_subscriber = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)

        # Velocity command subscriber
        self.velocity_subscriber = self.create_subscription(
            Twist, 'cmd_vel', self.velocity_callback, 10)

        # Parameters
        self.declare_parameter('control_frequency', 100)
        self.declare_parameter('balance_threshold', 0.1)

        # Timer for control loop
        control_frequency = self.get_parameter('control_frequency').value
        self.control_timer = self.create_timer(
            1.0 / control_frequency, self.control_loop)

        # Internal state
        self.imu_data = None
        self.target_velocity = Twist()
        self.joint_positions = {}

        self.get_logger().info('Humonoid Controller initialized')

    def imu_callback(self, msg):
        """Process IMU data for balance control"""
        self.imu_data = msg

        # Convert quaternion to Euler angles
        roll, pitch, yaw = self.quaternion_to_euler(
            msg.orientation.x,
            msg.orientation.y,
            msg.orientation.z,
            msg.orientation.w
        )

        # Check balance
        if abs(pitch) > self.get_parameter('balance_threshold').value:
            self.get_logger().warn(f'Balance threshold exceeded: pitch = {pitch:.3f}')

    def velocity_callback(self, msg):
        """Process velocity commands"""
        self.target_velocity = msg

    def control_loop(self):
        """Main control loop for humanoid robot"""
        if self.imu_data is None:
            return

        # Generate walking pattern based on target velocity
        trajectory = self.generate_walk_trajectory()
        self.joint_command_publisher.publish(trajectory)

        # Publish current joint states
        joint_state = self.get_current_joint_states()
        self.joint_state_publisher.publish(joint_state)

    def generate_walk_trajectory(self):
        """Generate walking trajectory for humanoid robot"""
        trajectory = JointTrajectory()
        trajectory.joint_names = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint',
            'left_shoulder_joint', 'left_elbow_joint',
            'right_shoulder_joint', 'right_elbow_joint'
        ]

        point = JointTrajectoryPoint()

        # Generate walking motion based on target velocity
        time_from_start = self.get_clock().now().nanoseconds / 1e9

        for i, joint_name in enumerate(trajectory.joint_names):
            # Walking pattern with phase offset
            amplitude = 0.1 if 'hip' in joint_name else 0.05
            frequency = 0.5 + abs(self.target_velocity.linear.x) * 0.5
            phase = i * math.pi / 4

            position = amplitude * math.sin(2 * math.pi * frequency * time_from_start + phase)
            point.positions.append(position)
            point.velocities.append(0.0)
            point.accelerations.append(0.0)

        point.time_from_start = Duration(sec=0, nanosec=10000000)  # 10ms
        trajectory.points.append(point)

        return trajectory

    def get_current_joint_states(self):
        """Get current joint states"""
        joint_state = JointState()
        joint_state.header.stamp = self.get_clock().now().to_msg()
        joint_state.name = [
            'left_hip_joint', 'left_knee_joint', 'left_ankle_joint',
            'right_hip_joint', 'right_knee_joint', 'right_ankle_joint'
        ]

        # For simulation, return current positions from trajectory
        # In real robot, this would come from encoders
        joint_state.position = [0.0] * len(joint_state.name)

        return joint_state

    def quaternion_to_euler(self, x, y, z, w):
        """Convert quaternion to Euler angles"""
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = math.atan2(sinr_cosp, cosr_cosp)

        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = math.copysign(math.pi / 2, sinp)
        else:
            pitch = math.asin(sinp)

        # Yaw (z-axis rotation)
        siny_cosp = 2 * (w * z + x * y)
        cosy_cosp = 1 - 2 * (y * y + z * z)
        yaw = math.atan2(siny_cosp, cosy_cosp)

        return roll, pitch, yaw

def main(args=None):
    rclpy.init(args=args)
    node = HumonoidController()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Humonoid Controller shutting down')
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### Humanoid Launch File

```python
# launch/humonoid_robot_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    # Launch arguments
    robot_name_launch_arg = DeclareLaunchArgument(
        'robot_name',
        default_value='humonoid_robot',
        description='Name of the humonoid robot'
    )

    use_sim_time_launch_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        choices=['true', 'false'],
        description='Use simulation time'
    )

    # Humonoid controller node
    humonoid_controller = Node(
        package='my_humonoid_robot',
        executable='humonoid_controller',
        name='humonoid_controller',
        parameters=[
            {'robot_name': LaunchConfiguration('robot_name')},
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
            PathJoinSubstitution([
                FindPackageShare('my_humonoid_robot'),
                'config',
                'humonoid_params.yaml'
            ])
        ],
        output='screen'
    )

    # Sensor processing node
    sensor_processor = Node(
        package='my_humonoid_robot',
        executable='sensor_processor',
        name='sensor_processor',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
        output='screen'
    )

    # Balance controller node
    balance_controller = Node(
        package='my_humonoid_robot',
        executable='balance_controller',
        name='balance_controller',
        parameters=[
            {'use_sim_time': LaunchConfiguration('use_sim_time')},
        ],
        output='screen'
    )

    return LaunchDescription([
        robot_name_launch_arg,
        use_sim_time_launch_arg,

        LogInfo(msg=['Starting humonoid robot system']),

        humonoid_controller,
        sensor_processor,
        balance_controller,
    ])
```

## 2.9 Best Practices for Package Development

### Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Package name | Lowercase with underscores | `my_robot_controller` |
| Node name | Lowercase with underscores | `robot_controller` |
| Topic name | Lowercase with forward slashes | `/cmd_vel`, `/sensor_data` |
| Parameter name | Lowercase with underscores | `robot_name`, `control_frequency` |

### Modular Architecture Principles

1. **Single Responsibility**: Each package should have one primary purpose
2. **Loose Coupling**: Packages should have minimal dependencies on each other
3. **High Cohesion**: Related functionality should be grouped within the same package
4. **Interface Stability**: Maintain stable interfaces between packages

### Scalability Considerations

```
Scalable Package Architecture
┌─────────────────────────────────────────┐
│        Core Package                     │
│  ┌─────────────────────────────────┐    │
│  │ • Message Definitions           │    │
│  │ • Service Definitions           │    │
│  │ • Action Definitions            │    │
│  │ • Common Utilities              │    │
│  └─────────────────────────────────┘    │
├─────────────────────────────────────────┤
│        Functional Packages              │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  │
│  │  Percep- │  │ Control │  │  Nav-   │  │
│  │  tion    │  │         │  │  igation│  │
│  │ Package  │  │ Package │  │ Package │  │
│  └─────────┘  └─────────┘  └─────────┘  │
├─────────────────────────────────────────┤
│        Application Package              │
│  ┌─────────────────────────────────┐    │
│  │ • Launch Files                  │    │
│  │ • Configuration Files           │    │
│  │ • Integration Code              │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

:::tip
Structure your packages in layers: core (messages/services), functional (specific capabilities), and application (integration and configuration).
:::

## 2.10 Complete Examples

### Python Node Example

```python
# my_robot_package/sensor_fusion_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan, Imu, JointState
from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
import numpy as np

class SensorFusionNode(Node):
    def __init__(self):
        super().__init__('sensor_fusion_node')

        # Subscribers for multiple sensor types
        self.laser_sub = self.create_subscription(
            LaserScan, 'scan', self.laser_callback, 10)
        self.imu_sub = self.create_subscription(
            Imu, 'imu/data', self.imu_callback, 10)
        self.joint_sub = self.create_subscription(
            JointState, 'joint_states', self.joint_callback, 10)

        # Publisher for fused sensor data
        self.fused_pub = self.create_publisher(
            Float32MultiArray, 'fused_sensor_data', 10)

        # Publisher for robot state
        self.state_pub = self.create_publisher(
            Twist, 'robot_state', 10)

        # Internal state storage
        self.laser_data = None
        self.imu_data = None
        self.joint_data = None

        # Parameters
        self.declare_parameter('fusion_frequency', 10)

        # Timer for fusion loop
        fusion_freq = self.get_parameter('fusion_frequency').value
        self.fusion_timer = self.create_timer(
            1.0 / fusion_freq, self.fusion_loop)

        self.get_logger().info('Sensor Fusion Node initialized')

    def laser_callback(self, msg):
        """Process laser scan data"""
        self.laser_data = msg

    def imu_callback(self, msg):
        """Process IMU data"""
        self.imu_data = msg

    def joint_callback(self, msg):
        """Process joint state data"""
        self.joint_data = msg

    def fusion_loop(self):
        """Main fusion loop"""
        if self.laser_data is not None and self.imu_data is not None:
            # Perform sensor fusion
            fused_data = self.perform_sensor_fusion()

            # Publish fused data
            fused_msg = Float32MultiArray()
            fused_msg.data = fused_data
            self.fused_pub.publish(fused_msg)

            # Publish robot state
            state_msg = self.calculate_robot_state()
            self.state_pub.publish(state_msg)

    def perform_sensor_fusion(self):
        """Perform sensor fusion algorithm"""
        # Example fusion: obstacle distance and orientation
        if self.laser_data.ranges:
            min_distance = min(self.laser_data.ranges)
        else:
            min_distance = float('inf')

        # Get orientation from IMU
        orientation = self.imu_data.orientation

        return [min_distance, orientation.x, orientation.y, orientation.z, orientation.w]

    def calculate_robot_state(self):
        """Calculate robot state from sensor data"""
        state = Twist()

        if self.laser_data and self.laser_data.ranges:
            # Simple obstacle avoidance based on laser data
            front_ranges = self.laser_data.ranges[:len(self.laser_data.ranges)//3]
            if front_ranges:
                min_front = min(front_ranges)
                if min_front < 1.0:  # Obstacle within 1m
                    state.linear.x = 0.0  # Stop
                    state.angular.z = 0.5  # Turn
                else:
                    state.linear.x = 0.5  # Move forward
                    state.angular.z = 0.0  # No turn

        return state

def main(args=None):
    rclpy.init(args=args)
    node = SensorFusionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Sensor Fusion Node shutting down')
    finally:
        node.destroy_node()
        rclpy.shutdown()
```

### C++ Node Example

```cpp
// src/path_planner_node.cpp
#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <nav_msgs/msg/path.hpp>
#include <sensor_msgs/msg/laser_scan.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <vector>
#include <cmath>

class PathPlannerNode : public rclcpp::Node
{
public:
    PathPlannerNode() : Node("path_planner_node")
    {
        // Publishers
        path_publisher_ = this->create_publisher<nav_msgs::msg::Path>("global_plan", 10);

        // Subscribers
        goal_subscriber_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
            "goal_pose", 10,
            std::bind(&PathPlannerNode::goal_callback, this, std::placeholders::_1));

        scan_subscriber_ = this->create_subscription<sensor_msgs::msg::LaserScan>(
            "scan", 10,
            std::bind(&PathPlannerNode::scan_callback, this, std::placeholders::_1));

        // Parameters
        this->declare_parameter("planner_frequency", 5.0);
        this->declare_parameter("max_plan_length", 100);

        // Timer
        double planner_freq = this->get_parameter("planner_frequency").as_double();
        planner_timer_ = this->create_wall_timer(
            std::chrono::milliseconds(static_cast<int>(1000.0 / planner_freq)),
            std::bind(&PathPlannerNode::planning_loop, this));

        RCLCPP_INFO(this->get_logger(), "Path Planner Node initialized");
    }

private:
    void goal_callback(const geometry_msgs::msg::PoseStamped::SharedPtr msg)
    {
        goal_pose_ = *msg;
        RCLCPP_INFO(this->get_logger(), "Received new goal: (%.2f, %.2f)",
                   msg->pose.position.x, msg->pose.position.y);
        plan_path();
    }

    void scan_callback(const sensor_msgs::msg::LaserScan::SharedPtr msg)
    {
        laser_scan_ = *msg;
    }

    void plan_path()
    {
        if (!goal_pose_.header.frame_id.empty()) {
            // Simple path planning - straight line to goal (with obstacle avoidance)
            auto path_msg = nav_msgs::msg::Path();
            path_msg.header.frame_id = "map";
            path_msg.header.stamp = this->now();

            // Generate path points
            geometry_msgs::msg::PoseStamped start_pose;
            start_pose.pose.position.x = 0.0;
            start_pose.pose.position.y = 0.0;
            start_pose.pose.orientation.w = 1.0;

            int max_points = this->get_parameter("max_plan_length").as_int();
            double step_size = 0.1;

            for (int i = 0; i < max_points; ++i) {
                double progress = static_cast<double>(i) / max_points;
                geometry_msgs::msg::PoseStamped pose;
                pose.pose.position.x = start_pose.pose.position.x +
                    progress * (goal_pose_.pose.position.x - start_pose.pose.position.x);
                pose.pose.position.y = start_pose.pose.position.y +
                    progress * (goal_pose_.pose.position.y - start_pose.pose.position.y);

                // Simple obstacle check
                if (is_path_clear(pose.pose.position)) {
                    pose.header.frame_id = "map";
                    pose.header.stamp = this->now();
                    path_msg.poses.push_back(pose);
                } else {
                    RCLCPP_WARN(this->get_logger(), "Path blocked at (%.2f, %.2f)",
                               pose.pose.position.x, pose.pose.position.y);
                    break;
                }
            }

            path_publisher_->publish(path_msg);
        }
    }

    bool is_path_clear(const geometry_msgs::msg::Point& point)
    {
        // Simple obstacle detection using laser scan
        if (laser_scan_.ranges.empty()) {
            return true; // No scan data, assume clear
        }

        // Check if point is within laser range
        double min_distance = 0.5; // Minimum safe distance
        for (const auto& range : laser_scan_.ranges) {
            if (range < min_distance) {
                return false; // Obstacle detected
            }
        }

        return true;
    }

    void planning_loop()
    {
        // Planning loop - could be used for continuous replanning
    }

    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_publisher_;
    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_subscriber_;
    rclcpp::Subscription<sensor_msgs::msg::LaserScan>::SharedPtr scan_subscriber_;
    rclcpp::TimerBase::SharedPtr planner_timer_;

    geometry_msgs::msg::PoseStamped goal_pose_;
    sensor_msgs::msg::LaserScan laser_scan_;
};

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PathPlannerNode>());
    rclcpp::shutdown();
    return 0;
}
```

## 2.11 Chapter Summary

This chapter has provided a comprehensive overview of ROS 2 packages, covering:

1. **Package Fundamentals**: Understanding what packages are and their role in ROS 2
2. **Directory Structure**: Standard organization of package files and directories
3. **Manifest Files**: Detailed explanation of `package.xml` and its fields
4. **Build Systems**: CMake configuration for C++ packages and Python setup
5. **Package Creation**: Using `ros2 pkg create` for efficient package generation
6. **Launch Systems**: Python-based launch files for node orchestration
7. **Parameter Management**: YAML configuration and runtime parameter handling
8. **Humanoid Integration**: Special considerations for humanoid robotics packages
9. **Best Practices**: Naming conventions, architecture, and scalability

These concepts form the foundation for creating well-structured, maintainable ROS 2 packages that can be effectively integrated into complex robotic systems, particularly humanoid robots with their unique requirements for sensor fusion, control, and coordination.

## 2.12 Exercises

### Exercise 1: Package Creation (Beginner)
Create a new ROS 2 package called `my_first_robot` with dependencies on `rclpy`, `std_msgs`, and `sensor_msgs`. Set up the basic structure with proper `package.xml` and `setup.py` files.

### Exercise 2: Node Implementation (Beginner)
Implement a simple ROS 2 node in Python that publishes random sensor data (temperature, humidity) to a topic called `sensor_data`. Include proper parameter handling for sensor update frequency.

### Exercise 3: Launch File Configuration (Intermediate)
Create a launch file that starts two nodes: a sensor simulator and a data processor. Configure parameters through a YAML file and include remapping of topics between the nodes.

### Exercise 4: C++ Package Integration (Intermediate)
Create a C++ package that includes a simple path planner node. Implement the necessary `CMakeLists.txt` configuration and demonstrate integration with a Python-based visualization node.

### Exercise 5: Parameter Validation (Advanced)
Implement a node with comprehensive parameter validation using callbacks. Include validation for numerical ranges, string patterns, and complex data structures. Test with various invalid parameter values.

## 2.13 Mini-Project: Complete Robot Package

Create a complete ROS 2 package for a simple mobile robot that includes:

- A sensor fusion node that combines data from multiple sensors
- A navigation node that plans paths and avoids obstacles
- A control node that executes motion commands
- Proper launch files for different operational modes
- YAML configuration files for all parameters
- Comprehensive `package.xml` with all necessary dependencies
- Unit tests for each node
- Proper documentation and README

The package should demonstrate all the concepts covered in this chapter and provide a working example of a modular, well-structured ROS 2 system suitable for humanoid robotics applications.

## Exercise Solutions

<details>
<summary>Click here to reveal Exercise 1 Solution: Package Creation</summary>

```bash
# Create a new ROS 2 package
ros2 pkg create --build-type ament_python my_first_robot \
  --dependencies rclpy std_msgs sensor_msgs geometry_msgs

# The command creates the following structure:
# my_first_robot/
# ├── my_first_robot/
# │   ├── __init__.py
# │   └── my_first_robot.py
# ├── test/
# │   ├── __init__.py
# │   ├── test_copyright.py
# │   ├── test_flake8.py
# │   └── test_pep257.py
# ├── package.xml
# ├── setup.cfg
# ├── setup.py
# └── README.md
```

```xml
<!-- package.xml -->
<?xml version="1.0"?>
<?xml-model href="http://download.ros.org/schema/package_format3.xsd" schematypens="http://www.w3.org/2001/XMLSchema"?>
<package format="3">
  <name>my_first_robot</name>
  <version>0.0.1</version>
  <description>Package for my first robot with sensor capabilities</description>
  <maintainer email="robotics@example.com">Robot Developer</maintainer>
  <license>Apache License 2.0</license>

  <depend>rclpy</depend>
  <depend>std_msgs</depend>
  <depend>sensor_msgs</depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

```python
# setup.py
from setuptools import find_packages, setup

package_name = 'my_first_robot'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Robot Developer',
    maintainer_email='robotics@example.com',
    description='Package for my first robot with sensor capabilities',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_publisher = my_first_robot.sensor_publisher:main',
        ],
    },
)
```

</details>

<details>
<summary>Click here to reveal Exercise 2 Solution: Node Implementation</summary>

```python
# my_first_robot/sensor_publisher.py
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from sensor_msgs.msg import Temperature, RelativeHumidity
import random

class SensorPublisher(Node):
    def __init__(self):
        super().__init__('sensor_publisher')

        # Create publishers
        self.temp_publisher = self.create_publisher(Temperature, 'temperature', 10)
        self.humidity_publisher = self.create_publisher(RelativeHumidity, 'humidity', 10)

        # Declare parameters
        self.declare_parameter('update_frequency', 1.0)
        self.declare_parameter('temperature_mean', 25.0)
        self.declare_parameter('temperature_stddev', 2.0)
        self.declare_parameter('humidity_mean', 50.0)
        self.declare_parameter('humidity_stddev', 10.0)

        # Get parameter values
        update_freq = self.get_parameter('update_frequency').value
        self.temp_mean = self.get_parameter('temperature_mean').value
        self.temp_stddev = self.get_parameter('temperature_stddev').value
        self.humidity_mean = self.get_parameter('humidity_mean').value
        self.humidity_stddev = self.get_parameter('humidity_stddev').value

        # Create timer
        self.timer = self.create_timer(1.0/update_freq, self.publish_sensor_data)

        self.get_logger().info(f'Sensor publisher initialized with {update_freq}Hz frequency')

    def publish_sensor_data(self):
        # Create and populate temperature message
        temp_msg = Temperature()
        temp_msg.header.stamp = self.get_clock().now().to_msg()
        temp_msg.header.frame_id = 'sensor_frame'
        temp_msg.temperature = random.gauss(self.temp_mean, self.temp_stddev)
        temp_msg.variance = self.temp_stddev ** 2

        # Create and populate humidity message
        humidity_msg = RelativeHumidity()
        humidity_msg.header.stamp = self.get_clock().now().to_msg()
        humidity_msg.header.frame_id = 'sensor_frame'
        humidity_msg.relative_humidity = max(0.0, min(1.0, random.gauss(self.humidity_mean/100.0, self.humidity_stddev/100.0)))
        humidity_msg.variance = (self.humidity_stddev/100.0) ** 2

        # Publish messages
        self.temp_publisher.publish(temp_msg)
        self.humidity_publisher.publish(humidity_msg)

        self.get_logger().info(f'Published: Temp={temp_msg.temperature:.2f}°C, Humidity={humidity_msg.relative_humidity*100:.2f}%')

def main(args=None):
    rclpy.init(args=args)
    sensor_publisher = SensorPublisher()

    try:
        rclpy.spin(sensor_publisher)
    except KeyboardInterrupt:
        sensor_publisher.get_logger().info('Shutting down sensor publisher')
    finally:
        sensor_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

</details>

<details>
<summary>Click here to reveal Exercise 3 Solution: Launch File Configuration</summary>

```python
# launch/sensor_processing_launch.py
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    # Declare launch arguments
    update_frequency_arg = DeclareLaunchArgument(
        'update_frequency',
        default_value='2.0',
        description='Sensor update frequency'
    )

    processing_rate_arg = DeclareLaunchArgument(
        'processing_rate',
        default_value='1.0',
        description='Data processing rate'
    )

    # Get launch configurations
    update_frequency = LaunchConfiguration('update_frequency')
    processing_rate = LaunchConfiguration('processing_rate')

    # Sensor simulator node
    sensor_simulator = Node(
        package='my_first_robot',
        executable='sensor_publisher',
        name='sensor_simulator',
        parameters=[
            {'update_frequency': update_frequency}
        ],
        remappings=[
            ('temperature', 'sensor_data/temperature'),
            ('humidity', 'sensor_data/humidity')
        ],
        output='screen'
    )

    # Data processor node
    data_processor = Node(
        package='my_first_robot',
        executable='data_processor',
        name='data_processor',
        parameters=[
            {'processing_rate': processing_rate}
        ],
        remappings=[
            ('input_temperature', 'sensor_data/temperature'),
            ('input_humidity', 'sensor_data/humidity'),
            ('processed_data', 'processed_sensor_data')
        ],
        output='screen'
    )

    return LaunchDescription([
        update_frequency_arg,
        processing_rate_arg,
        sensor_simulator,
        data_processor
    ])
```

```yaml
# config/sensor_params.yaml
sensor_simulator:
  ros__parameters:
    update_frequency: 2.0
    temperature_mean: 25.0
    temperature_stddev: 2.0
    humidity_mean: 50.0
    humidity_stddev: 10.0

data_processor:
  ros__parameters:
    processing_rate: 1.0
    temperature_threshold: 30.0
    humidity_threshold: 0.7
```

</details>

<details>
<summary>Click here to reveal Exercise 4 Solution: C++ Package Integration</summary>

```cpp
// include/path_planner.hpp
#ifndef PATH_PLANNER_HPP_
#define PATH_PLANNER_HPP_

#include <rclcpp/rclcpp.hpp>
#include <geometry_msgs/msg/pose_stamped.hpp>
#include <nav_msgs/msg/path.hpp>
#include <visualization_msgs/msg/marker.hpp>

class PathPlanner : public rclcpp::Node
{
public:
    PathPlanner();

private:
    void goalCallback(const geometry_msgs::msg::PoseStamped::SharedPtr msg);
    void publishPath();

    rclcpp::Subscription<geometry_msgs::msg::PoseStamped>::SharedPtr goal_subscriber_;
    rclcpp::Publisher<nav_msgs::msg::Path>::SharedPtr path_publisher_;
    rclcpp::Publisher<visualization_msgs::msg::Marker>::SharedPtr visualization_publisher_;

    geometry_msgs::msg::PoseStamped current_goal_;
    bool goal_received_;
};

#endif  // PATH_PLANNER_HPP_
```

```cpp
// src/path_planner.cpp
#include "path_planner.hpp"
#include <tf2/LinearMath/Quaternion.h>
#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>

PathPlanner::PathPlanner()
: Node("path_planner"), goal_received_(false)
{
    goal_subscriber_ = this->create_subscription<geometry_msgs::msg::PoseStamped>(
        "goal_pose", 10, std::bind(&PathPlanner::goalCallback, this, std::placeholders::_1));

    path_publisher_ = this->create_publisher<nav_msgs::msg::Path>("planned_path", 10);
    visualization_publisher_ = this->create_publisher<visualization_msgs::msg::Marker>(
        "path_visualization", 10);

    RCLCPP_INFO(this->get_logger(), "Path planner node initialized");
}

void PathPlanner::goalCallback(const geometry_msgs::msg::PoseStamped::SharedPtr msg)
{
    current_goal_ = *msg;
    goal_received_ = true;
    RCLCPP_INFO(this->get_logger(),
                "Received goal: (%.2f, %.2f)",
                msg->pose.position.x, msg->pose.position.y);

    publishPath();
}

void PathPlanner::publishPath()
{
    if (!goal_received_) return;

    nav_msgs::msg::Path path_msg;
    path_msg.header.frame_id = "map";
    path_msg.header.stamp = this->now();

    // Simple straight-line path (in real implementation, use proper path planning)
    geometry_msgs::msg::PoseStamped pose;
    pose.header = path_msg.header;
    pose.pose.position.x = 0.0;  // Start at origin
    pose.pose.position.y = 0.0;
    pose.pose.position.z = 0.0;
    path_msg.poses.push_back(pose);

    // Add intermediate points toward goal
    int num_points = 10;
    for (int i = 1; i <= num_points; ++i) {
        double ratio = static_cast<double>(i) / num_points;
        pose.pose.position.x = ratio * current_goal_.pose.position.x;
        pose.pose.position.y = ratio * current_goal_.pose.position.y;

        path_msg.poses.push_back(pose);
    }

    path_publisher_->publish(path_msg);
    RCLCPP_INFO(this->get_logger(), "Published planned path with %zu points", path_msg.poses.size());

    // Publish visualization marker
    visualization_msgs::msg::Marker marker;
    marker.header.frame_id = "map";
    marker.header.stamp = this->now();
    marker.ns = "path";
    marker.id = 0;
    marker.type = visualization_msgs::msg::Marker::LINE_STRIP;
    marker.action = visualization_msgs::msg::Marker::ADD;
    marker.pose.orientation.w = 1.0;
    marker.scale.x = 0.05;  // Line width
    marker.color.r = 1.0;
    marker.color.g = 0.0;
    marker.color.b = 0.0;
    marker.color.a = 1.0;

    for (const auto& pose_stamped : path_msg.poses) {
        marker.points.push_back(pose_stamped.pose.position);
    }

    visualization_publisher_->publish(marker);
}

int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PathPlanner>());
    rclcpp::shutdown();
    return 0;
}
```

```cmake
# CMakeLists.txt
cmake_minimum_required(VERSION 3.8)
project(robot_path_planner)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

# Include directories
include_directories(include)

# Create executable
add_executable(path_planner src/path_planner.cpp)
ament_target_dependencies(path_planner
  rclcpp
  geometry_msgs
  nav_msgs
  visualization_msgs)

# Install executables
install(TARGETS
  path_planner
  DESTINATION lib/${PROJECT_NAME})

ament_package()
```

</details>

<details>
<summary>Click here to reveal Exercise 5 Solution: Parameter Validation</summary>

```python
# my_first_robot/parameter_validation_node.py
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import ParameterDescriptor, ParameterType, SetParametersResult
import re

class ParameterValidationNode(Node):
    def __init__(self):
        super().__init__('parameter_validation_node')

        # Declare parameters with descriptors
        self.declare_parameter(
            'robot_name',
            'default_robot',
            ParameterDescriptor(
                type=ParameterType.PARAMETER_STRING,
                description='Name of the robot (alphanumeric and underscore only)'
            )
        )

        self.declare_parameter(
            'control_frequency',
            50.0,
            ParameterDescriptor(
                type=ParameterType.PARAMETER_DOUBLE,
                description='Control loop frequency in Hz (1.0 to 1000.0)',
                floating_point_range=[{"from_value": 1.0, "to_value": 1000.0, "step": 0.1}]
            )
        )

        self.declare_parameter(
            'safety_limits.max_velocity',
            1.0,
            ParameterDescriptor(
                type=ParameterType.PARAMETER_DOUBLE,
                description='Maximum allowed velocity (positive values only)',
                floating_point_range=[{"from_value": 0.0, "to_value": 10.0, "step": 0.01}]
            )
        )

        # Add parameter callback for validation
        self.add_on_set_parameters_callback(self.validate_parameters)

        # Get initial parameter values
        self.robot_name = self.get_parameter('robot_name').value
        self.control_frequency = self.get_parameter('control_frequency').value
        self.max_velocity = self.get_parameter('safety_limits.max_velocity').value

        self.get_logger().info(f'Initialized with robot_name: {self.robot_name}')
        self.get_logger().info(f'Control frequency: {self.control_frequency}Hz')
        self.get_logger().info(f'Max velocity: {self.max_velocity}m/s')

    def validate_parameters(self, parameters):
        """
        Validate parameters before they are set
        """
        result = SetParametersResult()
        result.successful = True
        result.reason = 'All parameters validated successfully'

        for param in parameters:
            if param.name == 'robot_name':
                # Validate robot name (alphanumeric and underscore only)
                if not re.match(r'^[a-zA-Z0-9_]+$', param.value):
                    result.successful = False
                    result.reason = f'Robot name must contain only alphanumeric characters and underscores: {param.value}'
                    return result

            elif param.name == 'control_frequency':
                # Validate control frequency range
                if param.value < 1.0 or param.value > 1000.0:
                    result.successful = False
                    result.reason = f'Control frequency must be between 1.0 and 1000.0 Hz: {param.value}'
                    return result

            elif param.name == 'safety_limits.max_velocity':
                # Validate max velocity (must be positive)
                if param.value <= 0.0 or param.value > 10.0:
                    result.successful = False
                    result.reason = f'Max velocity must be positive and <= 10.0: {param.value}'
                    return result

        return result

def main(args=None):
    import rclpy
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