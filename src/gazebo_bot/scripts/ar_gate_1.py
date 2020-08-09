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

ar_id = -1
right_ar_heading = 0
left_ar_heading = 0
posx = posy = posz = 0

left_distance = 0
right_distance = 0

yaw=0

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
twist = Twist()

def callback_pose(msg):
	global right_ar_heading, left_ar_heading, ar_id, posx, posy, posz, left_distance, right_distance

	ar_id = msg.id

	posx, posy, posz = msg.pose.position.x, msg.pose.position.y, msg.pose.position.z
	slope=posx/posz

	if (ar_id == 4 or ar_id == 6) or (ar_id == 8 or ar_id == 10):
		right_ar_heading = degrees(asin(slope))
		right_distance = hypot(posz,posx)
		#print(ar_id, right_ar_heading, right_distance)
	if (ar_id == 3 or ar_id == 5) or (ar_id == 7 or ar_id == 9):
		left_ar_heading = degrees(asin(slope))
		left_distance = hypot(posz,posx)
		#print(ar_id, left_ar_heading, left_distance)

def imu(pose):
	global yaw
	quaternion = (pose.orientation.x, pose.orientation.y, pose.orientation.z, pose.orientation.w)

	euler = euler_from_quaternion(quaternion)
	yaw= degrees(euler[2])
	yaw = abs(yaw-360)
	yaw = yaw%360
	
	#print(yaw)

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
			#print(yaw, final_yaw, angle)
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


def move(move_dist):
	move_dist=move_dist*3
	a=time.time()
	while (time.time()-a)<=(move_dist/0.8):
		twist.linear.x=0.8 
		pub.publish(twist)
	stop()


def listener():
	rospy.init_node('bot_yaw', anonymous=True,disable_signals= True)
	rospy.Subscriber("camera_1/visualization_marker", Marker, callback_pose)
	rospy.Subscriber("/imu", Imu, imu)

	rate = rospy.Rate(10) # 10hz

	while 1:

		angle_diff=right_ar_heading-left_ar_heading
		dist=sqrt(pow(right_distance,2)+pow(left_distance,2)-2*right_distance*left_distance*cos(radians(angle_diff)))

		print(right_ar_heading, left_ar_heading, right_distance, left_distance, dist)

		if dist>0 and right_distance>0 and left_distance>0 and right_ar_heading>1 and left_ar_heading<-1:

			if abs(right_ar_heading+left_ar_heading)<5:
				print(right_distance)
				move(right_distance+3)
				exit()
				
			if right_distance>left_distance+0.2:

				angle=asin(left_distance*sin(radians(angle_diff))/dist)
				move_dist=right_distance-dist/(2*cos(angle))
				final_angle=90-degrees(angle)+3
				through_gate_dist=tan(angle)*dist/2
				
				align(right_ar_heading)
				move(move_dist)
				align(-final_angle)
				move(through_gate_dist+4)
				exit()

			elif left_distance>right_distance+0.2:

				angle=asin(right_distance*sin(radians(angle_diff))/dist)
				move_dist=left_distance-dist/(2*cos(angle))
				final_angle=90-degrees(angle)+3
				through_gate_dist=tan(angle)*dist/2
				
				align(left_ar_heading)
				move(move_dist)
				align(final_angle)
				move(through_gate_dist+4)
				exit()
			
			else:
				print(right_distance)
				move(right_distance+3)
				exit()

	rospy.spin()

if __name__ == '__main__':
    listener()
