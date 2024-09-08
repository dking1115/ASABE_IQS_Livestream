import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "NDI Stream Viewer"

    Image {
        id:ndiImage
        anchors.fill: parent
        source: "image://ndiImageProvider/image"
        fillMode: Image.PreserveAspectFit
        Connections {
            target: frameNotifier
            onFrameChanged: {ndiImage.source = ""; ndiImage.source = "image://ndiImageProvider/ndiStream"}
        }
    }
}
