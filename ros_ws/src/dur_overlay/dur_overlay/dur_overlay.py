import sys
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtProperty, QVariant, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import rclpy
from iqs_msgs.msg import Durability
from threading import Thread
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
    def __init__(self):
        print("Backend active")
        super().__init__()
        self.toad_sub=node.create_subscription(Durability,"durability",self.load_toad_callback,10)
        self.thread()
    
    @pyqtProperty(QVariant,notify=load_changed)
    def load_toad(self):
        return self.load_toad_obj
    
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