#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"
#include "durability_msgs/msg/load_toad.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "geometry_msgs/msg/transform_stamped.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include <chrono>
#include <ctime>
#include <cmath>

class MyPublisher : public rclcpp::Node {
public:
    MyPublisher()
        : Node("Durability_Simulator") {
        publisher_ = create_publisher<durability_msgs::msg::LoadToad>("load_toad", 10);
        odom_publisher_ = create_publisher<nav_msgs::msg::Odometry>("load_toad_odom", 10);
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);
        timer_ = create_wall_timer(std::chrono::milliseconds(100), std::bind(&MyPublisher::publishMessage, this)); // Changed timer interval
        start_time = now();
    }

private:
    void publishMessage() {
        float time = (now().seconds() - start_time.seconds()) + ((now().nanoseconds() - start_time.nanoseconds()) / 1000000000.0);
        auto odom = nav_msgs::msg::Odometry();
        // Generate circular motion for x and y
        float radius = 5.0;  // Adjust the radius as needed
        float angular_speed = 2.0 * M_PI / 60.0;  // One revolution per second

        float x = 5.0+ radius * cos(angular_speed * time);
        float y = 5.0+ radius * sin(angular_speed * time);

        auto message = durability_msgs::msg::LoadToad();
        message.force = 100;
        message.speed = 1;
        message.power = 10;
        
        // Publish LoadToad message
        publisher_->publish(message);

        // Publish TF transform
        geometry_msgs::msg::TransformStamped transformStamped;
        transformStamped.header.stamp = now();
        transformStamped.header.frame_id = "map";  // Parent frame
        transformStamped.child_frame_id = "toad_link";    // Child frame
        transformStamped.transform.translation.x = x;    // Example translation
        transformStamped.transform.translation.y = y;

        transformStamped.transform.rotation.w = 1.0;       // Example rotation

        tf_broadcaster_->sendTransform(transformStamped);
        odom.pose.pose.position.x=x;
        odom.pose.pose.position.y=y;
        odom.header.stamp=now();
        odom.header.frame_id="map";
        odom.child_frame_id="toad_link";
        odom_publisher_->publish(odom);
    }
    rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr odom_publisher_;
    rclcpp::Publisher<durability_msgs::msg::LoadToad>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    rclcpp::Time start_time;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<MyPublisher>());
    rclcpp::shutdown();
    return 0;
}
