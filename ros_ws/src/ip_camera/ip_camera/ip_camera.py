import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import urllib.request
import numpy as np


class IPCameraPublisher(Node):
    def __init__(self):
        super().__init__('ip_camera_publisher')
        self.publisher_ = self.create_publisher(Image, 'image_topic', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Adjust the timer interval as needed
        self.bridge = CvBridge()

        # Replace 'your_ip_camera_url' with the actual URL of your IP camera
        self.ip_camera_url = 'rtsp://admin:darkcyde15@10.0.0.112/play1.sdp'
        self.cap = cv2.VideoCapture(self.ip_camera_url)

    def timer_callback(self):
        # Capture frame from IP camera
        img_np = self.capture_frame_from_ip_camera()

        if img_np is not None:
            # Convert the NumPy array to a ROS Image message
            ros_image = self.bridge.cv2_to_imgmsg(img_np, 'bgr8')

            # Publish the image message
            self.publisher_.publish(ros_image)

    def capture_frame_from_ip_camera(self):
        try:
            # Open the IP camera stream
            #stream = urllib.request.urlopen(self.ip_camera_url)

            # Read the frame
            #img_array = np.array(bytearray(stream.read()), dtype=np.uint8)

            #img_np = cv2.imdecode(img_array, -1)
            ret, img_np = self.cap.read()
            return img_np

        except Exception as e:
            self.get_logger().warn(f"Error capturing frame from IP camera: {str(e)}")
            return None

def main(args=None):
    rclpy.init(args=args)
    ip_camera_publisher = IPCameraPublisher()
    rclpy.spin(ip_camera_publisher)
    ip_camera_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
