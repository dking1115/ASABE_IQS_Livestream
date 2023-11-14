import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    color:"#FFFFFF"
    width:parent.width
    height:parent.height
    Rectangle{
        color:"#000000"
        width:parent.width/100
        height:parent.width/100
        x: dataModel.uwb_position.x * 100 +parent.width/2
        y: dataModel.uwb_position.y * -100 + parent.height/2
    }
}