---
title: "Module 4.3 - Chapter 3: Whole-Body Control"
sidebar_position: 3
---

# Module 4.3 - Whole-Body Control

## Overview

Whole-body control is a critical aspect of humanoid robotics that involves coordinating the motion of all robot joints simultaneously to achieve complex tasks while maintaining balance and stability. This chapter explores various whole-body control strategies, including kinematic and dynamic approaches, and their implementation for coordinated multi-limb motion in humanoid robots.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the principles of whole-body control for humanoid robots
- Implement kinematic and dynamic control approaches
- Design controllers for coordinated multi-limb motion
- Apply whole-body control for complex manipulation and locomotion tasks
- Integrate balance and manipulation in whole-body control frameworks
- Implement control hierarchies for multi-task coordination

## Introduction to Whole-Body Control

Whole-body control addresses the challenge of coordinating all degrees of freedom in a humanoid robot to achieve multiple simultaneous objectives such as balance maintenance, manipulation, and locomotion. Unlike separate control of individual limbs, whole-body control considers the entire robot as a coupled system.

### Challenges in Whole-Body Control

1. **Redundancy**: Humanoid robots typically have more degrees of freedom than required for a task
2. **Constraints**: Joint limits, torque limits, and environmental constraints
3. **Multi-objective optimization**: Balancing competing objectives (e.g., reaching and balancing)
4. **Real-time performance**: Computing control commands at high frequencies
5. **Stability**: Maintaining balance while performing complex motions

### Control Architecture

The typical whole-body control architecture follows a hierarchy:

```
High-Level Planner
        ↓
Task-Space Controllers (Cartesian, Joint-space)
        ↓
Inverse Kinematics/Dynamics
        ↓
Low-Level Joint Controllers
        ↓
Actuators
```

## Mathematical Foundations

### Kinematic Model

For a humanoid robot with n joints, the forward kinematics is given by:

```
x = f(q)
```

Where:
- x ∈ ℝ^m is the task space position
- q ∈ ℝ^n is the joint space position
- f: ℝ^n → ℝ^m is the forward kinematics function

The relationship between joint velocities and task velocities is:

```
ẋ = J(q)q̇
```

Where J(q) is the Jacobian matrix.

### Dynamic Model

The equation of motion for a humanoid robot is:

```
M(q)q̈ + C(q,q̇)q̇ + g(q) = τ + J^T(q)F
```

Where:
- M(q): Inertia matrix
- C(q,q̇): Coriolis and centrifugal forces
- g(q): Gravity vector
- τ: Joint torques
- J^T(q)F: External forces in joint space
- F: External forces in task space

## Whole-Body Control Approaches

### Task-Priority Framework

