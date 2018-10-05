#!/usr/bin/env python

import rospy
import math
import tf
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
from nav_msgs.msg import Path



pub_vel = rospy.Publisher('/mobile_base/commands/velocity', Twist, 
        queue_size=10)

# Hold the latest position and orientation
pose = Pose()
path = Path()



def odomCb(data):
    global pose
    pose = data.pose.pose


# Path callback
def pathCb(data):
    print 'In pathCb'
    global path
    path = data.poses

    # Go through each point on the path and move point to point
    # Assume that only moving in greater direction
    for p in path:
        goToPoint(p.pose.position.x, p.pose.position.y, 0.785, 0.1)



def findDistanceBetweenAngles(a, b):
    print 'In findDistanceBetweenAngles'
    
    difference = b - a
    print difference
    
    if difference > math.pi:
      difference = math.fmod(difference, PI)
      result = difference - PI

    elif(difference < -math.pi):
      result = difference + (2*math.pi)

    else:
      result = difference

      return result



def goToPoint(x, y, angSpeed, linSpeed):
    
    print 'In goToPoint'

    currentX = pose.position.x
    currentY = pose.position.y

    if currentX == x and currentY == y:
        return

    deltaX = x - currentX
    deltaY = y - currentY

    theta = math.atan2(deltaY, deltaX)

    turnToTheta(theta, angSpeed)

    dist = math.sqrt( math.pow( x - currentX,2) + 
                math.pow( y - currentY,2) )

    moveDist(dist, linSpeed)


# Turn the robot to a specified orientation (in radians)
def turnToTheta(theta, speed):
    print 'In turnToTheta'

    # Use turnRad
    # params: calculate the diff in orientation
    
    # The orientation before we start turning
    thetaStart = tf.transformations.euler_from_quaternion( [pose.orientation.x, 
            pose.orientation.y, pose.orientation.z, pose.orientation.w] )[2]
    print 'thetaStart: %s' % thetaStart

    thetaDist = findDistanceBetweenAngles(theta, thetaStart)
    print 'thetaDist: %s' % thetaDist

    r = rospy.Rate(30)

    thresh = 0.2
    currentTheta = thetaStart

    angleDist = findDistanceBetweenAngles(thetaStart, theta)
    
    t = Twist()
    t.angular.z = speed if angleDist > 0 else -speed

    while abs(angleDist) > thresh and not rospy.is_shutdown():

        currentTheta = tf.transformations.euler_from_quaternion( 
                [pose.orientation.x, pose.orientation.y, pose.orientation.z, 
                        pose.orientation.w] )[2]
        angleDist = findDistanceBetweenAngles(currentTheta, theta)


        pub_vel.publish(t)
        r.sleep()


# Turn the robot by a specified amount (in radians)
def turnRad(rad, speed):
    print 'In turnRad'
    
    # The orientation before we start turning
    thetaStart = tf.transformations.euler_from_quaternion( [pose.orientation.x, 
            pose.orientation.y, pose.orientation.z, pose.orientation.w] )[2]

    print thetaStart
    
    thetaRelative = 0


    t = Twist()
    t.linear.x = 0
    t.angular.z = speed

    r = rospy.Rate(30)

    while thetaRelative < rad and not rospy.is_shutdown():

        tempTheta = tf.transformations.euler_from_quaternion( 
                [pose.orientation.x, pose.orientation.y, pose.orientation.z, 
                        pose.orientation.w] )[2]

        thetaRelative = tempTheta - thetaStart
        print 'thetaRelative: %s' % thetaRelative


        pub_vel.publish(t)
        r.sleep()



def moveDist(d, speed):
    print 'In moveDist'

    # The position before we start moving
    p_start = pose.position
    print 'p_start: %s' % p_start

    dRelative = 0


    t = Twist()
    t.linear.x = speed
    t.angular.z = 0

    r = rospy.Rate(30)

    while dRelative < d and not rospy.is_shutdown():


        dRelative = math.sqrt( math.pow( pose.position.x - p_start.x,2) + 
                math.pow( pose.position.y - p_start.y,2) )

        print 'dRelative: %s' % dRelative

        pub_vel.publish(t)
        r.sleep()



def main():
    print 'In main'

    rospy.init_node('move_on_path', anonymous=True)

    # Subscribers
    sub_odom = rospy.Subscriber('/odom', Odometry, odomCb)

    sub_path = rospy.Subscriber('/path', Path, pathCb)

    # Initial sleep
    initSleep = rospy.Duration(1.0)
    rospy.sleep(initSleep)

    rospy.spin()

    print 'Exiting normally'



if __name__ == '__main__':
    main()
