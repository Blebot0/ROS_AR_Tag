#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist


def callback(msg):
    print(msg)
    ## ADD WHATEVER YOU WANT HERE


def listener():

    rospy.init_node('ar_pose')
    print(1)
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    print(2)
    rospy.spin()

if __name__ == '__main__':
    listener()
