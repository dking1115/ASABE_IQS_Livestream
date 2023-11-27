import QtQuick 2.15

Rectangle{
    id:rect
    property var xend:parent.xend-parent.x
    property var yend:parent.yend-parent.y
    
    property var length: Math.hypot(xend,yend)
    height:parent.weight
    y:-1*height/2
    property var angle: Math.asin(yend/length)*180/Math.PI
    transform: Rotation{origin.x:0; origin.y:rect.height/2; angle:rect.angle}
    //rotation:angle
    width:length
    
    color:parent.color
}