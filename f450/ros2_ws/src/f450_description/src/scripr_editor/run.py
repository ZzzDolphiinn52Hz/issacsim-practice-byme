import sys
import importlib
import os

# Neu may ban dung duong dan khac, chi can sua dong nay.
CONTROLLER_PATH = "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src"
SCRIPT_PATH = CONTROLLER_PATH + "/scripr_editor"
DATA_DIR = CONTROLLER_PATH + "/data"
TRACKING_CSV = DATA_DIR + "/f450_tracking.csv"

for path in (CONTROLLER_PATH, SCRIPT_PATH):
    if path not in sys.path:
        sys.path.insert(0, path)

os.makedirs(DATA_DIR, exist_ok=True)
importlib.invalidate_caches()

# Dung controller cu neu da Run truoc do.
try:
    f450_app.stop()
except Exception:
    pass

MODULE_NAMES = [
    "f450_controller.control_utils",
    "f450_controller.motor_model",
    "f450_controller.altitude_hold",
    "f450_controller.attitude_pid",
    "f450_controller.position_hold",
    "f450_controller.yaw_hold",
    "f450_controller.motor_mixer",
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

    # Neu khong khai bao x_target/y_target, drone se giu vi tri XY hien tai.
    # x_target=0.0,
    # y_target=0.0,
    z_target=1.0,

    # Gia tri da tune tu file tracking gan day.
    pwm_hover=1650.0,
)

# Gioi han goc nghieng do bo dieu khien XY tao ra.
f450_app.position_angle_limit_deg = 6.5
f450_app.position_accel_limit = 1.2

# Dat yaw mong muon, don vi radian. 0.0 la giu huong ban dau theo truc world.
f450_app.set_yaw_target(0.0)

# Bat log de ve do thi tracking.
f450_app.start_tracking_log(TRACKING_CSV, sample_period=0.02)

# Bat dau dieu khien.
f450_app.start()

print("F450 controller STARTED")
print("Tracking CSV:", TRACKING_CSV)
