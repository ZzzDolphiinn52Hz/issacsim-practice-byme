from f450_controller.control_utils import PWM_MAX, PWM_MIN, clamp


class AltitudeHoldPID:
    ########## INIT ALTITUDE PID ##########
    # Khoi tao bo giu do cao: muc tieu z/vz, PWM hover, he so PID va gioi han
    # tich phan de tranh integral windup.
    def __init__(
        self,
        z_target=3.0,
        vz_target=0.0,
        pwm_hover=1650.0,
        kp_z=220.0,
        kd_z=150.0,
        ki_z=15.0,
        integral_limit=12.0,
    ):
        # Target do cao va van toc doc mong muon.
        self.z_target = float(z_target)
        self.vz_target = float(vz_target)
        self.pwm_hover = float(pwm_hover)

        # He so PID cho truc z.
        self.kp_z = float(kp_z)
        self.kd_z = float(kd_z)
        self.ki_z = float(ki_z)

        # Bo nho tich phan va gioi han chong windup.
        self.integral_z = 0.0
        self.integral_limit = float(integral_limit)

    ########## SET ALTITUDE TARGET ##########
    # Cap nhat do cao muc tieu va reset tich phan de bo PID khong mang sai so cu
    # sang muc tieu moi.
    def set_target(self, z_target):
        self.z_target = float(z_target)
        self.reset_integral()

    ########## SET ALTITUDE PID PARAMS ##########
    # Cho phep thay tung he so PID rieng le; tham so nao bang None thi giu nguyen
    # gia tri hien tai.
    def set_pid(self, kp_z=None, kd_z=None, ki_z=None):
        if kp_z is not None:
            self.kp_z = float(kp_z)
        if kd_z is not None:
            self.kd_z = float(kd_z)
        if ki_z is not None:
            self.ki_z = float(ki_z)

        self.reset_integral()

    ########## SET HOVER PWM ##########
    # Cap nhat PWM hover va kep trong khoang an toan cua ESC/motor.
    def set_pwm_hover(self, pwm_hover):
        self.pwm_hover = clamp(float(pwm_hover), PWM_MIN, PWM_MAX)
        self.reset_integral()

    ########## RESET ALTITUDE INTEGRAL ##########
    # Xoa thanh phan tich phan cua PID do cao khi doi target hoac doi tham so.
    def reset_integral(self):
        self.integral_z = 0.0

    ########## COMPUTE ALTITUDE PWM BASE ##########
    # Tinh PWM nen tu sai so do cao va van toc doc. PWM nen nay se duoc mixer
    # cong/tru them hieu chinh roll, pitch, yaw cho tung motor.
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
