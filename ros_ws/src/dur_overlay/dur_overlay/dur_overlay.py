import sys
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtProperty, QVariant, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import rclpy
from iqs_msgs.msg import Durability
from threading import Thread
from std_msgs.msg import String, Float32,Int16
from iqs_msgs.msg import Sled
import time
#from unified_backend.data_model import DataModel
rclpy.init()
node = rclpy.create_node("Overlays")

class overlay_obj():
    def __init__(self,name,qml):
        self.qml=qml
        self.name=name

overlay_objs=[
    overlay_obj("Pulls","Pulls.qml"),
    overlay_obj("Durability","Durability.qml"),
]

class overlay_data(QObject):
    
    overlays_changed=pyqtSignal()
    load_changed=pyqtSignal()
    run_changed=pyqtSignal()
    sled_changed=pyqtSignal()
    def __init__(self):
        print("Backend active")
        super().__init__()
        self.run={}
        self.num=0
        self.run={"team_name":"NA"}
        self.run["start_time"]=time.time()
        self.sled_obj={"dist":0.0,"force":0.0,"speed":0.0}
        self.toad_sub=node.create_subscription(Durability,"durability",self.load_toad_callback,10)
        self.team_sub=node.create_subscription(String,"team_name",self.team_callback,10)
        self.lap_sub=node.create_subscription(Float32,"durability_laps",self.lap_callback,10)
        self.current_callback=node.create_subscription(Int16,"current_durability",self.start_run,10)
        self.sled_sub=node.create_subscription(Sled,"sled",self.sled_callback,10)
        self.timer=node.create_timer(1.0,self.timer_callback)
        self.thread()
        
    
    @pyqtProperty(QVariant,notify=load_changed)
    def load_toad(self):
        return self.load_toad_obj
    
    @pyqtProperty(QVariant,notify=run_changed)
    def run_qml(self):
        return self.run
    
    @pyqtProperty(QVariant,notify=sled_changed)
    def sled_obj_qt(self):
        return self.sled_obj
    
    def sled_callback(self,msg):
        self.sled_obj={}
        self.sled_obj["dist"]=msg.distance
        self.sled_obj["force"]=msg.force
        self.sled_obj["speed"]=msg.speed
        self.sled_changed.emit()

    def timer_callback(self):
        self.run["mins"]=19-((time.time()-self.run["start_time"])/60)
        self.run["secs"]=60-((time.time()-self.run["start_time"])%60)
        self.run_changed.emit()

    def start_run(self,msg):
        if self.num!=msg.data:
            self.run["start_time"]=time.time()
            self.run_changed.emit

    def team_callback(self,msg):
        self.run["team_name"]=msg.data
        self.run_changed.emit()

    def lap_callback(self,msg):
        self.run["laps"]=msg.data
        self.run_changed.emit()

    def load_toad_callback(self,msg):
        self.load_toad_obj={}
        self.load_toad_obj["Pressure"]=msg.drive_pressure
        self.load_toad_obj["speed"]=msg.speed
        self.load_changed.emit()

    def thread(self):
        t1=Thread(target=self.ros_thread)
        t1.start()

    def ros_thread(self):
        print("ros thread started")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        self.node.destroy_node()
        rclpy.shutdown()
        print("ros shutdown")
        


def main():
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = overlay_data()

    # Expose the DataModel instance to QML
    engine.rootContext().setContextProperty("dataModel", data_model)
    print("done")
    #engine.load("file://~/iqs/ros_ws/QML/management.qml")
    #engine.load("QML/management.qml")
    path=QUrl.fromLocalFile("QML/Overlay.qml").path()
    print(path)
    engine.load(path)
    
    print("done")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())