```python
import numpy as np
from scipy.linalg import null_space, qr
import cvxpy as cp

class TaskPriorityController:
    """
    Whole-body controller using task-priority framework.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.n_joints = robot_model.n_joints

        # Task weights and priorities
        self.task_weights = {}
        self.task_priorities = {}

        # Active tasks
        self.active_tasks = []

    def add_task(self, task_name, jacobian, desired_value, weight=1.0, priority=0):
        """
        Add a task to the controller.
        """
        task = {
            'name': task_name,
            'jacobian': jacobian,
            'desired': desired_value,
            'weight': weight,
            'priority': priority
        }

        self.active_tasks.append(task)
        self.active_tasks.sort(key=lambda x: x['priority'], reverse=True)

    def compute_control(self, current_q, current_qdot):
        """
        Compute whole-body control using task-priority framework.
        """
        # Initialize solution
        qdot_solution = np.zeros(self.n_joints)

        # Process tasks by priority
        for task in self.active_tasks:
            # Get current task value
            current_task_value = self.robot_model.forward_kinematics(
                current_q, task['name']
            )

            # Compute task error
            error = task['desired'] - current_task_value

            # Get task Jacobian
            J_task = task['jacobian']

            # Compute null space of higher priority tasks
            N_previous = self.compute_null_space(qdot_solution)

            # Compute weighted pseudo-inverse
            W = np.eye(self.n_joints) * task['weight']
            J_weighted = W @ J_task.T @ np.linalg.inv(J_task @ W @ J_task.T + 1e-6 * np.eye(len(error)))

            # Compute task contribution
            task_contribution = J_weighted @ (error + 0.1 * J_task @ current_qdot)  # With damping

            # Project to null space of higher priority tasks
            task_contribution = N_previous @ task_contribution

            # Add to solution
            qdot_solution += task_contribution

        return qdot_solution

    def compute_null_space(self, solution):
        """
        Compute null space projection matrix.
        """
        # For simplicity, returning identity
        # In practice, this would compute null space of higher priority tasks
        return np.eye(self.n_joints)

    def compute_reaction_forces(self, q, qdot, external_forces):
        """
        Compute reaction forces at contact points.
        """
        # Compute mass matrix
        M = self.robot_model.mass_matrix(q)

        # Compute Coriolis and gravity terms
        C = self.robot_model.coriolis_matrix(q, qdot)
        g = self.robot_model.gravity_vector(q)

        # Compute joint accelerations
        qddot = np.linalg.solve(M, -C @ qdot - g + external_forces)

        return qddot

class WholeBodyController:
    """
    Complete whole-body controller integrating multiple control objectives.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.n_joints = robot_model.n_joints

        # Initialize task controllers
        self.com_controller = ComController(robot_model)
        self.arm_controller = ArmController(robot_model)
        self.leg_controller = LegController(robot_model)
        self.trunk_controller = TrunkController(robot_model)

        # Task weights
        self.task_weights = {
            'balance': 1.0,
            'manipulation': 0.8,
            'locomotion': 0.6,
            'posture': 0.3
        }

        # Contact information
        self.contact_points = []
        self.support_polygon = None

    def update_contacts(self, contact_info):
        """
        Update contact information.
        """
        self.contact_points = contact_info['contact_points']
        self.support_polygon = contact_info['support_polygon']

    def compute_control(self, state, tasks):
        """
        Compute whole-body control commands.
        """
        # Extract state
        q = state['joint_positions']
        qdot = state['joint_velocities']
        com_pos = state['com_position']
        com_vel = state['com_velocity']

        # Initialize joint velocity command
        qdot_cmd = np.zeros(self.n_joints)

        # Balance control (highest priority)
        if 'balance' in tasks:
            balance_cmd = self.com_controller.compute_balance_command(
                com_pos, com_vel, self.support_polygon
            )
            qdot_cmd += balance_cmd * self.task_weights['balance']

        # Manipulation tasks
        if 'manipulation' in tasks:
            manip_cmd = self.arm_controller.compute_manipulation_command(
                tasks['manipulation']
            )
            qdot_cmd += manip_cmd * self.task_weights['manipulation']

        # Locomotion tasks
        if 'locomotion' in tasks:
            loco_cmd = self.leg_controller.compute_locomotion_command(
                tasks['locomotion']
            )
            qdot_cmd += loco_cmd * self.task_weights['locomotion']

        # Posture regulation (lowest priority)
        if 'posture' in tasks:
            posture_cmd = self.trunk_controller.compute_posture_command(
                tasks['posture'], q
            )
            qdot_cmd += posture_cmd * self.task_weights['posture']

        # Apply joint limits
        qdot_cmd = self.apply_joint_limits(q, qdot_cmd)

        return qdot_cmd

    def apply_joint_limits(self, q, qdot_cmd):
        """
        Apply joint limits to velocity commands.
        """
        # Get joint limits
        q_min = self.robot_model.joint_limits['min']
        q_max = self.robot_model.joint_limits['max']

        # Apply soft limits near boundaries
        for i in range(self.n_joints):
            if q[i] > q_max[i] - 0.1:  # Near upper limit
                qdot_cmd[i] = min(qdot_cmd[i], 0)
            elif q[i] < q_min[i] + 0.1:  # Near lower limit
                qdot_cmd[i] = max(qdot_cmd[i], 0)

        return qdot_cmd

class ComController:
    """
    Center of Mass controller for balance.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.com_height = 0.8  # Default CoM height
        self.gravity = 9.81
        self.omega = np.sqrt(self.gravity / self.com_height)

        # Control gains
        self.kp = 10.0
        self.kd = 2.0

    def compute_balance_command(self, current_com, current_com_vel, support_polygon):
        """
        Compute balance control command based on CoM state.
        """
        # Calculate current ZMP
        current_zmp = self.compute_zmp(current_com, current_com_vel)

        # Calculate desired ZMP (inside support polygon)
        desired_zmp = self.calculate_desired_zmp(current_zmp, support_polygon)

        # Compute CoM control
        com_error = desired_zmp[:2] - current_com[:2]
        com_vel_error = -current_com_vel[:2]

        com_acc = self.kp * com_error + self.kd * com_vel_error

        # Convert to joint space using Jacobian
        com_jacobian = self.robot_model.get_com_jacobian()

        # Pseudo-inverse for control
        J_pinv = np.linalg.pinv(com_jacobian)
        qddot_cmd = J_pinv @ np.concatenate([com_acc, [0]])  # Add zero for z acceleration

        return qddot_cmd

    def compute_zmp(self, com_pos, com_vel):
        """
        Compute Zero Moment Point from CoM state.
        """
        zmp_x = com_pos[0] - com_vel[0] / self.omega
        zmp_y = com_pos[1] - com_vel[1] / self.omega

        return np.array([zmp_x, zmp_y, 0])

    def calculate_desired_zmp(self, current_zmp, support_polygon):
        """
        Calculate desired ZMP inside support polygon.
        """
        if support_polygon is None:
            return current_zmp

        # Simple projection to keep ZMP inside support polygon
        desired_zmp = current_zmp.copy()

        # Project to support polygon bounds
        desired_zmp[0] = np.clip(current_zmp[0],
                                support_polygon['x_min'],
                                support_polygon['x_max'])
        desired_zmp[1] = np.clip(current_zmp[1],
                                support_polygon['y_min'],
                                support_polygon['y_max'])

        return desired_zmp

class ArmController:
    """
    Arm controller for manipulation tasks.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.left_arm_chain = robot_model.get_chain('left_arm')
        self.right_arm_chain = robot_model.get_chain('right_arm')

    def compute_manipulation_command(self, manipulation_tasks):
        """
        Compute manipulation commands for arms.
        """
        qdot_cmd = np.zeros(self.robot_model.n_joints)

        for task in manipulation_tasks:
            arm_name = task['arm']
            target_pose = task['target_pose']
            task_type = task['task_type']  # 'position', 'orientation', 'pose'

            if arm_name == 'left':
                chain = self.left_arm_chain
                arm_indices = self.robot_model.left_arm_indices
            elif arm_name == 'right':
                chain = self.right_arm_chain
                arm_indices = self.robot_model.right_arm_indices
            else:
                continue

            # Compute Jacobian for the task
            jacobian = self.robot_model.get_jacobian(chain, target_pose)

            # Compute task error
            current_pose = self.robot_model.get_end_effector_pose(chain)
            error = self.compute_pose_error(current_pose, target_pose, task_type)

            # Compute joint velocities using inverse kinematics
            J_pinv = np.linalg.pinv(jacobian)
            arm_qdot = J_pinv @ error

            # Apply to full joint vector
            qdot_cmd[arm_indices] = arm_qdot

        return qdot_cmd

    def compute_pose_error(self, current_pose, target_pose, task_type):
        """
        Compute pose error for manipulation task.
        """
        if task_type == 'position':
            error = target_pose[:3] - current_pose[:3]
        elif task_type == 'orientation':
            # Compute orientation error using quaternion difference
            current_quat = current_pose[3:]
            target_quat = target_pose[3:]
            error = self.quaternion_error(current_quat, target_quat)
        else:  # pose
            pos_error = target_pose[:3] - current_pose[:3]
            quat_error = self.quaternion_error(current_pose[3:], target_pose[3:])
            error = np.concatenate([pos_error, quat_error])

        return error

    def quaternion_error(self, q1, q2):
        """
        Compute error between two quaternions.
        """
        # Convert quaternion difference to angle-axis
        q_diff = self.quaternion_multiply(
            self.quaternion_inverse(q1),
            q2
        )

        # Convert to axis-angle representation
        angle = 2 * np.arccos(np.abs(q_diff[0]))
        if angle > 1e-6:  # Avoid division by zero
            axis = q_diff[1:] / np.sin(angle/2) * np.sign(q_diff[0])
        else:
            axis = np.zeros(3)

        return axis

    def quaternion_multiply(self, q1, q2):
        """
        Multiply two quaternions.
        """
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2

        return np.array([w, x, y, z])

    def quaternion_inverse(self, q):
        """
        Compute quaternion inverse.
        """
        return np.array([q[0], -q[1], -q[2], -q[3]])

class LegController:
    """
    Leg controller for locomotion tasks.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.left_leg_chain = robot_model.get_chain('left_leg')
        self.right_leg_chain = robot_model.get_chain('right_leg')

    def compute_locomotion_command(self, locomotion_tasks):
        """
        Compute locomotion commands for legs.
        """
        qdot_cmd = np.zeros(self.robot_model.n_joints)

        for task in locomotion_tasks:
            leg_name = task['leg']
            target_foot_pose = task['target_foot_pose']
            task_type = task['task_type']  # 'stepping', 'stance', 'sway'

            if leg_name == 'left':
                chain = self.left_leg_chain
                leg_indices = self.robot_model.left_leg_indices
            elif leg_name == 'right':
                chain = self.right_leg_chain
                leg_indices = self.robot_model.right_leg_indices
            else:
                continue

            # Compute Jacobian for foot
            jacobian = self.robot_model.get_jacobian(chain, target_foot_pose)

            # Compute task error
            current_foot_pose = self.robot_model.get_end_effector_pose(chain)
            error = self.compute_pose_error(current_foot_pose, target_foot_pose)

            # Compute joint velocities
            J_pinv = np.linalg.pinv(jacobian)
            leg_qdot = J_pinv @ error

            # Apply to full joint vector
            qdot_cmd[leg_indices] = leg_qdot

        return qdot_cmd

    def compute_pose_error(self, current_pose, target_pose):
        """
        Compute pose error for leg task.
        """
        pos_error = target_pose[:3] - current_pose[:3]
        return pos_error

class TrunkController:
    """
    Trunk controller for posture regulation.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.trunk_indices = robot_model.trunk_indices

        # Desired posture parameters
        self.desired_trunk_orientation = np.array([0, 0, 0, 1])  # Identity quaternion
        self.desired_joint_positions = np.zeros(len(self.trunk_indices))

    def compute_posture_command(self, posture_tasks, current_q):
        """
        Compute posture regulation command.
        """
        qdot_cmd = np.zeros(self.robot_model.n_joints)

        # Get current trunk state
        current_trunk_q = current_q[self.trunk_indices]

        # Compute posture error
        posture_error = self.desired_joint_positions - current_trunk_q

        # Add orientation regulation
        current_trunk_orient = self.robot_model.get_trunk_orientation(current_q)
        orient_error = self.compute_orientation_error(
            current_trunk_orient, self.desired_trunk_orientation
        )

        # Combine errors
        combined_error = np.concatenate([posture_error, orient_error])

        # Apply proportional control
        kp = 1.0
        trunk_qdot = kp * combined_error

        # Apply to full joint vector
        qdot_cmd[self.trunk_indices] = trunk_qdot

        return qdot_cmd

    def compute_orientation_error(self, current_orient, desired_orient):
        """
        Compute orientation error for trunk.
        """
        # Similar to arm controller
        q_diff = self.quaternion_multiply(
            self.quaternion_inverse(current_orient),
            desired_orient
        )

        angle = 2 * np.arccos(np.abs(q_diff[0]))
        if angle > 1e-6:
            axis = q_diff[1:] / np.sin(angle/2) * np.sign(q_diff[0])
        else:
            axis = np.zeros(3)

        return axis

    def quaternion_multiply(self, q1, q2):
        """
        Multiply two quaternions.
        """
        w1, x1, y1, z1 = q1
        w2, x2, y2, z2 = q2

        w = w1*w2 - x1*x2 - y1*y2 - z1*z2
        x = w1*x2 + x1*w2 + y1*z2 - z1*y2
        y = w1*y2 - x1*z2 + y1*w2 + z1*x2
        z = w1*z2 + x1*y2 - y1*x2 + z1*w2

        return np.array([w, x, y, z])

    def quaternion_inverse(self, q):
        """
        Compute quaternion inverse.
        """
        return np.array([q[0], -q[1], -q[2], -q[3]])
```

