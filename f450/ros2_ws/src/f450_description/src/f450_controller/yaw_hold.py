from f450_controller.control_utils import clamp, wrap_angle


class YawHoldPID:
    # Output unit is PWM microseconds, not torque.
    ########## INIT YAW PID ##########
    # Khoi tao bo giu yaw: target huong, trang thai bat/tat, he so PID va gioi
    # han PWM hieu chinh yaw.
    def __init__(
        self,
        yaw_target=0.0,
        enabled=True,
        kp_yaw=95.0,
        ki_yaw=8.0,
        kd_yaw=28.0,
        integral_limit=0.8,
        pwm_limit=120.0,
    ):
        # Trang thai bat/tat va huong yaw muc tieu.
        self.enabled = bool(enabled)
        self.yaw_target = float(yaw_target)

        # He so PID cho vong giu yaw.
        self.kp_yaw = float(kp_yaw)
        self.ki_yaw = float(ki_yaw)
        self.kd_yaw = float(kd_yaw)

        # Bo nho tich phan va gioi han PWM correction yaw.
        self.integral_yaw = 0.0
        self.integral_limit = float(integral_limit)
        self.pwm_limit = float(pwm_limit)

    ########## SET YAW TARGET ##########
    # Cap nhat huong yaw muc tieu va reset tich phan de dap ung sach hon.
    def set_target(self, yaw_target):
        self.yaw_target = float(yaw_target)
        self.reset_integral()

    ########## SET YAW PID PARAMS ##########
    # Cap nhat tung he so PID cua yaw, giu nguyen nhung tham so khong truyen vao.
    def set_pid(self, kp_yaw=None, ki_yaw=None, kd_yaw=None):
        if kp_yaw is not None:
            self.kp_yaw = float(kp_yaw)
        if ki_yaw is not None:
            self.ki_yaw = float(ki_yaw)
        if kd_yaw is not None:
            self.kd_yaw = float(kd_yaw)

        self.reset_integral()

    ########## RESET YAW INTEGRAL ##########
    # Xoa bo nho tich phan cua yaw controller.
    def reset_integral(self):
        self.integral_yaw = 0.0

    ########## COMPUTE YAW CORRECTION ##########
    # Tinh PWM hieu chinh yaw tu sai so huong va yaw rate, sau do kep theo
    # pwm_limit truoc khi dua vao mixer.
    def compute_correction(self, yaw, yaw_rate, dt):
        error_yaw = wrap_angle(self.yaw_target - yaw)

        self.integral_yaw += error_yaw * dt
        self.integral_yaw = clamp(
            self.integral_yaw,
            -self.integral_limit,
            self.integral_limit,
        )

        yaw_corr = (
            self.kp_yaw * error_yaw
            + self.ki_yaw * self.integral_yaw
            - self.kd_yaw * yaw_rate
        )
        yaw_corr = clamp(yaw_corr, -self.pwm_limit, self.pwm_limit)

        return yaw_corr, error_yaw
