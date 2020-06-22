#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist


def callback(msg):
    pose_x = msg.markers[0].pose.pose.position.x
    pose_y = msg.markers[0].pose.pose.position.y
    pose_z = msg.markers[0].pose.pose.position.z
    
    print("x = {0}, y = {1}, z = {2}".format(pose_x, pose_y, pose_z))
    ## ADD WHATEVER YOU WANT HERE


def listener():

    rospy.init_node('ar_pose')
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
