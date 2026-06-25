from f450_controller.control_utils import clamp, wrap_angle


class AttitudeHoldPID:
    def __init__(
        self,
        roll_target=0.0,
        pitch_target=0.0,
        kp_roll=520.0,
        ki_roll=25.0,
        kd_roll=130.0,
        kp_pitch=520.0,
        ki_pitch=25.0,
        kd_pitch=130.0,
        integral_limit=1.0,
        pwm_limit=260.0,
    ):
        self.roll_target = float(roll_target)
        self.pitch_target = float(pitch_target)

        self.kp_roll = float(kp_roll)
        self.ki_roll = float(ki_roll)
        self.kd_roll = float(kd_roll)

        self.kp_pitch = float(kp_pitch)
        self.ki_pitch = float(ki_pitch)
        self.kd_pitch = float(kd_pitch)

        self.integral_roll = 0.0
        self.integral_pitch = 0.0
        self.integral_limit = float(integral_limit)
        self.pwm_limit = float(pwm_limit)

    def set_pid(
        self,
        kp_roll=None,
        ki_roll=None,
        kd_roll=None,
        kp_pitch=None,
        ki_pitch=None,
        kd_pitch=None,
    ):
        if kp_roll is not None:
            self.kp_roll = float(kp_roll)
        if ki_roll is not None:
            self.ki_roll = float(ki_roll)
        if kd_roll is not None:
            self.kd_roll = float(kd_roll)

        if kp_pitch is not None:
            self.kp_pitch = float(kp_pitch)
        if ki_pitch is not None:
            self.ki_pitch = float(ki_pitch)
        if kd_pitch is not None:
            self.kd_pitch = float(kd_pitch)

        self.reset_integral()

    def reset_integral(self):
        self.integral_roll = 0.0
        self.integral_pitch = 0.0

    def compute_correction(self, roll, pitch, ang_vel, dt):
        error_roll = wrap_angle(self.roll_target - roll)
        error_pitch = wrap_angle(self.pitch_target - pitch)

        # Angular velocity around body axes.
        p = ang_vel.x
        q = ang_vel.y

        self.integral_roll += error_roll * dt
        self.integral_pitch += error_pitch * dt

        self.integral_roll = clamp(
            self.integral_roll,
            -self.integral_limit,
            self.integral_limit,
        )

        self.integral_pitch = clamp(
            self.integral_pitch,
            -self.integral_limit,
            self.integral_limit,
        )

        roll_corr = (
            self.kp_roll * error_roll
            + self.ki_roll * self.integral_roll
            - self.kd_roll * p
        )

        pitch_corr = (
            self.kp_pitch * error_pitch
            + self.ki_pitch * self.integral_pitch
            - self.kd_pitch * q
        )

        roll_corr = clamp(roll_corr, -self.pwm_limit, self.pwm_limit)
        pitch_corr = clamp(pitch_corr, -self.pwm_limit, self.pwm_limit)

        return roll_corr, pitch_corr, error_roll, error_pitch
