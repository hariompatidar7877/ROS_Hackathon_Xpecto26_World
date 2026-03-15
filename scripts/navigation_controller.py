#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist


class NavigationController(Node):

    def __init__(self):

        super().__init__('navigation_controller')

        self.cmd_pub = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.timer = self.create_timer(
            0.1,
            self.control_loop
        )

        self.step_counter = 0

        self.forward_speed = 1.0
        self.turn_speed = 0.3

        self.get_logger().info("Navigation controller started")

    def generate_command(self):

        cmd = Twist()

        # basic staged motion
        if self.step_counter < 100:

            cmd.linear.x = self.forward_speed
            cmd.linear.z = 0.2

        elif self.step_counter < 200:

            cmd.linear.x = self.forward_speed
            cmd.angular.z = self.turn_speed

        elif self.step_counter < 300:

            cmd.linear.x = self.forward_speed
            cmd.angular.z = -self.turn_speed

        else:

            cmd.linear.x = self.forward_speed
            cmd.angular.z = 0.0

        return cmd

    def control_loop(self):

        cmd = self.generate_command()

        self.cmd_pub.publish(cmd)

        self.step_counter += 1

        if self.step_counter % 50 == 0:

            self.get_logger().info(
                "Velocity command published"
            )

        if self.step_counter > 400:

            self.step_counter = 0


def main(args=None):

    rclpy.init(args=args)

    node = NavigationController()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:

        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()