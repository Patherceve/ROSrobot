#!/usr/bin/env python

import rospy
from nav_msgs.msg import Odometry

global var

def callback(var):
	rospy.loginfo(rospy.get_caller_id() + "I heard %s", var.pose.pose.position)

rospy.init_node('odo_node', anonymous = False)

var = rospy.Subscriber('/odom', Odometry, callback)

rospy.spin()