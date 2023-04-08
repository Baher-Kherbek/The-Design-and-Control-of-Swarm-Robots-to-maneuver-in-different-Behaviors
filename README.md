# The-Design-and-Control-of-Swarm-Robots-to-maneuver-in-different-Behaviors

<h2> The Goal </h2>
The goal of the project was to design and model multiple differential-drive  mobile robots to be used as agents in a swarm cluster. The goal was to make the robots move in different behaviors, using ROS NOETIC environment.

<h2> The Plan </h2>
The plan is to setup a ceiling-camera that projects the boundaries of the workspace that the Robots will be placed within. As far as the control of these robots, all processing will be done on the master computer and then transmit signals to each individual Robot.

<h2> Methods Used </h2>

<h4> Tracking the Robots </h4>
For tracking each Robot in real time, an AruCo marker with a unique ID is placed on each robot. This way, The location of each robot can be extracted and tracked.

<h4> Control </h4>
A Control node recieves the coordinates of the robots in real time from the camera node and inputs them to the control algorithm for the desired behavior.
Controlling each Robot in the desired behavior is done by calculating the trajectory maneuver of the robot and dividing the trajectory to m points, then moving the robot to each one of those m points through a basic PID controller that controls the two motors of each robot.  

<h4>Communication</h4>
The ROS workspace allows for smooth and efficient communication and transmission between all nodes.
There are 2 + (n) nodes involved, (n is the number of robots present in the workspace, each is an individual Node) The two other nodes are the Control Node that calculates the the motor velocity of each robot in order to allow the robots to move in the desired behavior, and the Camera Node  tracks and transmits the current location(coordinates) of the robots in the workspace to the control node in order to be utilized in the control algorithm.

Each Robot is controlled by an ESP-32S microcontroller, which is WiFi enabled. The WiFi option is used as medium of communication. All microcontrollers of the robots as well as the master computer (which runs the ROSCORE and holds the control and camera nodes) are connected to the same WiFi network, communication between all nodes is achieved through the ROSSERIAL package which uses XMLRPC communication protocol to transmit packets of messages to each robot.

<h2> The Result </h2>
Only two main behaviors were implemented, The first is an individual behavior of each robot that moves to a specific (x, y) coordinate supplied. The Secon behavior is the chain behavior (Master Slave), the Idea is that a Master robot moves to a designated (x, y) coordinate in the workspace, The slave robots follow wach other in a connected chain maneuver. Videos were uploaded to the Results Folder of the project, along with pictures of the mobile robots that were designed and 3D printed afterwards.

<h2> Acknowledgements </h2>
This project is a semster project for my Bachelor's Degree in Mechatronics at Tishreen University.
Special acknowledgement to my mentor and supervisor of the project Dr Iyad Hatem, PHD



This Project is the Semester Project in 3rd year of my Bachelor's in Mechatronics
