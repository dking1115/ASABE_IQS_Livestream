import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Management Console"

    Rectangle{
        color:"#333333"
        height:parent.height/2
        width:parent.width/4
        Loader{
            width:parent.width
            height:parent.height
            source: "durability_order.qml"
        }
        
    }
    Loader{
            width:parent.width/4
            height: parent.height/2
            x:0
            y: parent.height/2
            source: "durability_info.qml"
        }
    Loader{
        width:parent.width
        height:parent.height
        source: "track_setup.qml"
    }
}