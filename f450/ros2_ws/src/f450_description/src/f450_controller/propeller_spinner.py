import math

import carb

from omni.isaac.dynamic_control import _dynamic_control


class PhysicalPropellerSpinner:
    ########## INIT PHYSICAL PROPELLER SPINNER ##########
    # Luu cau hinh cac joint canh quat vat ly, chieu quay cua motor va ti le
    # chuyen RPM mo phong thanh van toc joint trong Isaac Sim.
    def __init__(
        self,
        enabled=True,
        articulation_path="/f450_simple/base_link",
        joint_names=None,
        motor_directions=None,
        speed_scale=0.7,
    ):
        # Cau hinh bat/tat va duong dan articulation chua joint canh quat.
        self.enabled = enabled
        self.articulation_path = articulation_path
        # Ten 4 joint canh quat theo thu tu motor.
        self.joint_names = joint_names or [
            "propeller_1_joint",
            "propeller_2_joint",
            "propeller_3_joint",
            "propeller_4_joint",
        ]
        # Chieu quay cua tung motor va ti le hien thi toc do quay.
        self.motor_directions = motor_directions or [1.0, -1.0, 1.0, -1.0]
        self.speed_scale = float(speed_scale)

        # Handle dynamic_control duoc tim trong init_dofs().
        self.articulation_handle = None
        self.dof_handles = []
        self.initialized = False
        self.last_debug_time = 0.0

    ########## INIT PROPELLER DOFS ##########
    # Tim articulation va DOF cua 4 joint canh quat, sau do cau hinh velocity
    # drive de co the dat van toc quay truc tiep.
    def init_dofs(self, dc, base_link_path):
        if self.initialized or not self.enabled:
            return

        self.dof_handles = []

        articulation_handle = dc.get_articulation(self.articulation_path)

        if articulation_handle == _dynamic_control.INVALID_HANDLE:
            articulation_handle = dc.get_articulation(base_link_path)

        if articulation_handle == _dynamic_control.INVALID_HANDLE:
            carb.log_warn(
                f"Cannot find articulation at {self.articulation_path} "
                f"or {base_link_path}. Propeller joints will not spin."
            )
            return

        self.articulation_handle = articulation_handle

        for joint_name in self.joint_names:
            dof_handle = dc.find_articulation_dof(
                articulation_handle,
                joint_name,
            )

            if dof_handle == _dynamic_control.INVALID_HANDLE:
                carb.log_warn(f"Cannot find propeller DOF: {joint_name}")
            else:
                print("Found propeller DOF:", joint_name)
                self._configure_velocity_drive(dc, dof_handle, joint_name)

            self.dof_handles.append(dof_handle)

        self.initialized = True

    ########## SPIN PHYSICAL PROPELLERS ##########
    # Nhan RPM tu motor model, doi sang rad/s co tinh chieu quay, roi dat target
    # velocity cho tung DOF canh quat.
    def spin(self, dc, base_link_path, rpms, sim_time):
        if not self.enabled:
            return

        if not self.initialized:
            self.init_dofs(dc, base_link_path)

        if len(self.dof_handles) != 4:
            return

        omega_cmds = []

        for i in range(4):
            dof_handle = self.dof_handles[i]

            if dof_handle == _dynamic_control.INVALID_HANDLE:
                omega_cmds.append(0.0)
                continue

            omega = rpms[i] * 2.0 * math.pi / 60.0
            omega_cmd = self.motor_directions[i] * self.speed_scale * omega
            omega_cmds.append(omega_cmd)

            try:
                dc.set_dof_velocity_target(dof_handle, omega_cmd)
            except Exception:
                try:
                    dc.set_dof_velocity(dof_handle, omega_cmd)
                except Exception:
                    pass

        if sim_time - self.last_debug_time > 1.0:
            self.last_debug_time = sim_time
            print(
                "Propeller omega_cmd:",
                [round(w, 2) for w in omega_cmds],
                "RPM:",
                [round(r, 0) for r in rpms],
            )

    ########## CONFIGURE VELOCITY DRIVE ##########
    # Dat DOF sang che do dieu khien van toc va cau hinh damping/max effort de
    # joint co the quay theo lenh omega_cmd.
    def _configure_velocity_drive(self, dc, dof_handle, joint_name):
        try:
            props = dc.get_dof_properties(dof_handle)

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

            dc.set_dof_properties(dof_handle, props)
            print("Configured velocity drive for", joint_name)

        except Exception as exc:
            print("Could not configure DOF properties for", joint_name, exc)
