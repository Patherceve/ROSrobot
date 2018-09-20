#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def main():
    pub = rospy.Publisher('topic_a', String, queue_size=10)
    rospy.init_node('node_a')
    rospy.Subscriber('topic_b', Int64, callback)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
    	helloString = String()
    	helloString.data = 'some string'
    	pub.publish(helloString)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass