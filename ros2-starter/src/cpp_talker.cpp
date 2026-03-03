#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

int main(int argc, char* argv[])
{
    rclcpp::init(argc, argv);
    auto node = rclcpp::Node::make_shared("cpp_talker");
    auto publisher = node->create_publisher<std_msgs::msg::String>("chatter", 10);
    int count = 0;
    
    rclcpp::WallRate rate(1); // 每秒1次
    
    while (rclcpp::ok()) {
        auto msg = std_msgs::msg::String();
        msg.data = "C++ says hello #" + std::to_string(count++);
        RCLCPP_INFO(node->get_logger(), "发布: '%s'", msg.data.c_str());
        publisher->publish(msg);
        rclcpp::spin_some(node);
        rate.sleep();
    }
    
    rclcpp::shutdown();
    return 0;
}

