import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Management Console"
    Rectangle{
        anchors.fill:parent
        color:"#f542e9"
    }
    Repeater{
        model:dataModel.overlay_obj_qt
        Loader{
        anchors.fill:parent
        source:modelData.path
        enabled:modelData.enabled
        //onLoaded: Console.log(modelData.path)
    }
    }
    

}