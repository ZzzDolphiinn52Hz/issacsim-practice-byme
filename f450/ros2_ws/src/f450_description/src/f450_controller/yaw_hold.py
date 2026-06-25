from f450_controller.control_utils import clamp, wrap_angle


class YawHoldPID:
    def __init__(
        self,
        yaw_target=0.0,
        enabled=True,
        kp_yaw=0.08,
        ki_yaw=0.004,
        kd_yaw=0.030,
        integral_limit=0.8,
        torque_limit=0.08,
    ):
        self.enabled = bool(enabled)
        self.yaw_target = float(yaw_target)

        self.kp_yaw = float(kp_yaw)
        self.ki_yaw = float(ki_yaw)
        self.kd_yaw = float(kd_yaw)

        self.integral_yaw = 0.0
        self.integral_limit = float(integral_limit)
        self.torque_limit = float(torque_limit)

    def set_target(self, yaw_target):
        self.yaw_target = float(yaw_target)
        self.reset_integral()

    def set_pid(self, kp_yaw=None, ki_yaw=None, kd_yaw=None):
        if kp_yaw is not None:
            self.kp_yaw = float(kp_yaw)
        if ki_yaw is not None:
            self.ki_yaw = float(ki_yaw)
        if kd_yaw is not None:
            self.kd_yaw = float(kd_yaw)

        self.reset_integral()

    def reset_integral(self):
        self.integral_yaw = 0.0

    def compute_torque(self, yaw, yaw_rate, dt):
        error_yaw = wrap_angle(self.yaw_target - yaw)

        self.integral_yaw += error_yaw * dt
        self.integral_yaw = clamp(
            self.integral_yaw,
            -self.integral_limit,
            self.integral_limit,
        )

        torque = (
            self.kp_yaw * error_yaw
            + self.ki_yaw * self.integral_yaw
            - self.kd_yaw * yaw_rate
        )
        torque = clamp(torque, -self.torque_limit, self.torque_limit)

        return torque, error_yaw
