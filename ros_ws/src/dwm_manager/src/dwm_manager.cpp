#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "tf2/utils.h"
#include <tf2/LinearMath/Transform.h>
#include <std_msgs/msg/float32.hpp>

class PointStampedSubscriber : public rclcpp::Node {
public:
    PointStampedSubscriber() : Node("point_stamped_subscriber") {
        // Subscribers
        tag2_subscription_ = this->create_subscription<geometry_msgs::msg::PointStamped>(
            "/passive/output/DW1CB5", 10,
            std::bind(&PointStampedSubscriber::Tag2pointStampedCallback, this, std::placeholders::_1));

        tag1_subscription_ = this->create_subscription<geometry_msgs::msg::PointStamped>(
            "/passive/output/DWDCA3", 10,
            std::bind(&PointStampedSubscriber::Tag1pointStampedCallback, this, std::placeholders::_1));
        team_number_subscription_ = this->create_subscription<std_msgs::msg::Float32>(
            "/team_number", 10,
            std::bind(&PointStampedSubscriber::TeamNumberCallback, this, std::placeholders::_1));

        //Publishers
        laps_publisher_ = this->create_publisher<std_msgs::msg::Float32>("/durability_laps", 10);

        //Timer cb
        base_pub_timer_ = this->create_wall_timer
            (std::chrono::milliseconds(100),std::bind(&PointStampedSubscriber::base_pub_cb, this));
        lap_counter_timer_ = this->create_wall_timer
            (std::chrono::milliseconds(500),std::bind(&PointStampedSubscriber::lap_counter_cb, this));

        //For tf2_ros
        tf_buffer_ =
        std::make_unique<tf2_ros::Buffer>(this->get_clock());
        tf_listener_ =
        std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
        // Initialize the transform broadcaster
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

        tag1_received = false;
        tag2_received = false;

        //Lap counter
        laps = 0;
        lap_quadrants = {false,false,false,false};

        current_team = -1;
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
        // Publish the transform
        if (!std::isnan(transform_stamped.transform.translation.x) && !std::isnan(transform_stamped.transform.translation.y)){
            tf_broadcaster_->sendTransform(transform_stamped);
            tag2_transform = transform_stamped;
            tag2_received = true;
        }
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
        if (!std::isnan(transform_stamped.transform.translation.x) && !std::isnan(transform_stamped.transform.translation.y)){
            tf_broadcaster_->sendTransform(transform_stamped);
            tag1_transform = transform_stamped;
            tag1_received = true;
        }


    }

    void TeamNumberCallback(const std_msgs::msg::Float32::SharedPtr msg)
    {
        if (msg->data != current_team){
            //Reset lap counter and update team
            current_team = msg->data;
            lap_quadrants = {false,false,false,false};
        }
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
    }

    void lap_counter_cb()
    {
       //Track position of the base frame relative to track center, ensure it has been in each quadrant before counting lap
        //Get transform from track center to base
        geometry_msgs::msg::TransformStamped transform;
        if (tf_buffer_->canTransform("track_center","base",rclcpp::Time(0),tf2::durationFromSec(0.1))){
            transform = tf_buffer_->lookupTransform("track_center","base",rclcpp::Time(0),tf2::durationFromSec(0.1));
        } else {
            RCLCPP_ERROR(this->get_logger(), "lap_counter_cb: Unable to transform from track_center to base");
            return;
        }
        
        //Distance that point must be within quadrant before checking off
        double dist_thresh = 1.0;

        double x,y;
        x = transform.transform.translation.x;
        y = transform.transform.translation.y;

        //Check quadrants in order
        if (!lap_quadrants[0]){
            //+-
            if(x > dist_thresh && x < -dist_thresh){
                lap_quadrants[0] = true;
            }
        } else if (!lap_quadrants[1]){
            //--
            if(x < -dist_thresh && x < -dist_thresh){
                lap_quadrants[1] = true;
            }
        } else if (!lap_quadrants[2]){
            //-+
            if(x < -dist_thresh && x > dist_thresh){
                lap_quadrants[2] = true;
            }
        } else if (!lap_quadrants[3]){
            //++
            if(x > dist_thresh && x > dist_thresh){
                lap_quadrants[0] = true;
            }
        } else {
            //Wait for machine to cross back into quad 1
            //+-
            if(x > dist_thresh && x < -dist_thresh){
                //Lap finished, increment count
                laps++;
                lap_quadrants = {false,false,false,false}; 
            }
        }

        //Publish laps
        std_msgs::msg::Float32 laps_msg;
        laps_msg.data = laps;
        laps_publisher_->publish(laps_msg);
    }

    //Subscribers
    rclcpp::Subscription<geometry_msgs::msg::PointStamped>::SharedPtr tag1_subscription_;
    rclcpp::Subscription<geometry_msgs::msg::PointStamped>::SharedPtr tag2_subscription_;
    rclcpp::Subscription<std_msgs::msg::Float32>::SharedPtr team_number_subscription_;

    //Publishers
    rclcpp::Publisher<std_msgs::msg::Float32>::SharedPtr laps_publisher_;


    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    //For tf2_ros
    std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
    std::unique_ptr<tf2_ros::Buffer> tf_buffer_;

    //Timer cb
    rclcpp::TimerBase::SharedPtr base_pub_timer_;
    rclcpp::TimerBase::SharedPtr lap_counter_timer_;

    geometry_msgs::msg::TransformStamped tag1_transform, tag2_transform;
    bool tag1_received;
    bool tag2_received;

    int current_team;

    //Lap counter
    int laps;
    //Given a tf at track center, check that all quadrants were hit before counting a lap
    std::vector<bool> lap_quadrants;

};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<PointStampedSubscriber>());
    rclcpp::shutdown();
    return 0;
}
