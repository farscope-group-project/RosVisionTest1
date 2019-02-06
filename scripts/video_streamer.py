#! /usr/bin/env python2
# -*- coding: utf-8 -*-
"""

Copyright (c) 2015 PAL Robotics SL.
Released under the BSD License.

Created on 7/14/15

@author: Sammy Pfeiffer

test_video_resource.py contains
a testing code to see if opencv can open a video stream
useful to debug if video_stream does not work
"""
import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


import time
import sys
sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
import cv2

bridge = CvBridge()

def videoStreamPublisher(cap):
    pub = rospy.Publisher('image_channel', Image, queue_size=3)
    rospy.init_node('video_stream_publisher', anonymous=True)
    #rate = rospy.Rate(1)
    time.sleep(2)
    rval,frame = cap.read()
    while (not rospy.is_shutdown()) and rval:
        rval,frame = cap.read()
        cv2.imshow("Stream", frame)
        time.sleep(1)
        try:
            msg_frame = bridge.cv2_to_imgmsg(frame, "bgr8")
        except CvBridgeError as e:
            print(e)

        pub.publish(msg_frame, "bgr8")
        cv2.waitKey(10)
        #rate.sleep()

    cv2.destroyWindow();


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "You must give an argument to open a video stream."
        print "  It can be a number as video device, e.g.: 0 would be /dev/video0"
        print "  It can be a url of a stream,        e.g.: rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov"
        print "  It can be a video file,             e.g.: myvideo.mkv"
        exit(0)

    resource = sys.argv[1]
    # If we are given just a number, interpret it as a video device
    if len(resource) < 3:
        resource_name = "/dev/video" + resource
        resource = int(resource)
    else:
        resource_name = resource
    print "Trying to open resource: " + resource_name
    cap = cv2.VideoCapture(resource)
    if not cap.isOpened():
        print "Error opening resource: " + str(resource)
        print "Maybe opencv VideoCapture can't open it"
        exit(0)


    try:
        videoStreamPublisher(cap)
    except rospy.ROSInterruptException:
        pass

