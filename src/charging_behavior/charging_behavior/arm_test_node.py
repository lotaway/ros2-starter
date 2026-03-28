#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

class ArmTestNode(Node):
    def __init__(self):
        super().__init__('arm_test_node')
        self.publisher_ = self.create_publisher(JointTrajectory, '/arm_controller/joint_trajectory', 10)
        self.timer = self.create_timer(2.0, self.send_goal)
        self.get_logger().info('Arm test node started.')
        self.step = 0

    def send_goal(self):
        msg = JointTrajectory()
        msg.joint_names = ['joint1', 'joint2', 'joint3']
        
        point = JointTrajectoryPoint()
        if self.step == 0:
            point.positions = [1.0, 0.5, 0.5]
            self.step = 1
        else:
            point.positions = [0.0, 0.0, 0.0]
            self.step = 0
            
        point.time_from_start = Duration(sec=1, nanosec=0)
        msg.points.append(point)
        self.publisher_.publish(msg)
        self.get_logger().info(f'Sent goal: {point.positions}')

def main(args=None):
    rclpy.init(args=args)
    node = ArmTestNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
