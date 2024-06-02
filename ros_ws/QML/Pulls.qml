import QtQuick 2.15
import QtQuick.Controls 2.15

Item {

    Rectangle {
        id: rectangle1
        x: 284
        y: 866
        width: 1353
        height: 169
        color: "#2b2b2b"
        radius: 3
        border.color: "#efd3d3d3"
        border.width: 2
        Text {
            id: text2
            x: 27
            y: 17
            width: 480
            height: 50
            color: "#ffffff"
            text: dataModel.run_qml.team_name
            font.pixelSize: 41
            font.styleName: "Bold"
            font.family: "Verdana"
        }

        Text {
            id: text6
            x: 530
            y: 95
            width: 232
            height: 48
            color: "#ffffff"
            text: dataModel.sled_obj_qt.force.toFixed(0) + " lbf"
            font.pixelSize: 41
            horizontalAlignment: Text.AlignRight
            font.styleName: "Bold"
            font.family: "Verdana"
        }

        Text {
            id: text8
            x: 515
            y: 31
            width: 262
            height: 50
            color: "#ffffff"
            text: dataModel.sled_obj_qt.speed.toFixed(2)+" mph"
            font.pixelSize: 41
            horizontalAlignment: Text.AlignRight
            font.styleName: "Bold"
            font.family: "Verdana"
        }

        Text {
            id: text7
            x: 27
            y: 73
            color: "#ffffff"
            text: dataModel.sled_obj_qt.dist.toFixed(2) + " ft"
            font.pixelSize: 61
            font.styleName: "Bold"
            font.family: "Verdana"
        }

        Image {
            id: image1
            x: 950
            y: 4
            width: 387
            height: 163
            source: "images/ASABE-IQS-logo-white.png"
            fillMode: Image.PreserveAspectFit
        }
    }
}
