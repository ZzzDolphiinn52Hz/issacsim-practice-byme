import omni
import omni.timeline
import omni.physx
import carb

from omni.isaac.dynamic_control import _dynamic_control

from f450_controller.motor_model import MotorModel


class F450PWMHover:
    def __init__(
        self,
        base_link_path="/f450_simple/base_link",
        pwm_commands=None,
        arm_xy=0.159,
        motor_z=0.04,
    ):
        self.base_link_path = base_link_path

        if pwm_commands is None:
            pwm_commands = [1550.0, 1550.0, 1550.0, 1550.0]

        self.pwm_commands = pwm_commands

        self.arm_xy = arm_xy
        self.motor_z = motor_z

        self.motor_positions = [
            carb.Float3( arm_xy,  arm_xy, motor_z),
            carb.Float3( arm_xy, -arm_xy, motor_z),
            carb.Float3(-arm_xy, -arm_xy, motor_z),
            carb.Float3(-arm_xy,  arm_xy, motor_z),
        ]

        self.motors = [
            MotorModel(),
            MotorModel(),
            MotorModel(),
            MotorModel(),
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

        print("F450 PWM hover started")
        print("base_link_path =", self.base_link_path)
        print("pwm_commands =", self.pwm_commands)

    def stop(self):
        if self.physics_subscription is not None:
            try:
                self.physics_subscription.unsubscribe()
            except Exception:
                pass

        self.physics_subscription = None

    def set_pwm(self, pwm1, pwm2, pwm3, pwm4):
        self.pwm_commands = [
            float(pwm1),
            float(pwm2),
            float(pwm3),
            float(pwm4),
        ]

        print("Updated PWM:", self.pwm_commands)

    def on_physics_step(self, dt):
        self.sim_time += dt

        body_handle = self.dc.get_rigid_body(self.base_link_path)

        if body_handle == _dynamic_control.INVALID_HANDLE:
            carb.log_error(f"Cannot find rigid body: {self.base_link_path}")
            return

        pose = self.dc.get_rigid_body_pose(body_handle)
        z = pose.p.z

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
                f"PWM={[round(p, 1) for p in self.pwm_commands]} | "
                f"F={[round(f, 3) for f in thrusts]} | "
                f"I={[round(i, 2) for i in currents]} | "
                f"RPM={[round(r, 0) for r in rpms]} | "
                f"F_total={sum(thrusts):.3f}"
            )