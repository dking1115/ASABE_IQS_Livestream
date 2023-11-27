import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_msgs.msg import Int16
from geometry_msgs.msg import TransformStamped
import tf2_ros
import math
import mysql.connector

bounding_1=[-11,-9,-1,1]
bounding_2=[9,11,-1,1]

def cursor_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkcyde15",
    database="IQS_2024"
    )
    cursor=mydb.cursor()
    return mydb, cursor
def dist(point1,point2):
    distance=math.sqrt((point1["x"]-point2["x"])**2+(point1["y"]-point2["y"])**2)
    return distance
def arc_length(point1,point2,point3,point4):
    center={"x":point2["x"],"y":point4["y"]}
    radius=(((dist(point1,center)+dist(point2,center))/2)+((dist(point3,center)+dist(point4,center))/2)/2)
    length=radius*math.pi/2
    return length
def split(point1,point2):
    center_1={"x":(point1["x"]+point2["x"])/2,"y":(point1["y"]+point2["y"])/2}
    return center_1

def straight_length(point1,point2,point3,point4):
    center_1=split(point1,point2)
    center_2=split(point3,point4)
    length=dist(center_1,center_2)
    return length

def is_in(point,point1,point2,point3,point4):
    x_max=max(point1["x"],point2["x"],point3["x"],point4["x"])
    x_min=min(point1["x"],point2["x"],point3["x"],point4["x"])
    y_max=max(point1["y"],point2["y"],point3["y"],point4["y"])
    y_min=min(point1["y"],point2["y"],point3["y"],point4["y"])
    return point["x"]>=x_min and point["x"] <=x_max and point["y"]>=y_min and point["y"]<=y_max

def arc_dist_travled(point,point1,point2,point3,point4):
    center={"x":point2["x"],"y":point4["y"]}
    radius=(((dist(point1,center)+dist(point2,center))/2)+((dist(point3,center)+dist(point4,center))/2)/2)
    theta=abs(math.asin((point["y"]-point2["y"])/radius))
    distance=theta*radius
    return distance

class LapCounter(Node):
    def __init__(self):
        super().__init__('Lap_Counter')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.subscription = self.create_subscription(
            String,
            'current_durability',
            self.current_durability_callback,
            10
        )
        self.current=0
        self.lap_count=0
        self.timer=self.create_timer(.1,self.timer_callback)
        self.in_b1=False
        self.in_b2=False
        self.b1_latch=False
        self.b2_latch=False
        self.track=[0]*19
        db,cursor=cursor_connection()
        sql="SELECT id,x,y FROM durability_track"
        cursor.execute(sql)
        results=cursor.fetchall()
        for i in results:
            id,x,y=i
            point={"x":x,"y":y}
            self.track[id]=point
        self.length_arc_4=arc_length(self.track[13],self.track[14],self.track[15],self.track[16])
        self.length_arc_1=arc_length(self.track[3],self.track[4],self.track[1],self.track[2])
        self.length_arc_3=arc_length(self.track[11],self.track[12],self.track[9],self.track[10])
        self.length_arc_2=arc_length(self.track[5],self.track[6],self.track[7],self.track[6])
        self.straight_length_1=straight_length(self.track[3],self.track[4],self.track[5],self.track[6])
        self.straight_length_2=straight_length(self.track[8],self.track[7],self.track[10],self.track[9])
        self.straight_length_3_1=straight_length(split(self.track[14],self.track[12]),split(self.track[11],self.track[13]),self.track[14],self.track[13])
        self.straight_length_3_2=straight_length(split(self.track[14],self.track[12]),split(self.track[11],self.track[13]),self.track[12],self.track[11])
        self.straight_length_4=straight_length(self.track[16],self.track[15],self.track[2],self.track[1])
        #print(f"straight length: {straight_length_1} {straight_length_2} {straight_length_3} {straight_length_4}")
        #print(f"arc length: {length_arc_1} {length_arc_2} {length_arc_3} {length_arc_4}")
        self.track_total_length=self.length_arc_1+self.length_arc_2+self.length_arc_3+self.length_arc_4+self.straight_length_1+self.straight_length_2+self.straight_length_3_1+self.straight_length_3_2+self.straight_length_4
    
    def current_durability_callback(self,msg):
        if self.current!=msg.data:
            self.current=msg.data
            self.lap_count=0

    def timer_callback(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                'map', 'toad_link', rclpy.time.Time())
            #self.get_logger().info(f"Transform: {transform.transform}")
            x=transform.transform.translation.x
            y=transform.transform.translation.y
            if bounding_1[0]<x and bounding_1[1]>x and bounding_1[2]<y and bounding_1[3]>y:
                self.in_b1=True
                self.b1_latch=True
                #print("b1")
            else:
                self.in_b1=False
            if bounding_2[0]<x and bounding_2[1]>x and bounding_2[2]<y and bounding_2[3]>y:
                self.in_b2=True
                self.b2_latch=True
                #print("b2")
            else:
                self.in_b2=False
            #print(f"b1: {self.in_b1} b2: {self.in_b2} b1_latch: {self.b1_latch} b2_latch: {self.b2_latch}")
            if self.in_b1 and self.b2_latch:
                self.lap_count+=1
                print(self.lap_count)
            
            if self.in_b1:
                self.b2_latch=False
            if self.in_b2:
                self.b1_latch=False
            
            point={"x":x,"y":y}

            if is_in(point,split(self.track[14],self.track[12]),split(self.track[13],self.track[11]),self.track[11],self.track[12]):
                dist_traveled=dist(point,split(split(self.track[14],self.track[12]),split(self.track[13],self.track[11])))
                print(f" dist travled: {dist_traveled}")
            
            if is_in(point,self.track[11],self.track[12],self.track[9],self.track[10]):
                dist_traveled=arc_dist_travled(point,self.track[11],self.track[12],self.track[13],self.track[14])+self.straight_length_3_2
                print(f" dist travled: {dist_traveled}")
            
            if is_in(point,self.track[4],self.track[3],self.track[5],self.track[6]):
                print("in 1")
            




            
                
        except tf2_ros.LookupException as e:
            self.get_logger().error(f"Transform lookup failed: {str(e)}")



def main(args=None):
    rclpy.init(args=args)

    lap_counter = LapCounter()

    try:
        rclpy.spin(lap_counter)
    except KeyboardInterrupt:
        pass
    finally:
        lap_counter.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
