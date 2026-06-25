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
import os

CONTROLLER_PATH = "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src"
DATA_DIR = CONTROLLER_PATH + "/data"
TRACKING_CSV = DATA_DIR + "/f450_tracking.csv"

if CONTROLLER_PATH not in sys.path:
    sys.path.insert(0, CONTROLLER_PATH)

os.makedirs(DATA_DIR, exist_ok=True)
importlib.invalidate_caches()

try:
    f450_app.stop()
except Exception:
    pass

# Reload all controller modules because Isaac Script Editor keeps module cache
# between runs.
MODULE_NAMES = [
    "f450_controller.control_utils",
    "f450_controller.motor_model",
    "f450_controller.altitude_hold",
    "f450_controller.attitude_pid",
    "f450_controller.position_hold",
    "f450_controller.motor_mixer",
    "f450_controller.disturbance",
    "f450_controller.propeller_spinner",
    "f450_controller.tracking_logger",
    "f450_controller.attitude_hold_compat",
    "f450_controller.issac_attitude_hold",
]

modules = {}

for module_name in MODULE_NAMES:
    modules[module_name] = importlib.import_module(module_name)

for module_name in MODULE_NAMES:
    modules[module_name] = importlib.reload(modules[module_name])

issac_attitude_hold = modules["f450_controller.issac_attitude_hold"]

f450_app = issac_attitude_hold.F450AttitudeHold(
    base_link_path="/f450_simple/base_link",
    # If x_target/y_target are omitted, the controller holds current XY position.
    # x_target=0.0,
    # y_target=0.0,
    z_target=1.0,
    pwm_hover=1568.0,
)

# Optional tuning for XY position hold.
f450_app.position_angle_limit_deg = 8.0
f450_app.position_accel_limit = 1.5

# Optional: log tracking data for live/static plotting.
f450_app.start_tracking_log(TRACKING_CSV, sample_period=0.02)

f450_app.start()

# After the run, stop logging before plotting:
# f450_app.stop_tracking_log()
#
# Live plot outside Isaac:
# python3 f450/ros2_ws/src/f450_description/src/data/live_plot_tracking.py f450/ros2_ws/src/f450_description/src/data/f450_tracking.csv --wait --window 20
#
# Static plot outside Isaac:
# python3 f450/ros2_ws/src/f450_description/src/data/plot_tracking.py f450/ros2_ws/src/f450_description/src/data/f450_tracking.csv
