import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    color:"#FFFFFF"
    width:parent.width
    height:parent.height
    Rectangle{
        x:18*parent.width/20
        y:18* parent.height/20
        height:1*parent.height/20
        width:1*parent.width/20
        color:"#999999"
        Button{
            height:parent.height
            width:parent.width
            opacity:0
            onClicked: dataModel.set_track_param(point_selector.currentIndex+1)
        }
    }
    Rectangle{
        x:1*parent.width/20
        y:1*parent.height/20
        height:parent.height/10
        width:parent.height/10
        color:"#444444"
        Button{
            anchors.fill:parent
            opacity:0
            onClicked:dataModel.change_screen(1)
        }
    }
    ComboBox{
        id: point_selector
        x:15*parent.width/20
        y:18*parent.height/20
        width:parent.width/20
        height:parent.height/20
        model: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
    }
    Loader{
        height:3*parent.height/4
        width:3*parent.width/4
        x:parent.width/8
        y:parent.height/8
        source: "durability_track.qml"
    }
}