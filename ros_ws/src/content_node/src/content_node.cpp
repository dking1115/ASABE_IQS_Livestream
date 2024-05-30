#include "rclcpp/rclcpp.hpp"
#include "geometry_msgs/msg/point_stamped.hpp"
#include "tf2_ros/transform_broadcaster.h"
#include "tf2/LinearMath/Quaternion.h"
#include "tf2_ros/transform_listener.h"
#include "tf2_ros/buffer.h"
#include "tf2/utils.h"
#include <tf2/LinearMath/Transform.h>
#include <std_msgs/msg/u_int8.hpp>
#include <iqs_msgs/msg/camera.hpp>
#include <std_msgs/msg/string.hpp>

class ContentNode : public rclcpp::Node {
public:
    ContentNode() : Node("content_node") {
        // Subscribers
        pull_state_sub = this->create_subscription<std_msgs::msg::UInt8>(
            "/pull_state", 10,
            std::bind(&ContentNode::PullStateCallback, this, std::placeholders::_1));
        dur_state_sub = this->create_subscription<std_msgs::msg::UInt8>(
            "/dur_state", 10,
            std::bind(&ContentNode::DurStateCallback, this, std::placeholders::_1));

        //Publishers
        obs_scene_pub = this->create_publisher<std_msgs::msg::String>("/OBS_Scene", 10);
        camera_2_pub = this->create_publisher<iqs_msgs::msg::Camera>("/Camera_2", 10);
        camera_3_pub = this->create_publisher<iqs_msgs::msg::Camera>("/Camera_3", 10);

        //Timer cb
        base_tracker_timer_ = this->create_wall_timer
            (std::chrono::milliseconds(500),std::bind(&ContentNode::base_tracker_cb, this));

        //For tf2_ros
        tf_buffer_ =
            std::make_unique<tf2_ros::Buffer>(this->get_clock());
        tf_listener_ =
            std::make_shared<tf2_ros::TransformListener>(*tf_buffer_);
        // Initialize the transform broadcaster
        tf_broadcaster_ = std::make_shared<tf2_ros::TransformBroadcaster>(this);

        pull_state = 0;
        dur_state = 0;

        //Default to camera 2
        camera_number = 2;

        //Set default zooms
        // 0 all the way out, 100 all the way in
        camera_2_msg.zoom_pos_cmd = 0.;
        camera_3_msg.zoom_pos_cmd = 0.;

        //Set zoom scaler 
        zoom_scaler = 2.0;

        //Default use pull state
        //Updates dependent on the state callback it gets
        use_pull_state = true;
    }

private:
    double dist(double x, double y){
        return hypot(x, y);
    }

    double normalize_angle_signed(double angle)
    {
        while(angle < -M_PI)
            angle += M_PI * 2.0;
        while(angle > M_PI)
            angle -= M_PI * 2.0;
        return angle;
    }

    void PullStateCallback(const std_msgs::msg::UInt8::SharedPtr msg) {
        pull_state = msg->data;
        use_pull_state = true;

    }

    void DurStateCallback(const std_msgs::msg::UInt8::SharedPtr msg) {
        dur_state = msg->data;
        use_pull_state = false;
    }

