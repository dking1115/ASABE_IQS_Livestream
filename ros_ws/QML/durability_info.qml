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
            ListView{
                id:infolist
                y:parent.height/20
                height:19*parent.height/20
                width:parent.width
                model:dataModel.durability_info_arr_qt
                delegate:Rectangle{
                    width:infolist.width
                    height:infolist.height/4
                    color:"#666666"
                    radius:10
                    Text{
                        text:modelData.key + ":" + modelData.value
                    }
                }
            }
}