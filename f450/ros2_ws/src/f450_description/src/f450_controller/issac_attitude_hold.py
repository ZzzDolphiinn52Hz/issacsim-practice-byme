import math
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


def wrap_angle(angle):
    while angle > math.pi:
        angle -= 2.0 * math.pi
    while angle < -math.pi:
        angle += 2.0 * math.pi
    return angle


def quat_to_euler(q):
    # dynamic_control quaternion thường là x, y, z, w
    x = q.x
    y = q.y
    z = q.z
    w = q.w

    # roll
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = 1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch
    sinp = 2.0 * (w * y - z * x)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    # yaw
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


class F450AttitudeHold:
    def __init__(
        self,
        base_link_path="/f450_simple/base_link",
        z_target=3.0,
        pwm_hover=1568.0,
        arm_xy=0.159,
        motor_z=0.04,
    ):
        self.base_link_path = base_link_path

        # Altitude target
        self.z_target = float(z_target)
        self.vz_target = 0.0
        self.pwm_hover = float(pwm_hover)

        # Altitude PID, dùng lại gain bạn đã tune ổn
        self.kp_z = 180.0
        self.kd_z = 110.0
        self.ki_z = 25.0

        self.integral_z = 0.0
        self.integral_limit = 5.0

        # Attitude target
        self.roll_target = 0.0
        self.pitch_target = 0.0

        # Attitude PID gain, đơn vị gần đúng:
        # Kp: us/rad
        # Ki: us/(rad*s)
        # Kd: us/(rad/s)

        self.kp_roll = 120.0
        self.ki_roll = 35.0
        self.kd_roll = 35.0

        self.kp_pitch = 120.0
        self.ki_pitch = 35.0
        self.kd_pitch = 35.0

        self.integral_roll = 0.0
        self.integral_pitch = 0.0
        self.attitude_integral_limit = 1.0

        # Giới hạn correction attitude để tránh motor lệch quá mạnh
        self.attitude_pwm_limit = 180.0

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

        # disturbance force
        self.enable_test_disturbance = True
        self.disturbance_start = 2.0
        self.disturbance_duration = 0.25

        # Lực nhiễu ngang, Newton
        self.disturbance_force_y = 3.0

        # Điểm đặt lực cao hơn tâm drone để tạo moment
        self.disturbance_z_offset = 0.12

        # =========================
        # Physical propeller joints
        # =========================

        self.enable_physical_propeller_spin = True

        # Articulation root thường là prim robot chính.
        # Nếu path này không đúng, ta sẽ thử base_link_path ở hàm init.
        self.articulation_path = "/f450_simple"

        self.propeller_joint_names = [
            "propeller_1_joint",
            "propeller_2_joint",
            "propeller_3_joint",
            "propeller_4_joint",
        ]

        # Chiều quay giả lập của 4 motor
        self.motor_directions = [
            1.0,
            -1.0,
            1.0,
            -1.0,
        ]

        # Để 1.0 là quay theo RPM thật.
        # Nếu mô phỏng bị nặng/rung, giảm xuống 0.2 hoặc 0.1.
        self.propeller_speed_scale = 0.9

        self.articulation_handle = None
        self.propeller_dof_handles = []
        self.propeller_dofs_initialized = False

    def apply_test_disturbance(self, body_handle):
        if not self.enable_test_disturbance:
            return

        if self.disturbance_start <= self.sim_time <= self.disturbance_start + self.disturbance_duration:
            # Apply lực ngang theo trục Y body frame tại điểm cao hơn tâm drone
            # Việc này tạo moment làm drone bị nghiêng roll.
            self.dc.apply_body_force(
                body_handle,
                carb.Float3(0.0, self.disturbance_force_y, 0.0),
                carb.Float3(0.0, 0.0, self.disturbance_z_offset),
                False,
            )    

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
        print("z_target =", self.z_target)
        print("pwm_hover =", self.pwm_hover)
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
        self.z_target = float(z_target)
        self.integral_z = 0.0
        print("Updated z_target:", self.z_target)

    def set_altitude_pid(self, kp_z=None, kd_z=None, ki_z=None):
        if kp_z is not None:
            self.kp_z = float(kp_z)
        if kd_z is not None:
            self.kd_z = float(kd_z)
        if ki_z is not None:
            self.ki_z = float(ki_z)

        self.integral_z = 0.0

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

        self.reset_attitude_integral()

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
        self.pwm_hover = clamp(float(pwm_hover), PWM_MIN, PWM_MAX)
        self.integral_z = 0.0
        print("Updated pwm_hover:", self.pwm_hover)

    def reset_integral(self):
        self.integral_z = 0.0
        print("Reset altitude integral")

    def compute_altitude_pwm_base(self, z, vz, dt):
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

    def compute_attitude_correction(self, roll, pitch, ang_vel, dt):
        error_roll = wrap_angle(self.roll_target - roll)
        error_pitch = wrap_angle(self.pitch_target - pitch)

        # angular velocity quanh body axes
        p = ang_vel.x
        q = ang_vel.y

        # Integral để bù motor mismatch / bias lâu dài
        self.integral_roll += error_roll * dt
        self.integral_pitch += error_pitch * dt

        self.integral_roll = clamp(
            self.integral_roll,
            -self.attitude_integral_limit,
            self.attitude_integral_limit,
        )

        self.integral_pitch = clamp(
            self.integral_pitch,
            -self.attitude_integral_limit,
            self.attitude_integral_limit,
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

        roll_corr = clamp(
            roll_corr,
            -self.attitude_pwm_limit,
            self.attitude_pwm_limit,
        )

        pitch_corr = clamp(
            pitch_corr,
            -self.attitude_pwm_limit,
            self.attitude_pwm_limit,
        )

        return roll_corr, pitch_corr, error_roll, error_pitch

    def mix_pwm(self, pwm_base, roll_corr, pitch_corr):
        # Motor order:
        # 1 front-left
        # 2 front-right
        # 3 rear-right
        # 4 rear-left
        #
        # Với thrust body-z:
        # roll torque  ~ y * F
        # pitch torque ~ -x * F

        pwm1 = pwm_base + roll_corr - pitch_corr
        pwm2 = pwm_base - roll_corr - pitch_corr
        pwm3 = pwm_base - roll_corr + pitch_corr
        pwm4 = pwm_base + roll_corr + pitch_corr

        return [
            clamp(pwm1, PWM_MIN, PWM_MAX),
            clamp(pwm2, PWM_MIN, PWM_MAX),
            clamp(pwm3, PWM_MIN, PWM_MAX),
            clamp(pwm4, PWM_MIN, PWM_MAX),
        ]

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
        vz = lin_vel.z

        roll, pitch, yaw = quat_to_euler(pose.r)

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
                f"z={z:.3f} | "
                f"vz={vz:.3f} | "
                f"target={self.z_target:.3f} | "
                f"err_z={error_z:.3f} | "
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
            
    def reset_attitude_integral(self):
        self.integral_roll = 0.0
        self.integral_pitch = 0.0
        print("Reset attitude integral")

    def init_propeller_dofs(self):
        if self.propeller_dofs_initialized:
            return

        if not self.enable_physical_propeller_spin:
            return

        self.propeller_dof_handles = []

        # Thử lấy articulation theo robot root trước
        articulation_handle = self.dc.get_articulation(self.articulation_path)

        # Nếu không được, thử theo base_link_path
        if articulation_handle == _dynamic_control.INVALID_HANDLE:
            articulation_handle = self.dc.get_articulation(self.base_link_path)

        if articulation_handle == _dynamic_control.INVALID_HANDLE:
            carb.log_warn(
                f"Cannot find articulation at {self.articulation_path} "
                f"or {self.base_link_path}. Propeller joints will not spin."
            )
            return

        self.articulation_handle = articulation_handle

        for joint_name in self.propeller_joint_names:
            dof_handle = self.dc.find_articulation_dof(
                articulation_handle,
                joint_name,
            )

            if dof_handle == _dynamic_control.INVALID_HANDLE:
                carb.log_warn(f"Cannot find propeller DOF: {joint_name}")
            else:
                print("Found propeller DOF:", joint_name)

                # Cấu hình drive cho joint quay theo velocity target
                try:
                    props = self.dc.get_dof_properties(dof_handle)

                    try:
                        props.drive_mode = _dynamic_control.DriveMode.DRIVE_VEL
                    except Exception:
                        pass

                    if hasattr(props, "stiffness"):
                        props.stiffness = 0.0

                    if hasattr(props, "damping"):
                        props.damping = 1.0

                    if hasattr(props, "max_effort"):
                        props.max_effort = 100.0

                    if hasattr(props, "max_force"):
                        props.max_force = 100.0

                    self.dc.set_dof_properties(dof_handle, props)

                    print("Configured velocity drive for", joint_name)

                except Exception as e:
                    print("Could not configure DOF properties for", joint_name, e)

            self.propeller_dof_handles.append(dof_handle)

        self.propeller_dofs_initialized = True

    def spin_physical_propellers(self, rpms):
        if not self.enable_physical_propeller_spin:
            return

        if not self.propeller_dofs_initialized:
            self.init_propeller_dofs()

        if len(self.propeller_dof_handles) != 4:
            return

        omega_cmds = []

        for i in range(4):
            dof_handle = self.propeller_dof_handles[i]

            if dof_handle == _dynamic_control.INVALID_HANDLE:
                omega_cmds.append(0.0)
                continue

            rpm = rpms[i]

            # RPM -> rad/s
            omega = rpm * 2.0 * math.pi / 60.0

            omega_cmd = (
                self.motor_directions[i]
                * self.propeller_speed_scale
                * omega
            )

            omega_cmds.append(omega_cmd)

            try:
                self.dc.set_dof_velocity_target(dof_handle, omega_cmd)
            except Exception as e:
                try:
                    self.dc.set_dof_velocity(dof_handle, omega_cmd)
                except Exception as e2:
                    pass

        # Debug mỗi 1 giây
        if self.sim_time - getattr(self, "last_prop_debug_time", 0.0) > 1.0:
            self.last_prop_debug_time = self.sim_time
            print(
                "Propeller omega_cmd:",
                [round(w, 2) for w in omega_cmds],
                "RPM:",
                [round(r, 0) for r in rpms],
            )