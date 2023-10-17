
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
#     flywheelMotor1      motor29       D
#     flywheelMotor2      motor29       F
#     intakeMotor         motor29       A
#     conveyorMotor       motor29       C
# Bottom of Vexcode Configures Devices KEY---------


# CONFIGURE DEVICES-------------------------------------------
# Brain should be defined by default
brain=Brain()

frontLeftMotor = Motor29(brain.three_wire_port.a, False)
frontRightMotor = Motor29(brain.three_wire_port.b, True)
backLeftMotor = Motor29(brain.three_wire_port.d, False)
backRightMotor = Motor29(brain.three_wire_port.c, True)

triport = Triport(Ports.PORT1)
<<<<<<< HEAD
redFlywheelMotor = Motor29(triport.c, True)
blueFlywheelMotor = Motor29(triport.d, False)
intakeMotor = Motor29(triport.a, False)
conveyorMotor = Motor29(triport.b, False)
=======
flywheelMotor1 = Motor29(triport.d, True)
flywheelMotor2 = Motor29(triport.f, False)
intakeMotor = Motor29(triport.a, False)
conveyorMotor = Motor29(triport.c, False)
>>>>>>> e63611871afd710c2235ce53f1dd9795b63e9a9f

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

<<<<<<< Updated upstream
=======
<<<<<<< HEAD
    
    
    intake()
    conveyor()
    shoot()
=======
>>>>>>> Stashed changes
    # Reverse motor directions if the X button is held
    if controller_1.buttonX.pressing():     
        direction = REVERSE
    else:
        direction = FORWARD
    
    intake()
    conveyor(direction)
    shoot(direction)
>>>>>>> e63611871afd710c2235ce53f1dd9795b63e9a9f

    # move drive wheels
    if(controller_1.buttonLeft.pressing()):
        drive(50, 0, math.radians(180), x)
    elif(controller_1.buttonRight.pressing()):
        drive(50, 0, 0, x)
    elif(controller_1.buttonDown.pressing()):
        drive(50, 0, math.radians(-90), x)
    elif(controller_1.buttonUp.pressing()):
        drive(50, 0, math.radians(90), x)
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
     #   rightFront = rightFront * CRABCRAWLALIGN
      #  leftFront = leftFront * CRABCRAWLALIGN

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
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
    if controller_2.buttonL2.pressing():     
        intakeMotor.spin(FORWARD, 70, PERCENT)
    elif controller_2.buttonL1.pressing():
        intakeMotor.spin(REVERSE, 70, PERCENT)
=======
>>>>>>> Stashed changes
    if controller_1.buttonL2.pressing():     
        intakeMotor.spin(FORWARD, 50, PERCENT)
    elif controller_1.buttonL1.pressing():
        intakeMotor.spin(REVERSE, 50, PERCENT)
<<<<<<< Updated upstream
=======
>>>>>>> e63611871afd710c2235ce53f1dd9795b63e9a9f
>>>>>>> Stashed changes
    else:
        intakeMotor.stop()


# Conveyor Mechanism----------------------------------------------------
<<<<<<< HEAD
def conveyor():
    if controller_2.buttonR1.pressing() or controller_2.buttonL1.pressing():     
        conveyorMotor.spin(FORWARD, 60, PERCENT)
        # controller_1.screen.clear_screen()
        # controller_1.screen.set_cursor(1,1)
        # controller_1.screen.print("print test ", direction)
    #oppsie button
    elif controller_2.buttonA.pressing():
        conveyorMotor.spin(REVERSE, 60, PERCENT)
=======
def conveyor(direction):
    if controller_1.buttonR1.pressing():     
        conveyorMotor.spin(direction, 60, PERCENT)
        # controller_1.screen.clear_screen()
        # controller_1.screen.set_cursor(1,1)
        # controller_1.screen.print("print test ", direction)
<<<<<<< Updated upstream
=======
>>>>>>> e63611871afd710c2235ce53f1dd9795b63e9a9f
>>>>>>> Stashed changes
    else:
        # controller_1.screen.clear_screen()
        # controller_1.screen.set_cursor(1,1)
        # controller_1.screen.print("not run ", direction)
        conveyorMotor.stop()


# Shooting Mechanism----------------------------------------------------
<<<<<<< Updated upstream
=======
<<<<<<< HEAD
def shoot():
    if controller_2.buttonR2.pressing():
        # If the motor state is on, spin the motors
        redFlywheelMotor.spin(FORWARD, 70, PERCENT)
        blueFlywheelMotor.spin(FORWARD, 65, PERCENT)
    elif controller_2.buttonX.pressing():
        # If the motor state is on, spin the motors
        redFlywheelMotor.spin(REVERSE, 90, PERCENT)
        blueFlywheelMotor.spin(REVERSE, 90, PERCENT)
    else:
        # If the motor state is off, stop the motors
        redFlywheelMotor.stop()
        blueFlywheelMotor.stop()
=======
>>>>>>> Stashed changes
g_isFlywheelOn = False
def shoot(direction):
    global g_isFlywheelOn

    if controller_1.buttonR2.pressing():
        # Toggle the state when the button is pressed
        g_isFlywheelOn = not g_isFlywheelOn

    if g_isFlywheelOn:
        # If the motor state is on, spin the motors
        flywheelMotor1.spin(direction, 70, PERCENT)
        flywheelMotor2.spin(direction, 70, PERCENT)
    else:
        # If the motor state is off, stop the motors
        flywheelMotor1.stop()
        flywheelMotor2.stop()
<<<<<<< Updated upstream
=======
>>>>>>> e63611871afd710c2235ce53f1dd9795b63e9a9f
>>>>>>> Stashed changes
    
    

# ---- START EXECUTING CODE ---- 


while 1:
    main()
<<<<<<< Updated upstream
    wait(10, MSEC)
=======
<<<<<<< HEAD
    wait(2, MSEC)
=======
    wait(10, MSEC)
>>>>>>> e63611871afd710c2235ce53f1dd9795b63e9a9f
>>>>>>> Stashed changes
