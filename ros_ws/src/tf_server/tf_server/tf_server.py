import rclpy
from rclpy.node import Node
from sql_package.connection import cursor_connection
from iqs_msgs.msg import Sled
import tf2_ros
from geometry_msgs.msg import TransformStamped
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
        transform.transform.translation.x = 10.1
        transform.transform.translation.y = 12.4
        transform.transform.translation.z = 1.4
        self.static_tf_broadcaster.sendTransform(transform)
    

    def sled_callback(self,msg):
        dist=msg.distance
        transform=TransformStamped()
        transform.header.stamp=msg.header.stamp
        transform.header.frame_id = 'map'
        transform.child_frame_id = f'sled'
        transform.transform.translation.x = 10.1 + (dist*0.3048)
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