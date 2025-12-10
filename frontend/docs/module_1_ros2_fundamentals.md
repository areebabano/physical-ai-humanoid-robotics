---
sidebar_position: 1
title: "Module 1: Robotic Nervous System (ROS 2)"
---

# Module 1: Robotic Nervous System (ROS 2)

## Overview
Welcome to the first module of the Physical AI & Humanoid Robotics Textbook! In this module, you'll learn about ROS 2 (Robot Operating System 2), which serves as the nervous system for robots. ROS 2 provides the communication framework that allows different parts of a robot to work together seamlessly.

## Learning Objectives
By the end of this module, you will be able to:
- Understand the fundamental concepts of ROS 2 architecture
- Install and configure ROS 2 on your development environment
- Create and run basic ROS 2 nodes, topics, and services
- Implement message passing between different robot components
- Use ROS 2 tools for debugging and visualization
- Build simple robot applications using ROS 2

## Table of Contents
1. [Introduction to ROS 2](#introduction-to-ros-2)
2. [ROS 2 Architecture](#ros-2-architecture)
3. [Installation and Setup](#installation-and-setup)
4. [Nodes, Topics, and Services](#nodes-topics-and-services)
5. [ROS 2 Tools](#ros-2-tools)
6. [Hands-on Exercises](#hands-on-exercises)
7. [Module Summary](#module-summary)

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is not an actual operating system, but rather a middleware framework that provides services designed for a heterogeneous computer cluster. It includes hardware abstraction, device drivers, libraries, visualizers, message-passing, package management, and more.

### Key Features of ROS 2
- **Distributed Computing**: Enables communication between processes running on different machines
- **Package Management**: Organizes code into reusable packages
- **Message Passing**: Provides a communication mechanism between nodes
- **Tool Ecosystem**: Rich set of tools for development, debugging, and visualization
- **Language Support**: Supports multiple programming languages (C++, Python, etc.)

### Why ROS 2?
ROS 2 is an evolution of the original ROS with improvements in:
- Security and authentication
- Real-time support
- Multi-robot systems
- Commercial deployment capabilities

## ROS 2 Architecture

The ROS 2 architecture is built around several core concepts:

### Nodes
A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are organized into packages to form a ROS 2 system.

### Topics
Topics are named buses over which nodes exchange messages. Publishers send messages to topics, and subscribers receive messages from topics.

### Services
Services provide a request/response communication pattern, where a client sends a request and receives a response from a server.

### Actions
Actions are a more complex communication pattern that includes goals, feedback, and results.

## Installation and Setup

### System Requirements
- Ubuntu 22.04 (recommended) or Windows 10/11 with WSL2
- Python 3.8 or higher
- At least 4GB RAM (8GB recommended)

### Installation Steps
1. Update your system packages
2. Set up your ROS 2 environment
3. Install the ROS 2 distribution (Humble Hawksbill recommended)

```bash
# Update system packages
sudo apt update

# Install ROS 2 Humble
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install ros-humble-desktop
```

## Nodes, Topics, and Services

### Creating a Simple Node

Here's an example of a basic ROS 2 node in Python:

```python
import rclpy
from rclpy.node import Node

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## ROS 2 Tools

### Common Tools
- `ros2 run`: Run a node
- `ros2 topic`: Work with topics
- `ros2 service`: Work with services
- `rqt`: Graphical user interface
- `rviz2`: 3D visualization tool

## Hands-on Exercises

### Exercise 1: Create Your First ROS 2 Package
Create a new ROS 2 package called `my_robot_bringup` and implement a simple publisher node.

### Exercise 2: Topic Communication
Create a publisher and subscriber that communicate sensor data between nodes.

### Exercise 3: Service Implementation
Implement a service that calculates the distance between two points.

## Module Summary

In this module, you've learned the fundamentals of ROS 2, including its architecture, installation process, and core communication patterns. You've created your first ROS 2 nodes and worked with topics and services. This foundation will be essential as you progress through the textbook and work with more complex robotic systems.

The next module will focus on simulation environments where you can test your ROS 2 applications in virtual worlds before deploying them on real robots.