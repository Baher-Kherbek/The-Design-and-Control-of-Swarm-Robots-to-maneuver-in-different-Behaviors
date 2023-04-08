# The-Design-and-Control-of-Swarm-Robots-to-maneuver-in-different-Behaviors

<h2> The Goal </h2>
The goal of the project was to design and model multiple differential-drive  mobile robots to be used as agents in a swarm cluster. The goal was to make the robots move in different behaviors, using ROS NOETIC environment.

<h2> The Plan </h2>
The plan is to setup a ceiling-camera that projects the boundaries of the workspace that the Robots will be placed within. As far as the control of these robots, all processing will be done on the master computer and then transmit signals to each individual Robot.

<h2> Methods Used </h2>

<h4> Tracking the Robots </h4>
For tracking each Robot in real time, an AruCo marker with a unique ID is placed on each robot. This way, The location of each robot can be extracted and tracked.

<h4> Control </h4>
A Control node recieves the coordinates of the robots in real time and inputs them to the control algorithm for the desired behavior. 

<h4>Communication</h4>
The ROS workspace allows for smooth and efficient communication and transmission between all nodes.
There are 2 + (n) nodes involved, (n is the number of robots present in the workspace, each is an individual Node) The two other nodes are the Control Node that calculates the the motor velocity of each robot in order to allow the robots to move in the desired behavior, and the Camera Node  tracks and transmits the current location(coordinates) of the robots in the workspace to the control node in order to be utilized in the control algorithm.

Each Robot is controlled by an ESP-32S microcontroller, which is WiFi enabled. The WiFi option is used for medium of communication. All microcontrollers of the robots as well as the master 



This Project is the Semester Project in 3rd year of my Bachelor's in Mechatronics
