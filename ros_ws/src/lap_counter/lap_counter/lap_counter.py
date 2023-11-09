import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import TransformStamped
import tf2_ros
import math


class SimplePublisher(Node):
    def __init__(self):
        super().__init__('simple_publisher')
        self.publisher = self.create_publisher(String, 'example_topic', 10)
        self.timer = self.create_timer(1, self.publish_message)

    def publish_message(self):
        msg = String()
        msg.data = 'Hello, ROS 2!'
        self.publisher.publish(msg)


class SimpleTransformListener(Node):
    def __init__(self):
        super().__init__('simple_transform_listener')
        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.subscription = self.create_subscription(
            String,
            'example_topic',
            self.message_callback,
            10
        )

    def message_callback(self, msg):
        try:
            transform = self.tf_buffer.lookup_transform(
                'map', 'toad_link', rclpy.time.Time())
            self.get_logger().info(f"Received message: {msg.data}")
            self.get_logger().info(f"Transform: {transform.transform}")
        except tf2_ros.LookupException as e:
            self.get_logger().error(f"Transform lookup failed: {str(e)}")


def main(args=None):
    rclpy.init(args=args)

    simple_publisher = SimplePublisher()
    simple_transform_listener = SimpleTransformListener()

    try:
        rclpy.spin(simple_publisher)
        rclpy.spin(simple_transform_listener)
    except KeyboardInterrupt:
        pass
    finally:
        simple_publisher.destroy_node()
        simple_transform_listener.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
