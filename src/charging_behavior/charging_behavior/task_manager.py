#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from charging_interfaces.msg import ChargingStatus
import time

class TaskManager(Node):
    def __init__(self):
        super().__init__('task_manager')
        
        # 内部状态
        self.state = "IDLE"
        self.retry_count = 0
        self.last_status = None
        
        # 1. 订阅感知模块生成的位姿判定结果
        self.status_sub = self.create_subscription(
            ChargingStatus,
            'charging_status_detailed',
            self.status_callback,
            10)
            
        # 2. 发布硬件控制命令给 hardware_node
        self.cmd_pub = self.create_publisher(String, 'charge_command', 10)
        
        # 3. 对外广播当前完整进度
        self.final_status_pub = self.create_publisher(ChargingStatus, 'charging_task_status', 10)
        
        # 行为流控 Timer
        self.timer = self.create_timer(0.5, self.control_loop)
        
        self.get_logger().info("Charging Task Manager (BT-style) Initialized.")

    def status_callback(self, msg):
        self.last_status = msg

    def control_loop(self):
        # 简易 BT 状态流
        if self.state == "IDLE":
            self.get_logger().info("State: IDLE -> Auto transition to SEARCHING.")
            self.state = "SEARCHING"
            
        elif self.state == "SEARCHING":
            # 告诉硬件正在扫描
            msg = String(); msg.data = "scan"
            self.cmd_pub.publish(msg)
            
            # 判断感知节点是否检测到充电口
            if self.last_status and self.last_status.is_detected:
                self.get_logger().info("Target detected! -> Transition to APPROACHING.")
                self.state = "APPROACHING"
                
        elif self.state == "APPROACHING":
            if not self.last_status or not self.last_status.is_detected:
                self.get_logger().warn("Lost target in approaching phase!")
                self.state = "SEARCHING"
            elif self.last_status.distance_error < 0.2:
                self.get_logger().info("Near target! -> Transition to PRE_ALIGN.")
                self.state = "PRE_ALIGN"
                
        elif self.state == "PRE_ALIGN":
            if self.last_status and self.last_status.distance_error < 0.05:
                self.get_logger().info("Aligned! -> Transition to INSERTING.")
                self.state = "INSERTING"
                
        elif self.state == "INSERTING":
            # 达成条件！下发实质指令给硬件驱动
            self.get_logger().info("Target Reached! Publish 'start' task down to Hardware / Arms...")
            msg = String(); msg.data = "start"
            self.cmd_pub.publish(msg)
            self.state = "CONNECTED"
            self.get_logger().info("Task COMPLETED.")

        self.publish_task_status()

    def publish_task_status(self):
        msg = ChargingStatus()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.current_state = self.state
        msg.retry_count = self.retry_count
        if self.last_status:
            msg.is_detected = self.last_status.is_detected
            msg.distance_error = self.last_status.distance_error
            # 复制目标位姿
            msg.target_pose = self.last_status.target_pose
        
        self.final_status_pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = TaskManager()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
