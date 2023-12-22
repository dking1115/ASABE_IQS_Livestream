import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    height:parent.height
    width:parent.width
    color:"#444444"
    ListModel{
            id:applistmodel
            ListElement{ name: "Durability track setup"; index: 2}
            ListElement{ name: "Pulls"; index: 3}
            ListElement{ name: "Manuverability Setup"; index: 4}
            ListElement{ name: "Camera Settings"; index: 5}
            ListElement{ name: "Exit"; index: 6}

        }
    ListView{
        id:applist
        model:applistmodel
        width:parent.width
        height:7*parent.height/8
        y:parent.height/8
        delegate:Rectangle{
                width:applist.width
                height:applist.height/8
                radius:10
                color:"#777777"
                Text{
                    text: name
                    anchors.centerIn: parent
                    

                }
                Button{
                    height:parent.height
                    width:parent.width
                    onClicked: dataModel.change_screen(index)
                    opacity:0
                }

            }
    }
}