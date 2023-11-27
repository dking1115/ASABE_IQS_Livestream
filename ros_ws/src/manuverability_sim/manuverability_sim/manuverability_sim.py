import rclpy
from rclpy.node import Node
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np

class PylonPublisherNode(Node):
    def __init__(self):
        super().__init__('pylon_publisher_node')
        self.publisher_ = self.create_publisher(Image, 'manuverability_top_down', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)  # Adjust the timer interval as needed
        self.bridge = CvBridge()

        # Create a black image
        self.img = np.zeros((512, 512, 3), np.uint8)
        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', self.draw_rectangle)

        self.drawing = False  # True if mouse is pressed
        self.ix, self.iy = -1, -1  # Starting coordinates

    def draw_pylon(self, x, y, ptype):
        color = (0, 255, 255) if ptype == 1 else (0, 0, 255)
        cv2.rectangle(self.img, (x - 10, y - 10), (x + 10, y + 10), color, -1)
        cv2.circle(self.img, (x, y), 5, (255, 255, 255), -1)
        cv2.imshow('Image', self.img)

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.draw_pylon(x, y, 1)
        if event == cv2.EVENT_RBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
            self.draw_pylon(x, y, 2)

    def timer_callback(self):
        # Publish the image on the 'pylon_image' topic
        image_msg = self.bridge.cv2_to_imgmsg(self.img, encoding='bgr8')
        self.publisher_.publish(image_msg)

        # Display the image
        cv2.imshow('Image', self.img)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    pylon_publisher_node = PylonPublisherNode()
    rclpy.spin(pylon_publisher_node)
    pylon_publisher_node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
