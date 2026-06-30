import math


PWM_MIN = 1100.0
PWM_MAX = 1940.0


########## CLAMP VALUE ##########
# Kep gia tri x trong khoang [lo, hi], dung de bao ve PWM, goc va tich phan PID.
def clamp(x, lo, hi):
    return max(lo, min(x, hi))


########## WRAP ANGLE ##########
# Dua goc radian ve khoang [-pi, pi] de tinh sai so goc theo duong ngan nhat.
def wrap_angle(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


########## QUATERNION TO EULER ##########
# Chuyen quaternion cua Isaac/dynamic_control sang roll, pitch, yaw theo radian.
def quat_to_euler(q):
    # dynamic_control quaternion is x, y, z, w.
    x = q.x
    y = q.y
    z = q.z
    w = q.w

    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw
