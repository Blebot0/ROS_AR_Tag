#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math


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
        pos_x = msg.markers[i].pose.pose.position.x *100
        pos_y = msg.markers[i].pose.pose.position.y *100
        pos_z = msg.markers[i].pose.pose.position.z *100
        
        or_x = msg.markers[i].pose.pose.orientation.x
        or_y = msg.markers[i].pose.pose.orientation.y
        or_z = msg.markers[i].pose.pose.orientation.z 
        or_w = msg.markers[i].pose.pose.orientation.w

        quaternion = (or_x, or_y, or_z, or_w)
        euler = euler_from_quaternion(quaternion)
        
        
        roll = math.degrees(euler[0])+180
        pitch = math.degrees(euler[1])+180
        yaw = math.degrees(euler[2])+180
      
        dist = pow( pow(pos_x,2) + pow(pos_y, 2) + pow(pos_z, 2) , 2) 
        print("x = {0}cm, y = {1}cm, z = {2}cm".format(pos_x  , pos_y , pos_z  ))

def listener():
    global pub
    rospy.init_node('ar_pose')
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)
    twist = Twist()
    
    rospy.spin()

if __name__ == '__main__':
    listener()
