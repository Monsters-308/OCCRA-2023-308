
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
# backRightMotor      motor29       C
# Triport:
#     redFlywheelMotor    motor29       C
#     blueFlywheelMotor   motor29       D
#     intakeMotor         motor29       A
#     conveyorMotor       motor29       B
# Bottom of Vexcode Configures Devices KEY---------


# CONFIGURE DEVICES-------------------------------------------
# Brain should be defined by default
brain=Brain()

frontLeftMotor = Motor29(brain.three_wire_port.a, False)
frontRightMotor = Motor29(brain.three_wire_port.b, True)
backLeftMotor = Motor29(brain.three_wire_port.d, False)
backRightMotor = Motor29(brain.three_wire_port.c, True)

triport = Triport(Ports.PORT1)
redFlywheelMotor = Motor29(triport.c, True)
blueFlywheelMotor = Motor29(triport.d, True)
intakeMotor = Motor29(triport.a, False)
conveyorMotor = Motor29(triport.b, False)

controller_1 = Controller(PRIMARY)
controller_2 = Controller(PARTNER)
#controller_2 = controller_1

# Constants
FORWARD_SPEED_MULTIPLIER = 1
STRAFE_SPEED_MULTIPLIER = 1
ROTATION_SPEED_MULTIPLIER = 0.42
CRABCRAWLALIGN = 2


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
    if abs(x) < 2:
       x = 0
    if abs(y) < 2:
       y = 0
    if abs(turn) < 2:
       turn = 0
    
    # Convert cartesian values (x and y) into polar values (angle and magnitude)
    theta = math.atan2(y, x) 
    power = math.sqrt(float(x**2) + float(y**2))

    
    
    intake()
    conveyor()
    shoot()

    # move drive wheels
    if(controller_1.buttonLeft.pressing()):
        drive(70, 0, math.radians(180), x)
    elif(controller_1.buttonRight.pressing()):
        drive(70, 0, 0, x)
    elif(controller_1.buttonDown.pressing()):
        drive(70, 0, math.radians(-90), x)
    elif(controller_1.buttonUp.pressing()):
        drive(70, 0, math.radians(90), x)
    else:
        drive(power, turn, theta, x)


# Controls Robot drive-------------------------------------------------------------------------------------------
# Forward & Turn control speed of chassiss wheels
# Values Span -100 to 100. 
def drive(power: float, turn: float, theta: float, strafeAxis: float):
    sin = math.sin(theta - math.pi/4)
    cos = math.cos(theta - math.pi/4)
    maxValue = max(abs(sin), abs(cos))
    
    leftFront = power * cos/maxValue + turn
    rightFront = power * sin/maxValue - turn
    leftRear = power * sin/maxValue + turn
    rightRear = power * cos/maxValue - turn

    # DEBUG: realign strafing 
    #if strafeAxis > 0 or strafeAxis < 0:
    #    rightFront = rightFront * CRABCRAWLALIGN
    #    leftFront = leftFront * CRABCRAWLALIGN

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
    frontLeftMotor.spin(FORWARD, leftFront, PERCENT)
    backLeftMotor.spin(FORWARD, leftRear, PERCENT)

    # drive right side
    frontRightMotor.spin(FORWARD, rightFront, PERCENT)
    backRightMotor.spin(FORWARD, rightRear, PERCENT)


    # Print motor vaules out for debugging

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
    if controller_2.buttonL2.pressing():     
        intakeMotor.spin(FORWARD, 80, PERCENT)
    elif controller_2.buttonL1.pressing():
        intakeMotor.spin(REVERSE, 70, PERCENT)
    else:
        intakeMotor.stop()


# Conveyor Mechanism----------------------------------------------------
def conveyor():
    if controller_2.buttonR1.pressing() or controller_2.buttonL1.pressing():     
        conveyorMotor.spin(FORWARD, 60, PERCENT)
    #oppsie button
    elif controller_2.buttonA.pressing():
        conveyorMotor.spin(REVERSE, 60, PERCENT)
    else:
        conveyorMotor.stop()


# Shooting Mechanism----------------------------------------------------
def shoot():
    if controller_2.buttonR2.pressing():
        # If the motor state is on, spin the motors
        redFlywheelMotor.spin(FORWARD, 65, PERCENT)
        blueFlywheelMotor.spin(FORWARD, 60, PERCENT)
    elif controller_2.buttonUp.pressing():
        # If the motor state is on, spin the motors
        redFlywheelMotor.spin(FORWARD, 75, PERCENT)
        blueFlywheelMotor.spin(FORWARD, 65, PERCENT)
    elif controller_2.buttonX.pressing():
        # If the motor state is on, spin the motors
        redFlywheelMotor.spin(REVERSE, 75, PERCENT)
        blueFlywheelMotor.spin(REVERSE, 75, PERCENT)
    else:
        # If the motor state is off, stop the motors
        redFlywheelMotor.stop()
        blueFlywheelMotor.stop()
    
    

# ---- START EXECUTING CODE ---- 


while 1:
    main()
    wait(7, MSEC)
