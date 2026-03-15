#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class GateDetector(Node):

    def __init__(self):

        super().__init__('gate_detector')

        # cv bridge
        self.bridge = CvBridge()

        # camera subscriber
        self.image_sub = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.image_callback,
            10
        )

        self.frame_count = 0
        self.last_detection = False

        self.get_logger().info("Gate detector initialized")

    def preprocess_frame(self, frame):

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edges = cv2.Canny(blur, 50, 150)

        return edges

    def detect_rectangles(self, edges):

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_TREE,
            cv2.CHAIN_APPROX_SIMPLE
        )

        rectangles = []

        for cnt in contours:

            area = cv2.contourArea(cnt)

            if area < 500:
                continue

            approx = cv2.approxPolyDP(
                cnt,
                0.02 * cv2.arcLength(cnt, True),
                True
            )

            if len(approx) == 4:
                rectangles.append(approx)

        return rectangles

    def draw_detections(self, frame, rectangles):

        for rect in rectangles:

            cv2.drawContours(
                frame,
                [rect],
                -1,
                (0, 255, 0),
                2
            )

        return frame

    def image_callback(self, msg):

        try:

            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        except Exception as e:

            self.get_logger().error("Image conversion failed")
            return

        edges = self.preprocess_frame(frame)

        rectangles = self.detect_rectangles(edges)

        output = self.draw_detections(frame, rectangles)

        if len(rectangles) > 0:

            if not self.last_detection:
                self.get_logger().info("Gate detected")

            self.last_detection = True

        else:

            self.last_detection = False

        cv2.imshow("Gate Detection", output)

        cv2.waitKey(1)

        self.frame_count += 1


def main(args=None):

    rclpy.init(args=args)

    node = GateDetector()

    try:

        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()