## Inverse Kinematics Solutions

### Closed-Form Inverse Kinematics

```python
class ClosedFormIK:
    """
    Closed-form inverse kinematics for humanoid limbs.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model

    def solve_arm_ik(self, target_pose, arm_type='left', current_q=None):
        """
        Solve inverse kinematics for 7-DOF arm using closed-form solution.
        """
        # Extract target position and orientation
        target_pos = target_pose[:3]
        target_orient = target_pose[3:]

        # Get arm link lengths
        l_shoulder = self.robot_model.link_lengths[f'{arm_type}_shoulder']
        l_upper_arm = self.robot_model.link_lengths[f'{arm_type}_upper_arm']
        l_forearm = self.robot_model.link_lengths[f'{arm_type}_forearm']
        l_hand = self.robot_model.link_lengths[f'{arm_type}_hand']

        # Solve for shoulder position (elbow position based on target)
        # For 7-DOF arm, we have redundancy that can be used for elbow positioning

        # Calculate elbow position based on target and preferred orientation
        elbow_pos = self.calculate_elbow_position(target_pos, target_orient,
                                                 l_upper_arm, l_forearm)

        # Solve shoulder to elbow
        shoulder_angles = self.solve_shoulder_to_elbow(
            target_pos, elbow_pos, l_shoulder, l_upper_arm
        )

        # Solve elbow to wrist
        elbow_angles = self.solve_elbow_to_wrist(
            elbow_pos, target_pos, l_forearm
        )

        # Solve wrist orientation
        wrist_angles = self.solve_wrist_orientation(target_orient)

        # Combine all angles
        solution = np.concatenate([shoulder_angles, elbow_angles, wrist_angles])

        return solution

    def calculate_elbow_position(self, target_pos, target_orient, l_upper_arm, l_forearm):
        """
        Calculate elbow position for 7-DOF arm.
        """
        # For a 7-DOF arm, we can choose elbow position along a plane
        # This provides redundancy for obstacle avoidance or posture optimization

        # Calculate elbow position along the plane perpendicular to the vector
        # from shoulder to wrist
        shoulder_pos = self.robot_model.get_shoulder_position()
        vec_shoulder_to_wrist = target_pos - shoulder_pos
        vec_norm = np.linalg.norm(vec_shoulder_to_wrist)

        if vec_norm > l_upper_arm + l_forearm:
            # Elbow is stretched
            elbow_pos = shoulder_pos + (vec_shoulder_to_wrist / vec_norm) * l_upper_arm
        elif vec_norm < abs(l_upper_arm - l_forearm):
            # Elbow is folded back
            elbow_pos = shoulder_pos + (vec_shoulder_to_wrist / vec_norm) * l_upper_arm * 0.9
        else:
            # Standard configuration - choose based on preferred orientation
            # This is a simplified approach
            elbow_pos = shoulder_pos + (vec_shoulder_to_wrist / vec_norm) * l_upper_arm * 0.7

        return elbow_pos

    def solve_shoulder_to_elbow(self, target_pos, elbow_pos, l_shoulder, l_upper_arm):
        """
        Solve for shoulder and upper arm joint angles.
        """
        # This is a simplified 3-DOF shoulder solution
        # In practice, would need to consider the full kinematic chain
        return np.zeros(3)  # Placeholder

    def solve_elbow_to_wrist(self, elbow_pos, target_pos, l_forearm):
        """
        Solve for elbow and forearm joint angles.
        """
        # This is a simplified 2-DOF elbow solution
        return np.zeros(2)  # Placeholder

    def solve_wrist_orientation(self, target_orient):
        """
        Solve for wrist orientation angles.
        """
        # Convert quaternion to Euler angles for wrist joints
        # This is a simplified approach
        return np.zeros(2)  # Assuming 2-DOF wrist

class NumericalIK:
    """
    Numerical inverse kinematics using iterative methods.
    """

    def __init__(self, robot_model, max_iterations=100, tolerance=1e-4):
        self.robot_model = robot_model
        self.max_iterations = max_iterations
        self.tolerance = tolerance

    def solve_ik(self, target_pose, current_q, chain_name, weights=None):
        """
        Solve inverse kinematics using iterative method (Jacobian transpose/pseudo-inverse).
        """
        if weights is None:
            weights = np.ones(len(current_q))

        q = current_q.copy()

        for i in range(self.max_iterations):
            # Compute current end-effector pose
            current_pose = self.robot_model.get_end_effector_pose(chain_name, q)

            # Compute error
            error = self.compute_pose_error(current_pose, target_pose)

            # Check convergence
            if np.linalg.norm(error) < self.tolerance:
                break

            # Compute Jacobian
            jacobian = self.robot_model.get_jacobian(chain_name, q)

            # Apply joint weights
            W = np.diag(weights)

            # Solve using weighted pseudo-inverse
            if jacobian.shape[0] >= jacobian.shape[1]:  # More equations than unknowns
                # Use pseudo-inverse
                J_pinv = np.linalg.pinv(jacobian @ W)
                delta_q = W @ J_pinv @ error
            else:  # Underdetermined system
                # Use transpose method
                J_weighted = jacobian @ W
                delta_q = W @ J_weighted.T @ error

            # Update joint positions
            q = q + 0.1 * delta_q  # Damping factor

            # Apply joint limits
            q = np.clip(q,
                       self.robot_model.joint_limits['min'],
                       self.robot_model.joint_limits['max'])

        return q

    def compute_pose_error(self, current_pose, target_pose):
        """
        Compute pose error vector.
        """
        pos_error = target_pose[:3] - current_pose[:3]

        # For orientation, compute error using rotation matrix difference
        # This is a simplified approach
        orient_error = target_pose[3:] - current_pose[3:]  # Quaternion difference

        return np.concatenate([pos_error, orient_error])

class OptimizationBasedIK:
    """
    Optimization-based inverse kinematics formulation.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model

    def solve_ik_qp(self, target_pose, current_q, chain_name,
                    priority_tasks=None, joint_weights=None):
        """
        Solve inverse kinematics using quadratic programming.
        """
        n_joints = len(current_q)

        if joint_weights is None:
            joint_weights = np.ones(n_joints)

        # Define optimization variables
        q_var = cp.Variable(n_joints)

        # Objective function: minimize joint displacement from current configuration
        # with optional joint weights
        obj_terms = []
        obj_terms.append(cp.sum_squares(cp.multiply(joint_weights, (q_var - current_q))))

        # Add priority tasks if provided
        constraints = []

        # Joint limits
        constraints.extend([
            q_var >= self.robot_model.joint_limits['min'],
            q_var <= self.robot_model.joint_limits['max']
        ])

        # Task constraints (simplified - in practice would be more complex)
        # Get current Jacobian
        J_current = self.robot_model.get_jacobian(chain_name, current_q)

        # Target task space velocity
        current_pose = self.robot_model.get_end_effector_pose(chain_name, current_q)
        pose_error = self.compute_pose_error(current_pose, target_pose)

        # Linearized task constraint: J * (q - q_current) ≈ pose_error
        constraints.append(J_current @ (q_var - current_q) == pose_error)

        # Formulate and solve QP
        objective = cp.Minimize(sum(obj_terms))
        problem = cp.Problem(objective, constraints)

        try:
            problem.solve(solver=cp.OSQP, verbose=False)

            if problem.status == cp.OPTIMAL:
                solution = q_var.value
                return solution
            else:
                # Return current configuration if no optimal solution
                return current_q

        except Exception as e:
            print(f"QP solution failed: {e}")
            return current_q

    def compute_pose_error(self, current_pose, target_pose):
        """
        Compute pose error for optimization.
        """
        pos_error = target_pose[:3] - current_pose[:3]
        orient_error = target_pose[3:] - current_pose[3:]
        return np.concatenate([pos_error, orient_error])
```

