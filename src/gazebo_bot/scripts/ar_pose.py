#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist
import numpy as np

def callback(msg):
    j = 0   
    ids = []
    while 1:
        try:
            x = int(msg.markers[j].id)
            ids.append(x)
            j += 1
        except IndexError:
            break
    

    for i in range(j):
        print("ID:       " + str(msg.markers[i].id))
        pose_x = msg.markers[i].pose.pose.position.x 
        pose_y = msg.markers[i].pose.pose.position.y
        pose_z = msg.markers[i].pose.pose.position.z 
        
        or_x = msg.markers[i].pose.pose.orientation.x
        or_y = msg.markers[i].pose.pose.orientation.y
        or_z = msg.markers[i].pose.pose.orientation.z 
        or_w = msg.markers[i].pose.pose.orientation.w
        print("x = {0}, y = {1}, z = {2}".format(pose_x, pose_y, pose_z))
        print("or_z = {0}, or_y = {1}, or_z = {2}, or_w = {3}".format(or_x, or_y, or_z, or_w)) 
    ## ADD WHATEVER YOU WANT HERE



def listener():

    rospy.init_node('ar_pose')
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
