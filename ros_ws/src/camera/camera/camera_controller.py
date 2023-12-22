#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from .submodules.camera_lib import camera as camera
import math
import time
import cv2 as cv
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from apriltag import Detector, DetectorOptions
import mysql.connector
from geometry_msgs.msg import PoseArray
from sql_package.connection import cursor_connection
from tf2_ros import TransformBuffer, TransformListener
from geometry_msgs.msg import TransformStamped



class camera_obj:
    def __init__(self,ip_addr,port,com_port):
        self.ip_addr=ip_addr
        self.port=port
        self.com_port=com_port
        self.visca_obj=camera(com_port,ip_addr)

class MyNode(Node):

    def __init__(self):
        super().__init__('my_node')
        cursor,db =cursor_connection()
        self.get_logger().info('camera controller startup')

        sql="SELECT camera_id, ip, port, com_port FROM camera_settings"
        result=cursor._execute_query(sql)
        self.cams={}
        for x in result:
            id,ip,port,com_port=x
            cam=camera_obj(ip,port,com_port)
            self.cams[id]=cam
        db.close()
        self.tf_buffer = TransformBuffer(self)
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def lookup_transform(self, target_frame, source_frame):
        try:
            transform = self.tf_buffer.lookup_transform(target_frame, source_frame, rclpy.time.Time())
            return transform
        except Exception as e:
            self.get_logger().error(f"Error looking up transform: {e}")
            return None

    def goto_point(self,point,camera):
        tf=self.lookup_transform("map",f"camera{camera}")
        t=tf.transform.translation
        x=point.x+t.x
        y=point.y+t.y
        z=point.z+t.z
        dist=math.sqrt(x**2+y**2+z**2)
        xy_dist=math.sqrt(x**2+y**2)
        camera_angle=[0,math.asin(x/xy_dist),math.asin(z/xy_dist)]
        

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
