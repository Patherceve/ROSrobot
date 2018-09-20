#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from std_msgs.msg import Int64

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

def main():
    rospy.init_node('node_c')
    rospy.Subscriber('topic_a', String, callback)
    rospy.Subscriber('topic_b', Int64, callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass