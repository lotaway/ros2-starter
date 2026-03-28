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

from ament_index_python.packages import get_package_share_directory

# Import custom message
# Note: In a real ROS2 environment, you'd need to build the package first
# to generate the python bindings for ChargingStatus.
try:
    from charging_interfaces.msg import ChargingStatus
except ImportError:
    # Fallback for code visibility before build
    ChargingStatus = None

class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')
        
        # Get package share directories
        pkg_perception = get_package_share_directory('charging_perception')
        pkg_description = get_package_share_directory('charging_robot_description')
        
        # Parameters
        self.declare_parameter('model_path', os.path.join(pkg_description, 'models', 'detector', 'weights', 'best.pt'))
        self.declare_parameter('vehicle_model_path', 'yolov8n.pt')
        self.declare_parameter('regions_path', os.path.join(pkg_perception, 'config', 'parking_regions.json'))
        
        model_path = self.get_parameter('model_path').get_parameter_value().string_value
        vehicle_model_path = self.get_parameter('vehicle_model_path').get_parameter_value().string_value
        regions_path = self.get_parameter('regions_path').get_parameter_value().string_value
        
        # Initialize Models
        model_dir = os.path.join(pkg_description, 'models')
        os.makedirs(model_dir, exist_ok=True)
        
        self.get_logger().info(f"Loading vehicle model: {vehicle_model_path}")
        # 如果是 yolov8n.pt，让它去固定目录找/存
        if vehicle_model_path == 'yolov8n.pt':
            vehicle_model_path = os.path.join(model_dir, 'yolov8n.pt')
            
        self.vehicle_model = YOLO(vehicle_model_path)
        
        self.get_logger().info(f"Loading charging port model: {model_path}")
        if os.path.exists(model_path):
            self.charging_model = YOLO(model_path)
        else:
            self.get_logger().warn(f"Model file not found: {model_path}. Using base yolov8n for testing.")
            # 同样，fallback 模型也存在固定目录
            fallback_path = os.path.join(model_dir, 'yolov8n.pt')
            self.charging_model = YOLO(fallback_path)

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
        
        # 1. Vehicle Detection & Tracking
        # Only detect: car(2), motorcycle(3), bus(5), truck(7) to speed up and reduce false positives
        vehicle_results = self.vehicle_model.track(frame, persist=True, classes=[2, 3, 5, 7], verbose=False)
        
        # 2. ROI-based Charging Port Detection
        # Instead of searching the whole frame, we only look at specific parking regions
        detected_ports = []
        
        for region in self.parking_regions:
            # Simple ROI extraction based on config points
            pts = region['points']
            x_coords = [p[0] for p in pts]
            y_coords = [p[1] for p in pts]
            x1, y1, x2, y2 = min(x_coords), min(y_coords), max(x_coords), max(y_coords)
            
            # Crop the parking spot with a small margin
            margin = 20
            roi = frame[max(0, y1-margin):min(frame.shape[0], y2+margin), 
                        max(0, x1-margin):min(frame.shape[1], x2+margin)]
            
            if roi.size > 0:
                # 3. Detection on the small ROI is MUCH faster
                charging_results = self.charging_model(roi, verbose=False)
                
                if charging_results[0].boxes is not None and len(charging_results[0].boxes) > 0:
                    for box in charging_results[0].boxes:
                        cls_id = int(box.cls[0])
                        conf = float(box.conf[0])
                        cls_name = self.charging_model.names[cls_id]
                        detected_ports.append({
                            'spot_id': region['id'],
                            'type': cls_name,
                            'conf': conf
                        })
                        
                        # (Optional) Publish detailed status per port
                        if ChargingStatus:
                            status_msg = ChargingStatus()
                            status_msg.header = msg.header
                            status_msg.is_charging = True
                            status_msg.port_type = cls_name
                            status_msg.confidence = conf
                            status_msg.parking_spot_id = region['id']
                            self.detailed_status_pub.publish(status_msg)
        
        # Publish summary
        summary = f"System Status: Monitoring {len(self.parking_regions)} spots. Detected {len(detected_ports)} active charging ports."
        self.status_pub.publish(String(data=summary))

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    rclpy.spin(node)
    node.destroy_node() 
    rclpy.shutdown()

if __name__ == '__main__':
    main()
