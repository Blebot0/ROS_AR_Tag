#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math

j = 0
dat = 0

def callback(msg):
    global j, dat
    dat = msg
    j = 0
    ids = []
    while 1:
        try:
            x = int(msg.markers[j].id)
            ids.append(x)
            j += 1
        except IndexError:
            break



rospy.init_node('ar_gate')

rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

speed = Twist()
r = rospy.Rate(100)

while not rospy.is_shutdown():
    pos_x = []    
    pos_z = []
    ids = []
    or_x = []
    or_y = []
    or_z = []
    or_w = []
    quaternion = []
    euler = []
    roll = []
    pitch = []
    yaw = []
    dist = []
    print(j)
    if j == 2:
		try:
		    for i in range(j):
		    	
		        ids.append(dat.markers[i].id)

		        pos_x.append(dat.markers[i].pose.pose.position.x)
		        pos_z.append(dat.markers[i].pose.pose.position.z)
                        dist.append(pow(pow(pos_x, 2) + pow(pos_z, 2) , 0.5))           
		        or_x.append(dat.markers[i].pose.pose.orientation.x)
		        or_y.append(dat.markers[i].pose.pose.orientation.y)
		        or_z.append(dat.markers[i].pose.pose.orientation.z)
		        or_w.append(dat.markers[i].pose.pose.orientation.w)
		        
		        quaternion.append([or_x[i], or_y[i], or_z[i], or_w[i]])
		        euler.append(euler_from_quaternion(quaternion[i]))
                        
                        print("dist: ", pos_z)

		      #  roll.append(math.degrees(euler[i][0])+180)
		        pitch.append((math.degrees(euler[i][1])+180 + 180)%360)
		      #  yaw.append( math.degrees(euler[i][2])+180)
		        #pitch values are what we require    
		        #print("pitch: ", pitch)

                        max_dist = max(dist)
                        a = dist.index(max_dist)

                        print(max_dist, a)
		except:
		    pass

    r.sleep()
