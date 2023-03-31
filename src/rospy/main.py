"""
Author:
	Baher Kher Bek
"""


#!/usr/bin/env python3.8
import cv2
import cv2.aruco as aruco
import numpy as np
import freenect
import rospy
from geometry_msgs.msg import Point
import time
import math



class SwarmRobot(object):

    def __init__(self):
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.arucoParameters = aruco.DetectorParameters_create()
        self.target_x = None
        self.target_y = None
        self.robot_angle = None
        self.target_angle = None
        self.id = None
        self.ids = None
        self.index = None
        self.Max_Speed = 700
        self.Min_Speed = 400
        self.average_speed = 1023
        self.left_motor_speed = self.average_speed
        self.right_motor_speed = self.average_speed
        self.pub = rospy.Publisher("Control", Point, queue_size=10)
        self.ids = None
        self.delay = 0.001
        self.behavior = 'gotopose'
        self.center_x = None
        self.center_y = None
        self.frame = None
        self.distance = 50
        self.flag = False
        self.kp = 80
        self.ki = 0
        self.kd = 0
        self.key = None
        self.reached = False
        self.theta = 0
        self.radius = 90
        self.Cx = None
        self.Cy = None
        self.iterator = 0
        self.stat_multi = True
        self.targets = []
        self.path = []
        self.start = rospy.get_time()
        self.last_time = 0
        self.old_erorr = 0
        self.Error = 0

    def get_center(self, x1, x2, x3, x4, y1, y2, y3, y4): # get center of Aruco marker from corner coordinates
        center_x = (x1 + x2 + x3 + x4) // 4
        center_y = (y1 + y2 + y3 + y4) // 4

        return (int(center_x), int(center_y))

    def Mouse_Callback(self, event, x, y, flags, param):
        try:
            if event == cv2.EVENT_LBUTTONDOWN and self.corners != None:  # left mouse for getting ID

                for i in range(len(self.ids)):
                    (center_X, center_Y) = self.get_center(self.corners[i][0][0][0], self.corners[i][0][1][0],
                                                           self.corners[i][0][2][0], self.corners[i][0][3][0],
                                                           self.corners[i][0][0][1], self.corners[i][0][1][1],
                                                           self.corners[i][0][2][1], self.corners[i][0][3][1])

                    if abs(x - center_X) < 50 and abs(y - center_Y) < 50:
                        self.id = self.ids[i]
                        self.index = int(i)
                        self.center_x = center_X
                        self.center_y = center_Y
                        break

            elif event == cv2.EVENT_MBUTTONDOWN:  # right mouse for getting target coordinates
                print('here too')
                self.target_x = x
                self.target_y = y
                self.Cx = x
                self.Cy = y
                self.targets.append((self.target_x, self.target_y))
                print(self.targets)

        except:
            pass

    def go_to_position(self, id, index, target_x, target_y):
        # calculating left and right distances from target
        left_length = pow((pow((self.corners[index][0][0][0] - target_x), 2)
                           + pow((self.corners[index][0][0][1] - target_y), 2)), 0.5)

        right_length = pow((pow((self.corners[index][0][1][0] - target_x), 2)
                            + pow((self.corners[index][0][1][1] - target_y), 2)), 0.5)

        # target deviation
        deviation = left_length - right_length

        if abs(deviation) > 20:
            msg = Point()
            msg.x = self.id
            msg.y = self.average_speed
            msg.z = -self.average_speed
            self.pub.publish(msg)

        else:
            # angle error
            middle_pointX = (self.corners[self.index][0][0][0] + self.corners[self.index][0][1][0]) // 2
            middle_pointY = (self.corners[self.index][0][0][1] + self.corners[self.index][0][1][1]) // 2

            cv2.circle(self.frame, (int(middle_pointX), int(middle_pointY)), 20, [0, 0, 255], -1)

            self.robot_angle = math.atan(self.center_y - middle_pointY / self.center_x - middle_pointX)
            self.target_angle = math.atan(self.center_y - self.target_y / self.center_x - self.target_x)

            error = self.target_angle - self.robot_angle
            error = math.atan2(math.sin(error), math.cos(error))
            time_now = rospy.get_time() - self.start()
            duration = time_now - self.last_time
            self.last_time = time_now
            angular_velocity = self.kp * error + self.kd * (error - self.old_erorr) + self.ki * E * duration
            self.old_erorr = error
            self.Error += error







    def keyboard_control(self, id):

        # W : 119   D : 100     S : 115     A : 97

        if self.key == ord('w'):

            msg = Point()
            msg.x = id
            msg.y = self.average_speed
            msg.z = self.average_speed
            self.pub.publish(msg)
            time.sleep(self.delay)

        elif self.key == ord('d'):
            msg = Point()
            msg.x = id
            msg.y = -self.average_speed
            msg.z = self.average_speed
            self.pub.publish(msg)
            time.sleep(self.delay)

        elif self.key == ord('a'):
            msg = Point()
            msg.x = id
            msg.y = self.average_speed
            msg.z = -self.average_speed
            self.pub.publish(msg)
            time.sleep(self.delay)

        elif self.key == ord('s'):
            msg = Point()
            msg.x = id
            msg.y = -self.average_speed
            msg.z = -self.right_motor_speed
            self.pub.publish(msg)
            time.sleep(self.delay)


        else:
            msg = Point()
            msg.x = self.id
            msg.y = 0
            msg.z = 0
            self.pub.publish(msg)

    def chain(self, id, index):
        try:
            self.keyboard_control(id)

            if self.ids[self.index] == self.id:
                (self.center_x, self.center_y) = self.get_center(self.corners[index][0][0][0],
                                                                 self.corners[index][0][1][0],
                                                                 self.corners[index][0][2][0],
                                                                 self.corners[index][0][3][0],
                                                                 self.corners[index][0][0][1],
                                                                 self.corners[index][0][1][1],
                                                                 self.corners[index][0][2][1],
                                                                 self.corners[index][0][3][1])

            self.target_x = self.center_x
            self.target_y = self.center_y

            if len(self.ids):
                for i in range(0, len(self.ids)):
                    if self.ids[i] != self.id:
                        self.go_to_position(self.ids[i], i, self.target_x, self.target_y)

        except:
            pass

    def stop(self):
        for i in self.ids.flatten():
            msg = Point
            msg.x = i
            msg.y = 0
            msg.z = 0

            self.pub.publish(msg)

    def circle(self, id, index):
        print('circle')

        self.target_x = self.radius * math.cos(self.theta * math.pi / 180) + self.Cx
        self.target_y = self.radius * math.sin(self.theta * math.pi / 180) + self.Cy

        self.go_to_position(id, index, self.target_x, self.target_y)


    def multi_go_to_position(self):
        print('iam in')

        try:
            i = self.index
            if self.stat_multi:
                (self.center_x, self.center_y) = self.get_center(self.corners[i][0][0][0], self.corners[i][0][1][0],
                                                                 self.corners[i][0][2][0], self.corners[i][0][3][0],
                                                                 self.corners[i][0][0][1], self.corners[i][0][1][1],
                                                                 self.corners[i][0][2][1], self.corners[i][0][3][1])

                self.path.append((self.center_x, self.center_y))

                for i in range(len(self.path) - 1):
                    cv2.circle(self.frame, (self.path[i][0], self.path[i][1]), 4, [50, 100, 255], -1)


            self.go_to_position(self.id, self.index, int(self.targets[self.iterator][0]),  int(self.targets[self.iterator][1]))
            if self.reached == True:
                self.iterator += 1
                self.reached = False


        except Exception as inst:
            d = inst
            print(d)


    def get_video(self):
        frame, _ = freenect.sync_get_video()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #image = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY )

        return frame

    def start(self):
        while True:
            # self.frame = cv2.imread('aruco.png')
            self.frame = self.get_video()

            # Assign Aruco Marker Values
            self.ids = True
            self.corners, self.ids, self.rejectedPoints = aruco.detectMarkers(self.frame, self.aruco_dict, parameters=self.arucoParameters)
            self.frame = aruco.drawDetectedMarkers(self.frame, self.corners)
            cv2.namedWindow('frame')
            if len(self.corners):
                cv2.setMouseCallback('frame', self.Mouse_Callback)


            # Keyboard Input
            self.key = cv2.waitKey(1)


            try:
                if self.behavior == 'Keyboard' and self.id != None:
                    self.keyboard_control(self.id)

                elif self.behavior == 'gotopose' and self.id != None and self.target_x != None and self.index != None and self.ids != None and self.id == \
                        self.ids[self.index]:
                    self.go_to_position(self.id, self.index, self.target_x, self.target_y)

                elif self.behavior == 'chainKeyboard' and self.id != None and self.ids[self.index] == self.id:
                    # and self.id == self.ids[self.index]
                    self.chain(self.id, self.index)

                elif self.behavior == 'circle' and self.id != None and self.target_x != None and self.id == self.ids[
                    self.index]:
                    self.circle(self.id, self.index)

                elif self.behavior == 'stop':
                    self.stop()

                elif self.behavior == 'multi' and len(self.ids) > 0:
                    self.multi_go_to_position()

            except:
                pass

            cv2.imshow('frame', self.frame)



            if self.key == 27:
                break

            elif self.key == ord('p'):
               self.stop()

            elif self.key == ord('k'):
                self.behavior = 'Keyboard'
                self.target_y = None
                self.target_x = None

            elif self.key == ord('g'):
                self.behavior = 'gotopose'

            elif self.key == 13:
                self.behavior = 'multi'

            elif self.key == 49:
                self.id = int(ord('1'))

            elif self.key == 50:
                self.id = int(ord('2'))

            elif self.key == 51:
                self.id = int(ord('3'))



        

if __name__ == '__main__':
    rospy.init_node('Swarm', anonymous=True)
    robot = SwarmRobot()
    robot.start()

