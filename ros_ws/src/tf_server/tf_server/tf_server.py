import rclpy
from rclpy.node import Node
from sql_package.connection import cursor_connection
from iqs_msgs.msg import Sled
import tf2_ros
from geometry_msgs.msg import TransformStamped
import math
class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        db,cursor =cursor_connection()
        self.get_logger().info('tf server startup')
        self.static_tf_broadcaster = tf2_ros.StaticTransformBroadcaster(self)
        self.dyn_tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        self.cam_timer=self.create_timer(10,self.publish_camera_tf)
        self.sled_sub=self.create_subscription(Sled,"sled",self.sled_callback,10)

    def get_track(self):
        db,cursor=cursor_connection()
        sql="SELECT track_start_x,track_start_y,track_end_x,track_end_y FROM pull_track_settings WHERE id = 1"
        cursor.execute(sql)
        result=cursor.fetchone()
        for i in result:
            start_x,start_y,end_x,end_y=i
    
    def publish_camera_tf(self):
        i=2
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'map'
        transform.child_frame_id = f'camera{i}'
        transform.transform.translation.x = 67.0
        transform.transform.translation.y = 10.0
        transform.transform.translation.z = 2.0
        
        roll=0.0
        pitch=0.0

        yaw = 3*math.pi / 2  # 45 degrees in radians
        quaternion = self.euler_to_quaternion(roll, pitch, yaw)
        transform.transform.rotation.x = quaternion[0]
        transform.transform.rotation.y = quaternion[1]
        transform.transform.rotation.z = quaternion[2]
        transform.transform.rotation.w = quaternion[3]
        self.static_tf_broadcaster.sendTransform(transform)
        

    def euler_to_quaternion(self, roll, pitch, yaw):
        cy = math.cos(yaw * 0.5)
        sy = math.sin(yaw * 0.5)
        cr = math.cos(roll * 0.5)
        sr = math.sin(roll * 0.5)
        cp = math.cos(pitch * 0.5)
        sp = math.sin(pitch * 0.5)

        qw = cy * cr * cp + sy * sr * sp
        qx = cy * sr * cp - sy * cr * sp
        qy = cy * cr * sp + sy * sr * cp
        qz = sy * cr * cp - cy * sr * sp

        return [qx, qy, qz, qw]


    def sled_callback(self,msg):
        dist=msg.distance
        transform=TransformStamped()
        transform.header.stamp=msg.header.stamp
        transform.header.frame_id = 'map'
        transform.child_frame_id = f'sled'
        transform.transform.translation.x = 0 + (dist*0.3048)
        transform.transform.translation.y = 0.0
        transform.transform.translation.z = 1.0
        
        self.dyn_tf_broadcaster.sendTransform(transform)

        

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()