#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class AutonomousNavigation(Node):

    def __init__(self):

        super().__init__('autonomous_navigation')

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.navigation_loop
        )

        self.state = 0
        self.counter = 0

        self.get_logger().info("Autonomous navigation node running")

    def navigate_forward(self, cmd):

        cmd.linear.x = 1.0
        cmd.linear.z = 0.2

    def adjust_left(self, cmd):

        cmd.linear.x = 0.8
        cmd.angular.z = 0.3

    def adjust_right(self, cmd):

        cmd.linear.x = 0.8
        cmd.angular.z = -0.3

    def stabilize(self, cmd):

        cmd.linear.x = 0.5
        cmd.angular.z = 0.0

    def navigation_loop(self):

        cmd = Twist()

        if self.state == 0:

            self.navigate_forward(cmd)

        elif self.state == 1:

            self.adjust_left(cmd)

        elif self.state == 2:

            self.adjust_right(cmd)

        else:

            self.stabilize(cmd)

        self.cmd_pub.publish(cmd)

        self.counter += 1

        if self.counter > 120:

            self.state += 1
            self.counter = 0

        if self.state > 3:

            self.state = 0


def main(args=None):

    rclpy.init(args=args)

    node = AutonomousNavigation()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()