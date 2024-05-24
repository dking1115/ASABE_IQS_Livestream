import sys
from PyQt5.QtCore import QUrl, pyqtSignal, pyqtProperty, QVariant, QObject
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
import rclpy
from iqs_msgs.msg import OverlayArray, OverlayObj
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

    def __init__(self):
        print("Backend active")
        super().__init__()
        self.overlay_sub=node.create_subscription(OverlayArray,"overlay_cmd",self.overlay_cmd_callback,10)
        self.thread()
    
    @pyqtProperty(QVariant,notify=overlays_changed)
    def overlay_obj_qt(self):
        return self.obj

    def overlay_cmd_callback(self,msg):
        self.obj=[]
        for overlay in msg.overlays:
            ov={"name":overlay.name,"enabled":overlay.enabled,"x":overlay.x,"y":overlay.y,"scale":overlay.scale}
            for over in overlay_objs:
                if overlay.name==over.name:
                    ov["path"]=over.qml
                    self.obj.append(ov)
        self.overlays_changed.emit()
        #print(self.obj)
    
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