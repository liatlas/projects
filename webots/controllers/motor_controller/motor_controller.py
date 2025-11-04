# toy_scooper_controller_4wd.py
# Author: ChatGPT (GPT-5)
# Webots demo controller for a GoPiGo-like robot with 4-wheel drive and two-joint scooper
# Detects a red toy, scoops it, and drops it at a blue zone.

from controller import Robot
import cv2
import numpy as np

TIME_STEP = 32
FORWARD_SPEED = 2.0
TURN_SPEED = 1.5

robot = Robot()

# Devices
camera = robot.getDevice("camera")
camera.enable(TIME_STEP)

# Four wheels
wheel_front_left = robot.getDevice("Wheel_FL")
wheel_front_right = robot.getDevice("Wheel_FR")
wheel_back_left = robot.getDevice("Wheel_BL")
wheel_back_right = robot.getDevice("Wheel_BR")

for w in [wheel_front_left, wheel_front_right, wheel_back_left, wheel_back_right]:
    w.setPosition(float('inf'))  # continuous rotation
    w.setVelocity(0.0)

# Scooper joints
scoop_base = robot.getDevice("scoop_base_motor")
scoop_tip = robot.getDevice("scoop_tip_motor")
for m in [scoop_base, scoop_tip]:
    m.setVelocity(1.5)
    m.setPosition(0.0)

# --- Motion helpers ---
def drive(left_speed, right_speed):
    """Drive robot with 4-wheel drive."""
    wheel_front_left.setVelocity(left_speed)
    wheel_back_left.setVelocity(left_speed)
    wheel_front_right.setVelocity(right_speed)
    wheel_back_right.setVelocity(right_speed)

def stop():
    drive(0, 0)

def set_scoop(base, tip):
    scoop_base.setPosition(base)
    scoop_tip.setPosition(tip)

# --- Vision detection ---
def get_target_offset(image, lower, upper, lower2=None, upper2=None):
    """Return center of detected color. Optional second range for wrap-around colors."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask1 = cv2.inRange(hsv, lower, upper)
    mask = mask1
    if lower2 is not None and upper2 is not None:
        mask2 = cv2.inRange(hsv, lower2, upper2)
        mask = mask1 + mask2
    M = cv2.moments(mask)
    if M["m00"] == 0:
        return None
    cx = int(M["m10"]/M["m00"])
    cy = int(M["m01"]/M["m00"])
    return (cx, cy)

# --- State machine ---
state = "SEARCH"
timer = 0

while robot.step(TIME_STEP) != -1:
    # Get camera image
    width = camera.getWidth()
    height = camera.getHeight()
    img = np.frombuffer(camera.getImage(), np.uint8).reshape((height, width, 4))
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    if state == "SEARCH":
        # Look for red toy (handle wrap-around red)
        result = get_target_offset(
            img,
            np.array([0,120,70]), np.array([10,255,255]),
            np.array([170,120,70]), np.array([180,255,255])
        )
        if result:
            cx, cy = result
            error = cx - width/2
            # Turn to align with object
            if abs(error) > 20:
                turn = TURN_SPEED if error > 0 else -TURN_SPEED
                drive(-turn, turn)
            else:
                # Keep moving forward until object is very close
                drive(FORWARD_SPEED, FORWARD_SPEED)
            # Stop and start scooping only when very close
            if cy > height*0.85:
                stop()
                state = "SCOOP_DOWN"
                timer = robot.getTime()
        else:
            # Rotate to search for object if not visible
            drive(0.8, -0.8)

    elif state == "SCOOP_DOWN":
        set_scoop(0.6, -0.4)
        stop()
        if robot.getTime() - timer > 1.5:
            state = "PUSH"
            timer = robot.getTime()

    elif state == "PUSH":
        drive(2.0, 2.0)
        if robot.getTime() - timer > 1.2:
            stop()
            state = "SCOOP_UP"
            timer = robot.getTime()

    elif state == "SCOOP_UP":
        set_scoop(0.0, 0.3)
        if robot.getTime() - timer > 1.5:
            state = "GO_DROP"
            timer = robot.getTime()

    elif state == "GO_DROP":
        # Look for blue drop zone
        result = get_target_offset(img, np.array([90,100,70]), np.array([130,255,255]))
        if result:
            cx, cy = result
            error = cx - width/2
            # Turn to align with drop zone
            if abs(error) > 25:
                turn = TURN_SPEED if error > 0 else -TURN_SPEED
                drive(-turn, turn)
            else:
                drive(FORWARD_SPEED, FORWARD_SPEED)
            if cy > height*0.7:
                stop()
                state = "DROP"
                timer = robot.getTime()
        else:
            # Rotate if drop zone not visible
            drive(-1, 1)

    elif state == "DROP":
        set_scoop(0.6, -0.4)
        if robot.getTime() - timer > 2.0:
            stop()
            state = "DONE"

    elif state == "DONE":
        stop()
        print("✅ Demo complete!")
        break
