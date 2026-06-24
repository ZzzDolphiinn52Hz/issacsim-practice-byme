import math


class MotorModel:
    """
    Simple ESC + BLDC motor + propeller model.

    Input:
        PWM in microseconds

    Output:
        thrust in Newton
    """

    def __init__(
        self,
        pwm_min=1100.0,
        pwm_max=1940.0,
        vbat=14.8,
        kv=1100.0,
        rm=0.073,
        i0=0.9,
        i_max=30.0,
        j_motor_prop=2.5e-5,
        kf=4.0e-6,
        kq=1.0e-7,
        omega_max=1800.0,
    ):
        self.pwm_min = pwm_min
        self.pwm_max = pwm_max

        self.vbat = vbat
        self.kv = kv

        # Ke ≈ Kt in SI units
        self.ke = 60.0 / (2.0 * math.pi * kv)
        self.kt = self.ke

        self.rm = rm
        self.i0 = i0
        self.i_max = i_max

        self.j_motor_prop = j_motor_prop

        # Tune these two parameters in simulation
        self.kf = kf
        self.kq = kq

        self.omega_max = omega_max

        self.omega = 0.0
        self.current = 0.0
        self.thrust = 0.0
        self.torque_motor = 0.0
        self.torque_load = 0.0

    @staticmethod
    def clamp(x, lo, hi):
        return max(lo, min(x, hi))

    def pwm_to_u(self, pwm):
        pwm = self.clamp(pwm, self.pwm_min, self.pwm_max)
        return (pwm - self.pwm_min) / (self.pwm_max - self.pwm_min)

    def update(self, pwm, dt):
        """
        Update motor state for one simulation step.

        Returns:
            thrust, current, rpm
        """

        dt = max(dt, 1e-6)

        u = self.pwm_to_u(pwm)

        # Effective voltage from ESC
        vm = u * self.vbat

        # Simple DC-equivalent motor current
        current = (vm - self.ke * self.omega) / self.rm
        current = self.clamp(current, 0.0, self.i_max)

        # Motor torque
        torque_motor = self.kt * max(current - self.i0, 0.0)

        # Propeller aerodynamic load torque
        torque_load = self.kq * self.omega * self.omega

        # Rotor dynamics
        omega_dot = (torque_motor - torque_load) / self.j_motor_prop
        self.omega += omega_dot * dt
        self.omega = self.clamp(self.omega, 0.0, self.omega_max)

        # Thrust
        thrust = self.kf * self.omega * self.omega

        self.current = current
        self.thrust = thrust
        self.torque_motor = torque_motor
        self.torque_load = torque_load

        rpm = self.omega * 60.0 / (2.0 * math.pi)

        return thrust, current, rpm