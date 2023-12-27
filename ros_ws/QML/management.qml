import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Management Console"
    //visibility: "FullScreen"
    Rectangle{
        color:"#333333"
        height:parent.height/2
        width:parent.width/4
        Loader{
            width:parent.width
            height:parent.height
            source: "durability_order.qml"
        }
        
    }
    Loader{
        active: dataModel.screen_index_qt == 1
        x: 3*parent.width/4
        width:parent.width/4
        height:parent.height/2
        source: "app_selector.qml"
    }
    Loader{
        active:dataModel.screen_index_qt == 1
        x:parent.width/4
        width:parent.width/4
        height:parent.height/2
        source:"state_selector.qml"
    }
     Loader{
        active:dataModel.screen_index_qt == 1
        x:2*parent.width/4
        width:parent.width/4
        height:parent.height/2
        source:"state_display_panel.qml"
    }

    Loader{
            width:parent.width/4
            height: parent.height/2
            x:0
            y: parent.height/2
            source: "durability_info.qml"
        }
    Loader{
        active: dataModel.screen_index_qt == 2
        width:parent.width
        height:parent.height
        source: "track_setup.qml"
    }
    Loader{
        active: dataModel.screen_index_qt == 5
        width:parent.width
        height:parent.height
        source: "camera.qml"
    }
}