import math

from f450_controller.control_utils import PWM_MAX, PWM_MIN, clamp


class AttitudeHoldCompatibilityMixin:
    @property
    def enable_position_hold(self):
        return self.position_controller.enabled

    @enable_position_hold.setter
    def enable_position_hold(self, value):
        self.position_controller.enabled = bool(value)

    @property
    def x_target(self):
        return self.position_controller.x_target

    @x_target.setter
    def x_target(self, value):
        if hasattr(self, "_auto_set_x_target"):
            self._auto_set_x_target = False
        self.position_controller.x_target = float(value)

    @property
    def y_target(self):
        return self.position_controller.y_target

    @y_target.setter
    def y_target(self, value):
        if hasattr(self, "_auto_set_y_target"):
            self._auto_set_y_target = False
        self.position_controller.y_target = float(value)

    @property
    def vx_target(self):
        return self.position_controller.vx_target

    @vx_target.setter
    def vx_target(self, value):
        self.position_controller.vx_target = float(value)

    @property
    def vy_target(self):
        return self.position_controller.vy_target

    @vy_target.setter
    def vy_target(self, value):
        self.position_controller.vy_target = float(value)

    @property
    def kp_x(self):
        return self.position_controller.kp_x

    @kp_x.setter
    def kp_x(self, value):
        self.position_controller.kp_x = float(value)

    @property
    def kd_x(self):
        return self.position_controller.kd_x

    @kd_x.setter
    def kd_x(self, value):
        self.position_controller.kd_x = float(value)

    @property
    def ki_x(self):
        return self.position_controller.ki_x

    @ki_x.setter
    def ki_x(self, value):
        self.position_controller.ki_x = float(value)

    @property
    def kp_y(self):
        return self.position_controller.kp_y

    @kp_y.setter
    def kp_y(self, value):
        self.position_controller.kp_y = float(value)

    @property
    def kd_y(self):
        return self.position_controller.kd_y

    @kd_y.setter
    def kd_y(self, value):
        self.position_controller.kd_y = float(value)

    @property
    def ki_y(self):
        return self.position_controller.ki_y

    @ki_y.setter
    def ki_y(self, value):
        self.position_controller.ki_y = float(value)

    @property
    def integral_x(self):
        return self.position_controller.integral_x

    @integral_x.setter
    def integral_x(self, value):
        self.position_controller.integral_x = float(value)

    @property
    def integral_y(self):
        return self.position_controller.integral_y

    @integral_y.setter
    def integral_y(self, value):
        self.position_controller.integral_y = float(value)

    @property
    def position_integral_limit(self):
        return self.position_controller.integral_limit

    @position_integral_limit.setter
    def position_integral_limit(self, value):
        self.position_controller.integral_limit = float(value)

    @property
    def position_accel_limit(self):
        return self.position_controller.accel_limit

    @position_accel_limit.setter
    def position_accel_limit(self, value):
        self.position_controller.accel_limit = float(value)

    @property
    def position_angle_limit_deg(self):
        return math.degrees(self.position_controller.angle_limit)

    @position_angle_limit_deg.setter
    def position_angle_limit_deg(self, value):
        self.position_controller.angle_limit = math.radians(float(value))

    @property
    def z_target(self):
        return self.altitude_controller.z_target

    @z_target.setter
    def z_target(self, value):
        self.altitude_controller.z_target = float(value)

    @property
    def vz_target(self):
        return self.altitude_controller.vz_target

    @vz_target.setter
    def vz_target(self, value):
        self.altitude_controller.vz_target = float(value)

    @property
    def pwm_hover(self):
        return self.altitude_controller.pwm_hover

    @pwm_hover.setter
    def pwm_hover(self, value):
        self.altitude_controller.pwm_hover = clamp(float(value), PWM_MIN, PWM_MAX)

    @property
    def kp_z(self):
        return self.altitude_controller.kp_z

    @kp_z.setter
    def kp_z(self, value):
        self.altitude_controller.kp_z = float(value)

    @property
    def kd_z(self):
        return self.altitude_controller.kd_z

    @kd_z.setter
    def kd_z(self, value):
        self.altitude_controller.kd_z = float(value)

    @property
    def ki_z(self):
        return self.altitude_controller.ki_z

    @ki_z.setter
    def ki_z(self, value):
        self.altitude_controller.ki_z = float(value)

    @property
    def integral_z(self):
        return self.altitude_controller.integral_z

    @integral_z.setter
    def integral_z(self, value):
        self.altitude_controller.integral_z = float(value)

    @property
    def integral_limit(self):
        return self.altitude_controller.integral_limit

    @integral_limit.setter
    def integral_limit(self, value):
        self.altitude_controller.integral_limit = float(value)

    @property
    def roll_target(self):
        return self.attitude_controller.roll_target

    @roll_target.setter
    def roll_target(self, value):
        self.attitude_controller.roll_target = float(value)

    @property
    def pitch_target(self):
        return self.attitude_controller.pitch_target

    @pitch_target.setter
    def pitch_target(self, value):
        self.attitude_controller.pitch_target = float(value)

    @property
    def kp_roll(self):
        return self.attitude_controller.kp_roll

    @kp_roll.setter
    def kp_roll(self, value):
        self.attitude_controller.kp_roll = float(value)

    @property
    def ki_roll(self):
        return self.attitude_controller.ki_roll

    @ki_roll.setter
    def ki_roll(self, value):
        self.attitude_controller.ki_roll = float(value)

    @property
    def kd_roll(self):
        return self.attitude_controller.kd_roll

    @kd_roll.setter
    def kd_roll(self, value):
        self.attitude_controller.kd_roll = float(value)

    @property
    def kp_pitch(self):
        return self.attitude_controller.kp_pitch

    @kp_pitch.setter
    def kp_pitch(self, value):
        self.attitude_controller.kp_pitch = float(value)

    @property
    def ki_pitch(self):
        return self.attitude_controller.ki_pitch

    @ki_pitch.setter
    def ki_pitch(self, value):
        self.attitude_controller.ki_pitch = float(value)

    @property
    def kd_pitch(self):
        return self.attitude_controller.kd_pitch

    @kd_pitch.setter
    def kd_pitch(self, value):
        self.attitude_controller.kd_pitch = float(value)

    @property
    def integral_roll(self):
        return self.attitude_controller.integral_roll

    @integral_roll.setter
    def integral_roll(self, value):
        self.attitude_controller.integral_roll = float(value)

    @property
    def integral_pitch(self):
        return self.attitude_controller.integral_pitch

    @integral_pitch.setter
    def integral_pitch(self, value):
        self.attitude_controller.integral_pitch = float(value)

    @property
    def attitude_integral_limit(self):
        return self.attitude_controller.integral_limit

    @attitude_integral_limit.setter
    def attitude_integral_limit(self, value):
        self.attitude_controller.integral_limit = float(value)

    @property
    def attitude_pwm_limit(self):
        return self.attitude_controller.pwm_limit

    @attitude_pwm_limit.setter
    def attitude_pwm_limit(self, value):
        self.attitude_controller.pwm_limit = float(value)

    @property
    def enable_test_disturbance(self):
        return self.disturbance.enabled

    @enable_test_disturbance.setter
    def enable_test_disturbance(self, value):
        self.disturbance.enabled = bool(value)

    @property
    def disturbance_start(self):
        return self.disturbance.start_time

    @disturbance_start.setter
    def disturbance_start(self, value):
        self.disturbance.start_time = float(value)

    @property
    def disturbance_duration(self):
        return self.disturbance.duration

    @disturbance_duration.setter
    def disturbance_duration(self, value):
        self.disturbance.duration = float(value)

    @property
    def disturbance_force_y(self):
        return self.disturbance.force_y

    @disturbance_force_y.setter
    def disturbance_force_y(self, value):
        self.disturbance.force_y = float(value)

    @property
    def disturbance_z_offset(self):
        return self.disturbance.z_offset

    @disturbance_z_offset.setter
    def disturbance_z_offset(self, value):
        self.disturbance.z_offset = float(value)

    @property
    def enable_physical_propeller_spin(self):
        return self.propeller_spinner.enabled

    @enable_physical_propeller_spin.setter
    def enable_physical_propeller_spin(self, value):
        self.propeller_spinner.enabled = bool(value)

    @property
    def articulation_path(self):
        return self.propeller_spinner.articulation_path

    @articulation_path.setter
    def articulation_path(self, value):
        self.propeller_spinner.articulation_path = value

    @property
    def propeller_joint_names(self):
        return self.propeller_spinner.joint_names

    @propeller_joint_names.setter
    def propeller_joint_names(self, value):
        self.propeller_spinner.joint_names = list(value)

    @property
    def motor_directions(self):
        return self.propeller_spinner.motor_directions

    @motor_directions.setter
    def motor_directions(self, value):
        self.propeller_spinner.motor_directions = list(value)

    @property
    def propeller_speed_scale(self):
        return self.propeller_spinner.speed_scale

    @propeller_speed_scale.setter
    def propeller_speed_scale(self, value):
        self.propeller_spinner.speed_scale = float(value)

    @property
    def articulation_handle(self):
        return self.propeller_spinner.articulation_handle

    @property
    def propeller_dof_handles(self):
        return self.propeller_spinner.dof_handles

    @property
    def propeller_dofs_initialized(self):
        return self.propeller_spinner.initialized
