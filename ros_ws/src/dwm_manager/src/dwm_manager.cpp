#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "tf2/utils.h"
#include <tf2/LinearMath/Transform.h>

class PointStampedSubscriber : public rclcpp::Node {
public:
    PointStampedSubscriber() : Node("point_stamped_subscriber") {
        // Subscribe to the point stamped topic
        tag2_subscription_ = this->create_subscription<geometry_msgs::msg::PointStamped>(
            "/passive/output/DW1CB5", 10,
            std::bind(&PointStampedSubscriber::Tag2pointStampedCallback, this, std::placeholders::_1));

        tag1_subscription_ = this->create_subscription<geometry_msgs::msg::PointStamped>(
            "/passive/output/DWDCA3", 10,
            std::bind(&PointStampedSubscriber::Tag1pointStampedCallback, this, std::placeholders::_1));

        //Timer cb
        base_pub_timer_ = this->create_wall_timer
            (std::chrono::milliseconds(500),std::bind(&PointStampedSubscriber::base_pub_cb, this));

        //For tf2_ros
        tf_buffer_ =
        std::make_unique<tf2_ros::Buffer>(this->get_clock());
        tf_listener_ =
        std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
        // Initialize the transform broadcaster
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

        tag1_received = false;
        tag2_received = false;

    }

private:
    void Tag2pointStampedCallback(const geometry_msgs::msg::PointStamped::SharedPtr msg) {
        // Create a transform object
        geometry_msgs::msg::TransformStamped transform_stamped;
        
        // Set the frame IDs
        transform_stamped.header.frame_id = "initiator";
        transform_stamped.child_frame_id = "tag2";

        // Set the translation
        transform_stamped.transform.translation.x = msg->point.x;
        transform_stamped.transform.translation.y = msg->point.y;
        transform_stamped.transform.translation.z = msg->point.z;

        // Set the rotation (assuming no rotation for simplicity)
        transform_stamped.transform.rotation.x = 0.0;
        transform_stamped.transform.rotation.y = 0.0;
        transform_stamped.transform.rotation.z = 0.0;
        transform_stamped.transform.rotation.w = 1.0;

        // Set the timestamp
        transform_stamped.header.stamp = msg->header.stamp;

        // Publish the transform
        tf_broadcaster_->sendTransform(transform_stamped);

        tag2_transform = transform_stamped;

        tag2_received = true;
    }

    void Tag1pointStampedCallback(const geometry_msgs::msg::PointStamped::SharedPtr msg) {
        // Create a transform object
        geometry_msgs::msg::TransformStamped transform_stamped;
        
        // Set the frame IDs
        transform_stamped.header.frame_id = "initiator";
        transform_stamped.child_frame_id = "tag1";

        // Set the translation
        transform_stamped.transform.translation.x = msg->point.x;
        transform_stamped.transform.translation.y = msg->point.y;
        transform_stamped.transform.translation.z = msg->point.z;

        // Set the rotation (assuming no rotation for simplicity)
        transform_stamped.transform.rotation.x = 0.0;
        transform_stamped.transform.rotation.y = 0.0;
        transform_stamped.transform.rotation.z = 0.0;
        transform_stamped.transform.rotation.w = 1.0;

        // Set the timestamp
        transform_stamped.header.stamp = msg->header.stamp;

        // Publish the transform
        tf_broadcaster_->sendTransform(transform_stamped);

        tag1_transform = transform_stamped;

        tag1_received = true;
    }

    //Publish initiator to base transform based on tag locations
    void base_pub_cb()
    {
        if (tag1_received & tag2_received){
            geometry_msgs::msg::TransformStamped base_transform;
            double x_diff, y_diff, yaw;
            x_diff = tag2_transform.transform.translation.x - tag1_transform.transform.translation.x;
            y_diff = tag2_transform.transform.translation.y - tag1_transform.transform.translation.y;

            yaw = std::atan2(y_diff,x_diff);

            tf2::Quaternion q;
            q.setRPY(0.,0.,yaw);

            base_transform.transform.rotation.w = q.getW();
            base_transform.transform.rotation.x = q.getX();
            base_transform.transform.rotation.y = q.getY();
            base_transform.transform.rotation.z = q.getZ();
            base_transform.transform.translation = tag1_transform.transform.translation;
            base_transform.header.frame_id = "initiator";
            base_transform.child_frame_id = "base";
            base_transform.header.stamp = this->get_clock()->now();
            // Publish the transform
            tf_broadcaster_->sendTransform(base_transform);
        } else {
            RCLCPP_ERROR(this->get_logger(), "Tag1pointStampedCallback:: Waiting for transform from both Tag1 and Tag2");
        }

        // //Get transform between Tag1 and Tag2
        // geometry_msgs::msg::TransformStamped transform, base_transform;
        // if (tf_buffer_->canTransform("tag1","tag2",rclcpp::Time(0),tf2::durationFromSec(0.5))){
        //     transform = tf_buffer_->lookupTransform("tag1","tag2",rclcpp::Time(0),tf2::durationFromSec(0.5));
        //     RCLCPP_INFO(this->get_logger(), "Tag1pointStampedCallback:: Got transform");

        //     //Set base transform as tag 1, using the quat of the the transform between the two
        //     base_transform = transform;
        //     base_transform.transform.translation = transform_stamped.transform.translation;
        //     base_transform.header.frame_id = "initiator";
        //     base_transform.child_frame_id = "base";

        //     // Publish the transform
        //     tf_broadcaster_->sendTransform(base_transform);
        // } else {
        //     RCLCPP_ERROR(this->get_logger(), "Tag1pointStampedCallback:: Unable to transform from Tag1 to Tag2");
        // }
    }

    rclcpp::Subscription<geometry_msgs::msg::PointStamped>::SharedPtr tag1_subscription_;
    rclcpp::Subscription<geometry_msgs::msg::PointStamped>::SharedPtr tag2_subscription_;
    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    //For tf2_ros
    std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
    std::unique_ptr<tf2_ros::Buffer> tf_buffer_;

    //Timer cb
    rclcpp::TimerBase::SharedPtr base_pub_timer_;

    geometry_msgs::msg::TransformStamped tag1_transform, tag2_transform;
    bool tag1_received;
    bool tag2_received;


};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PointStampedSubscriber>());
    rclcpp::shutdown();
    return 0;
}