    void base_tracker_cb()
    {

        //Use to choose which camera
        //Get transform from track center to base
        geometry_msgs::msg::TransformStamped transform;
        if (tf_buffer_->canTransform("track_center","base",this->get_clock()->now(),tf2::durationFromSec(0.2))){
            transform = tf_buffer_->lookupTransform("track_center","base",this->get_clock()->now(),tf2::durationFromSec(0.2));
        } else {
            RCLCPP_ERROR(this->get_logger(), "base_tracker_cb: Unable to transform from track_center to base");
            return;
        }

        //Default to camera 2
        camera_number = 2;

        //Distance that point must be within quadrant before checking off
        double dist_thresh = 1.0;

        double x,y;
        x = transform.transform.translation.x;
        y = transform.transform.translation.y;

            
        if(x > dist_thresh && x < -dist_thresh){
            //+-
            camera_number = 2;
        } else if (x < -dist_thresh && x < -dist_thresh){
            //--
            camera_number = 3;

        } else if (x < -dist_thresh && x > dist_thresh){
            //-+
            camera_number = 3;
        } else if (x > dist_thresh && x > dist_thresh){
            //++
            camera_number = 2;
        }

        //Get transforms for camera 2 and camera 3 to base
        geometry_msgs::msg::TransformStamped camera_2_transform;
        if (tf_buffer_->canTransform("camera_2","base",this->get_clock()->now(),tf2::durationFromSec(0.2))){
            camera_2_transform = tf_buffer_->lookupTransform("camera_2","base",this->get_clock()->now(),tf2::durationFromSec(0.2));
        } else {
            RCLCPP_ERROR(this->get_logger(), "base_tracker_cb: Unable to transform from camera_2 to base");
            return;
        }
        geometry_msgs::msg::TransformStamped camera_3_transform;
        if (tf_buffer_->canTransform("camera_3","base",this->get_clock()->now(),tf2::durationFromSec(0.2))){
            camera_3_transform = tf_buffer_->lookupTransform("camera_3","base",this->get_clock()->now(),tf2::durationFromSec(0.2));
        } else {
            RCLCPP_ERROR(this->get_logger(), "base_tracker_cb: Unable to transform from camera_3 to base");
            return;
        }

        RCLCPP_INFO(this->get_logger(), "base_tracker_cb: camera 2 x: %g y: %g",camera_2_transform.transform.translation.x,camera_2_transform.transform.translation.y);

        //Get angles for both cameras 
        double camera_2_angle, camera_3_angle;
        camera_2_angle = normalize_angle_signed(std::atan2(camera_2_transform.transform.translation.y,camera_2_transform.transform.translation.x));
        camera_3_angle = normalize_angle_signed(std::atan2(camera_3_transform.transform.translation.y,camera_3_transform.transform.translation.x));

        double camera_2_z_angle, camera_3_z_angle, camera_2_dist, camera_3_dist;
        camera_2_dist = dist(camera_2_transform.transform.translation.x,camera_2_transform.transform.translation.y);
        camera_3_dist = dist(camera_3_transform.transform.translation.x,camera_3_transform.transform.translation.y);
        //Using fixed z
        camera_2_z_angle = normalize_angle_signed(std::atan2(-1.0, camera_2_dist));
        camera_3_z_angle = normalize_angle_signed(std::atan2(-1.0, camera_3_dist));
        RCLCPP_INFO(this->get_logger(), "base_tracker_cb: camera 2 dist: %g camera 3 dist: %g",camera_2_dist,camera_3_dist);
        RCLCPP_INFO(this->get_logger(), "base_tracker_cb: camera 2 angle: %g camera 3 angle: %g",camera_2_angle*180/M_PI,camera_3_angle*180/M_PI);
        RCLCPP_INFO(this->get_logger(), "base_tracker_cb: camera 2 z angle: %g camera 3 z angle: %g",camera_2_z_angle*180/M_PI,camera_3_z_angle*180/M_PI);

        int state;
        if (use_pull_state){
            state = pull_state;
        } else {
            state = dur_state;
        }

        //Populate messages
        camera_2_msg.pan_pos_cmd = camera_2_angle;
        camera_2_msg.pan_speed_cmd = 0.;
        camera_2_msg.tilt_pos_cmd = camera_2_z_angle;
        camera_2_msg.tilt_speed_cmd = 0.;

        camera_3_msg.pan_pos_cmd = camera_3_angle;
        camera_3_msg.pan_speed_cmd = 0.;
        camera_3_msg.tilt_pos_cmd = camera_3_z_angle;
        camera_3_msg.tilt_speed_cmd = 0.;

        //Set zoom cmds
        if (state == 1){
            //Running
            camera_2_msg.zoom_pos_cmd = camera_2_dist*zoom_scaler;
            camera_3_msg.zoom_pos_cmd = camera_3_dist*zoom_scaler;
        } else if (state == 3){
            //Resetting
            camera_2_msg.zoom_pos_cmd = 0.;
            camera_3_msg.zoom_pos_cmd = 0.;
        } else {
            //Stopping or other
            //Use last, don't set
        }

        //Publish camera messages
        camera_2_pub->publish(camera_2_msg);
        camera_3_pub->publish(camera_3_msg);

        //Publish obs scene message
        std_msgs::msg::String obs_scene_msg;
        if (camera_number == 2){
            obs_scene_msg.data = "high_track";
        } else if (camera_number == 3){
            obs_scene_msg.data = "low_track";
        } else {
            //Default
            obs_scene_msg.data = "high_track";
        }
        obs_scene_pub->publish(obs_scene_msg);
    }

    //Subscribers
    rclcpp::Subscription<std_msgs::msg::UInt8>::SharedPtr pull_state_sub;
    rclcpp::Subscription<std_msgs::msg::UInt8>::SharedPtr dur_state_sub;

    //Publishers
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr obs_scene_pub;
    rclcpp::Publisher<iqs_msgs::msg::Camera>::SharedPtr camera_2_pub;
    rclcpp::Publisher<iqs_msgs::msg::Camera>::SharedPtr camera_3_pub;

    std::shared_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    //For tf2_ros
    std::shared_ptr<tf2_ros::TransformListener> tf_listener_{nullptr};
    std::unique_ptr<tf2_ros::Buffer> tf_buffer_;

    //Timer cb
    rclcpp::TimerBase::SharedPtr base_tracker_timer_;

    //Camera numbers 2 or 3
    int camera_number;

    bool use_pull_state;

    // Enumerated states
    // Running 1
    // Stopped 2
    // Resetting 2
    int pull_state;
    int dur_state;

    // Scaler to multiply dist by for zoom
    double zoom_scaler;

    iqs_msgs::msg::Camera camera_2_msg;
    iqs_msgs::msg::Camera camera_3_msg;
};

int main(int argc, char** argv) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<ContentNode>());
    rclcpp::shutdown();
    return 0;
}