## Multi-Task Coordination

### Hierarchical Task Control

```python
class HierarchicalTaskController:
    """
    Controller for coordinating multiple tasks with different priorities.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.n_joints = robot_model.n_joints

        # Task hierarchy
        self.task_hierarchy = []
        self.task_jacobians = {}
        self.task_desired_values = {}
        self.task_weights = {}

    def add_task(self, task_name, jacobian, desired_value, priority, weight=1.0):
        """
        Add a task to the hierarchy.
        """
        task_info = {
            'name': task_name,
            'jacobian': jacobian,
            'desired_value': desired_value,
            'priority': priority,
            'weight': weight,
            'active': True
        }

        # Insert task based on priority (higher priority first)
        inserted = False
        for i, existing_task in enumerate(self.task_hierarchy):
            if priority > existing_task['priority']:
                self.task_hierarchy.insert(i, task_info)
                inserted = True
                break

        if not inserted:
            self.task_hierarchy.append(task_info)

    def solve_hierarchical_tasks(self, current_q, current_qdot):
        """
        Solve hierarchical task control problem.
        """
        n_tasks = len(self.task_hierarchy)
        qdot_solution = np.zeros(self.n_joints)

        # Process tasks in priority order
        for i, task in enumerate(self.task_hierarchy):
            if not task['active']:
                continue

            # Get task information
            J_task = task['jacobian']
            desired_value = task['desired_value']

            # Get current task value
            current_task_value = self.robot_model.forward_kinematics(
                current_q, task['name']
            )

            # Compute task error
            task_error = desired_value - current_task_value

            # Compute null space of higher priority tasks
            N_previous = self.compute_null_space_for_task(i)

            # Compute task contribution in current null space
            if J_task.shape[0] <= J_task.shape[1]:  # Underdetermined
                # Use weighted pseudo-inverse
                W = np.eye(self.n_joints) * task['weight']

                # Apply null space constraint
                J_task_projected = J_task @ N_previous
                A = J_task_projected @ W @ J_task_projected.T + 1e-6 * np.eye(J_task.shape[0])

                if np.linalg.matrix_rank(A) == A.shape[0]:
                    lambda_vec = np.linalg.solve(A, task_error)

                    # Compute joint velocity contribution
                    dq_task = W @ N_previous.T @ J_task_projected.T @ lambda_vec
                else:
                    # Use QR decomposition for rank-deficient case
                    Q, R = np.linalg.qr(J_task_projected.T)
                    R_inv = np.linalg.pinv(R)
                    lambda_vec = R_inv @ Q.T @ task_error
                    dq_task = W @ N_previous.T @ J_task_projected.T @ lambda_vec
            else:  # Overdetermined
                # Use pseudo-inverse directly
                J_pinv = np.linalg.pinv(J_task)
                dq_task = J_pinv @ task_error

            # Add to solution
            qdot_solution += dq_task

        return qdot_solution

    def compute_null_space_for_task(self, task_index):
        """
        Compute null space projection matrix for a specific task.
        """
        if task_index == 0:
            # First task operates in full space
            return np.eye(self.n_joints)

        # Compute null space of all higher priority tasks
        N_combined = np.eye(self.n_joints)

        for i in range(task_index):
            if not self.task_hierarchy[i]['active']:
                continue

            J_higher = self.task_hierarchy[i]['jacobian']

            # Compute null space projector for this task
            # P = I - J⁺J where J⁺ is pseudo-inverse of J
            J_pinv = np.linalg.pinv(J_higher)
            P_i = np.eye(self.n_joints) - J_pinv @ J_higher

            # Combine with previous null spaces
            N_combined = P_i @ N_combined

        return N_combined

class TaskSpaceController:
    """
    Controller for task-space operations with null space optimization.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.n_joints = robot_model.n_joints

        # Configuration space objectives
        self.configuration_objectives = []

    def add_configuration_objective(self, objective_type, objective_params, weight=1.0):
        """
        Add configuration space objective (e.g., joint centering, obstacle avoidance).
        """
        objective = {
            'type': objective_type,
            'params': objective_params,
            'weight': weight
        }
        self.configuration_objectives.append(objective)

    def solve_with_configuration_optimization(self, primary_tasks, current_q, current_qdot):
        """
        Solve task control with configuration space optimization.
        """
        # Solve primary tasks using hierarchical approach
        primary_solution = self.solve_hierarchical_tasks(primary_tasks, current_q, current_qdot)

        # Compute null space of primary tasks
        N_primary = self.compute_null_space_of_tasks(primary_tasks)

        # Optimize configuration in null space
        dq_nullspace = self.optimize_configuration_in_nullspace(
            N_primary, current_q
        )

        # Combine solutions
        final_solution = primary_solution + dq_nullspace

        return final_solution

    def compute_null_space_of_tasks(self, tasks):
        """
        Compute null space of primary tasks.
        """
        # For multiple tasks, compute combined null space
        J_combined = np.vstack([task['jacobian'] for task in tasks])

        # Compute pseudo-inverse
        J_pinv = np.linalg.pinv(J_combined)

        # Null space projector
        N = np.eye(self.n_joints) - J_pinv @ J_combined

        return N

    def optimize_configuration_in_nullspace(self, null_space_proj, current_q):
        """
        Optimize configuration objectives in the null space.
        """
        # Formulate optimization problem
        # Minimize ||W(q - q_center)||² subject to q in null space
        # where W is a weight matrix and q_center is desired configuration

        # For now, use a simple approach
        dq_null = np.zeros(self.n_joints)

        # Example: joint centering in null space
        for obj in self.configuration_objectives:
            if obj['type'] == 'joint_centering':
                q_center = obj['params']['center']
                weight = obj['weight']

                # Compute deviation from center
                q_deviation = current_q - q_center

                # Project to null space
                dq_centering = null_space_proj @ (q_center - current_q) * weight

                # Add to solution
                dq_null += dq_centering

        return dq_null

class OperationalSpaceController:
    """
    Operational space controller for compliant motion.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.n_joints = robot_model.n_joints

        # Task space impedance parameters
        self.kp_task = np.eye(6) * 1000  # Stiffness
        self.kd_task = np.eye(6) * 100   # Damping
        self.ki_task = np.eye(6) * 10    # Integral gain (for force control)

        # Joint space impedance parameters
        self.kp_joint = np.eye(self.n_joints) * 100
        self.kd_joint = np.eye(self.n_joints) * 10

        # Force/torque limits
        self.max_force = 100  # Newtons
        self.max_torque = 50  # Nm

    def compute_operational_control(self, task_desired, current_state, external_forces=None):
        """
        Compute operational space control with compliance.
        """
        # Extract current state
        q = current_state['joint_positions']
        qdot = current_state['joint_velocities']

        # Get current task state
        current_task_pos = self.robot_model.get_end_effector_position(q)
        current_task_vel = self.get_task_velocity(q, qdot)

        # Compute task errors
        pos_error = task_desired['position'] - current_task_pos
        vel_error = task_desired['velocity'] - current_task_vel

        # Compute task space control
        task_force = (self.kp_task @ pos_error +
                     self.kd_task @ vel_error +
                     self.ki_task @ self.integral_error)  # Not shown for brevity

        # Apply force limits
        task_force = self.limit_task_force(task_force)

        # Convert to joint torques using Jacobian transpose
        J = self.robot_model.get_jacobian(q)
        tau = J.T @ task_force

        # Add joint space control for posture
        posture_tau = self.compute_posture_control(q, qdot)

        # Combine controls
        total_tau = tau + posture_tau

        # Apply torque limits
        total_tau = self.limit_joint_torques(total_tau)

        return total_tau

    def get_task_velocity(self, q, qdot):
        """
        Compute task space velocity from joint velocities.
        """
        J = self.robot_model.get_jacobian(q)
        return J @ qdot

    def limit_task_force(self, force):
        """
        Limit task space force magnitude.
        """
        norm = np.linalg.norm(force)
        if norm > self.max_force:
            force = force * self.max_force / norm
        return force

    def compute_posture_control(self, q, qdot):
        """
        Compute joint space posture control.
        """
        # Desired joint positions (posture)
        q_desired = self.get_desired_posture()

        # Compute errors
        pos_error = q_desired - q
        vel_error = -qdot  # Damping term

        # Compute joint torques
        tau = self.kp_joint @ pos_error + self.kd_joint @ vel_error

        return tau

    def get_desired_posture(self):
        """
        Get desired joint posture.
        """
        # This would come from higher-level planner or stored posture
        return np.zeros(self.n_joints)  # Placeholder

    def limit_joint_torques(self, torques):
        """
        Limit joint torques.
        """
        limited_torques = np.clip(torques,
                                 -self.max_torque,
                                 self.max_torque)
        return limited_torques
```

