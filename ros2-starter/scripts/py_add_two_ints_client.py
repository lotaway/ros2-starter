#!/usr/bin/env python3
import sys
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node


class AddTwoIntsClient(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('等待服务启动...')
        self.get_logger().info('服务已连接')

    def send_request(self, a, b):
        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        self.get_logger().info(f'发送请求: {a} + {b}')
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)
        return future.result()


def main(args=None):
    rclpy.init(args=args)
    client = AddTwoIntsClient()
    
    # 从命令行参数获取两个数
    if len(sys.argv) != 3:
        print('用法: ros2 run ros2-starter py_add_two_ints_client.py <a> <b>')
        return
    
    a = int(sys.argv[1])
    b = int(sys.argv[2])
    
    response = client.send_request(a, b)
    client.get_logger().info(f'结果: {a} + {b} = {response.sum}')
    
    client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

