// ArcComponent.qml

import QtQuick 2.15
import QtQuick.Shapes 1.15

Item {
    property real x_start: parent.x
    property real y_start: parent.y
    property real x_end: parent.x_end
    property real y_end: parent.y_end

    width: x_end - x_start
    height: y_end - y_start

    Shape {
        anchors.fill: parent
        layer.enabled: true
        layer.samples: 4

        ShapePath {
            strokeColor: "#000000"
            fillColor: "#FFFFFF"
            fillRule: ShapePath.WindingFill
            strokeWidth: 10
            capStyle: ShapePath.RoundCap

            PathAngleArc {
                centerX: parent.width / 2
                centerY: parent.height / 2
                radiusX: parent.width / 2
                radiusY: parent.width / 2

                // Calculate the start and sweep angles based on the two points
                startAngle: 0//Math.atan2(y_end - y_start, x_end - x_start) * 180 / Math.PI
                sweepAngle: -90
            }
        }
    }
}
