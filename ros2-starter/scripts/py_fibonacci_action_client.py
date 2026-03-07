#!/usr/bin/env python3
import sys
from action_tutorials_interfaces.action import Fibonacci
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node


class FibonacciActionClient(Node):
    def __init__(self):
        super().__init__('fibonacci_action_client')
        self.action_client = ActionClient(self, Fibonacci, 'fibonacci')
        self.get_logger().info('等待 Action 服务器...')
        
    def send_goal(self, order=10):
        self.action_client.wait_for_server()
        self.get_logger().info('Action 服务器已连接')
        
        goal_msg = Fibonacci.Goal()
        goal_msg.order = order
        
        self.get_logger().info(f'发送目标: order={order}')
        
        send_goal_options = Fibonacci.Goal.GoalOptions()
        send_goal_options.feedback_callback = self.feedback_callback
        send_goal_options.result_callback = self.result_callback
        
        self._send_goal_future = self.action_client.send_goal_async(
            goal_msg, send_goal_options)
        self._send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('目标被拒绝')
            return
        
        self.get_logger().info('目标已被接受')
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(f'反馈: {feedback.partial_sequence}')

    def result_callback(self, result_future):
        result = result_future.result()
        self.get_logger().info(f'最终结果: {result.result.sequence}')
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    client = FibonacciActionClient()
    
    # 从命令行参数获取 order，默认 10
    order = 10
    if len(sys.argv) > 1:
        order = int(sys.argv[1])
    
    client.send_goal(order)
    rclpy.spin(client)


if __name__ == '__main__':
    main()

