#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist
import numpy as np
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math
import time
j = 0
dat = 0
flag= 0
flag2 = 0
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


## NODE INTITIALIZATION
rospy.init_node('ar_gate', disable_signals=True)

rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
pub = rospy.Publisher('cmd_vel', Twist, queue_size = 1)

speed = Twist()
r = rospy.Rate(10)


while not rospy.is_shutdown():
    print("No. of tags: ",j )
    if j == 2:
        flag = 1
        try:
            global id1, id2
            ## Tag IDS
            id1 = dat.markers[0].id
            id2 = dat.markers[1].id
            
            ## POSITION OF TAGS
            pos_z1 = dat.markers[0].pose.pose.position.z*100
            pos_x1 = dat.markers[0].pose.pose.position.x*100
            
            pos_x2 = dat.markers[1].pose.pose.position.x*100
            pos_z2 = dat.markers[1].pose.pose.position.z*100
            
            ## DISTANCE BETWEEN TAG AND BOT
            dist1 = pow(pow(pos_x1, 2) + pow(pos_z1, 2), 0.5)
            dist2 = pow(pow(pos_x2, 2) + pow(pos_z2, 2), 0.5)
            
            ## CONDITIONS --

            if dist2>dist1:
                x = dist2-dist1
                print("x: ", x)
                if x > 10:
                    speed.linear.x = -0.4
                    speed.angular.z = -pos_x2/500
                    pub.publish(speed)
                else: 
                    speed.linear.x = -0.4
                    speed.angular.z = 0
                    pub.publish(speed)

            if dist1> dist2:
                y = dist1 - dist2
                print("y: ", y)
                if y > 10:
                    speed.linear.x = -0.4
                    speed.angular.z = -pos_x1/500
                    pub.publish(speed)
                else:
                    speed.linear.x = -0.4
                    speed.angular.z = 0
                    pub.publish(speed)

            print(speed)
        except NameError as e:
            print(e)
            pass
    
    if j==1:
        id_val = dat.markers[0].id
        if id_val == id1:
            print(1)
            speed.linear.x = -0.4
            speed.angular.z = -pos_x1/500 + 0.12
            print(speed)

        elif id_val == id2:
            print(2)
            speed.linear.x = -0.4
            speed.angular.z = -pos_x2/500 + 0.12
            print(speed)

        pub.publish(speed)


    elif j==0 and flag == 1:
        if flag == 1:
            speed.linear.x = -0.3
            speed.angular.z = 0
            pub.publish(speed)
            print(speed)
            time.sleep(4)
            flag =2
        if flag == 2:
            speed.linear.x = 0
            speed.angular.z = 0
            pub.publish(speed)
            print(speed)

        
        
    r.sleep()
                                         
