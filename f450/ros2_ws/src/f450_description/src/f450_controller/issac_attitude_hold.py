import math

import carb
import omni
import omni.physx
import omni.timeline

from omni.isaac.dynamic_control import _dynamic_control

from f450_controller.altitude_hold import AltitudeHoldPID
from f450_controller.attitude_hold_compat import AttitudeHoldCompatibilityMixin
from f450_controller.attitude_pid import AttitudeHoldPID
from f450_controller.control_utils import quat_to_euler
from f450_controller.motor_mixer import QuadXPwmMixer, build_motor_positions
from f450_controller.motor_model import MotorModel
from f450_controller.position_hold import PositionHoldPID
from f450_controller.propeller_spinner import PhysicalPropellerSpinner
from f450_controller.disturbance import TestDisturbance


class F450AttitudeHold(AttitudeHoldCompatibilityMixin):
    def __init__(
        self,
        base_link_path="/f450_simple/base_link",
        x_target=None,
        y_target=None,
        z_target=3.0,
        pwm_hover=1568.0,
        arm_xy=0.159,
        motor_z=0.04,
    ):
        self.base_link_path = base_link_path

        self.altitude_controller = AltitudeHoldPID(
            z_target=z_target,
            pwm_hover=pwm_hover,
        )
        self.attitude_controller = AttitudeHoldPID()
        self.position_controller = PositionHoldPID(
            x_target=0.0 if x_target is None else x_target,
            y_target=0.0 if y_target is None else y_target,
        )
        self._auto_set_x_target = x_target is None
        self._auto_set_y_target = y_target is None
        self.mixer = QuadXPwmMixer()
        self.disturbance = TestDisturbance()
        self.propeller_spinner = PhysicalPropellerSpinner()

        self.arm_xy = arm_xy
        self.motor_z = motor_z
        self.motor_positions = build_motor_positions(arm_xy, motor_z)

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

        print("F450 attitude hold started")
        print("base_link_path =", self.base_link_path)
        print("x_target =", "current" if self._auto_set_x_target else self.x_target)
        print("y_target =", "current" if self._auto_set_y_target else self.y_target)
        print("z_target =", self.z_target)
        print("pwm_hover =", self.pwm_hover)
        print(
            "Position PID:",
            "x =",
            (self.kp_x, self.kd_x, self.ki_x),
            "y =",
            (self.kp_y, self.kd_y, self.ki_y),
        )
        print("Altitude PID:", self.kp_z, self.kd_z, self.ki_z)
        print("Roll/Pitch PD:", self.kp_roll, self.kd_roll, self.kp_pitch, self.kd_pitch)

    def stop(self):
        if self.physics_subscription is not None:
            try:
                self.physics_subscription.unsubscribe()
            except Exception:
                pass

        self.physics_subscription = None

    def set_target(self, z_target):
        self.altitude_controller.set_target(z_target)
        print("Updated z_target:", self.z_target)

    def set_position_target(self, x_target=None, y_target=None):
        if x_target is not None:
            self._auto_set_x_target = False
        if y_target is not None:
            self._auto_set_y_target = False

        self.position_controller.set_target(
            x_target=x_target,
            y_target=y_target,
        )
        print("Updated position target:", "x =", self.x_target, "y =", self.y_target)

    def set_xyz_target(self, x_target=None, y_target=None, z_target=None):
        if x_target is not None or y_target is not None:
            if x_target is not None:
                self._auto_set_x_target = False
            if y_target is not None:
                self._auto_set_y_target = False

            self.position_controller.set_target(
                x_target=x_target,
                y_target=y_target,
            )
        if z_target is not None:
            self.altitude_controller.set_target(z_target)

        print(
            "Updated XYZ target:",
            "x =", self.x_target,
            "y =", self.y_target,
            "z =", self.z_target,
        )

    def set_position_pid(
        self,
        kp_x=None,
        kd_x=None,
        ki_x=None,
        kp_y=None,
        kd_y=None,
        ki_y=None,
    ):
        self.position_controller.set_pid(
            kp_x=kp_x,
            kd_x=kd_x,
            ki_x=ki_x,
            kp_y=kp_y,
            kd_y=kd_y,
            ki_y=ki_y,
        )
        print(
            "Updated position PID:",
            "kp_x =", self.kp_x,
            "kd_x =", self.kd_x,
            "ki_x =", self.ki_x,
            "kp_y =", self.kp_y,
            "kd_y =", self.kd_y,
            "ki_y =", self.ki_y,
        )

    def set_altitude_pid(self, kp_z=None, kd_z=None, ki_z=None):
        self.altitude_controller.set_pid(kp_z=kp_z, kd_z=kd_z, ki_z=ki_z)
        print(
            "Updated altitude PID:",
            "kp_z =", self.kp_z,
            "kd_z =", self.kd_z,
            "ki_z =", self.ki_z,
        )

    def set_attitude_pid(
        self,
        kp_roll=None,
        ki_roll=None,
        kd_roll=None,
        kp_pitch=None,
        ki_pitch=None,
        kd_pitch=None,
    ):
        self.attitude_controller.set_pid(
            kp_roll=kp_roll,
            ki_roll=ki_roll,
            kd_roll=kd_roll,
            kp_pitch=kp_pitch,
            ki_pitch=ki_pitch,
            kd_pitch=kd_pitch,
        )
        print(
            "Updated attitude PID:",
            "kp_roll =", self.kp_roll,
            "ki_roll =", self.ki_roll,
            "kd_roll =", self.kd_roll,
            "kp_pitch =", self.kp_pitch,
            "ki_pitch =", self.ki_pitch,
            "kd_pitch =", self.kd_pitch,
        )

    def set_pwm_hover(self, pwm_hover):
        self.altitude_controller.set_pwm_hover(pwm_hover)
        print("Updated pwm_hover:", self.pwm_hover)

    def reset_integral(self):
        self.altitude_controller.reset_integral()
        print("Reset altitude integral")

    def reset_attitude_integral(self):
        self.attitude_controller.reset_integral()
        print("Reset attitude integral")

    def reset_position_integral(self):
        self.position_controller.reset_integral()
        print("Reset position integral")

    def compute_position_attitude_target(self, x, y, vx, vy, yaw, dt):
        return self.position_controller.compute_attitude_target(
            x,
            y,
            vx,
            vy,
            yaw,
            dt,
        )

    def compute_altitude_pwm_base(self, z, vz, dt):
        return self.altitude_controller.compute_pwm_base(z, vz, dt)

    def compute_attitude_correction(self, roll, pitch, ang_vel, dt):
        return self.attitude_controller.compute_correction(roll, pitch, ang_vel, dt)

    def mix_pwm(self, pwm_base, roll_corr, pitch_corr):
        return self.mixer.mix(pwm_base, roll_corr, pitch_corr)

    def apply_test_disturbance(self, body_handle):
        self.disturbance.apply(self.dc, body_handle, self.sim_time)

    def init_propeller_dofs(self):
        self.propeller_spinner.init_dofs(self.dc, self.base_link_path)

    def spin_physical_propellers(self, rpms):
        self.propeller_spinner.spin(
            self.dc,
            self.base_link_path,
            rpms,
            self.sim_time,
        )

    def _format_xy_error(self, position_debug):
        if position_debug is None:
            return "off"

        return (
            f"({position_debug['error_x']:.3f},"
            f"{position_debug['error_y']:.3f})"
        )

    def _set_initial_xy_target_if_needed(self, x, y):
        if not (self._auto_set_x_target or self._auto_set_y_target):
            return

        self.position_controller.set_target(
            x_target=x if self._auto_set_x_target else None,
            y_target=y if self._auto_set_y_target else None,
        )
        self._auto_set_x_target = False
        self._auto_set_y_target = False

        print("Auto XY target:", "x =", self.x_target, "y =", self.y_target)

    def on_physics_step(self, dt):
        self.sim_time += dt

        body_handle = self.dc.get_rigid_body(self.base_link_path)

        if body_handle == _dynamic_control.INVALID_HANDLE:
            carb.log_error(f"Cannot find rigid body: {self.base_link_path}")
            return

        self.apply_test_disturbance(body_handle)

        pose = self.dc.get_rigid_body_pose(body_handle)
        lin_vel = self.dc.get_rigid_body_linear_velocity(body_handle)
        ang_vel = self.dc.get_rigid_body_angular_velocity(body_handle)

        z = pose.p.z
        x = pose.p.x
        y = pose.p.y
        vz = lin_vel.z
        vx = lin_vel.x
        vy = lin_vel.y
        roll, pitch, yaw = quat_to_euler(pose.r)

        position_debug = None

        self._set_initial_xy_target_if_needed(x, y)

        if self.enable_position_hold:
            position_debug = self.compute_position_attitude_target(
                x,
                y,
                vx,
                vy,
                yaw,
                dt,
            )
            self.roll_target = position_debug["roll_target"]
            self.pitch_target = position_debug["pitch_target"]

        pwm_base, error_z, error_vz, delta_pwm_z = self.compute_altitude_pwm_base(
            z,
            vz,
            dt,
        )

        roll_corr, pitch_corr, error_roll, error_pitch = self.compute_attitude_correction(
            roll,
            pitch,
            ang_vel,
            dt,
        )

        self.pwm_commands = self.mix_pwm(
            pwm_base,
            roll_corr,
            pitch_corr,
        )

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

        self.spin_physical_propellers(rpms)

        if self.sim_time - self.last_print_time > 0.5:
            self.last_print_time = self.sim_time

            print(
                f"x={x:.3f} | "
                f"y={y:.3f} | "
                f"z={z:.3f} | "
                f"target_xy=({self.x_target:.2f},{self.y_target:.2f}) | "
                f"vz={vz:.3f} | "
                f"target={self.z_target:.3f} | "
                f"err_z={error_z:.3f} | "
                f"err_xy={self._format_xy_error(position_debug)} | "
                f"rtgt={math.degrees(self.roll_target):.2f}deg | "
                f"ptgt={math.degrees(self.pitch_target):.2f}deg | "
                f"roll={math.degrees(roll):.2f}deg | "
                f"pitch={math.degrees(pitch):.2f}deg | "
                f"Iroll={self.integral_roll:.3f} | "
                f"Ipitch={self.integral_pitch:.3f} | "
                f"rCorr={roll_corr:.1f} | "
                f"pCorr={pitch_corr:.1f} | "
                f"PWM={[round(p, 1) for p in self.pwm_commands]} | "
                f"F_total={sum(thrusts):.3f} | "
                f"RPM={[round(r, 0) for r in rpms]}"
            )