## Implementation Example: Whole-Body Controller

```python
#!/usr/bin/env python3
"""
Complete implementation of a whole-body controller for humanoid robots.
"""

import rospy
import numpy as np
from sensor_msgs.msg import JointState, Imu
from geometry_msgs.msg import Vector3, Pose
from std_msgs.msg import Float64MultiArray
from nav_msgs.msg import Odometry
import time

class HumanoidWholeBodyController:
    """
    ROS node for whole-body control of humanoid robots.
    """

    def __init__(self):
        rospy.init_node('humanoid_whole_body_controller')

        # Initialize controllers
        self.whole_body_controller = WholeBodyController(robot_model=None)  # Will be initialized
        self.ik_solver = ClosedFormIK(robot_model=None)  # Will be initialized
        self.hierarchical_controller = HierarchicalTaskController(robot_model=None)  # Will be initialized

        # Robot state
        self.current_joint_positions = np.zeros(28)  # Example: 28 DOF humanoid
        self.current_joint_velocities = np.zeros(28)
        self.current_joint_efforts = np.zeros(28)
        self.current_imu = Vector3(0, 0, 0)
        self.current_com = np.array([0.0, 0.0, 0.8])  # Center of mass
        self.current_com_vel = np.array([0.0, 0.0, 0.0])

        # Publishers and subscribers
        self.joint_command_pub = rospy.Publisher(
            '/joint_group_position_controller/command',
            Float64MultiArray,
            queue_size=10
        )

        rospy.Subscriber('/joint_states', JointState, self.joint_state_callback)
        rospy.Subscriber('/imu/data', Imu, self.imu_callback)

        # Task command subscribers
        rospy.Subscriber('/whole_body_task', Pose, self.task_callback)
        rospy.Subscriber('/balance_task', Vector3, self.balance_callback)
        rospy.Subscriber('/manipulation_task', Pose, self.manipulation_callback)

        # Control parameters
        self.control_rate = 100  # 100 Hz
        self.rate = rospy.Rate(self.control_rate)

        # Task queues
        self.balance_tasks = []
        self.manipulation_tasks = []
        self.locomotion_tasks = []

        # Contact information
        self.contact_info = {
            'contact_points': [],
            'support_polygon': None
        }

        print("Humanoid Whole-Body Controller initialized")

    def joint_state_callback(self, msg):
        """
        Handle joint state updates.
        """
        if len(msg.position) == len(self.current_joint_positions):
            self.current_joint_positions = np.array(msg.position)
            if len(msg.velocity) == len(self.current_joint_velocities):
                self.current_joint_velocities = np.array(msg.velocity)
            if len(msg.effort) == len(self.current_joint_efforts):
                self.current_joint_efforts = np.array(msg.effort)

    def imu_callback(self, msg):
        """
        Handle IMU data for balance control.
        """
        self.current_imu.x = msg.linear_acceleration.x
        self.current_imu.y = msg.linear_acceleration.y
        self.current_imu.z = msg.linear_acceleration.z

    def task_callback(self, msg):
        """
        Handle general whole-body task commands.
        """
        # Parse task from message
        task_type = msg.header.frame_id  # Use frame ID to indicate task type

        if 'balance' in task_type.lower():
            self.balance_tasks.append({
                'target': [msg.position.x, msg.position.y, msg.position.z],
                'timestamp': rospy.Time.now()
            })
        elif 'manipulation' in task_type.lower():
            self.manipulation_tasks.append({
                'target': [msg.position.x, msg.position.y, msg.position.z],
                'orientation': [msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w],
                'timestamp': rospy.Time.now()
            })

    def balance_callback(self, msg):
        """
        Handle balance-specific commands.
        """
        self.balance_tasks.append({
            'target_com': [msg.x, msg.y, msg.z],
            'timestamp': rospy.Time.now()
        })

    def manipulation_callback(self, msg):
        """
        Handle manipulation-specific commands.
        """
        self.manipulation_tasks.append({
            'target_pose': [
                msg.position.x, msg.position.y, msg.position.z,
                msg.orientation.x, msg.orientation.y, msg.orientation.z, msg.orientation.w
            ],
            'timestamp': rospy.Time.now()
        })

    def compute_whole_body_control(self):
        """
        Main whole-body control computation.
        """
        # Create state dictionary
        state = {
            'joint_positions': self.current_joint_positions,
            'joint_velocities': self.current_joint_velocities,
            'com_position': self.current_com,
            'com_velocity': self.current_com_vel,
            'imu_data': self.current_imu
        }

        # Create tasks dictionary
        tasks = {}

        # Add balance tasks if available
        if self.balance_tasks:
            latest_balance = self.balance_tasks[-1]  # Use latest task
            tasks['balance'] = latest_balance
            # Remove old tasks
            self.balance_tasks = [latest_balance]

        # Add manipulation tasks if available
        if self.manipulation_tasks:
            latest_manip = self.manipulation_tasks[-1]  # Use latest task
            tasks['manipulation'] = [latest_manip]
            # Remove old tasks
            self.manipulation_tasks = [latest_manip]

        # Add locomotion tasks if available
        if self.locomotion_tasks:
            tasks['locomotion'] = self.locomotion_tasks
            # Clear after processing
            self.locomotion_tasks = []

        # Add posture task (always active)
        tasks['posture'] = {'desired_posture': np.zeros(len(self.current_joint_positions))}

        # Update contact information (simplified)
        self.update_contact_information()

        # Compute whole-body control
        joint_velocities = self.whole_body_controller.compute_control(state, tasks)

        # Convert to position commands (simple integration)
        dt = 1.0 / self.control_rate
        new_positions = self.current_joint_positions + joint_velocities * dt

        return new_positions

    def update_contact_information(self):
        """
        Update contact information from sensors.
        """
        # This would interface with force/torque sensors and contact detection
        # For simulation, assume feet are in contact
        self.contact_info['contact_points'] = [
            [0.1, 0.1, 0],  # Left foot contact point
            [0.1, -0.1, 0], # Right foot contact point
        ]

        # Calculate support polygon
        contact_x = [pt[0] for pt in self.contact_info['contact_points']]
        contact_y = [pt[1] for pt in self.contact_info['contact_points']]

        self.contact_info['support_polygon'] = {
            'x_min': min(contact_x) - 0.05,  # Add margin
            'x_max': max(contact_x) + 0.05,
            'y_min': min(contact_y) - 0.1,
            'y_max': max(contact_y) + 0.1
        }

        # Update controller with contact info
        self.whole_body_controller.update_contacts(self.contact_info)

    def run(self):
        """
        Main control loop.
        """
        print("Starting whole-body control loop...")

        loop_count = 0
        while not rospy.is_shutdown():
            try:
                # Compute whole-body control
                joint_commands = self.compute_whole_body_control()

                # Publish joint commands
                cmd_msg = Float64MultiArray()
                cmd_msg.data = joint_commands.tolist()
                self.joint_command_pub.publish(cmd_msg)

                # Periodic status updates
                if loop_count % 100 == 0:  # Every second
                    rospy.loginfo(f"Whole-body control running, joints: {len(joint_commands)}")

                # Sleep to maintain control rate
                self.rate.sleep()
                loop_count += 1

            except rospy.ROSInterruptException:
                print("Whole-body controller interrupted")
                break
            except Exception as e:
                rospy.logerr(f"Error in whole-body control: {e}")
                rospy.sleep(0.1)  # Brief pause before continuing

def main():
    """
    Main function to start the whole-body controller.
    """
    try:
        controller = HumanoidWholeBodyController()
        controller.run()
    except rospy.ROSInterruptException:
        pass
    except KeyboardInterrupt:
        print("Whole-body controller stopped by user")

if __name__ == '__main__':
    main()
```

