#include "charge_port/hardware_node.hpp"

namespace charge_port {

HardwareNode::HardwareNode() : Node("hardware_node") {
    // Parameters
    this->declare_parameter("camera_id", 0);
    this->declare_parameter("frame_rate", 30.0);
    this->declare_parameter("video_path", "");
    
    camera_id_ = this->get_parameter("camera_id").as_int();
    double fps = this->get_parameter("frame_rate").as_double();
    std::string video_path = this->get_parameter("video_path").as_string();
    
    // Initialize Camera or Video File
    if (!video_path.empty()) {
        cap_.open(video_path);
        if (!cap_.isOpened()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open video file: %s", video_path.c_str());
        } else {
            RCLCPP_INFO(this->get_logger(), "Simulating with video file: %s", video_path.c_str());
        }
    } else {
        cap_.open(camera_id_);
        if (!cap_.isOpened()) {
            RCLCPP_ERROR(this->get_logger(), "Failed to open camera %d", camera_id_);
        } else {
            RCLCPP_INFO(this->get_logger(), "Opened camera %d", camera_id_);
        }
    }
    
    // Publishers & Subscribers
    rmw_qos_profile_t custom_qos = rmw_qos_profile_default;
    image_pub_ = image_transport::create_publisher(this, "camera/image_raw", custom_qos);
    
    command_sub_ = this->create_subscription<std_msgs::msg::String>(
        "charge_command", 10,
        std::bind(&HardwareNode::command_callback, this, std::placeholders::_1));
        
    // Timer for image acquisition
    auto period = std::chrono::milliseconds(static_cast<int>(1000.0 / fps));
    timer_ = this->create_wall_timer(period, std::bind(&HardwareNode::timer_callback, this));
    
    RCLCPP_INFO(this->get_logger(), "Hardware node initialized.");
}

HardwareNode::~HardwareNode() {
    if (cap_.isOpened()) {
        cap_.release();
    }
}

void HardwareNode::timer_callback() {
    cv::Mat frame;
    if (cap_.read(frame)) {
        auto msg = cv_bridge::CvImage(std_msgs::msg::Header(), "bgr8", frame).toImageMsg();
        msg->header.stamp = this->now();
        msg->header.frame_id = "camera_link";
        image_pub_.publish(*msg);
    } else {
        // If it's a video file, loop back to the beginning
        if (this->get_parameter("video_path").as_string() != "") {
            cap_.set(cv::CAP_PROP_POS_FRAMES, 0);
        }
    }
}

void HardwareNode::command_callback(const std_msgs::msg::String::SharedPtr msg) {
    RCLCPP_INFO(this->get_logger(), "Received hardware command: %s", msg->data.c_str());
    control_charging_pile(msg->data);
}

void HardwareNode::control_charging_pile(const std::string& command) {
    // STUB: Replace with actual serial/CAN/Modbus communication logic
    if (command == "start") {
        RCLCPP_INFO(this->get_logger(), "HARDWARE: Starting charging cycle...");
    } else if (command == "stop") {
        RCLCPP_INFO(this->get_logger(), "HARDWARE: Stopping charging cycle...");
    } else {
        RCLCPP_WARN(this->get_logger(), "HARDWARE: Unknown command: %s", command.c_str());
    }
}

} // namespace charge_port

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<charge_port::HardwareNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
