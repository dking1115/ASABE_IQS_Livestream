import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped

class UWBPositionPublisher(Node):
    def __init__(self):
        super().__init__('uwb_position_publisher')
        self.subscription = self.create_subscription(
            PoseStamped,
            'goal_pose',
            self.goal_pose_callback,
            10)
        self.publisher = self.create_publisher(PoseStamped, 'UWB_position', 10)

    def goal_pose_callback(self, msg):
        self.get_logger().info('Received Goal Pose')
        # Modify the pose if needed
        # For example, you might want to republish the same pose
        self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)

    uwb_position_publisher = UWBPositionPublisher()

    try:
        rclpy.spin(uwb_position_publisher)
    except KeyboardInterrupt:
        pass

    uwb_position_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
