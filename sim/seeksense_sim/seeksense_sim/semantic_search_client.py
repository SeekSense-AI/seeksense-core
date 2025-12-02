import rclpy
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image


class SemanticSearchClient(Node):
    """
    Placeholder ROS2 node for integrating a robot with the SeekSense semantic search API.

    This is intentionally minimal and heavily commented so it can be shown as
    R&D scaffolding while you build the real logic.
    """

    def __init__(self):
        super().__init__('semantic_search_client')

        # TODO: adjust topics to your robot stack
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/robot_pose',  # or /amcl_pose, /pose, etc.
            self.pose_callback,
            10,
        )
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10,
        )

        self.current_pose = None
        self.latest_image = None
        self.session_id = None

        self.get_logger().info('SemanticSearchClient node initialised (placeholder).')

    def pose_callback(self, msg: PoseStamped) -> None:
        """Store the latest robot pose."""
        self.current_pose = msg

    def image_callback(self, msg: Image) -> None:
        """Store the latest camera frame."""
        self.latest_image = msg

    def start_search(self, target_text: str) -> None:
        """
        TODO: Call SeekSense API `search_start` with:
          - target description (text)
          - current pose
          - basic camera intrinsics

        For now, we just log the intent.
        """
        if self.current_pose is None:
            self.get_logger().warn('Cannot start search – no pose received yet.')
            return

        self.get_logger().info(f'[TODO] Starting semantic search for: "{target_text}"')
        # Example placeholder: assign a dummy session id
        self.session_id = 'dummy-session-id'

    def spin_once(self) -> None:
        """
        TODO: Call SeekSense API `search_next`, convert the returned waypoint
        into a Nav2 goal, and monitor progress.

        Right now, this simply logs that it would perform a step.
        """
        if self.session_id is None:
            self.get_logger().warn('spin_once() called but no active search session.')
            return

        self.get_logger().info('[TODO] spin_once: call search_next and forward waypoint to Nav2')

    # You can later add helper methods:
    # - send_nav2_goal(...)
    # - handle search_verify(...)
    # - checkpoint state, etc.


def main(args=None) -> None:
    rclpy.init(args=args)
    node = SemanticSearchClient()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()