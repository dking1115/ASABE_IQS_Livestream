# my_service_pkg/my_service_pkg/add_two_ints_server.py
import rclpy
from rclpy.node import Node
from iqs_msgs.srv import GetTrack, SetParam
import csv
from geometry_msgs.msg import Point


class TrackManager(Node):

    def __init__(self):
        super().__init__('track_manager')
        self.srv = self.create_service(GetTrack, 'get_track', self.get_track_callback)
        self.set = self.create_service(SetParam, "set_track_param", self.set_param_callback)
        self.track=[]
        with open('track.csv', newline='') as csvfile:
            reader=csv.reader(csvfile)
            for row in reader:
                print(f"x: {row[0]}, y: {row[1]}")
                pt=Point()
                pt.x=float(row[0])
                pt.y=float(row[1])
                self.track.append(pt)

    def save_path(self):
        file = open('track.csv', newline='',mode="w")
        writer=csv.writer(file)
        for x in self.track:
            row=x.x,x.y
            writer.writerow(row)
    def get_track_callback(self, request, response):
        self.get_logger().info(f"Received request:")
        response.points=self.track
        return response
    
    def set_param_callback(self, request, response):
        self.get_logger().info(f"point {request.param_num} changed to x:{request.point.x} y:{request.point.y}")

        self.track[request.param_num]=request.point

        response.success= True
        self.save_path()
        return response


def main(args=None):
    rclpy.init(args=args)
    track_server = TrackManager()
    rclpy.spin(track_server)
    track_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