## Advanced Whole-Body Control Techniques

### Model Predictive Control for Whole-Body Motion

```python
import cvxpy as cp

class WholeBodyMPC:
    """
    Model Predictive Control for whole-body motion planning and control.
    """

    def __init__(self, robot_model, prediction_horizon=20, dt=0.01):
        self.robot_model = robot_model
        self.N = prediction_horizon  # Prediction horizon
        self.dt = dt  # Time step

        # State dimensions
        self.n_joints = robot_model.n_joints
        self.n_states = 2 * self.n_joints  # [q, qdot]
        self.n_controls = self.n_joints   # Joint torques

        # Cost weights
        self.state_weights = np.eye(self.n_states) * 0.1
        self.control_weights = np.eye(self.n_controls) * 0.01
        self.terminal_weights = np.eye(self.n_states) * 1.0

        # Constraint bounds
        self.joint_limits = robot_model.joint_limits
        self.torque_limits = np.ones(self.n_controls) * 100  # 100 Nm

    def setup_mpc_problem(self, current_state, reference_trajectory):
        """
        Set up the MPC optimization problem.
        """
        # Define variables
        X = cp.Variable((self.n_states, self.N + 1))  # State trajectory
        U = cp.Variable((self.n_controls, self.N))    # Control trajectory

        # Objective function
        objective = 0

        # Running costs
        for k in range(self.N):
            state_error = X[:, k] - reference_trajectory[k]
            control_effort = U[:, k]

            objective += cp.quad_form(state_error, self.state_weights)
            objective += cp.quad_form(control_effort, self.control_weights)

        # Terminal cost
        terminal_error = X[:, self.N] - reference_trajectory[self.N]
        objective += cp.quad_form(terminal_error, self.terminal_weights)

        # Constraints
        constraints = []

        # Initial state
        constraints.append(X[:, 0] == current_state)

        # System dynamics (simplified - in practice would use full dynamics)
        for k in range(self.N):
            # This is a simplified linearized model
            # In practice, would use full nonlinear dynamics
            A_k, B_k = self.linearize_dynamics(X[:, k])

            # Linearized dynamics: x_{k+1} = A_k * x_k + B_k * u_k
            constraints.append(X[:, k+1] == A_k @ X[:, k] + B_k @ U[:, k])

        # Joint position limits
        q_min = self.joint_limits['min']
        q_max = self.joint_limits['max']

        for k in range(self.N + 1):
            constraints.append(X[:self.n_joints, k] >= q_min)
            constraints.append(X[:self.n_joints, k] <= q_max)

        # Joint velocity limits
        qdot_max = np.ones(self.n_joints) * 5.0  # 5 rad/s max velocity
        for k in range(self.N + 1):
            constraints.append(X[self.n_joints:, k] >= -qdot_max)
            constraints.append(X[self.n_joints:, k] <= qdot_max)

        # Torque limits
        for k in range(self.N):
            constraints.append(cp.norm(U[:, k], 2) <= np.linalg.norm(self.torque_limits))

        # Solve the problem
        problem = cp.Problem(cp.Minimize(objective), constraints)

        return problem, X, U

    def linearize_dynamics(self, state):
        """
        Linearize robot dynamics around the current state.
        """
        # This would involve computing the linearization of the full
        # robot dynamics: dx/dt = f(x, u) ≈ A*x + B*u
        # For simplicity, returning identity matrices
        A = np.eye(self.n_states)
        B = np.eye(self.n_controls)

        # In practice, would compute proper linearization
        # using the robot's dynamic model

        return A, B

    def solve_mpc(self, current_state, reference_trajectory):
        """
        Solve the MPC problem and return optimal control.
        """
        problem, X, U = self.setup_mpc_problem(current_state, reference_trajectory)

        try:
            problem.solve(solver=cp.ECOS, verbose=False)

            if problem.status == cp.OPTIMAL:
                # Return the first control input
                optimal_control = U[:, 0].value
                return optimal_control, True
            else:
                # Return zero control if infeasible
                return np.zeros(self.n_controls), False

        except Exception as e:
            print(f"MPC solution failed: {e}")
            return np.zeros(self.n_controls), False

    def update_reference_trajectory(self, current_state, desired_trajectory):
        """
        Update reference trajectory based on current state and desired motion.
        """
        # This would generate a receding horizon reference trajectory
        # based on the desired motion and current state
        reference_trajectory = []

        for k in range(self.N + 1):
            # Simple reference: maintain current state or follow desired trajectory
            if k < len(desired_trajectory):
                ref_state = desired_trajectory[k]
            else:
                # Hold final desired state
                ref_state = desired_trajectory[-1] if desired_trajectory else current_state

            reference_trajectory.append(ref_state)

        return reference_trajectory

class WholeBodyOptimization:
    """
    Optimization-based whole-body controller using constrained optimization.
    """

    def __init__(self, robot_model):
        self.robot_model = robot_model
        self.n_joints = robot_model.n_joints

        # Task priorities and weights
        self.task_priorities = {}
        self.task_weights = {}

    def formulate_optimization_problem(self, tasks, current_state, constraints=None):
        """
        Formulate whole-body optimization problem.
        """
        # Decision variables: joint accelerations
        qddot = cp.Variable(self.n_joints)

        # Objective function combining multiple tasks
        objective_terms = []

        for task_name, task_info in tasks.items():
            # Get task Jacobian and desired acceleration
            J_task = task_info['jacobian']
            desired_acc = task_info['desired_acceleration']

            # Task error: J*qddot = desired_acc - (coriolis_gravity_terms)
            coriolis_gravity = self.robot_model.coriolis_gravity_terms(
                current_state['q'], current_state['qdot']
            )

            task_error = J_task @ qddot - (desired_acc - coriolis_gravity)

            # Add task cost
            weight = self.task_weights.get(task_name, 1.0)
            objective_terms.append(weight * cp.sum_squares(task_error))

        # Add regularization term for smooth motion
        regularization_weight = 0.01
        objective_terms.append(regularization_weight * cp.sum_squares(qddot))

        # Formulate objective
        objective = cp.Minimize(sum(objective_terms))

        # Constraints
        constraints_list = []

        # Torque limits: tau = M*qddot + coriolis_gravity_terms
        M = self.robot_model.mass_matrix(current_state['q'])
        coriolis_gravity = self.robot_model.coriolis_gravity_terms(
            current_state['q'], current_state['qdot']
        )

        tau = M @ qddot + coriolis_gravity

        tau_max = np.ones(self.n_joints) * 100  # 100 Nm limit
        constraints_list.extend([
            tau <= tau_max,
            tau >= -tau_max
        ])

        # Joint acceleration limits
        qddot_max = np.ones(self.n_joints) * 100  # 100 rad/s²
        constraints_list.extend([
            qddot <= qddot_max,
            qddot >= -qddot_max
        ])

        # Add any additional constraints
        if constraints:
            constraints_list.extend(constraints)

        # Create and return problem
        problem = cp.Problem(objective, constraints_list)

        return problem, qddot

    def solve_optimization(self, tasks, current_state, constraints=None):
        """
        Solve the whole-body optimization problem.
        """
        problem, qddot_var = self.formulate_optimization_problem(
            tasks, current_state, constraints
        )

        try:
            problem.solve(solver=cp.MOSEK, verbose=False)

            if problem.status == cp.OPTIMAL:
                qddot_solution = qddot_var.value

                # Compute required torques
                M = self.robot_model.mass_matrix(current_state['q'])
                coriolis_gravity = self.robot_model.coriolis_gravity_terms(
                    current_state['q'], current_state['qdot']
                )

                tau_solution = M @ qddot_solution + coriolis_gravity

                return qddot_solution, tau_solution, True
            else:
                return None, None, False

        except Exception as e:
            print(f"Optimization solution failed: {e}")
            return None, None, False
```

