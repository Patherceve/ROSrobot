#!/usr/bin/env python

import rospy

def main():
    rospy.init_node('Hello_World')
    print("Hello World From ROS")

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass