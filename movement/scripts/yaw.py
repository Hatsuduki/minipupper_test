#!/usr/bin/env python3
#credits to: https://github.com/mangdangroboticsclub/minipupper_ros/blob/master/mini_pupper_detect/scripts/oak_detect.py
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
import math

roll=0
pitch=0
yaw = 0
yaw_increment=0
pose = Pose()

#yaw 水平左右向く

def move():
    rospy.init_node("pose", anonymous=True)
    pub_pose = rospy.Publisher("/body_pose", Pose, queue_size=10) 

    global pose,roll,pitch,yaw,yaw_increment
    count = 0
    rate = rospy.Rate(3)
    rate.sleep()
    rate = rospy.Rate(20) # 20hz

    for i in range(4):
        if count == 0 or count == 3:
            yaw_increment = 0.1 #left
        else:
            yaw_increment = -0.1 #right

        for j in range(7):
        
            yaw = yaw + yaw_increment
            print(yaw)
            cy = math.cos(yaw * 0.5)
            sy = math.sin(yaw * 0.5)
            cp = math.cos(pitch * 0.5)
            sp = math.sin(pitch * 0.5)
            cr = math.cos(roll * 0.5)
            sr = math.sin(roll * 0.5)

            pose.orientation.w = cy * cp * cr + sy * sp * sr
            pose.orientation.x = cy * cp * sr - sy * sp * cr
            pose.orientation.y = sy * cp * sr + cy * sp * cr
            pose.orientation.z = sy * cp * cr - cy * sp * sr

            pub_pose.publish(pose)
            rate.sleep()
        count = count + 1

if __name__ == "__main__":
    try:
        move()
    except rospy.ROSInterruptException: pass
