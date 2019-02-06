#!/usr/bin/env python
import rospy
import roslib
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float32
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import sys
#print(sys.path)
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
#print(sys.path)
import cv2

bridge = CvBridge()


def callback(image_msg):
    print("Received Image")
    #First convert the image to OpenCV image
    try:
        cv_image = bridge.imgmsg_to_cv2(image_msg, "bgr8")
    except CvBridgeError as e:
        print(e)
        rospy.loginfo(rospy.get_caller_id() + " " + e)
        return

    (rows,cols,channels) = cv_image.shape
    if cols > 60 and rows > 60 :
        cv2.circle(cv_image, (50,50), 10, 255)
    cv2.imshow("Classify", cv_image)
    rospy.loginfo(rospy.get_caller_id() + "Received Image")

def listner():

    rospy.init_node('classify', anonymous=True)
    rospy.Subscriber("image_channel", Image, callback)

    rospy.spin()

    cv2.destroyWindow()

if __name__ == "__main__":
    listner()
