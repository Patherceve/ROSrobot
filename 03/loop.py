#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import tf.transformations as tft

global linVel, angVel

odoData = Odometry()

linVel = 0.10
angVel = 0.52

def callback(data):

	global odoData

	#rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.pose.pose.position)
	odoData = data

def drive(dist, direc, zeroPos):

	pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	rate = rospy.Rate(30)
	zero = (zeroPos.pose.pose.position.x, zeroPos.pose.pose.position.y)

	while(math.sqrt(math.pow(odoData.pose.pose.position.x - zeroPos.pose.pose.position.x, 2) + math.pow(odoData.pose.pose.position.y - zeroPos.pose.pose.position.y, 2)) < dist):
		pub.publish(direc)
		rate.sleep()

def rotation(speOrient, dir, zeroOrient):

	pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	rate = rospy.Rate(30)

	o = zeroOrient.pose.pose.orientation
	q = tft.euler_from_quaternion([o.x, o.y, o.z, o.w])
	(roll, pitch, yaw) = q
	theta = yaw

	currentTheta = theta

	while(currentTheta - theta < dir):
		pub.publish(speOrient)

		current = odoData.pose.pose.orientation
		r = tft.euler_from_quaternion([current.x, current.y, current.z, current.w])
		(rollR, pitchR, yawR) = r
		currentTheta = yawR

		rate.sleep()

def main():

	global odoData

	rospy.init_node('itsAlive_node', anonymous = False)
	
	rospy.Subscriber('/odom', Odometry, callback)

	f = Twist()
	b = Twist()
	l = Twist()
	r = Twist()

	f.linear.x = linVel
	b.linear.x = -(linVel)
	l.angular.z = angVel
	r.angular.z = -(angVel)

	while not rospy.is_shutdown():
		
		tZero = odoData
		data = raw_input('input dir: ')
		d = float(raw_input('input distance/angle: '))

		if(data == 'w'):
			drive(d, f, tZero)
		elif(data == 's'):
			drive(d, b, tZero)
		elif(data == 'a'):
			rotation(l, d, tZero)
		elif(data == 'd'):
			rotation(r, d, tZero)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass