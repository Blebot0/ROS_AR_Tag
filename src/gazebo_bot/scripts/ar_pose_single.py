#!/usr/bin/env python
import rospy
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist
from tf.transformations import euler_from_quaternion, quaternion_from_euler
import math


pos_x = 0
pos_y = 0
pos_z = 0
markers = 0


def callback(msg):
    global pos_x, pos_y, pos_z, markers
    markers = len(msg.markers)
    if len(msg.markers)==1:
        print("ID:       " + str(msg.markers[0].id))
        pos_x = msg.markers[0].pose.pose.position.x *100
        pos_y = msg.markers[0].pose.pose.position.y *100
        pos_z = msg.markers[0].pose.pose.position.z *100
        print("x = {0}cm, y = {1}cm, z = {2}cm".format(pos_x  , pos_y , pos_z  ))
        

rospy.init_node('ar_pose_single')

rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
pub = rospy.Publisher('cmd_vel', Twist, queue_size = 10)

r = rospy.Rate(100)
speed = Twist()


while not rospy.is_shutdown():
       # speed.linear.x = -pos_z/300
        speed.linear.x = -0.5
        speed.angular.z = -pos_x/50

        dis1 = pow( pow(pos_x , 2) + pow(pos_z , 2) , 0.5)
        
        print(speed)
        if pos_z > 30 and pos_z<45:
            print(speed)
            speed.linear.x = -0.2
        
        if pos_z < 30 or markers == 0:
            print(1)            
            speed.linear.x = 0
            speed.angular.z = 0
        
        print("Distance", dis1)
        
        pub.publish(speed)    
        r.sleep()


    

