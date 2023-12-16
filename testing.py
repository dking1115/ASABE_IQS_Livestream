import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Create a QML application engine
    engine = QQmlApplicationEngine()

    # Load the QML file
    engine.load(QUrl.fromLocalFile("testing.qml"))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec_())
