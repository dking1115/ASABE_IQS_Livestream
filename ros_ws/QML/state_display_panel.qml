import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    width:parent.width
    height:parent.height
    color:"#555555"
    Rectangle{
        id:titleBox
        height:parent.height/20
        width:parent.width
        color:"#777777"
        Text{
            anchors.centerIn:parent
            text:"State Display"
            font.pointSize:parent.height/5
        }
    }
    Rectangle{
        y:parent.height/20
        height:parent.height*19/20
        width:parent.width/2
        Loader{
            width:parent.width
            height:parent.height
            source:"state_display.qml"
            property string event:"Pulls"
            property string team:"Iowa State"
            property string state: (dataModel.man_state_qt == 1) ? "Running" : "Stopped"
            property color state_color:"#00FF00"
        }
    }
    Rectangle{
        y:parent.height/20
        x:parent.width/2
        height:parent.height*19/20
        width:parent.width/2
        Loader{
            width:parent.width
            height:parent.height
            source:"state_display.qml"
            property string event:"Pulls"
            property string team:"Iowa State"
            property string state:"Running"
            property color state_color:"#00FF00"
        }
    }
}