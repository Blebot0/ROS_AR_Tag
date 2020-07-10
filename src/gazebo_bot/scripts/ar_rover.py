#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math
import time


##CALLBACKS

def callback1(msg):
    if len(msg.markers) == 1:
        print("CAM1(right) markers: ", msg.markers[0].id)
        pos_x = msg.markers[0].pose.pose.position.x
        pos_y = msg.markers[0].pose.pose.position.y
        pos_z = msg.markers[0].pose.pose.position.z
        print("x: ", pos_x)
        print("y: ", pos_y)
        print("z: ", pos_z)

    
    else:
        print("NONE CAM1")

def callback2(msg):
    if len(msg.markers) == 1:
        print("CAM2(left) markers: ", msg.markers[0].id)
    else:
        print("NONE CAM2")
## NODE INTITIALIZATION
rospy.init_node('ar_gate', disable_signals=True)

rospy.Subscriber("/camera_1/ar_pose_marker", AlvarMarkers, callback1)
rospy.Subscriber("/camera_2/ar_pose_marker", AlvarMarkers, callback2)

speed = rospy.Publisher('cmd_vel', Twist, queue_size = 10)

speed = Twist()
r = rospy.Rate(100)


while not rospy.is_shutdown():
    r.sleep()

