#!/usr/bin/env python
import rospy
from visualization_msgs.msg import Marker
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import PointStamped, Twist
import tf
from tf.transformations import euler_from_quaternion
from math import *
from sensor_msgs.msg import Imu
import time

ar_id=0
dist=0
sign=0
other_tag=0
gate_dist=2
markers=[]

yaw=0

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
twist = Twist()

def callback_pose(msg):
	global ar_id, dist, sign, other_tag
	
	ar_id=msg.id
	posx, posy, posz = msg.pose.position.x, msg.pose.position.y, msg.pose.position.z

	if ar_id == 4:
		dist=posz
		sign=-1
		other_tag=5
	if ar_id == 5:
		dist=posz
		sign=1
		other_tag=4

def callback_ar(msg):
	global markers
	if len(msg.markers)>1:
		for i in msg.markers:
			markers.append(i.id)
        

def imu(pose):
	global yaw
	quaternion = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)

	euler = euler_from_quaternion(quaternion)
	yaw= degrees(euler[2])+180
	yaw = abs(yaw-360)
	yaw = yaw%360

def stop():
	twist.linear.y = 0
	twist.linear.z = 0
	twist.angular.x=0
	twist.angular.y=0
	twist.angular.z=0
	twist.linear.x = 0
	pub.publish(twist)

def align(angle): 
	flag=0
	while 1:
		if flag==0:
			time.sleep(0.1)
			final_yaw = yaw + angle
			if final_yaw<0:
				final_yaw=360+final_yaw
        		if final_yaw>360:
				final_yaw=final_yaw%360
			flag=1
		angle_diff = yaw-final_yaw
		if angle_diff<1 and angle_diff>-1: 
				stop()
				break
		if angle>0:
			twist.angular.z = -1
			pub.publish(twist)
		elif angle<0:
			twist.angular.z = 1
			pub.publish(twist)

def move(move_dist, sign):
	move_dist=move_dist*5
	a=time.time()
	while (time.time()-a)<=(move_dist/0.8):
		twist.linear.x=sign*0.8 
		pub.publish(twist)
	stop()

def gate_trav():
	move_dist=gate_dist/2
	align(90)
	time.sleep(0.1)
	initial_dist=dist
	initial_sign=sign
	initial_other_tag=other_tag
	tri_dist=(2*sqrt(3)*(initial_dist+sqrt(3)/30)-gate_dist)/2
	move(move_dist, initial_sign)
	while 1:
		time.sleep(1)
		if initial_other_tag in markers:
			align(-90)
			move(dist+2, 1)
			stop()
			break
		move(tri_dist, initial_sign)
		align(-1*initial_sign*120)
		move(move_dist+tri_dist, initial_sign)
		time.sleep(1)
	
def listener():
	rospy.init_node('bot_yaw', anonymous=True,disable_signals= True)
	rospy.Subscriber("camera_2/visualization_marker", Marker, callback_pose)
	rospy.Subscriber("camera_2/ar_pose_marker", AlvarMarkers, callback_ar)
	rospy.Subscriber("/imu", Imu, imu)

	rate = rospy.Rate(10) # 10hz

	while 1:
		gate_trav()
		exit()	

	rospy.spin()

if __name__ == '__main__':
    listener()
