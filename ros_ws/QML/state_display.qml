import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    id:root
    property string event:parent.event
    property string team:parent.team
    property string state:parent.state
    property color state_color:parent.state_color
    width:parent.width
    height:parent.height
    color:"#555555"
    Rectangle{
        id:titleBox
        color:"#777777"
        height:parent.height*1/20
        width:parent.width
        Text{
            anchors.centerIn:parent
            text:root.event
            font.pointSize:parent.height/2.5
        }
    }
    Rectangle{
        id:contentBox
        y:parent.height/20
        height:parent.height*19/20
        width:parent.width
        color:parent.color
        Rectangle{
            color:root.state_color
            height:parent.height/10
            width:parent.width
            Text{
                anchors.centerIn:parent
                text:root.state
                font.pointSize:parent.height/2.5
            }
        }
        Rectangle{
            width:parent.width
            height:parent.height/5
            y:parent.height/5
            color:parent.color
            
            Text{
                anchors.centerIn: parent
                font.pointSize:parent.height/5
                text:root.team
                wrapMode:Text.WordWrap
            }
        }
    }
}