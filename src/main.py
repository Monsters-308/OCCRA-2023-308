
# Documentation/Vex Code link: https://www.robotmesh.com/studio/content/docs/vexv5-python/html/annotated.html

# ---------------------------------------------------------------------------- #
# 	Module:       main.py                                                      #
# 	Author:       Noah Nicolas Gabe Jerry Sofie                                #
# 	Created:      9/13/2023, 1:06:06 PM                                        #
# 	Description:  V5 project                                                   #                                                         
# ---------------------------------------------------------------------------- #


# Library imports----
from vex import *
import math


# Top of Vexcode Configures Devices KEY------------
# frontLeftMotor      motor29       A
# frontRightMotor     motor29       B
# backLeftMotor       motor29       D
# backRightMotor      motor29       E
# Bottom of Vexcode Configures Devices KEY---------


# CONFIGURE DEVICES-------------------------------------------
# Brain should be defined by default
brain=Brain()

frontLeftMotor = Motor29(brain.three_wire_port.a, False)
frontRightMotor = Motor29(brain.three_wire_port.b, True)
backLeftMotor = Motor29(brain.three_wire_port.d, False)
backRightMotor = Motor29(brain.three_wire_port.c, True)
#flywheelMotor = Motor29(brain.three_wire_port.f, False)
controller_1 = Controller(PRIMARY)
controller_2 = Controller(PARTNER)

# Constants
FORWARD_SPEED_MULTIPLIER = 1
STRAFE_SPEED_MULTIPLIER = 1
ROTATION_SPEED_MULTIPLIER = 0.5
CRABCRAWLALIGN = .1


#================================================================= wait for stuff to configure =================================================================#
wait(25, MSEC)
#================================================================= wait for stuff to configure =================================================================#


# Main programming loop---------------------------------------------------------------------------
def main():
    # left joystick y axis (3)
    y = controller_1.axis3.position() * FORWARD_SPEED_MULTIPLIER
    # left joystick x axis (4)
    x = controller_1.axis4.position() * STRAFE_SPEED_MULTIPLIER
    # right joystick x axis (1)
    turn = controller_1.axis1.position() * ROTATION_SPEED_MULTIPLIER
    
    # deadband for joystick drift
    if abs(x) < 5:
       x = 0
    if abs(y) < 5:
       y = 0
    if abs(turn) < 5:
       turn = 0
    
    # Convert cartesian values (x and y) into polar values (angle and magnitude)
    theta = math.atan2(y, x) 
    power = math.sqrt(float(x**2) + float(y**2))


    # move drive wheels
    drive(power, turn, theta, x, CRABCRAWLALIGN)
    directMovement()



# Controls Robot drive-------------------------------------------------------------------------------------------
# Forward & Turn control speed of chassiss wheels
# Values Span -100 to 100. 
def drive(power: float, turn: float, theta: float, x: float, crabCrawlAlign: float):
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
    if x > 0 or x < 0:
        rightFront = x * crabCrawlAlign
        leftFront = x * crabCrawlAlign

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


# Intake Mechanism----------------------------------------------------
def intake(): 
    # only want to intake if button "a" is being pressed 
    if controller_1.buttonA.pressing():     
        #flywheelMotor.spin(FORWARD, 50)
        pass
    else:
        #flywheelMotor.stop()
        pass


# Conveyor Mechanism----------------------------------------------------
def conveyor():
    pass


# Shooting Mechanism----------------------------------------------------
def shoot():
    pass
    
def directMovement():
    if controller_1.buttonUp.pressing():     
        frontLeftMotor.spin(FORWARD, 50)
        backLeftMotor.spin(FORWARD, 50)

        frontRightMotor.spin(FORWARD, 50)
        backRightMotor.spin(FORWARD, 50)
    elif controller_1.buttonRight.pressing():
        frontLeftMotor.spin(FORWARD, 50)
        backLeftMotor.spin(FORWARD, -50)
        
        frontRightMotor.spin(FORWARD, -50 * 1) #1 is the offset to get perfectly moving wheels
        backRightMotor.spin(FORWARD, 50 * 1)
    elif controller_1.buttonDown.pressing():
        frontLeftMotor.spin(FORWARD, -50)
        backLeftMotor.spin(FORWARD, -50)
        
        frontRightMotor.spin(FORWARD, -50)
        backRightMotor.spin(FORWARD, -50)
    elif controller_1.buttonLeft.pressing():
        frontLeftMotor.spin(FORWARD, -50)
        backLeftMotor.spin(FORWARD, 50)
        
        frontRightMotor.spin(FORWARD, 50 * 1) 
        backRightMotor.spin(FORWARD, -50 * 1)


     


    

# ---- START ACTUALLY EXECUTING CODE ---- 


while 1:
    main()
    wait(50, MSEC)
