
# Documentation link: https://www.robotmesh.com/studio/content/docs/vexv5-python/html/annotated.html

# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       Noah Nicolas Gabe Jerry Sofie                                #
# 	Created:      9/13/2023, 1:06:06 PM                                        #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

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
frontRightMotor = Motor29(brain.three_wire_port.b, False)
backLeftMotor = Motor29(brain.three_wire_port.d, True)
backRightMotor = Motor29(brain.three_wire_port.e, True)
flywheelMotor = Motor29(brain.three_wire_port.f, False)
controller_1 = Controller(PRIMARY)
controller_2 = Controller(PARTNER)

# wait for stuff to configure
wait(25, MSEC)

# Constants
FORWARD_SPEED_MULTIPLIER = 1
STRAFE_SPEED_MULTIPLIER = 1
ROTATION_SPEED_MULTIPLIER = 1

# Finds the distance of a point from (0, 0)
def hypot(x: float, y: float) -> float:
    return math.sqrt(x**2+y**2)

# Main programming loop
def main():
    y = controller_1.axis3.position() * FORWARD_SPEED_MULTIPLIER
    x = controller_1.axis4.position() * STRAFE_SPEED_MULTIPLIER
    turn = controller_1.axis1.position() * ROTATION_SPEED_MULTIPLIER
    
    # deadband for joystick drift
    if abs(x) < 5:
       x = 0
    if abs(y) < 5:
       y = 0
    if abs(turn) < 5:
       turn = 0
    
    # turn cartesian values into polar values
    theta = math.atan2(y,x)
    power = hypot(x,y)
    
    # move drive wheels
    drive(power, turn, theta)


# Moves the chassis wheels. Powers is how fast to move, theta is what angle to move in, and turn is how much to turn
# Motor values range from -100 to 100.
def drive(power: float, turn: float, theta: float):
    sin = math.sin(theta - math.pi/4)
    cos = math.cos(theta - math.pi/4)
    maxValue = max(abs(sin), abs(cos))
    
    leftFront = power * cos/maxValue + turn
    rightFront = power * sin/maxValue - turn
    leftRear = power * sin/maxValue + turn
    rightRear = power * cos/maxValue - turn

    # if one motor needs to move faster than the max, all of the motor speeds are reduced
    if ((power + abs(turn)) > 100):
        leftFront /= power + abs(turn) 
        rightFront /= power + abs(turn) 
        leftRear /= power + abs(turn)
        rightRear /= power + abs(turn) 
        leftFront *= 100
        rightFront *= 100
        leftRear *= 100
        rightRear *= 100

    # drive left side
    frontLeftMotor.spin(FORWARD, leftFront)
    backLeftMotor.spin(FORWARD, leftRear)

    # drive right side
    frontRightMotor.spin(FORWARD, rightFront)
    backRightMotor.spin(FORWARD, rightRear)

    # Print motor vaules out for debugging
    # brain.screen.clear_screen()
    # brain.screen.set_cursor(1,1)
    # brain.screen.print("LF: ", leftFront)
    # brain.screen.new_line()
    # brain.screen.print("LR: ", leftRear)
    # brain.screen.new_line()
    # brain.screen.print("RF: ", rightFront)
    # brain.screen.new_line()
    # brain.screen.print("RR: ", rightRear)
    # brain.screen.new_line()
    # brain.screen.print("Theta ", theta*57.29)
    # brain.screen.new_line()
    # brain.screen.print("Power ", power)
    # brain.screen.new_line()
    # brain.screen.print("Turn ", turn)


def intake(): 
    pass 

def shoot():
    # only want to intake if button "a" is being pressed 
    if controller_1.buttonA.pressing():     
        flywheelMotor.spin(FORWARD, 50)
    else:
        flywheelMotor.stop()


# ---- START ACTUALLY EXECUTING CODE ---- 

while 1:
    main()
    wait(50, MSEC)
