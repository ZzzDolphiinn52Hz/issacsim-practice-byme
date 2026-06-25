conda init

conda deactivate

conda activate env_isaaclab

issacsim

# script test

Ví dụ dùng:
ctrl = F450AttitudeHold(z_target=3.0)
ctrl.start()
Hoặc đặt target cụ thể:
ctrl = F450AttitudeHold(x_target=1.0, y_target=2.0, z_target=3.0)
ctrl.start()
Đổi target khi đang chạy:
ctrl.set_position_target(2.0, -1.0)
ctrl.set_xyz_target(0.0, 0.0, 4.0)
Tune PID XY:
ctrl.set_position_pid(kp_x=0.7, kd_x=1.0, kp_y=0.7, kd_y=1.0)
ctrl.position_angle_limit_deg = 8.0
ctrl.position_accel_limit = 1.5

# script editor
import sys
import importlib

CONTROLLER_PATH = "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src"

if CONTROLLER_PATH not in sys.path:
    sys.path.insert(0, CONTROLLER_PATH)

importlib.invalidate_caches()

import f450_controller.motor_model as motor_model
import f450_controller.issac_attitude_hold as issac_attitude_hold

importlib.reload(motor_model)
importlib.reload(issac_attitude_hold)

try:
    f450_app.stop()
except Exception:
    pass

f450_app = issac_attitude_hold.F450AttitudeHold(
    base_link_path="/f450_simple/base_link",
    z_target=1.0,
    pwm_hover=1568.0,
)

f450_app.start()