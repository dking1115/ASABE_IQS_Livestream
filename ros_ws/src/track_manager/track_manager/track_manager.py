# my_service_pkg/my_service_pkg/add_two_ints_server.py
import rclpy
from rclpy.node import Node
from track_manager.srv import GetTrack, SetParam


class AddTwoIntsServer(Node):

    def __init__(self):
        super().__init__('add_two_ints_server')
        self.srv = self.create_service(GetTrack, 'get_track', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        self.get_logger().info(f"Received request: {request.id}")
        response.params[0]=1.0
        return response


def main(args=None):
    rclpy.init(args=args)
    add_two_ints_server = AddTwoIntsServer()
    rclpy.spin(add_two_ints_server)
    add_two_ints_server.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
