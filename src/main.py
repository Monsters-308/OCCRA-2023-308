# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       noahn                                                        #
# 	Created:      9/13/2023, 1:06:06 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

# ---- START VEXCODE CONFIGURED DEVICES ----
# frontLeftMotor      motor29       A
# frontRightMotor     motor29       B
# backLeftMotor       motor29       D
# backRightMotor      motor29       E
# ---- END VEXCODE CONFIGURED DEVICES ----

# Configure devices
frontLeftMotor = Motor29(brain.three_wire_port.a, False)
FrontRightMotor = Motor29(brain.three_wire_port.b, False)
backLeftMotor = Motor29(brain.three_wire_port.d, True)
backRightMotor = Motor29(brain.three_wire_port.e, True)
controller_1 = Controller(PRIMARY)

# wait for stuff to configure
wait(25, MSEC)

# Constants
FORWARD_SPEED_MULTIPLIER = 1
ROTATION_SPEED_MULTIPLIER = 1

# Code ran once on startup
def robotInit():
    pass 


# Main programming loop
def main():
    # get joystick axises
    Axis3 = controller_1.axis3.position() * FORWARD_SPEED_MULTIPLIER
    Axis1 = controller_1.axis1.position() * -ROTATION_SPEED_MULTIPLIER
    

    # deadband for joystick drift
    if abs(Axis3) < 5:
        Axis3 = 0
    if abs(Axis1) < 5:
        Axis1 = 0

    # move drive wheels
    drive(Axis3, Axis1)


# Moves the chassis wheels. forwardSpeed represents how fast forward, turningSpeed represents how fast you're turning (positive is right). 
# Both are values from -100 to 100.
def drive(forwardSpeed: float, turningSpeed: float):
    
    # alters the speed of each side depending on which direction you're turning and by how much
    leftSpeed = forwardSpeed + turningSpeed
    rightSpeed = forwardSpeed - turningSpeed
    
    # drive left side
    frontLeftMotor.spin(FORWARD, leftSpeed)
    backLeftMotor.spin(FORWARD, leftSpeed)

    # drive right side
    FrontRightMotor.spin(FORWARD, rightSpeed)
    backRightMotor.spin(FORWARD, rightSpeed)


# ---- START ACTUALLY EXECUTING CODE ---- 
robotInit()

while 1:
    main()
    wait(50, MSEC)