## Exercises

### Exercise 1: Whole-Body Task Prioritization
Implement a whole-body controller that can handle multiple simultaneous tasks with different priorities. Create a scenario where the robot must maintain balance while reaching for an object and turning its head to look at a target. Test the controller's ability to prioritize balance over other tasks.

### Exercise 2: Redundancy Resolution
Create a redundant manipulator control system that resolves kinematic redundancy for a 7-DOF humanoid arm. Implement different redundancy resolution strategies such as joint centering, obstacle avoidance, and singularity avoidance, and compare their performance.

### Exercise 3: Multi-Contact Whole-Body Control
Implement a whole-body controller that can handle multiple contact points with the environment (e.g., hands on table, feet on ground). Test the controller with different contact configurations and evaluate its stability.

### Exercise 4: Whole-Body MPC Implementation
Implement a Model Predictive Control approach for whole-body motion planning that considers both kinematic and dynamic constraints. Test the controller with complex multi-task scenarios and evaluate its computational efficiency.

## Summary

This chapter covered the fundamental concepts of whole-body control for humanoid robots, including task-priority frameworks, inverse kinematics solutions, and multi-task coordination strategies. We explored various mathematical approaches for handling the redundancy and constraints inherent in whole-body systems, including hierarchical control, optimization-based methods, and model predictive control.

The key takeaways include:
- Whole-body control requires careful consideration of task priorities and constraints
- Inverse kinematics solutions must handle redundancy effectively
- Multi-task coordination balances competing objectives
- Optimization-based approaches provide systematic solutions to complex control problems
- Real-time performance is critical for effective whole-body control

In the next chapter, we'll explore perception-action integration, combining the control systems developed here with sensory feedback for autonomous humanoid behavior.