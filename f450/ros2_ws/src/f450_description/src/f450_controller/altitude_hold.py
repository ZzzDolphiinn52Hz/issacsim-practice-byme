from f450_controller.control_utils import PWM_MAX, PWM_MIN, clamp


class AltitudeHoldPID:
    def __init__(
        self,
        z_target=3.0,
        vz_target=0.0,
        pwm_hover=1307.0,
        kp_z=220.0,
        kd_z=150.0,
        ki_z=15.0,
        integral_limit=12.0,
    ):
        self.z_target = float(z_target)
        self.vz_target = float(vz_target)
        self.pwm_hover = float(pwm_hover)

        self.kp_z = float(kp_z)
        self.kd_z = float(kd_z)
        self.ki_z = float(ki_z)

        self.integral_z = 0.0
        self.integral_limit = float(integral_limit)

    def set_target(self, z_target):
        self.z_target = float(z_target)
        self.reset_integral()

    def set_pid(self, kp_z=None, kd_z=None, ki_z=None):
        if kp_z is not None:
            self.kp_z = float(kp_z)
        if kd_z is not None:
            self.kd_z = float(kd_z)
        if ki_z is not None:
            self.ki_z = float(ki_z)

        self.reset_integral()

    def set_pwm_hover(self, pwm_hover):
        self.pwm_hover = clamp(float(pwm_hover), PWM_MIN, PWM_MAX)
        self.reset_integral()

    def reset_integral(self):
        self.integral_z = 0.0

    def compute_pwm_base(self, z, vz, dt):
        error_z = self.z_target - z
        error_vz = self.vz_target - vz

        self.integral_z += error_z * dt
        self.integral_z = clamp(
            self.integral_z,
            -self.integral_limit,
            self.integral_limit,
        )

        delta_pwm = (
            self.kp_z * error_z
            + self.kd_z * error_vz
            + self.ki_z * self.integral_z
        )

        pwm_base = self.pwm_hover + delta_pwm
        pwm_base = clamp(pwm_base, PWM_MIN, PWM_MAX)

        return pwm_base, error_z, error_vz, delta_pwm
