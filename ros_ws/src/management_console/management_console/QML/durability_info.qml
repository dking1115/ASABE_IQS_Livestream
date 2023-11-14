import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
            id:info
            height:parent.height
            width:parent.width
            color: "#444444"
            Rectangle{
                height:parent.height/20
                width: parent.width
                color: "#777777"
                Text{
                    anchors.centerIn: parent
                    text:"Durability Info"
                }
            }
            Rectangle{
                
            }
}