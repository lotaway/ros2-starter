#ifndef CHARGE_PORT__HARDWARE_NODE_HPP_
#define CHARGE_PORT__HARDWARE_NODE_HPP_

#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/image.hpp"
#include "std_msgs/msg/string.hpp"
#include "cv_bridge/cv_bridge.h"
#include "image_transport/image_transport.hpp"
#include <opencv2/opencv.hpp>

namespace charge_port {

class HardwareNode : public rclcpp::Node {
public:
    HardwareNode();
    ~HardwareNode();

private:
    void timer_callback();
    void command_callback(const std_msgs::msg::String::SharedPtr msg);
    
    // ROS2 elements
    rclcpp::TimerBase::SharedPtr timer_;
    image_transport::Publisher image_pub_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr command_sub_;
    
    // OpenCV elements
    cv::VideoCapture cap_;
    int camera_id_;
    
    // Hardware control simulation/stub
    void control_charging_pile(const std::string& command);
};

} // namespace charge_port

#endif // CHARGE_PORT__HARDWARE_NODE_HPP_
