#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class PyListener(Node):
    def __init__(self):
        super().__init__('py_listener')
        self.sub = self.create_subscription(String, 'chatter', self.callback, 10)
        self.get_logger().info('Python监听器已启动')
    
    def callback(self, msg):
        self.get_logger().info(f'收到: "{msg.data}"')

def main():
    rclpy.init()
    node = PyListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

