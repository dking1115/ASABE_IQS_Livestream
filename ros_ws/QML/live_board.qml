import QtQuick 2.15
import QtQuick.Controls 2.15

ApplicationWindow {
    visible: true
    width: 1920
    height: 1080
    title: "Live Board"
    Loader{
        active:true
        height:parent.height
        width:parent.height
        source:"pulls_live_board.qml"
    }
    Loader{
        active:dataModel.active_events_qt.man
        height:parent.height
        width:parent.height
        source:"man_live_board.qml"
    }
    Loader{
        active:dataModel.active_events_qt.dur
        height:parent.height
        width:parent.height
        source:"dur_live_board.qml"
    }
    Loader{
        active:dataModel.active_events_qt.man && dataModel.active_events_qt.dur
        height:parent.height
        width:parent.height
        source:"man_dur_live_board.qml"
    }
    Button{
        height:parent.height /2
        width:parent.width/2
        x:parent.width/2
        y:parent.height/2
        onClicked:{
            console.log(dataModel.active_events_qt.man)
        }
    }
}