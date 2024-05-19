# Import necessary ROS 2 modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from iqs_msgs.msg import Camera

class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')  # Node name
        self.obs_publisher_ = self.create_publisher(String, 'OBS_Scene', 10)
        self.camera_publisher = self.create_publisher(Camera, "Camera_1",10)
        self.timer = self.create_timer(.01,self.timer_callback)
    
    def timer_callback(self):
        camera_msg=Camera()
        camera_msg.header.stamp=self.get_clock().now().to_msg()
        self.camera_publisher.publish(camera_msg)
        

    

def main(args=None):
    rclpy.init(args=args)  # Initialize ROS 2

    simple_publisher = SimplePublisher()  # Create an instance of the SimplePublisher node

    rclpy.spin(simple_publisher)  # Start spinning the node

    simple_publisher.destroy_node()  # Destroy the node when spinning is stopped
    rclpy.shutdown()  # Shutdown ROS 2

if __name__ == '__main__':
    main()
