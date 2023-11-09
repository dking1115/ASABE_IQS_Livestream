import sys
from PyQt5.QtCore import QObject, QUrl, pyqtProperty, pyqtSignal, pyqtSlot, QVariant, Qt
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import mysql.connector
import rclpy
from threading import *
import uuid


rclpy.init()
uu=uuid.uuid4().hex
node=rclpy.create_node(f'durability_overlays_{uu}')

class DataModel(QObject):
    def __init__(self):
        super().__init__()
        # Initialize data as an array of dictionaries
        self.thread()

    #@pyqtProperty(QVariant, notify=lastChanged)
    #def last_pulls_qt(self):
    #    return self.last_pulls_list

    def thread(self):
        t1=Thread(target=self.ros_thread)
        t1.start()

    def ros_thread(self):
        print("ros thread started")
        try:
            rclpy.spin(node)
        except KeyboardInterrupt:
            pass
        node.destroy_node()
        rclpy.shutdown()
        print("ros shutdown")

    def track_state_callback(self,msg):
        if msg.trackstate!=self.current_track_state:
            self.current_track_state=msg.trackstate
            self.trackChanged.emit()


        
        

def main():
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = DataModel()

    # Expose the DataModel instance to QML
    engine.rootContext().setContextProperty("dataModel", data_model)

    engine.load(QUrl("src/durability_overlay/durability_overlay/QML/Durability_Overlay.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
