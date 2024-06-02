import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Overlays"
    Rectangle{
        anchors.fill:parent
        color:"#f542e9"
    }
    
        Loader{
        anchors.fill:parent
        source:"Pulls.qml"
        enabled:true
        //onLoaded: Console.log(modelData.path)
    }
    
    

}