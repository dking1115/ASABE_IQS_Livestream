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
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener
from geometry_msgs.msg import TransformStamped
import tf2_ros
from std_msgs.msg import Int16
from iqs_msgs.msg import Camera
from functools import partial

class camera_obj:
    def __init__(self,ip_addr,port,com_port,x,y,z,yaw):
        self.ip_addr=ip_addr
        self.port=port
        self.com_port=com_port
        self.visca_obj=camera(com_port,ip_addr,port)
        self.x=x
        self.y=y
        self.z=z
        self.yaw=yaw
        self.mode=0 # 0:unset 1:joystick 2:preset 3: tag 4:auto
        self.joystick=0
        self.tag=0
        self.track_state_setting={}
        self.auto_mode=0 # 0:unset 1:joystick 2:preset 3:tag
        self.tilt_pos_cmd=0
        self.pan_pos_cmd=0
        self.zoom_pos_cmd=0
        self.pan_speed_cmd=0
        self.tilt_speed_cmd=0
        self.pzoom=1

class MyNode(Node):

    def __init__(self):
        super().__init__('camera_controller')
        db,cursor =cursor_connection()
        self.get_logger().info('camera controller startup')
        sql="SELECT camera_id, ip, port, com_port,x,y,z,yaw FROM camera_settings"
        cursor.execute(sql)
        result=cursor.fetchall()
        self.cams={}
        for x in result:
            print(x)
            id,ip,port,com_port,x,y,z,yaw=x
            cam=camera_obj(ip,port,com_port,x,y,z,yaw)
            self.cams[id]=cam
        db.close()
        print(self.cams)
        for cam_key in self.cams.keys():
            self.create_subscription(Camera,f"Camera_{cam_key}",partial(self.camera_msg_callback,id=cam_key),10)

    def camera_msg_callback(self,msg,id):
        """
        Modes:
        0: idle
        1: speed control
        2: closed loop control
        3: position control
        4: preset
        """
        cam_id=int(id)
        self.cams[cam_id].visca_obj.control_mode=msg.control_mode
        self.cams[cam_id].tilt_pos_cmd=msg.tilt_pos_cmd #not doing anything
        self.cams[cam_id].pan_pos_cmd=msg.pan_pos_cmd #not doing anything
        # self.cams[cam_id].visca_obj.closed_pan_goal=0.0
        self.cams[cam_id].visca_obj.closed_pan_goal=-msg.pan_pos_cmd
        # self.cams[cam_id].visca_obj.closed_tilt_goal=0.0
        self.cams[cam_id].visca_obj.closed_tilt_goal=msg.tilt_pos_cmd
        self.cams[cam_id].zoom_pos_cmd=msg.zoom_pos_cmd
        self.cams[cam_id].pan_speed_cmd=msg.pan_speed_cmd
        self.cams[cam_id].tilt_speed_cmd=msg.tilt_speed_cmd

        if msg.control_mode==0:
            pass
        elif msg.control_mode==1:
            self.cams[cam_id].visca_obj.move(int(msg.pan_speed_cmd),int(msg.tilt_speed_cmd))
            cmd=msg.zoom_speed_cmd
            if int(msg.zoom_speed_cmd*7) != 0 or self.cams[cam_id].pzoom!=0:
                self.cams[cam_id].visca_obj.zoom_speed(int(msg.zoom_speed_cmd*7))
        elif msg.control_mode ==2:
            self.cams[cam_id].visca_obj.closed_zoom_goal=msg.zoom_pos_cmd
            self.get_logger().info(f"Cam: {cam_id} Zoom {self.cams[cam_id].visca_obj.zoom} Cmd: {msg.zoom_pos_cmd}")
        elif msg.control_mode ==3:
            self.cams[cam_id].visca_obj.abs_pos(int(msg.pan_speed_cmd),msg.pan_pos_cmd,msg.tilt_pos_cmd)
        elif msg.control_mode ==4:
            pass


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