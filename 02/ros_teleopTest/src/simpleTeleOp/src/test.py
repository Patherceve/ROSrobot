#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

global linVel, angVel

linVel = 0.10
angVel = 0.52

def drive(dur, direc):
	pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	rate = rospy.Rate(30)
	t_start = rospy.Time.now()
	d = rospy.Duration(dur)
	while((rospy.Time.now() - t_start) < d):
		print('indawhile')
		pub.publish(direc)
		rate.sleep()

def main():
	rospy.init_node('fw_node', anonymous = False)
	
	f = Twist()
	b = Twist()
	l = Twist()
	r = Twist()

	f.linear.x = linVel
	b.linear.x = -(linVel)
	l.angular.z = angVel
	r.angular.z = -(angVel)

	while not rospy.is_shutdown():
		data = raw_input('input dir: ')
		t = float(raw_input('input time: '))
		d = float(raw_input('input distance: '))
		
		if(t > 2):
			dur = 2
		if(d > 0.33):
			dist = 0.33	

		if(data == 'w'):
			drive(t, f)
		elif(data == 's'):
			drive(t, b)
		elif(data == 'a'):
			drive(t, l)
		elif(data == 'd'):
			drive(t, r)
		
		if(data == 'u'):
			drive(float(linVel/d), f)
		elif(data == 'j'):
			drive(float(linVel/d), b)
		elif(data == 'h'):
			drive(float(linVel/d), l)
		elif(data == 'k'):
			drive(float(linVel/d), r)

if __name__ == '__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass
	
