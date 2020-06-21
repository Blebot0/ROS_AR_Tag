#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from ar_track_alvar_msgs.msg import AlvarMarkers
from geometry_msgs.msg import Point, Twist

def callback(msg):
    try:
       # x =  msg.pose.postition.x
   #     y =  msg.pose.position.y
    #    z =  msg.pose.position.z
        pose_id = str(msg.id)
        conf = str(msg.confidence)
   #     print("x= {0}, y= {1}, z= {2}".format(x, y, z))
        print(pose_id + " " + conf)
    except:
        print("No tag detected")


def listener():

    rospy.init_node('ar_pose')
    print(1)
    rospy.Subscriber("/ar_pose_marker", AlvarMarkers, callback)
    print(2)
    rospy.spin()

if __name__ == '__main__':
    listener()
