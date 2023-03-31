"""
Author:
	Baher Kher Bek
"""

import cv2
import rospy
from geometry_msgs.msg import Point
import time

#119 -> w 100 -> d 97 -> a 115 -> s

rospy.init_node('ManualControl')
pub = rospy.Publisher('/Manual', Point, queue_size=100)

prev = [0, 0]
def response(key):
    msg = Point()
    time.sleep(0.05)
    if key == ord('w'):
        msg.x = 255
        msg.y = 255

    elif key == ord('d'):
        msg.x = 255
        msg.y = -255

    elif key == ord('a'):
        msg.x = -255
        msg.y = 255

    elif key == ord('s'):
        msg.x = -255
        msg.y = -255
    
    else:
        msg.x = 0
        msg.y = 0

    pub.publish(msg)
    

while True:
    cv2.namedWindow('Control')

    key = cv2.waitKey(1)
    response(key=key)
    if key == 27:
        break

