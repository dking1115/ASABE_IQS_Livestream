# Import necessary ROS 2 modules
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from iqs_msgs.msg import Camera
from sensor_msgs.msg import Joy
import tf2_ros
import math
from iqs_msgs.msg import OverlayObj, OverlayArray
class SimplePublisher(Node):
    def __init__(self):
        super().__init__('Video_Controller')  # Node name
        self.obs_publisher_ = self.create_publisher(String, 'OBS_Scene', 10)
        self.camera_2_publisher = self.create_publisher(Camera, "Camera_2",10)
        self.camera_3_publisher = self.create_publisher(Camera, "Camera_3",10)
        self.timer = self.create_timer(.01,self.timer_callback)
        self.tf_buffer = tf2_ros.Buffer()
        self.joy_move=[0.0,0.0,0.0]
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.joystick_sub=self.create_subscription(Joy,"joy",self.joy_callback,10)
        self.overlay_pub=self.create_publisher(OverlayArray,"overlay_cmd",10)
        self.cam_2_mode=0
        self.cam_3_mode=0
        self.js_msg=Joy()
    
    def joy_callback(self,msg):
        self.js_msg=msg
        if msg.buttons[2]:
            self.cam_2_mode=1
        elif msg.buttons[3]:
            self.cam_2_mode=0
        
    
    def js_control(self,i):
        msg=self.js_msg
        camera_msg=Camera()
        self.joy_move[0]=msg.axes[0]
        self.joy_move[1]=msg.axes[1]
        self.joy_move[2]=msg.axes[4]
        camera_msg.control_mode=1
        camera_msg.pan_speed_cmd=self.joy_move[0]*18*-1
        camera_msg.tilt_speed_cmd=self.joy_move[1]*18
        camera_msg.zoom_speed_cmd=self.joy_move[2]
        return camera_msg

    def timer_callback(self):
        if self.cam_2_mode==0:
            self.camera_2_publisher.publish(self.auto_mode(2))
        elif self.cam_2_mode==1:
            self.camera_2_publisher.publish(self.js_control(2))
    

    
    def auto_mode(self,i):
        camera_msg=Camera()
        camera_msg.header.stamp=self.get_clock().now().to_msg()
        x=1.0
        y=1.0
        z=1.0
        try:
            transform = self.tf_buffer.lookup_transform(f'camera{i}', 'sled', rclpy.time.Time())
            t=[transform.transform.translation.x,transform.transform.translation.y,transform.transform.translation.z]
            print(t)
            x=transform.transform.translation.x
            y=transform.transform.translation.y
            z=transform.transform.translation.z
        except Exception as E:
            print(E)
        
        
        dist=math.sqrt(x**2+y**2+z**2)
        xy_dist=math.sqrt(x**2+y**2)
        print(math.degrees(math.asin(x/xy_dist)))
        print(-1*math.degrees(math.asin(-1*z/xy_dist)))
        cam_angle=[0,math.degrees(math.asin(x/xy_dist))*-1+90,-1*math.degrees(math.asin(-1*z/xy_dist))]
        camera_msg.pan_pos_cmd=cam_angle[1]
        camera_msg.tilt_pos_cmd=cam_angle[2]
        camera_msg.control_mode=2
        zoom=dist/200 * 8
        camera_msg.zoom_pos_cmd=zoom
        ob=OverlayObj()
        ar=OverlayArray()
        ob.name="Pulls"
        ob.enabled=True
        ar.overlays.append(ob)
        self.overlay_pub.publish(ar)
        #self.camera_publisher.publish(camera_msg)
        return camera_msg

        

    

def main(args=None):
    rclpy.init(args=args)  # Initialize ROS 2

    simple_publisher = SimplePublisher()  # Create an instance of the SimplePublisher node

    rclpy.spin(simple_publisher)  # Start spinning the node

    simple_publisher.destroy_node()  # Destroy the node when spinning is stopped
    rclpy.shutdown()  # Shutdown ROS 2

if __name__ == '__main__':
    main()
