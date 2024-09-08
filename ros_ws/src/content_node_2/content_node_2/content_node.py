import rclpy
from rclpy.node import Node
from iqs_msgs.msg import Camera
from std_msgs.msg import String
from sensor_msgs.msg import Joy
class TrackState():
    def __init__(self,number,zones=None):
        self.number=number
        self.zones=zones

class Zone():
    def __init__(self,name,contentstate=None,bounds=[0,0,0,0]):
        self.name=name
        self.contentstate=contentstate
        self.bounds=bounds

    def __str__(self):
        return f"Name: {self.name} Bounds {self.bounds} content_state: {self.contentstate}"

class ContentState():
    def __init__(self,camera_targets=[],camera_target_data=[],obs_scene=None):
        self.camera_targets=camera_targets
        self.camera_target_data=camera_target_data
        self.obs_scene=obs_scene
    
    def __str__(self):
        return f"Camera Targets: {self.camera_targets} Data: {self.camera_target_data} Scene: {self.obs_scene}"


class MyNode(Node):
    def __init__(self):
        # Initialize the node with the allow_undeclared_parameters option set to True
        super().__init__('content_node', allow_undeclared_parameters=True,automatically_declare_parameters_from_overrides=True)
        #self.get_logger().info("Node started with allow_undeclared_parameters=True")
        #print("start")
        #list=self.get_parameters(["number_of_cameras","states"])
        list=self.get_parameters_by_prefix("states")
        #print("end")
        #print(list)
        #print(list)
        self.num_cameras=self.get_parameter("number_of_cameras").value
        states=[]
        #self.get_logger().info(f"Param: {list.keys()}")
        for param in list.keys():
            state=param.split(".")[0]
            if state not in states:
                states.append(state)
        states=[int(state) for state in states]
        self.get_logger().info(f"States: {states}")
        self.state_objs=[]
        for state in states:
            zones=[]
            zone_objs=[]
            for param in list.keys():
                sp=param.split(".")
                if sp[0]==str(state) and sp[1]=="zones":
                    #self.get_logger().info(f"True")
                    if sp[2] not in zones:
                        zones.append(sp[2])
            for zone in zones:
                params=self.get_parameters_by_prefix(f"states.{state}.zones.{zone}")
                targets=[]
                data=[]
                for i in range(self.num_cameras):
                    cam_num=i+1
                    targets.append(self.get_parameter(f"states.{state}.zones.{zone}.camera_{cam_num}_target").value)
                    data.append(self.get_parameter(f"states.{state}.zones.{zone}.camera_{cam_num}_target_data").value)
                scene=self.get_parameter(f"states.{state}.zones.{zone}.obs_scene").value
                contentstate=ContentState(targets,data,scene)
                self.get_logger().info(f"{contentstate}")
                par=f"states.{state}.zones.{zone}."
                pars=[par+p for p in ["x_min","x_max","y_min","y_max"]]
                bounds=[i.value for i in self.get_parameters(pars)]
                zone_obj=Zone(zone,contentstate,bounds)
                self.get_logger().info(f"{zone_obj}")
                zone_objs.append(zone_obj)

            self.get_logger().info(f"State {state} Zones: {zones}")
            
            state_obj=TrackState(state,zone_objs)
            self.state_objs.append(state_obj)
        self.state_dict={a.number:a for a in self.state_objs}


        self.camera_pubs=[self.create_publisher(Camera,f"Camera_{i}",10) for i in range(self.num_cameras)]
        self.obs_pub=self.create_publisher(String,"obs_scene",10)
        self.joy_sub=self.create_subscription(Joy,"joy",self.joy_callback,10)
        self.timer=self.create_timer(.01,self.timer_callback)


    def timer_callback(self):
        pass

    def track_state_callback(self,msg):
        pass

    def joy_callback(self,msg):
        pan_cmd=msg.axes[0]*-12
        tilt_cmd=msg.axes[1]*12
        if msg.buttons[4]:
            pan_cmd=pan_cmd*2
            tilt_cmd=tilt_cmd*2
        zoom_cmd=msg.axes[4]
        cam_msg=Camera()
        cam_msg.control_mode=1
        cam_msg.pan_speed_cmd=pan_cmd
        cam_msg.tilt_speed_cmd=tilt_cmd
        cam_msg.zoom_speed_cmd=zoom_cmd
        self.camera_pubs[0].publish(cam_msg)

    
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
