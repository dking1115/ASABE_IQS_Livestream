import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, Qt,QCoreApplication
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QPixmap, QImage
import mysql.connector
import rclpy
from threading import *
from geometry_msgs.msg import PoseStamped
from iqs_msgs.srv import SetParam, GetTrack
from sensor_msgs.msg import Image
from nav_msgs.msg import Odometry
import numpy as np
import os
import cv2 as cv
from cv_bridge import CvBridge
from sql_package.connection import cursor_connection


"""def cursor_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkcyde15",
    database="IQS_2024"
    )
    cursor=mydb.cursor()
    return mydb, cursor
"""

rclpy.init()
node=rclpy.create_node('Management')

class DataModel(QObject):
    dur_order_changed = pyqtSignal()
    uwb_position_changed=pyqtSignal()
    track_extent_changed=pyqtSignal()
    track_changed=pyqtSignal()
    screen_index_changed=pyqtSignal()
    durability_info_changed=pyqtSignal()
    man_pic_changed=pyqtSignal()
    load_toad_position_changed=pyqtSignal()
    def __init__(self):
        super().__init__()
        #self.sled_sub=node.create_subscription(Sled,'sled',self.sled_callback,10)
        #self.current_pull_sub = node.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        #self.trackstate_sub = node.create_subscription(Currentpull, 'track_state',self.track_state_callback,10)
        #self.set_client = node.create_client(SetParam,'set_track_param')
        #while not self.set_client.wait_for_service(timeout_sec=1.0):
        #node.get_logger().info('set service not available, waiting again...')
        
        #self.get_client = node.create_client(GetTrack, "get_track")
        #while not self.get_client.wait_for_service(timeout_sec=1.0):
        #node.get_logger().info('get service not available, waiting again...')
        self.durrability_order=[]
        self.teams={}
        self.get_teams()
        self.durability_current_run=0 #id of current durability run going on
        self.durability_current_team=0 #id of team currently running durability
        self.update_dur_order()
        self.update_dur_info()
        self.durability_track_state=1 #1:running 2: stopped 3: reseting
        
        self.load_toad_pos={"x":0.0,"y":0.0}

        #self.uwb_position=PoseStamped()
        self.uwb_pos_obj={"x":0.0,"y":0.0}
        self.uwb_sub=node.create_subscription(PoseStamped,"UWB_position",self.uwb_callback,10)
        self.man_img_sub=node.create_subscription(Image,"manuverability_top_down",self.img_callback,10)
        self.dur_odom_sub=node.create_subscription(Odometry, "load_toad_odom",self.load_toad_odom_callback,10)
        self.track_extent_obj={"x_min":-10,"x_max":10,"y_min":-10,"y_max":10}
        self.track=[]*19
        self.get_track()
        self.thread()
        self.generate_pull_order(1)
        self.man_img_obj=QImage()
        self.screen_index=1
        self.bridge = CvBridge()

    
    @pyqtSlot(int)
    def dur_drop(self,id):
        db,cursor=cursor_connection()
        cursor.execute("SELECT MAX(order_col) FROM Durability_Runs")
        result=cursor.fetchone()
        #print(result)
        cursor.execute(f"UPDATE Durability_Runs SET order_col = {result[0]+1} WHERE (id = {id})")
        db.commit()
        self.update_dur_order()
    
    @pyqtSlot(int)
    def change_screen(self,id):
        self.screen_index=id
        node.get_logger().info(f"Changing to screen {id}")
        self.screen_index_changed.emit()
        if id==6:
            self.exit_app()

    @pyqtSlot()
    def update_track(self):
        self.get_track()
    
    @pyqtSlot(int)
    def set_track_param(self,id):
        print(f"setting point {id}")
        db,cursor=cursor_connection()
        sql=f"UPDATE durability_track SET x = {self.uwb_pos_obj['x']} WHERE (id = {id})"
        cursor.execute(sql)
        sql=f"UPDATE durability_track SET y = {self.uwb_pos_obj['y']} WHERE (id = {id})"
        cursor.execute(sql)
        db.commit()
        db.close()
        self.get_track()
        
    @pyqtSlot(int)
    def set_current_durability_run(self,id):
        #print("hello")
        self.durability_current_run=id
        self.update_dur_order()
        self.update_dur_info()
    
    @pyqtSlot()
    def exit_app(self):
        QCoreApplication.quit()
        sys.exit(-1)
        
    def get_track(self):
        db,cursor=cursor_connection()
        sql = "SELECT id, x, y FROM durability_track"
        cursor.execute(sql)
        result=cursor.fetchall()
        self.track=[0]*19
        
        for i in result:
            id,x,y=i
            point={"x":x,"y":y}
            self.track[id]=point
        self.track_changed.emit()
        sql="SELECT Max(x) FROM durability_track"
        cursor.execute(sql)
        result=cursor.fetchone()
        self.track_extent_obj["x_max"]=result[0]
        sql="SELECT Max(y) FROM durability_track"
        cursor.execute(sql)
        result=cursor.fetchone()
        self.track_extent_obj["y_max"]=result[0]
        sql="SELECT Min(x) FROM durability_track"
        cursor.execute(sql)
        result=cursor.fetchone()
        self.track_extent_obj["x_min"]=result[0]
        sql="SELECT Min(y) FROM durability_track"
        cursor.execute(sql)
        result=cursor.fetchone()
        self.track_extent_obj["y_min"]=result[0]
        print(self.track_extent_obj)
        self.track_extent_changed.emit()

    @pyqtProperty(QVariant, notify=dur_order_changed)
    def dur_order(self):
        return self.durrability_order

    @pyqtProperty(QVariant, notify=uwb_position_changed)
    def uwb_position(self):
        return self.uwb_pos_obj

    @pyqtProperty(QVariant, notify=track_extent_changed)
    def track_extent(self):
        return self.track_extent_obj

    @pyqtProperty(QVariant, notify=load_toad_position_changed)
    def load_toad_pos_qt(self):
        return self.load_toad_pos

    @pyqtProperty(QVariant,notify=track_changed)
    def track_qt(self):
        return self.track
    
    @pyqtProperty(int,notify=screen_index_changed)
    def screen_index_qt(self):
        return self.screen_index

    @pyqtProperty(QVariant,notify=durability_info_changed)
    def durability_info_qt(self):
        return self.durability_info

    @pyqtProperty(QVariant,notify=durability_info_changed)
    def durability_info_arr_qt(self):
        return self.durability_info_arr
    
    @pyqtProperty(QImage,notify=man_pic_changed)
    def man_pic(self):
        return self.man_img_obj


    def get_teams(self):
        db,cursor=cursor_connection()
        cursor.execute("SELECT team_id, team_name, team_number, team_Color, team_abv FROM teams")
        result=cursor.fetchall()
        self.teams={}
        for x in result:
            id,name,number,color,abv=x
            team={"team_name":name,"number":number,"color":color,"abv":abv}
            self.teams[id]=team

    def img_callback(self,msg):
        cv_img=self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
        cv.imwrite("man_pic.png",cv_img)
        #self.man_img_obj=QImage.fromData(msg.data.tobytes())
        #print("img")

    def load_toad_odom_callback(self,msg):
        self.load_toad_pos["x"]=msg.pose.pose.position.x
        self.load_toad_pos["y"]=msg.pose.pose.position.y
        self.load_toad_position_changed.emit()

    def update_dur_info(self):
        db,cursor=cursor_connection()
        print("updating durability info")
        self.durability_info={}
        sql=f"SELECT team_id, team_Name,team_Number,team_color,tractor_name,advisor_name,team_captain,driver_1000lb,drivers_1500lb,team_motto,specfications,biggest_challenge,best_part,weeks_hours_building,years_at_competition,theme_song,5_words,unique_thing,advisor_super_hero FROM teams WHERE team_id={self.durability_current_team}"
        cursor.execute(sql)
        result=cursor.fetchone()
        team_id,name,number,color,tractor_name,advisor,captain,driver_1000,driver_1500,team_motto,specs,biggest_challenge,best_part,time_building,years_at_competition,theme_song,five_words,unique_thing,advisor_superhero=result
        team={"id":team_id,"team_name":name,"team_number":number,"color":color,"tractor_name":tractor_name,"advisor_name":advisor,"captain_name":captain,"drivers_1000":driver_1000,"drivers_1500":driver_1500,"team_motto":team_motto,"tractor_specfications":specs,"biggest_challenge":biggest_challenge,"best_part":best_part,"time_building":time_building,"years_at_competition":years_at_competition,"theme_song":theme_song,"five_words":five_words,"unique_thing":unique_thing,"advisor_superhero":advisor_superhero}
        self.durability_info=team
        team_two=[]
        #team.keys()
        for key in team.keys():
            item={"key":key,"value":team[key]}
            team_two.append(item)
        self.durability_info_arr=team_two
        self.durability_info_changed.emit()
        db.close()
            
    def generate_pull_order(self,hook):
        db,cursor=cursor_connection()
        sql="SELECT team_id FROM teams"
        cursor.execute(sql)
        result=cursor.fetchall()
        teams=[]
        for x in result:
            team_id=x[0]
            team=[team_id,np.random.random()]
            teams.append(team)
        for team in teams:
            sql=f"INSERT INTO pulls (team_id, hook_id) VALUES (%s, %s)"
            vals=team[0],hook
            print(vals)
            cursor.execute(sql,vals)
        db.commit()
        db.close()
        



    def update_dur_order(self):
        db,cursor=cursor_connection()
        cursor.execute("SELECT id, team_id, lap_count FROM Durability_Runs ORDER BY order_col ASC")
        results=cursor.fetchall()
        dur_order=[]
        for x in results:
            id,team_id,laps=x
            obj={"id":id,"team_id":team_id,"team_num":self.teams[team_id]["number"],"team_name":self.teams[team_id]["team_name"],"laps":laps}
            dur_order.append(obj)
            if id==self.durability_current_run:
                self.durability_current_team=team_id
        self.durrability_order=dur_order
        
        self.dur_order_changed.emit()
        #print(dur_order)

    def ros_thread(self):
        print("ros thread started")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        node.destroy_node()
        rclpy.shutdown()
        print("ros shutdown")

    def thread(self):
        t1=Thread(target=self.ros_thread)
        t1.start()

    def uwb_callback(self,msg):
        #self.uwb_position=msg
        self.uwb_pos_obj["x"]=msg.pose.position.x
        self.uwb_pos_obj["y"]=msg.pose.position.y
        self.uwb_position_changed.emit()

        

def main():
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = DataModel()

    # Expose the DataModel instance to QML
    engine.rootContext().setContextProperty("dataModel", data_model)
    print("done")
    #engine.load("file://~/iqs/ros_ws/QML/management.qml")
    #engine.load("QML/management.qml")
    path=QUrl.fromLocalFile("file:///home/david/iqs/ros_ws/QML/management.qml").path()
    print(path)
    engine.load(path)
    
    print("done")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())