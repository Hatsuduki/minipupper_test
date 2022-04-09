#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Pose
import math

roll = 0
pitch = 0
yaw = 0
pitch_increment = 0
yaw_increment = 0
pose = Pose()

def move():
    rospy.init_node("pose", anonymous=True)
    pub_pose = rospy.Publisher("/body_pose", Pose, queue_size=10) 

    global pose,roll,pitch,yaw,pitch_increment
    count = 0
    rate = rospy.Rate(3)
    pitch_increment = 0.1*(3/6)
    yaw_increment = 0.05

    rate.sleep()
    rate = rospy.Rate(20) # 20hz

    for i in range(4):
        if count == 0 or count == 3:
            yaw_increment = 0.05 #left
        else:
            yaw_increment = -0.05 #right

        pitch_count = 0
        for j in range(12):
            if count == 0 or count == 2: #to outer move
                if pitch_count <= 5:
                    pitch_increment = -0.1*(3/6) #up
                elif pitch_count > 5:
                    pitch_increment = 0.1*(3/6) #down
                else:
                    pitch_increment = 0 #same height
            else: #to inner move
                if pitch_count <= 5:
                    pitch_increment = 0.1*(2.5/6) #down
                elif pitch_count > 5:
                    pitch_increment = -0.1*(2.5/6) #up
                else:
                    pitch_increment = 0 #same height

            pitch = pitch + pitch_increment
            yaw = yaw + yaw_increment
            print(pitch)
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
            
            pitch_count = pitch_count + 1
            pub_pose.publish(pose)
            rate.sleep()
        count = count + 1
            

if __name__ == "__main__":
    try:
        move()
    except rospy.ROSInterruptException: pass