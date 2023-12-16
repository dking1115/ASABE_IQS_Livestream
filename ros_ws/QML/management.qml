import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Management Console"

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
        x: 3*parent.width/4
        width:parent.width/4
        height:parent.height/2
        source: "app_selector.qml"
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
<<<<<<< HEAD
     Image {
        width: parent.width
        height: parent.height
        source: "man_pic.png"
        asynchronous: true
    }
    
=======
    Button{
        x:parent.width/2
        y:parent.height/2
        onClicked:exit_app()
    }
>>>>>>> bf7f81bca5bdb3766dab6cd8d2b154728de83ffb
}