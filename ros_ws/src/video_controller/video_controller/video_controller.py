# Import necessary ROS 2 modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from iqs_msgs.msg import Camera
from sensor_msgs.msg import Joy
import tf2_ros
import math
class SimplePublisher(Node):
    def __init__(self):
        super().__init__('Video_Controller')  # Node name
        self.obs_publisher_ = self.create_publisher(String, 'OBS_Scene', 10)
        self.camera_publisher = self.create_publisher(Camera, "Camera_1",10)
        #self.timer = self.create_timer(.01,self.timer_callback)
        self.tf_buffer = tf2_ros.Buffer()
        self.joy_move=[0.0,0.0,0.0]
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.joystick_sub=self.create_subscription(Joy,"joy",self.joy_callback,10)
    
    def joy_callback(self,msg):
        camera_msg=Camera()
        self.joy_move[0]=msg.axes[0]
        self.joy_move[1]=msg.axes[1]
        self.joy_move[2]=msg.axes[4]
        camera_msg.control_mode=1
        camera_msg.pan_speed_cmd=self.joy_move[0]*18*-1
        camera_msg.tilt_speed_cmd=self.joy_move[1]*18
        camera_msg.zoom_speed_cmd=self.joy_move[2]

        self.camera_publisher.publish(camera_msg)

    def timer_callback(self):
        camera_msg=Camera()
        camera_msg.header.stamp=self.get_clock().now().to_msg()
        x=1.0
        y=1.0
        z=1.0
        try:
            transform = self.tf_buffer.lookup_transform('camera2', 'sled', rclpy.time.Time())
            t=[transform.transform.translation.x,transform.transform.translation.y,transform.transform.translation.z]
            print(t)
            x=transform.transform.translation.x
            y=transform.transform.translation.y
            z=transform.transform.translation.z
        except:
            pass
        
        
        dist=math.sqrt(x**2+y**2+z**2)
        xy_dist=math.sqrt(x**2+y**2)
        cam_angle=[0,math.degrees(math.asin(x/xy_dist))*-1+90,-1*math.degrees(math.asin(-1*z/xy_dist))]
        camera_msg.pan_pos_cmd=cam_angle[1]
        camera_msg.tilt_pos_cmd=cam_angle[2]
        camera_msg.control_mode=2

        

    

def main(args=None):
    rclpy.init(args=args)  # Initialize ROS 2

    simple_publisher = SimplePublisher()  # Create an instance of the SimplePublisher node

    rclpy.spin(simple_publisher)  # Start spinning the node

    simple_publisher.destroy_node()  # Destroy the node when spinning is stopped
    rclpy.shutdown()  # Shutdown ROS 2

if __name__ == '__main__':
    main()
