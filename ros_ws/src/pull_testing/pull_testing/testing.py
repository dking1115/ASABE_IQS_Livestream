import rclpy
from rclpy.node import Node
from iqs_msgs.msg import Sled
from std_msgs.msg import Int8
#from sled_msg.msg import Currentpull
from rclpy.serialization import serialize_message
import random
import time
import csv
class YourNode(Node):
    def __init__(self):
        super().__init__('your_node')
        self.get_logger().info("Your ROS 2 Node is running!")
        self.sled_pub_timer=self.create_timer(.01,self.sled_timer_callback)
        self.sled_pub = self.create_publisher(Sled,'sled',10)
        self.track_state_pub = self.create_publisher(Int8, 'pull_state',10)
        #self.current_pull_sub = self.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        #self.track_state_timer = self.create_timer(1,self.track_state_publish)
        self.track_state_sub = self.create_subscription(Int8,"pull_state",self.track_state_callback,10)
        self.track_state=0
        self.current_pull=0
        self.speed=0.0
        self.dist=0.0
        self.load=0.0
        self.pull_active=False
        self.offset=0
        
    def sled_timer_callback(self):
        if self.track_state==1:
            msg=Sled()
            print(f"Pulling {self.dist} {self.speed}")
            self.speed=-1*(self.dist-99)**4 /10000000 +10+self.offset
            self.dist=1.46667*self.speed/100 +self.dist
            self.load=self.dist*10
            msg.distance=self.dist
            msg.speed=self.speed
            msg.force=self.load
            msg.header.stamp=self.get_clock().now().to_msg()
            self.sled_pub.publish(msg)
            if self.speed<.01:
                self.track_state=2
                #self.track_state_publish()
                time.sleep(10)
                self.track_state=3
                self.track_state_publish()
                
    
    def track_state_callback(self,msg):
        self.track_state=msg.data
        self.dist=0
    
    def track_state_publish(self):
        msg = Int8()
        msg.data=self.track_state
        #msg.header.stamp=self.get_clock().now().to_msg()
        self.track_state_pub.publish(msg)
    
    def current_pull_callback(self,msg):
        self.current_pull=msg.pullid
        time.sleep(10)
        print("Starting Pull")
        self.track_state=1
        self.track_state_publish()
        self.offset=random.random()
        self.dist=0


    


            






def main(args=None):
    rclpy.init(args=args)
    node = YourNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()