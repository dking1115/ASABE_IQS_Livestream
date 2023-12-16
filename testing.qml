import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 400
    height: 300
    title: "QML Example"

    Rectangle {
        width: 200
        height: 100
        color: "lightblue"
        anchors.centerIn: parent

        Text {
            anchors.centerIn: parent
            text: "Hello from QML!"
        }
    }
}
