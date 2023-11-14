import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import mysql.connector
import rclpy
from threading import *
from geometry_msgs.msg import PoseStamped


def cursor_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkcyde15",
    database="IQS_2024"
    )
    cursor=mydb.cursor()
    return mydb, cursor

rclpy.init()
node=rclpy.create_node('Management')

class DataModel(QObject):
    dur_order_changed = pyqtSignal()
    uwb_position_changed=pyqtSignal()
    track_extent_changed=pyqtSignal()
    def __init__(self):
        super().__init__()
        #self.sled_sub=node.create_subscription(Sled,'sled',self.sled_callback,10)
        #self.current_pull_sub = node.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        #self.trackstate_sub = node.create_subscription(Currentpull, 'track_state',self.track_state_callback,10)

        self.durrability_order=[]
        self.teams={}
        self.get_teams()
        self.update_dur_order()
        self.durability_track_state=1 #1:running 2: stopped 3: reseting
        self.durability_current_run=0 #id of current durability run going on
        #self.uwb_position=PoseStamped()
        self.uwb_pos_obj={"x":0.0,"y":0.0}
        self.uwb_sub=node.create_subscription(PoseStamped,"UWB_position",self.uwb_callback,10)
        self.track_extent_obj={"x_min":-10,"x_max":10,"y_min":-10,"y_max":10}

        self.thread()

    
    @pyqtSlot(int)
    def dur_drop(self,id):
        db,cursor=cursor_connection()
        cursor.execute("SELECT MAX(order_col) FROM Durability_Runs")
        result=cursor.fetchone()
        #print(result)
        cursor.execute(f"UPDATE Durability_Runs SET order_col = {result[0]+1} WHERE (id = {id})")
        db.commit()
        self.update_dur_order()
        

    @pyqtProperty(QVariant, notify=dur_order_changed)
    def dur_order(self):
        return self.durrability_order

    @pyqtProperty(QVariant, notify=uwb_position_changed)
    def uwb_position(self):
        return self.uwb_pos_obj

    @pyqtProperty(QVariant, notify=track_extent_changed)
    def teack_extent(self):
        return self.track_extent_obj

    def get_teams(self):
        db,cursor=cursor_connection()
        cursor.execute("SELECT team_id, team_name, team_number, team_Color, team_abv FROM teams")
        result=cursor.fetchall()
        self.teams={}
        for x in result:
            id,name,number,color,abv=x
            team={"team_name":name,"number":number,"color":color,"abv":abv}
            self.teams[id]=team



    def update_dur_order(self):
        db,cursor=cursor_connection()
        cursor.execute("SELECT id, team_id, lap_count FROM Durability_Runs ORDER BY order_col ASC")
        results=cursor.fetchall()
        dur_order=[]
        for x in results:
            id,team_id,laps=x
            obj={"id":id,"team_id":team_id,"team_num":self.teams[team_id]["number"],"team_name":self.teams[team_id]["team_name"],"laps":laps}
            dur_order.append(obj)
        self.durrability_order=dur_order
        self.dur_order_changed.emit()
        print(dur_order)

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

    engine.load(QUrl("src/management_console/management_console/QML/management.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())