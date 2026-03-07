#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2
import json
import os
from ultralytics import YOLO

# Import custom message
# Note: In a real ROS2 environment, you'd need to build the package first
# to generate the python bindings for ChargingStatus.
try:
    from charge_port.msg import ChargingStatus
except ImportError:
    # Fallback for code visibility before build
    ChargingStatus = None

class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')
        
        # Parameters
        self.declare_parameter('model_path', 'runs/train_charging/charging_detector/weights/best.pt')
        self.declare_parameter('vehicle_model_path', 'yolov8n.pt')
        self.declare_parameter('regions_path', 'config/parking_regions.json')
        
        model_path = self.get_parameter('model_path').get_parameter_value().string_value
        vehicle_model_path = self.get_parameter('vehicle_model_path').get_parameter_value().string_value
        regions_path = self.get_parameter('regions_path').get_parameter_value().string_value
        
        # Initialize Models
        self.get_logger().info(f"Loading vehicle model: {vehicle_model_path}")
        self.vehicle_model = YOLO(vehicle_model_path)
        
        self.get_logger().info(f"Loading charging port model: {model_path}")
        if os.path.exists(model_path):
            self.charging_model = YOLO(model_path)
        else:
            self.get_logger().warn(f"Model file not found: {model_path}. Using base yolov8n for testing.")
            self.charging_model = YOLO('yolov8n.pt')

        # Load Regions
        try:
            with open(regions_path, 'r') as f:
                self.parking_regions = json.load(f)
        except Exception as e:
            self.get_logger().error(f"Failed to load regions: {e}")
            self.parking_regions = []

        # ROS2 Utilities
        self.bridge = CvBridge()
        
        # Subscriptions & Publishers
        self.subscription = self.create_subscription(
            Image,
            'camera/image_raw',
            self.image_callback,
            10)
            
        self.status_pub = self.create_publisher(String, 'charging_status_summary', 10)
        
        # Optional: Custom message publisher
        if ChargingStatus:
            self.detailed_status_pub = self.create_publisher(ChargingStatus, 'charging_status_detailed', 10)
        
        self.get_logger().info("Detection node started.")

    def image_callback(self, msg):
        # Convert ROS Image to OpenCV
        frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        
        # 1. Vehicle Detection (Simulation of logic from documentation)
        vehicle_results = self.vehicle_model.track(frame, persist=True, verbose=False)
        
        # 2. Charging Port Detection in Occupied Areas
        # (Simplified logic for demonstration in ROS2 node)
        charging_results = self.charging_model(frame, verbose=False)
        
        count = 0
        if charging_results[0].boxes is not None:
            for box in charging_results[0].boxes:
                count += 1
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                cls_name = self.charging_model.names[cls_id]
                x1, y1, x2, y2 = box.xyxy[0].cpu().tolist()
                
                # Publish detailed status if available
                if ChargingStatus:
                    status_msg = ChargingStatus()
                    status_msg.header = msg.header
                    status_msg.is_charging = True
                    status_msg.port_type = cls_name
                    status_msg.confidence = conf
                    # ROI etc.
                    self.detailed_status_pub.publish(status_msg)
        
        # Publish summary
        summary = f"Detected {count} charging ports in current frame."
        self.status_pub.publish(String(data=summary))

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
