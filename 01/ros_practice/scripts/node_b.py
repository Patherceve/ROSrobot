#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def main():
    pub = rospy.Publisher('topic_b', Int64, queue_size=10)
    rospy.init_node('node_b')
    rospy.Subscriber('topic_a', String, callback)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
    	helloInt64 = Int64()
    	helloInt64.data = 42
    	pub.publish(helloInt64)

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass