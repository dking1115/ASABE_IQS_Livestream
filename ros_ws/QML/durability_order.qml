import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    id: list_rect
    width: parent.width
    height: parent.height
    color: "#333333"
    Rectangle{
        color: "#777777"
        height:parent.height/20
        width: parent.width
        Rectangle{
            height:parent.height
            width:parent.width/2
            color:parent.color
        }
        Text{
            anchors.centerIn: parent
            text: "Durability Order"
            font.pointSize: 13
        }
    }
    ListView {
        id: list
        y:2*parent.height/20
        height: 16*parent.height/20
        width:  parent.width 
        model: dataModel.dur_order

        delegate: Item {
            width: list.width
            height: list.height / 10

            Rectangle {
                height: parent.height - 10
                width: parent.width
                color: "#999999"
                Rectangle{
                    height:parent.height
                    width:3*parent.width/4
                    color: parent.color
                    Text {
                        anchors.centerIn: parent
                        text: modelData.team_name
                    }
                }
                Rectangle{
                    x:3*parent.width/4
                    height:parent.height
                    width:parent.width/4
                    color: parent.color
                    Text {
                        anchors.centerIn: parent
                        text: modelData.laps
                    }
                }

                

                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        // Set the currentIndex to the clicked item index
                        list.currentIndex = index;
                    }
                }
            }
        }

        highlight: Rectangle {
            color: "lightsteelblue"
            radius: 5
        }
    }

    Rectangle{
            color: "#777777"
            x:2*parent.width/3
            y:18*parent.height /20
            height: parent.height/10
            width: parent.width/3
            radius:5
            Text{
                text:"Drop"
                font.pointSize: 13
                anchors.centerIn: parent
            }
    Button {
        onClicked: dataModel.dur_drop(list.model[list.currentIndex].id)
        width:parent.width
        height:parent.height
        opacity:0
        
    }
    }
    Rectangle{
            color: "#777777"
            x:1*parent.width/3
            y:18*parent.height /20
            height: parent.height/10
            width: parent.width/3
            radius:5
            Text{
                text:"Run"
                font.pointSize: 13
                anchors.centerIn: parent
            }
    Button {
        onClicked: dataModel.set_current_durability_run(list.model[list.currentIndex].id)
        width:parent.width
        height:parent.height
        opacity:0
        
    }
    }
}