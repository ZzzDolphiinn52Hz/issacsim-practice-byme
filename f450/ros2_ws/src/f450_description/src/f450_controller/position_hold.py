import math

from f450_controller.control_utils import clamp


class PositionHoldPID:
    def __init__(
        self,
        x_target=0.0,
        y_target=0.0,
        vx_target=0.0,
        vy_target=0.0,
        enabled=True,
        kp_x=0.65,
        kd_x=0.90,
        ki_x=0.0,
        kp_y=0.65,
        kd_y=0.90,
        ki_y=0.0,
        integral_limit=2.0,
        accel_limit=2.0,
        angle_limit_deg=10.0,
        gravity=9.81,
    ):
        self.enabled = bool(enabled)

        self.x_target = float(x_target)
        self.y_target = float(y_target)
        self.vx_target = float(vx_target)
        self.vy_target = float(vy_target)

        self.kp_x = float(kp_x)
        self.kd_x = float(kd_x)
        self.ki_x = float(ki_x)

        self.kp_y = float(kp_y)
        self.kd_y = float(kd_y)
        self.ki_y = float(ki_y)

        self.integral_x = 0.0
        self.integral_y = 0.0
        self.integral_limit = float(integral_limit)

        self.accel_limit = float(accel_limit)
        self.angle_limit = math.radians(angle_limit_deg)
        self.gravity = float(gravity)

    def set_target(self, x_target=None, y_target=None):
        if x_target is not None:
            self.x_target = float(x_target)
        if y_target is not None:
            self.y_target = float(y_target)

        self.reset_integral()

    def set_pid(
        self,
        kp_x=None,
        kd_x=None,
        ki_x=None,
        kp_y=None,
        kd_y=None,
        ki_y=None,
    ):
        if kp_x is not None:
            self.kp_x = float(kp_x)
        if kd_x is not None:
            self.kd_x = float(kd_x)
        if ki_x is not None:
            self.ki_x = float(ki_x)

        if kp_y is not None:
            self.kp_y = float(kp_y)
        if kd_y is not None:
            self.kd_y = float(kd_y)
        if ki_y is not None:
            self.ki_y = float(ki_y)

        self.reset_integral()

    def reset_integral(self):
        self.integral_x = 0.0
        self.integral_y = 0.0

    def compute_attitude_target(self, x, y, vx, vy, yaw, dt):
        error_x = self.x_target - x
        error_y = self.y_target - y
        error_vx = self.vx_target - vx
        error_vy = self.vy_target - vy

        self.integral_x += error_x * dt
        self.integral_y += error_y * dt

        self.integral_x = clamp(
            self.integral_x,
            -self.integral_limit,
            self.integral_limit,
        )
        self.integral_y = clamp(
            self.integral_y,
            -self.integral_limit,
            self.integral_limit,
        )

        ax_cmd = (
            self.kp_x * error_x
            + self.kd_x * error_vx
            + self.ki_x * self.integral_x
        )
        ay_cmd = (
            self.kp_y * error_y
            + self.kd_y * error_vy
            + self.ki_y * self.integral_y
        )

        ax_cmd, ay_cmd = self._limit_accel(ax_cmd, ay_cmd)

        cos_yaw = math.cos(yaw)
        sin_yaw = math.sin(yaw)

        forward_accel = cos_yaw * ax_cmd + sin_yaw * ay_cmd
        left_accel = -sin_yaw * ax_cmd + cos_yaw * ay_cmd

        pitch_target = math.atan2(forward_accel, self.gravity)
        roll_target = -math.atan2(left_accel, self.gravity)

        pitch_target = clamp(pitch_target, -self.angle_limit, self.angle_limit)
        roll_target = clamp(roll_target, -self.angle_limit, self.angle_limit)

        return {
            "roll_target": roll_target,
            "pitch_target": pitch_target,
            "error_x": error_x,
            "error_y": error_y,
            "error_vx": error_vx,
            "error_vy": error_vy,
            "ax_cmd": ax_cmd,
            "ay_cmd": ay_cmd,
        }

    def _limit_accel(self, ax_cmd, ay_cmd):
        accel_mag = math.sqrt(ax_cmd * ax_cmd + ay_cmd * ay_cmd)

        if accel_mag <= self.accel_limit or accel_mag <= 1e-6:
            return ax_cmd, ay_cmd

        scale = self.accel_limit / accel_mag
        return ax_cmd * scale, ay_cmd * scale
