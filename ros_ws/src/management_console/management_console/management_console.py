import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from unified_backend.data_model import DataModel

def main():
    app = QGuiApplication(sys.argv)
    
    engine = QQmlApplicationEngine()
    
    data_model = DataModel(name="Management_console",management=True)

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
