import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    id: rect
    width:parent.width
    height:parent.height
    property var x_min: dataModel.track_extent.x_min
    property var y_min: dataModel.track_extent.y_min
    property var x_max: dataModel.track_extent.x_max
    property var y_max: dataModel.track_extent.y_max
    property var width_meters: x_max-x_min
    property var height_meters: y_max-y_min
    property var x_offset: (x_max+y_max)/2
    color:"#ffFFFF"
    function meters_to_pixels_x(xin)
    {
        var x_out;
        x_out=(rect.width/width_meters)*(xin-x_min);
        return x_out;
    }
    function meters_to_pixels_y(yin)
    {
        var y_out;
        y_out=rect.height-((rect.height/height_meters)*(yin-y_min));
        return y_out;
    }

    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[15].x)
        y:meters_to_pixels_y(dataModel.track_qt[15].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[1].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[1].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[16].x)
        y:meters_to_pixels_y(dataModel.track_qt[16].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[2].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[2].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[10].x)
        y:meters_to_pixels_y(dataModel.track_qt[10].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[8].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[8].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[9].x)
        y:meters_to_pixels_y(dataModel.track_qt[9].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[7].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[7].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[12].x)
        y:meters_to_pixels_y(dataModel.track_qt[12].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[14].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[14].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[11].x)
        y:meters_to_pixels_y(dataModel.track_qt[11].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[13].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[13].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[4].x)
        y:meters_to_pixels_y(dataModel.track_qt[4].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[6].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[6].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[3].x)
        y:meters_to_pixels_y(dataModel.track_qt[3].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[5].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[5].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    /*Loader{
        x:100//meters_to_pixels_x(dataModel.track_qt[1].x)
        y:100//meters_to_pixels_y(dataModel.track_qt[1].y)
        
        property var y_end:400//meters_to_pixels_y(dataModel.track_qt[3].y)
        property var x_end:200//meters_to_pixels_x(dataModel.track_qt[3].x)
        source: "curve.qml"

    }*/

    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[1].x)
        y:meters_to_pixels_y(dataModel.track_qt[1].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[3].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[3].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[2].x)
        y:meters_to_pixels_y(dataModel.track_qt[2].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[4].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[4].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[8].x)
        y:meters_to_pixels_y(dataModel.track_qt[8].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[6].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[6].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[7].x)
        y:meters_to_pixels_y(dataModel.track_qt[7].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[5].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[5].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[11].x)
        y:meters_to_pixels_y(dataModel.track_qt[11].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[9].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[9].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[12].x)
        y:meters_to_pixels_y(dataModel.track_qt[12].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[10].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[10].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[13].x)
        y:meters_to_pixels_y(dataModel.track_qt[13].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[15].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[15].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }
    Loader{
        x:meters_to_pixels_x(dataModel.track_qt[14].x)
        y:meters_to_pixels_y(dataModel.track_qt[14].y)
        property var xend:meters_to_pixels_x(dataModel.track_qt[16].x)
        property var yend:meters_to_pixels_y(dataModel.track_qt[16].y)
        property color color:"#000000"
        property int weight: 10
        source:"line.qml"
    }

    Repeater{
        model:dataModel.track_qt
        delegate:Item{
            x:meters_to_pixels_x(modelData.x)
            y:meters_to_pixels_y(modelData.y)
            Text{
                text: index
            }
        }
    }
    Rectangle{
        color:"#0000FF"
        width:parent.width/100
        height:parent.width/100
        x: meters_to_pixels_x(dataModel.uwb_position.x)-width/2
        y: meters_to_pixels_y(dataModel.uwb_position.y)-height/2
    }

    Rectangle{
        color:"#00FF00"
        width:parent.width/100
        height:parent.width/100
        x: meters_to_pixels_x(dataModel.load_toad_pos_qt.x)-width/2
        y: meters_to_pixels_y(dataModel.load_toad_pos_qt.y)-height/2
    }


}