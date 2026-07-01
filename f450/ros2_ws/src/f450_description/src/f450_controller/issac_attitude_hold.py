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
from f450_controller.tracking_logger import TrackingLogger
from f450_controller.yaw_hold import YawHoldPID


class F450AttitudeHold(AttitudeHoldCompatibilityMixin):
    ########## INIT F450 ATTITUDE HOLD NODE ##########
    # Tao tat ca controller con, mixer, motor model, spinner canh quat va cac
    # bien trang thai de dieu khien F450 trong Isaac Sim.
    def __init__(
        self,
        base_link_path="/f450_simple/base_link",
        x_target=None,
        y_target=None,
        z_target=1.50,
        pwm_hover=1650.0,
        arm_xy=0.159,
        motor_z=0.04,
    ):
        # Duong dan rigid body chinh cua drone trong stage Isaac Sim.
        self.base_link_path = base_link_path

        # Cac vong dieu khien rieng: do cao, roll/pitch, yaw va vi tri XY.
        self.altitude_controller = AltitudeHoldPID(
            z_target=z_target,
            pwm_hover=pwm_hover,
        )
        self.attitude_controller = AttitudeHoldPID()
        self.yaw_controller = YawHoldPID()
        self.position_controller = PositionHoldPID(
            x_target=0.0 if x_target is None else x_target,
            y_target=0.0 if y_target is None else y_target,
        )
        self._auto_set_x_target = x_target is None
        self._auto_set_y_target = y_target is None
        self.mixer = QuadXPwmMixer()
        self.propeller_spinner = PhysicalPropellerSpinner()

        # Hinh hoc khung F450 va vi tri gan luc day cua 4 motor.
        self.arm_xy = arm_xy
        self.motor_z = motor_z
        self.motor_positions = build_motor_positions(arm_xy, motor_z)

        # Bon mo hinh motor doc lap, moi motor nhan mot lenh PWM rieng.
        self.motors = [
            MotorModel(),
            MotorModel(),
            MotorModel(),
            MotorModel(),
        ]

        # Lenh PWM hien tai, khoi tao bang PWM hover.
        self.pwm_commands = [
            self.pwm_hover,
            self.pwm_hover,
            self.pwm_hover,
            self.pwm_hover,
        ]

        # Interface voi Isaac Sim: dynamic_control de doc/ghi body, timeline de play.
        self.dc = _dynamic_control.acquire_dynamic_control_interface()
        self.timeline = omni.timeline.get_timeline_interface()

        # Trang thai runtime: subscription physics, dong ho mo phong, debug va logger.
        self.physics_subscription = None
        self.sim_time = 0.0
        self.last_print_time = 0.0
        self.tracking_logger = None

    ########## START PHYSICS CONTROL LOOP ##########
    # Dang ky callback physics_step, chay timeline va in cac tham so dieu khien
    # ban dau de de kiem tra khi bat controller.
    def start(self):
        self._unsubscribe_physics()

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
        print("Yaw PID:", self.kp_yaw, self.ki_yaw, self.kd_yaw)

    ########## UNSUBSCRIBE PHYSICS CALLBACK ##########
    # Huy subscription cu neu co, tranh viec mot controller duoc goi nhieu lan
    # moi physics step.
    def _unsubscribe_physics(self):
        if self.physics_subscription is not None:
            try:
                self.physics_subscription.unsubscribe()
            except Exception:
                pass

        self.physics_subscription = None

    ########## STOP CONTROLLER ##########
    # Dung callback physics va dong tracking log neu dang ghi.
    def stop(self):
        self._unsubscribe_physics()
        self.stop_tracking_log()

    ########## SET ALTITUDE TARGET ##########
    # Doi target do cao z va de altitude_controller reset bo nho tich phan.
    def set_target(self, z_target):
        self.altitude_controller.set_target(z_target)
        print("Updated z_target:", self.z_target)

    ########## SET XY POSITION TARGET ##########
    # Cap nhat target x/y; neu nguoi dung dat thu cong thi tat co che auto lay
    # vi tri hien tai lam target ban dau.
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

    ########## SET XYZ TARGET ##########
    # Cap nhat dong thoi target vi tri XY va do cao Z neu co tham so duoc truyen.
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

    ########## SET POSITION PID PARAMS ##########
    # Thay doi he so PID giu vi tri cho truc x/y va in lai gia tri moi.
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

    ########## SET ALTITUDE PID PARAMS ##########
    # Thay doi he so PID giu do cao z va in lai gia tri moi.
    def set_altitude_pid(self, kp_z=None, kd_z=None, ki_z=None):
        self.altitude_controller.set_pid(kp_z=kp_z, kd_z=kd_z, ki_z=ki_z)
        print(
            "Updated altitude PID:",
            "kp_z =", self.kp_z,
            "kd_z =", self.kd_z,
            "ki_z =", self.ki_z,
        )

    ########## SET ATTITUDE PID PARAMS ##########
    # Thay doi he so PID giu roll/pitch va in lai gia tri moi.
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

    ########## SET YAW PID PARAMS ##########
    # Thay doi he so PID giu yaw va in lai gia tri moi.
    def set_yaw_pid(self, kp_yaw=None, ki_yaw=None, kd_yaw=None):
        self.yaw_controller.set_pid(
            kp_yaw=kp_yaw,
            ki_yaw=ki_yaw,
            kd_yaw=kd_yaw,
        )
        print(
            "Updated yaw PID:",
            "kp_yaw =", self.kp_yaw,
            "ki_yaw =", self.ki_yaw,
            "kd_yaw =", self.kd_yaw,
        )

    ########## SET YAW TARGET ##########
    # Cap nhat huong yaw muc tieu cua drone.
    def set_yaw_target(self, yaw_target):
        self.yaw_controller.set_target(yaw_target)
        print("Updated yaw_target:", self.yaw_target)

    ########## SET HOVER PWM ##########
    # Cap nhat PWM hover dung lam diem can bang luc nang.
    def set_pwm_hover(self, pwm_hover):
        self.altitude_controller.set_pwm_hover(pwm_hover)
        print("Updated pwm_hover:", self.pwm_hover)

    ########## RESET ALTITUDE INTEGRAL ##########
    # Xoa rieng tich phan cua altitude controller.
    def reset_integral(self):
        self.altitude_controller.reset_integral()
        print("Reset altitude integral")

    ########## RESET ATTITUDE INTEGRAL ##########
    # Xoa tich phan cua roll/pitch controller.
    def reset_attitude_integral(self):
        self.attitude_controller.reset_integral()
        print("Reset attitude integral")

    ########## RESET YAW INTEGRAL ##########
    # Xoa tich phan cua yaw controller.
    def reset_yaw_integral(self):
        self.yaw_controller.reset_integral()
        print("Reset yaw integral")

    ########## RESET POSITION INTEGRAL ##########
    # Xoa tich phan cua position controller.
    def reset_position_integral(self):
        self.position_controller.reset_integral()
        print("Reset position integral")

    ########## START TRACKING LOG ##########
    # Mo file CSV de ghi trang thai va target theo chu ky sample_period.
    def start_tracking_log(self, csv_path="/tmp/f450_tracking.csv", sample_period=0.02):
        self.stop_tracking_log()
        self.tracking_logger = TrackingLogger(csv_path, sample_period=sample_period)
        self.tracking_logger.start()
        print("Started tracking log:", self.tracking_logger.csv_path)

    ########## STOP TRACKING LOG ##########
    # Dong logger CSV hien tai neu dang bat.
    def stop_tracking_log(self):
        if self.tracking_logger is None:
            return

        csv_path = self.tracking_logger.csv_path
        self.tracking_logger.stop()
        self.tracking_logger = None
        print("Stopped tracking log:", csv_path)

    ########## COMPUTE POSITION ATTITUDE TARGET ##########
    # Wrapper goi position_controller de doi sai so XY thanh roll/pitch target.
    def compute_position_attitude_target(self, x, y, vx, vy, yaw, dt):
        return self.position_controller.compute_attitude_target(
            x,
            y,
            vx,
            vy,
            yaw,
            dt,
        )

    ########## COMPUTE ALTITUDE PWM BASE ##########
    # Wrapper goi altitude_controller de tinh PWM nen tu do cao va van toc doc.
    def compute_altitude_pwm_base(self, z, vz, dt):
        return self.altitude_controller.compute_pwm_base(z, vz, dt)

    ########## COMPUTE ATTITUDE CORRECTION ##########
    # Wrapper goi attitude_controller de tinh hieu chinh roll/pitch.
    def compute_attitude_correction(self, roll, pitch, ang_vel, dt):
        return self.attitude_controller.compute_correction(roll, pitch, ang_vel, dt)

    ########## COMPUTE YAW CORRECTION ##########
    # Wrapper goi yaw_controller de tinh hieu chinh yaw.
    def compute_yaw_correction(self, yaw, yaw_rate, dt):
        return self.yaw_controller.compute_correction(yaw, yaw_rate, dt)

    ########## MIX PWM ##########
    # Wrapper goi mixer de tron PWM nen va cac correction thanh 4 lenh motor.
    def mix_pwm(self, pwm_base, roll_corr, pitch_corr, yaw_corr=0.0):
        return self.mixer.mix(pwm_base, roll_corr, pitch_corr, yaw_corr)

    ########## INIT PROPELLER DOFS ##########
    # Tim va cau hinh DOF cac canh quat vat ly trong articulation.
    def init_propeller_dofs(self):
        self.propeller_spinner.init_dofs(self.dc, self.base_link_path)

    ########## SPIN PHYSICAL PROPELLERS ##########
    # Cap nhat toc do quay hinh hoc cua canh quat dua tren RPM tu motor model.
    def spin_physical_propellers(self, rpms):
        self.propeller_spinner.spin(
            self.dc,
            self.base_link_path,
            rpms,
            self.sim_time,
        )

    ########## FORMAT XY ERROR ##########
    # Dinh dang sai so XY cho dong debug; tra ve "off" khi position hold tat.
    def _format_xy_error(self, position_debug):
        if position_debug is None:
            return "off"

        return (
            f"({position_debug['error_x']:.3f},"
            f"{position_debug['error_y']:.3f})"
        )

    ########## AUTO SET INITIAL XY TARGET ##########
    # Neu nguoi dung khong dat x/y target, lay vi tri hien tai cua drone lam
    # target giu vi tri ban dau trong physics step dau tien.
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

    ########## APPLY YAW REACTION TORQUE ##########
    # Doi tong torque yaw cua canh quat thanh cap luc ngang dat doi xung len body
    # de tao moment quanh truc z.
    def apply_yaw_reaction_torque(self, body_handle, torque_z):
        if abs(torque_z) < 1e-9:
            return

        force_y = torque_z / (2.0 * max(self.arm_xy, 1e-6))

        self.dc.apply_body_force(
            body_handle,
            carb.Float3(0.0, force_y, 0.0),
            carb.Float3(self.arm_xy, 0.0, 0.0),
            False,
        )
        self.dc.apply_body_force(
            body_handle,
            carb.Float3(0.0, -force_y, 0.0),
            carb.Float3(-self.arm_xy, 0.0, 0.0),
            False,
        )

    ########## PHYSICS STEP CONTROL LOOP ##########
    # Callback chay moi buoc physics: doc pose/velocity, tinh PID, mix PWM, cap
    # nhat motor model, ap luc len rigid body, quay canh quat va ghi log/debug.
    def on_physics_step(self, dt):
        self.sim_time += dt

        body_handle = self.dc.get_rigid_body(self.base_link_path)

        if body_handle == _dynamic_control.INVALID_HANDLE:
            carb.log_error(f"Cannot find rigid body: {self.base_link_path}")
            return

        ########## READ DRONE STATE ##########
        # Lay pose, van toc thang/goc va doi quaternion thanh roll/pitch/yaw.
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

        ########## POSITION OUTER LOOP ##########
        # Neu bat position hold, bo PID XY se tao roll/pitch target cho vong
        # attitude ben trong.
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

        ########## ALTITUDE OUTER LOOP ##########
        # Tinh PWM nen de giu do cao z.
        pwm_base, error_z, error_vz, delta_pwm_z = self.compute_altitude_pwm_base(
            z,
            vz,
            dt,
        )

        yaw_corr = 0.0
        error_yaw = 0.0

        ########## YAW HOLD LOOP ##########
        # Tinh hieu chinh yaw neu yaw hold dang bat.
        if self.enable_yaw_hold:
            yaw_corr, error_yaw = self.compute_yaw_correction(
                yaw,
                ang_vel.z,
                dt,
            )

        ########## ATTITUDE INNER LOOP ##########
        # Tinh hieu chinh roll/pitch tu goc hien tai va target da duoc dat.
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
            yaw_corr,
        )

        ########## MOTOR MODEL AND BODY FORCES ##########
        # Cap nhat 4 motor tu PWM, lay luc day/RPM/torque va ap luc len base_link.
        thrusts = []
        currents = []
        rpms = []
        reaction_torques = []

        for i in range(4):
            thrust, current, rpm = self.motors[i].update(
                self.pwm_commands[i],
                dt,
            )

            thrusts.append(thrust)
            currents.append(current)
            rpms.append(rpm)
            reaction_torques.append(self.motors[i].reaction_torque)

            self.dc.apply_body_force(
                body_handle,
                carb.Float3(0.0, 0.0, thrust),
                self.motor_positions[i],
                False,
            )

        ########## YAW REACTION AND PROPELLER VISUALS ##########
        # Cong torque phan luc cua cac canh quat, ap moment yaw len body va quay
        # joint canh quat vat ly neu co.
        body_yaw_torque = 0.0
        for direction, reaction_torque in zip(self.motor_directions, reaction_torques):
            body_yaw_torque += -direction * reaction_torque

        self.apply_yaw_reaction_torque(body_handle, body_yaw_torque)
        self.spin_physical_propellers(rpms)

        ########## TRACKING LOG SAMPLE ##########
        # Ghi mau tracking de ve/phan tich duong bay neu logger dang bat.
        if self.tracking_logger is not None:
            self.tracking_logger.log(
                self.sim_time,
                x,
                y,
                z,
                roll,
                pitch,
                yaw,
                self.x_target,
                self.y_target,
                self.z_target,
                self.roll_target,
                self.pitch_target,
                self.yaw_target,
            )

        ########## PERIODIC DEBUG PRINT ##########
        # In thong tin dieu khien moi 0.5s de theo doi loi, target, PWM va RPM.
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
                f"yaw={math.degrees(yaw):.2f}deg | "
                f"yCorr={yaw_corr:.1f} | "
                f"Mz={body_yaw_torque:.4f}Nm | "
                f"Iroll={self.integral_roll:.3f} | "
                f"Ipitch={self.integral_pitch:.3f} | "
                f"rCorr={roll_corr:.1f} | "
                f"pCorr={pitch_corr:.1f} | "
                f"PWM={[round(p, 1) for p in self.pwm_commands]} | "
                f"F_total={sum(thrusts):.3f} | "
                f"RPM={[round(r, 0) for r in rpms]}"
            )
