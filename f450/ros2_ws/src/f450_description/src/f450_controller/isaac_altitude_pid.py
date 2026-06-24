import omni
import omni.timeline
import omni.physx
import carb

from omni.isaac.dynamic_control import _dynamic_control

from f450_controller.motor_model import MotorModel


PWM_MIN = 1100.0
PWM_MAX = 1940.0


def clamp(x, lo, hi):
    return max(lo, min(x, hi))


class F450AltitudePID:
    def __init__(
        self,
        base_link_path="/f450_simple/base_link",
        z_target=3.0,
        pwm_hover=1550.0,
        arm_xy=0.159,
        motor_z=0.04,
    ):
        self.base_link_path = base_link_path

        self.z_target = float(z_target)
        self.vz_target = 0.0

        self.pwm_hover = float(pwm_hover)

        # PID gains, unit: microsecond PWM
        self.kp_z = 150.0    # us / m
        self.kd_z = 90.0     # us / (m/s)
        self.ki_z = 10.0      # us / (m*s)

        self.integral_z = 0.0
        self.integral_limit = 2.0

        self.arm_xy = arm_xy
        self.motor_z = motor_z

        self.motor_positions = [
            carb.Float3( arm_xy,  arm_xy, motor_z),   # motor 1: front-left
            carb.Float3( arm_xy, -arm_xy, motor_z),   # motor 2: front-right
            carb.Float3(-arm_xy, -arm_xy, motor_z),   # motor 3: rear-right
            carb.Float3(-arm_xy,  arm_xy, motor_z),   # motor 4: rear-left
        ]

        self.motors = [
            MotorModel(),
            MotorModel(),
            MotorModel(),
            MotorModel(),
        ]

        self.pwm_commands = [
            self.pwm_hover,
            self.pwm_hover,
            self.pwm_hover,
            self.pwm_hover,
        ]

        self.dc = _dynamic_control.acquire_dynamic_control_interface()
        self.timeline = omni.timeline.get_timeline_interface()

        self.physics_subscription = None

        self.sim_time = 0.0
        self.last_print_time = 0.0

    def start(self):
        self.stop()

        self.physics_subscription = (
            omni.physx.get_physx_interface().subscribe_physics_step_events(
                self.on_physics_step
            )
        )

        self.timeline.play()

        print("F450 altitude PID started")
        print("base_link_path =", self.base_link_path)
        print("z_target =", self.z_target)
        print("pwm_hover =", self.pwm_hover)
        print("kp_z =", self.kp_z)
        print("kd_z =", self.kd_z)
        print("ki_z =", self.ki_z)

    def stop(self):
        if self.physics_subscription is not None:
            try:
                self.physics_subscription.unsubscribe()
            except Exception:
                pass

        self.physics_subscription = None

    def set_target(self, z_target):
        self.z_target = float(z_target)
        self.integral_z = 0.0
        print("Updated z_target:", self.z_target)

    def set_pid(self, kp_z=None, kd_z=None, ki_z=None):
        if kp_z is not None:
            self.kp_z = float(kp_z)
        if kd_z is not None:
            self.kd_z = float(kd_z)
        if ki_z is not None:
            self.ki_z = float(ki_z)

        self.integral_z = 0.0

        print(
            "Updated PID:",
            "kp_z =", self.kp_z,
            "kd_z =", self.kd_z,
            "ki_z =", self.ki_z,
        )

    def set_pwm_hover(self, pwm_hover):
        self.pwm_hover = clamp(float(pwm_hover), PWM_MIN, PWM_MAX)
        print("Updated pwm_hover:", self.pwm_hover)

    def reset_integral(self):
        self.integral_z = 0.0
        print("Reset altitude integral")

    def compute_altitude_pwm(self, z, vz, dt):
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

        pwm = self.pwm_hover + delta_pwm
        pwm = clamp(pwm, PWM_MIN, PWM_MAX)

        return pwm, error_z, error_vz, delta_pwm

    def on_physics_step(self, dt):
        self.sim_time += dt

        body_handle = self.dc.get_rigid_body(self.base_link_path)

        if body_handle == _dynamic_control.INVALID_HANDLE:
            carb.log_error(f"Cannot find rigid body: {self.base_link_path}")
            return

        pose = self.dc.get_rigid_body_pose(body_handle)
        lin_vel = self.dc.get_rigid_body_linear_velocity(body_handle)

        z = pose.p.z
        vz = lin_vel.z

        pwm_common, error_z, error_vz, delta_pwm = self.compute_altitude_pwm(
            z,
            vz,
            dt,
        )

        self.pwm_commands = [
            pwm_common,
            pwm_common,
            pwm_common,
            pwm_common,
        ]

        thrusts = []
        currents = []
        rpms = []

        for i in range(4):
            thrust, current, rpm = self.motors[i].update(
                self.pwm_commands[i],
                dt,
            )

            thrusts.append(thrust)
            currents.append(current)
            rpms.append(rpm)

            self.dc.apply_body_force(
                body_handle,
                carb.Float3(0.0, 0.0, thrust),
                self.motor_positions[i],
                False,
            )

        if self.sim_time - self.last_print_time > 0.5:
            self.last_print_time = self.sim_time

            print(
                f"z={z:.3f} | "
                f"vz={vz:.3f} | "
                f"target={self.z_target:.3f} | "
                f"err_z={error_z:.3f} | "
                f"PWM={pwm_common:.1f} | "
                f"dPWM={delta_pwm:.1f} | "
                f"F_total={sum(thrusts):.3f} | "
                f"I={[round(i, 2) for i in currents]} | "
                f"RPM={[round(r, 0) for r in rpms]}"
            )