import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16
from geometry_msgs.msg import TransformStamped
import tf2_ros
import math

bounding_1=[-11,-9,-1,1]
bounding_2=[9,11,-1,1]

class LapCounter(Node):
    def __init__(self):
        super().__init__('Lap_Counter')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.subscription = self.create_subscription(
            String,
            'current_durability',
            self.current_durability_callback,
            10
        )
        self.current=0
        self.lap_count=0
        self.timer=self.create_timer(.1,self.timer_callback)
        self.in_b1=False
        self.in_b2=False
        self.b1_latch=False
        self.b2_latch=False

    def current_durability_callback(self,msg):
        if self.current!=msg.data:
            self.current=msg.data
            self.lap_count=0

    def timer_callback(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                'map', 'toad_link', rclpy.time.Time())
            #self.get_logger().info(f"Transform: {transform.transform}")
            x=transform.transform.translation.x
            y=transform.transform.translation.y
            if bounding_1[0]<x and bounding_1[1]>x and bounding_1[2]<y and bounding_1[3]>y:
                self.in_b1=True
                self.b1_latch=True
                #print("b1")
            else:
                self.in_b1=False
            if bounding_2[0]<x and bounding_2[1]>x and bounding_2[2]<y and bounding_2[3]>y:
                self.in_b2=True
                self.b2_latch=True
                #print("b2")
            else:
                self.in_b2=False
            #print(f"b1: {self.in_b1} b2: {self.in_b2} b1_latch: {self.b1_latch} b2_latch: {self.b2_latch}")
            if self.in_b1 and self.b2_latch:
                self.lap_count+=1
                print(self.lap_count)
            
            if self.in_b1:
                self.b2_latch=False
            if self.in_b2:
                self.b1_latch=False
            
                
        except tf2_ros.LookupException as e:
            self.get_logger().error(f"Transform lookup failed: {str(e)}")



def main(args=None):
    rclpy.init(args=args)

    lap_counter = LapCounter()

    try:
        rclpy.spin(lap_counter)
    except KeyboardInterrupt:
        pass
    finally:
        lap_counter.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
