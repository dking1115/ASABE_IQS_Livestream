import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle{
    id:root
    property int selected_camera:0
    property int selected_camera_id:1
    height:parent.height
    width:parent.width
    color: "#444444"
    Button{
        onClicked: dataModel.change_screen(1)
    }

    Rectangle{
        //x:parent.width/20
        y:parent.height/20
        width:parent.width/20
        height:parent.height
        color:parent.color
        ListView{
            id:cameraList
            height:parent.height*18/20
            width:parent.width
            model:dataModel.camera_setting_obj_qt
            spacing: cameraList.height/80
            delegate:Rectangle{
                    height:cameraList.width
                    width:cameraList.width
                    color:"#999999"
                    radius:height/5
                    Text{
                        text:modelData.id
                        anchors.centerIn:parent
                    }
                    Button{
                        width:parent.width
                        height:parent.height
                        opacity:0
                        onClicked: {root.selected_camera=index; 
                                    root.selected_camera_id=modelData.id}
                    }
                
            }
        }
    }
    Rectangle{
        color:parent.color
        x:parent.width/20
        width:parent.width*19/20
        height:parent.height
        Rectangle{
            height:parent.height/4
            width:parent.width/5
            radius:height/10
            color:"#777777"
            Rectangle{
            height:parent.height/4
            width:parent.height/4
            x:parent.width/4-width/2
            y:parent.height/10
            
            radius:height/10
            color:"#888888"
            Rectangle{
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:"X"
                font.pointSize:parent.height/2
                anchors.centerIn:parent
            }
            }
            Rectangle{
                y:parent.height/2
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:dataModel.camera_setting_obj_qt[root.selected_camera].x
                font.pointSize:parent.height/3
                anchors.centerIn:parent
            }
            }
            }
            Rectangle{
            height:parent.height/4
            width:parent.height/4
            x:parent.width/2-width/2
            y:parent.height/10
            
            radius:height/10
            color:"#888888"
            Rectangle{
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:"Y"
                font.pointSize:parent.height/2
                anchors.centerIn:parent
            }
            }
            Rectangle{
                y:parent.height/2
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:dataModel.camera_setting_obj_qt[root.selected_camera].y
                font.pointSize:parent.height/3
                anchors.centerIn:parent
            }
            }
            }
            Rectangle{
            height:parent.height/4
            width:parent.height/4
            x:parent.width*3/4-width/2
            y:parent.height/10
            
            radius:height/10
            color:"#888888"
            Rectangle{
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:"Z"
                font.pointSize:parent.height/2
                anchors.centerIn:parent
            }
            }
            Rectangle{
                y:parent.height/2
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:dataModel.camera_setting_obj_qt[root.selected_camera].z
                font.pointSize:parent.height/3
                anchors.centerIn:parent
            }
            }
            }
            Rectangle{
            
            y:4*parent.height/10
            height:parent.height/4
            width:parent.height/4
            x:parent.width/2-width/2
            radius:height/10
            color:"#888888"
            Rectangle{
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:"Yaw"
                anchors.centerIn:parent
            }
            }
            Rectangle{
                y:parent.height/2
                radius:parent.radius
                height:parent.height/2
                width:parent.width
                color:parent.color
                Text{
                text:dataModel.camera_setting_obj_qt[root.selected_camera].yaw
                anchors.centerIn:parent
            }
            }
            }
            Rectangle{
                width:parent.height/2
                height:parent.height/5
                y:8*parent.height/10
                x:parent.width/4-width/2
                radius:height/4
                color:"#888888"
                Text{
                    anchors.centerIn:parent
                    text:"Set"
                    font.pointSize:parent.height/4
                }
                Button{
                    opacity:0

                }
            }
            Rectangle{
                width:parent.height/2
                height:parent.height/5
                y:8*parent.height/10
                x:parent.width*3/4-width/2
                radius:height/4
                color:"#888888"
                ComboBox {
                width: parent.width
                height:parent.height
                model: [ "Tag 1", "Tag 2", "Tag 3" ]
                }
            }


    
        }

        Rectangle{
                width:parent.width
                height:parent.height/3
                x:0//2*parent.width/4
                y:2*parent.height/4
                color:parent.color
                ListView{
                    id:stateList
                    height:parent.height
                    width:parent.width
                    spacing: parent.height/30
                    model: dataModel.camera_setting_obj_qt[root.selected_camera].states
                    delegate:Rectangle{
                        height:stateList.height/4
                        width:stateList.width
                        radius:height/5
                        color:"#666666"
                        Rectangle{
                            height:parent.height*3/4
                            width:parent.width/5
                            x:parent.width/20
                            y:parent.height/2-height/2
                            radius:parent.height/10
                            color:"#888888"
                            Text{
                            text:"Track State "+modelData.track_state
                            anchors.centerIn:parent
                            }
                        }
                        ComboBox {
                            id:tagSelect
                            currentIndex:modelData.tag-1
                            width: parent.width/8
                            height:parent.height/2
                            x:2*parent.width/3-width/2
                            y:parent.height/2-height/2
                            model: [1,2,3,4,5,6]//modelData.tag_list_qt
                            //textRole:"text"
                            //valueRole: "value"
                            displayText: "Tag: " + currentText
                            
                        }
                        ComboBox {
                            id:modeSelect
                            currentIndex:modelData.mode
                            width: parent.width/8
                            height:parent.height/2
                            x:parent.width/3-width/2
                            y:parent.height/2-height/2
                            model: ["Unset","Joystick","Preset","Tag"]//modelData.tag_list_qt
                            //textRole:"text"
                            //valueRole: "value"
                            displayText: "Mode: " + currentText
                            
                        }
                        ComboBox {
                            id:presetSelect
                            currentIndex:modelData.preset-1
                            width: parent.width/8
                            height:parent.height/2
                            x:parent.width/2-width/2
                            y:parent.height/2-height/2
                            model: [1,2,3,4,5,6,7,8,9,10]//modelData.tag_list_qt
                            //textRole:"text"
                            //valueRole: "value"
                            displayText: "Preset: " + currentText
                            
                        }
                        ComboBox {
                            id:joystickSelect
                            currentIndex:modelData.joystick-1
                            width: parent.width/8
                            height:parent.height/2
                            x:3*parent.width/4-width/2
                            y:parent.height/2-height/2
                            model: [1,2,3,4,5,6,7,8,9,10]//modelData.tag_list_qt
                            //textRole:"text"
                            //valueRole: "value"
                            displayText: "Joystick: " + currentText
                            
                        }

                        Rectangle{
                            width:parent.width/10
                            height:parent.height/2
                            x:7*parent.width/8
                            y:parent.height/2-height/2
                            color:"#888888"
                            radius:height/5
                            Text{
                                text:"Write"
                                anchors.centerIn:parent
                            }
                            Button{
                                anchors.fill:parent
                                onClicked:dataModel.set_camera_trackstate_setting(root.selected_camera_id,modelData.track_state,modeSelect.currentIndex,presetSelect.currentIndex,joystickSelect.currentIndex,tagSelect.currentIndex)
                                opacity:0
                            }
                        }
                        

                    }
                }
            }
                Rectangle{
                    height:parent.height/15
                    width:parent.width/10
                    x:parent.width*16/20
                    y:parent.height*18/20
                    Text{
                        text:"Add"
                        font.pointSize:parent.height/5
                        anchors.centerIn:parent
                    }
                    Button{
                        anchors.fill:parent
                        opacity:0
                        onClicked:dataModel.add_camera_trackstate_setting(root.selected_camera_id)
                    }
                }

                Rectangle{
                    height:parent.height/10
                    width:parent.width/10
                    x:parent.width/4-width/2
                    y:parent.height/4-height/4
                    radius:height/5
                    Rectangle{
                        height:parent.height/3
                        width:parent.width
                        Text{
                            anchors.centerIn:parent
                            text:"IP Address"
                        }
                    }
                    Rectangle{
                        height:2*parent.height/3
                        y:parent.height/3
                        width:parent.width
                        Text{
                            anchors.centerIn:parent
                            text:dataModel.camera_setting_obj_qt[selected_camera].ip
                        }
                    }


                }
                Rectangle{
                    height:parent.height/10
                    width:parent.width/10
                    x:2*parent.width/4-width/2
                    y:parent.height/4-height/4
                    radius:height/5
                    Rectangle{
                        height:parent.height/3
                        width:parent.width
                        Text{
                            anchors.centerIn:parent
                            text:"Port"
                        }
                    }
                    Rectangle{
                        height:2*parent.height/3
                        y:parent.height/3
                        width:parent.width
                        Text{
                            anchors.centerIn:parent
                            text:dataModel.camera_setting_obj_qt[selected_camera].port
                        }
                    }


                }
                Rectangle{
                    height:parent.height/10
                    width:parent.width/10
                    x:3*parent.width/4-width/2
                    y:parent.height/4-height/4
                    radius:height/5
                    Rectangle{
                        height:parent.height/3
                        width:parent.width
                        Text{
                            anchors.centerIn:parent
                            text:"Com Port"
                        }
                    }
                    Rectangle{
                        height:2*parent.height/3
                        y:parent.height/3
                        width:parent.width
                        Text{
                            anchors.centerIn:parent
                            text:dataModel.camera_setting_obj_qt[selected_camera].com_port
                        }
                    }


                }

                ComboBox{
                    id:modeSelect
                    width:parent.width/10
                    height:parent.height/20
                    x:10*parent.width/20-width/2
                    y:8*parent.height/20-height/2
                    model:["Unset","Joystick","Preset","Tag","Auto"]
                    currentIndex: dataModel.camera_setting_obj_qt[selected_camera].mode
                    displayText: "Mode: " + currentText
                }
                ComboBox{
                    id:tagSelect
                    width:parent.width/10
                    height:parent.height/20
                    x:12*parent.width/20-width/2
                    y:8*parent.height/20-height/2
                    model:[1,2,3,4,5,6,7,8,9,10]
                    currentIndex: dataModel.camera_setting_obj_qt[selected_camera].tag
                    displayText: "Tag: " + currentText
                }
                ComboBox{
                    id:presetSelect
                    width:parent.width/10
                    height:parent.height/20
                    x:14*parent.width/20-width/2
                    y:8*parent.height/20-height/2
                    model:[1,2,3,4,5,6,7,8,9,10]
                    currentIndex: dataModel.camera_setting_obj_qt[selected_camera].preset
                    displayText: "Preset: " + currentText
                }
                ComboBox{
                    id:joystickSelect
                    width:parent.width/10
                    height:parent.height/20
                    x:16*parent.width/20-width/2
                    y:8*parent.height/20-height/2
                    model:[1,2,3,4,5,6,7,8,9,10]
                    currentIndex: dataModel.camera_setting_obj_qt[selected_camera].joystick
                    displayText: "Joystick: " + currentText
                    onAccepted: console.log("accepted")
                }
                Rectangle{
                    width:parent.width/10
                    height:parent.height/20
                    x:18*parent.width/20-width/2
                    y:8*parent.height/20-height/2
                    MouseArea{
                        anchors.fill:parent
                        onClicked:dataModel.set_camera_setting(root.selected_camera_id,modeSelect.currentIndex,presetSelect.currentIndex,joystickSelect.currentIndex,tagSelect.currentIndex)

                    }
                }


                


            
        
    }

}