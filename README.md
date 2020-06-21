# ROS_AR_Tag
AR TAG Detection using ROS and Gazebo

Requirements:

ROS (melodic)

Rviz

Gazebo

AR ALVAR pkg from ros website

# How To Run:

Clone Repository and run following commands:

```bash
git clone https://github.com/Blebot0/ROS_AR_Tag.git

source devel/setup.bash

roslaunch gazebo_bot world.launch
```

errors while running ar_pose.py

PATH: ar_tag/src/gazebo_bot/scripts

```bash 
[ERROR] [1592738394.843636254, 468.266000000]: Client [/ar_pose] wants topic /ar_pose_marker to have datatype/md5sum [ar_track_alvar_msgs/AlvarMarker/ef2b6ad42bcb18e16b22fefb5c0fb85f], but our version has [ar_track_alvar_msgs/AlvarMarkers/943fe17bfb0b4ea7890368d0b25ad0ad]. 
Dropping connection.
```



