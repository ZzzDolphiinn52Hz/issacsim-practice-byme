import carb

from f450_controller.control_utils import PWM_MAX, PWM_MIN, clamp


def build_motor_positions(arm_xy=0.159, motor_z=0.04):
    return [
        carb.Float3(arm_xy, arm_xy, motor_z),    # motor 1: front-left
        carb.Float3(arm_xy, -arm_xy, motor_z),   # motor 2: front-right
        carb.Float3(-arm_xy, -arm_xy, motor_z),  # motor 3: rear-right
        carb.Float3(-arm_xy, arm_xy, motor_z),   # motor 4: rear-left
    ]


class QuadXPwmMixer:
    def mix(self, pwm_base, roll_corr, pitch_corr, yaw_corr=0.0):
        # Body-z thrust: roll torque ~ y * F, pitch torque ~ -x * F.
        #
        # Yaw uses reaction torque from propeller drag. Positive yaw_corr
        # increases motors with negative spin direction and decreases motors
        # with positive spin direction.
        pwm1 = pwm_base + roll_corr - pitch_corr - yaw_corr
        pwm2 = pwm_base - roll_corr - pitch_corr + yaw_corr
        pwm3 = pwm_base - roll_corr + pitch_corr - yaw_corr
        pwm4 = pwm_base + roll_corr + pitch_corr + yaw_corr

        return [
            clamp(pwm1, PWM_MIN, PWM_MAX),
            clamp(pwm2, PWM_MIN, PWM_MAX),
            clamp(pwm3, PWM_MIN, PWM_MAX),
            clamp(pwm4, PWM_MIN, PWM_MAX),
        ]
