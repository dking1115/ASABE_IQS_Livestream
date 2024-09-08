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
            self.create_subscription(Camera,f"Camera_{0}",partial(self.camera_msg_callback,id=cam_key),10)
        # self.tf_buffer = Buffer()
        # self.tf_listener = TransformListener(self.tf_buffer, self)
        # self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)
        # self.timer=self.create_timer(.1,self.publish_transform)
        # self.tag_sub= self.create_subscription(PoseArray,"tag_array",self.tag_callback,10)
        # self.track_state_sub=self.create_subscription(Int16,"track_state",self.track_state_callback,10)
        # #self.track_state_camera_setting_update()
        #self.camera_msg_sub = self.create_subscription(Camera,"Camera_1",self.camera_msg_callback,10)
        

    # def lookup_transform(self, target_frame, source_frame):
    #     try:
    #         transform = self.tf_buffer.lookup_transform(target_frame, source_frame, rclpy.time.Time())
    #         return transform
    #     except Exception as e:
    #         self.get_logger().error(f"Error looking up transform: {e}")
    #         return None

    # def publish_transform(self):
    #     for i in self.cams.keys():
    #         # Example: Publishing a transform from 'base_link' to 'camera_link'
    #         transform = TransformStamped()
    #         transform.header.stamp = self.get_clock().now().to_msg()
    #         transform.header.frame_id = 'map'
    #         transform.child_frame_id = f'camera{i}'
    #         transform.transform.translation.x = self.cams[i].x
    #         transform.transform.translation.y = self.cams[i].y
    #         transform.transform.translation.z = self.cams[i].z
    #         #transform.transform.rotation = tf2_ros.transformations.quaternion_from_euler(0, 0, self.cams[i].yaw)
    #         self.tf_broadcaster.sendTransform(transform)

    # def goto_point(self,point,camera,zoom_constant,speed):
    #     tf=self.lookup_transform("map",f"camera{camera}")
    #     t=tf.transform.translation
    #     x=point.x+t.x
    #     y=point.y+t.y
    #     z=point.z+t.z
    #     dist=math.sqrt(x**2+y**2+z**2)
    #     xy_dist=math.sqrt(x**2+y**2)
    #     zoom=dist*zoom_constant
    #     camera_angle=[0,math.asin(x/xy_dist),math.asin(z/xy_dist)]
    #     self.cams[camera].visca_obj.abs_pos(speed,camera_angle[1],camera_angle[2])

    # def tag_callback(self,msg):
    #     for i in self.cams.keys():
    #         if self.cams[i].mode==3 and self.cams[i].auto_mode==3:
    #             self.goto_point(msg.poses[self.cams[i].tag].position,.1,17)
    
    # def joystick_callback(self,msg):
    #     for i in self.cams.keys():
    #         if self.cams[i].mode==1 or self.cams[i].mode==3 and self.cams[i].auto_mode==1:
    #             self.cams[i].visca_obj.move(int(msg.axes[0]*17),int(msg.axes[1]*17))

    # def track_state_camera_setting_update(self):
    #     db,cursor=cursor_connection()
    #     sql="SELECT data_id, camera_id, track_state_id, mode, joystick, tag, preset FROM camera_trackstates"
    #     cursor.execute(sql)
    #     results=cursor.fetchall()
    #     for x in results:
    #         id,camera_id,track_state,mode,joystick,tag,preset=x
    #         self.cams[camera_id].track_state_setting[track_state]=[mode,joystick,tag,preset]
        
    # def track_state_callback(self,msg):
    #     for i in self.cams.keys():
    #         cam=self.cams[i]
    #         cam.auto_mode=cam.track_state_setting[msg.data][0]
    #         cam.joystick=cam.track_state_setting[msg.data][1]
    #         cam.tag=cam.track_state_setting[msg.data][2]
    #         cam.preset=cam.track_state_setting[msg.data][3]
    #         if cam.auto_mode==2 and cam.mode==3:
    #             cam.visca_obj.call_preset(cam.preset)

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
            pass
        elif msg.control_mode ==2:
            # if self.cams[cam_id].visca_obj.zoom < msg.zoom_pos_cmd - 5:
            #     self.cams[cam_id].visca_obj.zoom_speed(4)
            #     self.get_logger().info("1")

            # elif self.cams[cam_id].visca_obj.zoom > msg.zoom_pos_cmd + 5:
            #     self.cams[cam_id].visca_obj.zoom_speed(-4)
            #     self.get_logger().info("-1")

            # else:
            #     self.cams[cam_id].visca_obj.zoom_speed(0)
            #     self.get_logger().info("0")
            
            self.cams[cam_id].visca_obj.closed_zoom_goal=msg.zoom_pos_cmd
            self.get_logger().info(f"Cam: {cam_id} Zoom {self.cams[cam_id].visca_obj.zoom} Cmd: {msg.zoom_pos_cmd}")
        elif msg.control_mode ==3:
            self.cams[cam_id].visca_obj.abs_pos(int(msg.pan_speed_cmd),msg.pan_pos_cmd,msg.tilt_pos_cmd)
            pass
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