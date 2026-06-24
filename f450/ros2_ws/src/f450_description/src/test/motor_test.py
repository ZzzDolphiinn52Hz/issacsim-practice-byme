import math
import time
import tkinter as tk
from tkinter import ttk


class BatteryModel:
    """
    Simple LiPo battery model.

    Models:
    - SOC decrease by coulomb counting
    - open-circuit voltage depends on SOC
    - voltage sag due to internal resistance
    """

    def __init__(
        self,
        cells=4,
        capacity_ah=5.3,
        soc_init=1.0,
        internal_resistance=0.035,
        v_cell_full=4.2,
        v_cell_empty=3.3,
    ):
        self.cells = cells
        self.capacity_ah = capacity_ah
        self.internal_resistance = internal_resistance

        self.v_cell_full = v_cell_full
        self.v_cell_empty = v_cell_empty

        self.soc = self.clamp(soc_init, 0.0, 1.0)
        self.ah_used = 0.0

        self.v_oc = self.compute_open_circuit_voltage()
        self.v_loaded = self.v_oc

    @staticmethod
    def clamp(x, lo, hi):
        return max(lo, min(x, hi))

    def compute_open_circuit_voltage(self):
        """
        Approximate LiPo open-circuit voltage curve.
        This is intentionally simple, not a precise electrochemical battery model.
        """
        soc = self.clamp(self.soc, 0.0, 1.0)

        # Nonlinear approximation:
        # full cell ≈ 4.2 V
        # nominal area ≈ 3.7–3.8 V
        # near empty ≈ 3.3 V
        v_cell = self.v_cell_empty + (self.v_cell_full - self.v_cell_empty) * (soc ** 0.55)

        return self.cells * v_cell

    def update(self, total_current, dt):
        dt = max(dt, 1e-6)
        total_current = max(0.0, total_current)

        # Coulomb counting
        self.ah_used += total_current * dt / 3600.0

        if self.capacity_ah > 1e-9:
            self.soc = 1.0 - self.ah_used / self.capacity_ah
        else:
            self.soc = 0.0

        self.soc = self.clamp(self.soc, 0.0, 1.0)

        # Open-circuit voltage by SOC
        self.v_oc = self.compute_open_circuit_voltage()

        # Voltage sag
        self.v_loaded = self.v_oc - total_current * self.internal_resistance

        # Prevent unrealistic voltage collapse
        self.v_loaded = max(self.v_loaded, self.cells * 3.0)

        return self.v_loaded

    def reset(self, soc=1.0):
        self.soc = self.clamp(soc, 0.0, 1.0)
        self.ah_used = 0.0
        self.v_oc = self.compute_open_circuit_voltage()
        self.v_loaded = self.v_oc


class MotorPropModel:
    """
    Simplified ESC + BLDC motor + propeller model.

    Input:
        PWM in microseconds.

    Internal state:
        omega: motor angular velocity, rad/s.

    Output:
        thrust, current, torque, RPM.
    """

    def __init__(
        self,
        pwm_min=1100.0,
        pwm_max=1940.0,
        kv=1100.0,
        rm=0.073,
        i0=0.9,
        i_max=30.0,
        j_motor_prop=2.5e-5,
        kf=5.4e-6,
        kq=1.0e-7,
        omega_max=2200.0,
    ):
        self.pwm_min = pwm_min
        self.pwm_max = pwm_max

        self.kv = kv
        self.rm = rm
        self.i0 = i0
        self.i_max = i_max

        self.j_motor_prop = j_motor_prop
        self.kf = kf
        self.kq = kq

        self.omega_max = omega_max
        self.omega = 0.0

        self.update_motor_constants()

    def update_motor_constants(self):
        # Kv: RPM/V
        # Ke and Kt in SI units
        self.ke = 60.0 / (2.0 * math.pi * self.kv)
        self.kt = self.ke

    @staticmethod
    def clamp(x, lo, hi):
        return max(lo, min(x, hi))

    def pwm_to_u(self, pwm):
        pwm = self.clamp(pwm, self.pwm_min, self.pwm_max)
        return (pwm - self.pwm_min) / (self.pwm_max - self.pwm_min)

    def reset(self, rpm=0.0):
        self.omega = max(0.0, rpm * 2.0 * math.pi / 60.0)

    def compute_outputs(self, pwm, vbat):
        u = self.pwm_to_u(pwm)

        # ESC effective motor voltage
        vm = u * vbat

        # Equivalent motor current model
        current = (vm - self.ke * self.omega) / self.rm
        current = self.clamp(current, 0.0, self.i_max)

        # Motor torque
        torque_motor = self.kt * max(current - self.i0, 0.0)

        # Propeller load torque
        torque_load = self.kq * self.omega * self.omega

        # Rotor acceleration
        omega_dot = (torque_motor - torque_load) / self.j_motor_prop

        # Thrust
        thrust = self.kf * self.omega * self.omega

        rpm = self.omega * 60.0 / (2.0 * math.pi)

        electrical_power = vm * current
        mechanical_power = torque_motor * self.omega

        efficiency = 0.0
        if electrical_power > 1e-6:
            efficiency = mechanical_power / electrical_power

        no_load_rpm = self.kv * vm

        return {
            "u": u,
            "vm": vm,
            "current": current,
            "torque_motor": torque_motor,
            "torque_load": torque_load,
            "omega_dot": omega_dot,
            "omega": self.omega,
            "rpm": rpm,
            "thrust": thrust,
            "electrical_power": electrical_power,
            "mechanical_power": mechanical_power,
            "efficiency": efficiency,
            "no_load_rpm": no_load_rpm,
        }

    def update(self, pwm, dt, vbat):
        dt = max(1e-6, dt)

        out = self.compute_outputs(pwm, vbat)

        self.omega += out["omega_dot"] * dt
        self.omega = self.clamp(self.omega, 0.0, self.omega_max)

        return self.compute_outputs(pwm, vbat)


class DroneMotorBatteryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("F450 Motor / ESC / Propeller / Battery Simulator")
        self.root.geometry("980x720")
        self.root.configure(padx=16, pady=16)

        self.motor = MotorPropModel()
        self.battery = BatteryModel(
            cells=4,
            capacity_ah=5.3,
            soc_init=1.0,
            internal_resistance=0.035,
        )

        self.running = False
        self.last_time = time.perf_counter()
        self.sim_time = 0.0

        # Control variables
        self.pwm_var = tk.DoubleVar(value=1550.0)
        self.reset_rpm_var = tk.StringVar(value="0")
        self.reset_soc_var = tk.StringVar(value="100")

        # Drone / motor parameters
        self.mass_var = tk.StringVar(value="1.5")
        self.kv_var = tk.StringVar(value="1100")
        self.rm_var = tk.StringVar(value="0.073")
        self.i0_var = tk.StringVar(value="0.9")
        self.imax_var = tk.StringVar(value="30")
        self.j_var = tk.StringVar(value="2.5e-5")
        self.kf_var = tk.StringVar(value="5.4e-6")
        self.kq_var = tk.StringVar(value="1.0e-7")

        # Battery parameters
        self.cells_var = tk.StringVar(value="4")
        self.capacity_var = tk.StringVar(value="5.3")
        self.r_internal_var = tk.StringVar(value="0.035")
        self.v_cell_full_var = tk.StringVar(value="4.2")
        self.v_cell_empty_var = tk.StringVar(value="3.3")

        # Outputs
        self.out = {}
        output_keys = [
            "u", "vm", "current_per_motor", "total_current",
            "torque_motor", "torque_load", "omega_dot",
            "rpm", "no_load_rpm",
            "thrust_per_motor", "total_thrust",
            "hover_thrust_each", "thrust_ratio",
            "electrical_power_per_motor", "electrical_power_total",
            "mechanical_power_per_motor", "efficiency",
            "battery_soc", "battery_ah_used",
            "battery_v_oc", "battery_v_loaded",
            "estimated_flight_time",
            "sim_time", "status",
        ]
        for key in output_keys:
            self.out[key] = tk.StringVar(value="-")

        self.setup_ui()
        self.loop()

    @staticmethod
    def get_float(var, default):
        try:
            return float(var.get())
        except ValueError:
            return default

    @staticmethod
    def get_int(var, default):
        try:
            return int(float(var.get()))
        except ValueError:
            return default

    def setup_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        title = ttk.Label(
            self.root,
            text="F450 Motor / ESC / Propeller / Battery Dynamic Model",
            font=("Helvetica", 16, "bold"),
        )
        title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        # =========================
        # Input control frame
        # =========================
        input_frame = ttk.LabelFrame(self.root, text="Control", padding=12)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="PWM input (µs)").grid(row=0, column=0, sticky="w")

        pwm_scale = ttk.Scale(
            input_frame,
            from_=1100,
            to=1940,
            variable=self.pwm_var,
            orient="horizontal",
        )
        pwm_scale.grid(row=0, column=1, sticky="ew", padx=10)

        self.pwm_label = ttk.Label(input_frame, width=12)
        self.pwm_label.grid(row=0, column=2, sticky="e")

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=1, column=0, columnspan=3, sticky="w", pady=(12, 0))

        self.run_button = ttk.Button(button_frame, text="Start", command=self.toggle_run)
        self.run_button.pack(side="left")

        ttk.Button(button_frame, text="Reset motor", command=self.reset_motor).pack(side="left", padx=(8, 0))
        ttk.Label(button_frame, text="RPM:").pack(side="left", padx=(8, 4))
        ttk.Entry(button_frame, textvariable=self.reset_rpm_var, width=8).pack(side="left")

        ttk.Button(button_frame, text="Reset battery", command=self.reset_battery).pack(side="left", padx=(18, 0))
        ttk.Label(button_frame, text="SOC %:").pack(side="left", padx=(8, 4))
        ttk.Entry(button_frame, textvariable=self.reset_soc_var, width=8).pack(side="left")

        # =========================
        # Left panel: parameters
        # =========================
        left_frame = ttk.Frame(self.root)
        left_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 8))
        left_frame.columnconfigure(0, weight=1)

        motor_param_frame = ttk.LabelFrame(left_frame, text="Motor / propeller parameters", padding=12)
        motor_param_frame.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        motor_param_frame.columnconfigure(1, weight=1)

        self.add_param(motor_param_frame, 0, "Drone mass (kg)", self.mass_var)
        self.add_param(motor_param_frame, 1, "Motor Kv (RPM/V)", self.kv_var)
        self.add_param(motor_param_frame, 2, "Motor Rm (ohm)", self.rm_var)
        self.add_param(motor_param_frame, 3, "No-load current I0 (A)", self.i0_var)
        self.add_param(motor_param_frame, 4, "Max current clamp / motor (A)", self.imax_var)
        self.add_param(motor_param_frame, 5, "Rotor inertia J", self.j_var)
        self.add_param(motor_param_frame, 6, "Thrust coeff kf", self.kf_var)
        self.add_param(motor_param_frame, 7, "Load torque coeff kq", self.kq_var)

        battery_param_frame = ttk.LabelFrame(left_frame, text="Battery parameters", padding=12)
        battery_param_frame.grid(row=1, column=0, sticky="ew")
        battery_param_frame.columnconfigure(1, weight=1)

        self.add_param(battery_param_frame, 0, "Cells", self.cells_var)
        self.add_param(battery_param_frame, 1, "Capacity (Ah)", self.capacity_var)
        self.add_param(battery_param_frame, 2, "Internal resistance pack (ohm)", self.r_internal_var)
        self.add_param(battery_param_frame, 3, "Full cell voltage", self.v_cell_full_var)
        self.add_param(battery_param_frame, 4, "Empty cell voltage", self.v_cell_empty_var)

        note = ttk.Label(
            left_frame,
            text=(
                "Gợi ý:\n"
                "- Pin không tụt trực tiếp theo RPM, mà tụt theo tổng dòng điện.\n"
                "- RPM cao thường làm dòng cao, nên pin tụt nhanh hơn.\n"
                "- Hover hợp lý khi Total thrust ≈ m·g.\n"
                "- Nếu PWM cao mà vẫn thiếu lực: tăng kf.\n"
                "- Nếu RPM quá cao: tăng kq hoặc giảm omega_max."
            ),
            justify="left",
            foreground="#555555",
        )
        note.grid(row=2, column=0, sticky="w", pady=(12, 0))

        # =========================
        # Right panel: outputs
        # =========================
        output_frame = ttk.LabelFrame(self.root, text="Live outputs", padding=12)
        output_frame.grid(row=2, column=1, sticky="nsew", padx=(8, 0))
        output_frame.columnconfigure(1, weight=1)

        row = 0
        row = self.add_output(output_frame, row, "Throttle ratio u", self.out["u"])
        row = self.add_output(output_frame, row, "Motor voltage Vm", self.out["vm"])
        row = self.add_output(output_frame, row, "Current / motor", self.out["current_per_motor"])
        row = self.add_output(output_frame, row, "Total current 4 motors", self.out["total_current"])

        row = self.add_separator(output_frame, row)

        row = self.add_output(output_frame, row, "Motor torque Te", self.out["torque_motor"])
        row = self.add_output(output_frame, row, "Prop load torque TL", self.out["torque_load"])
        row = self.add_output(output_frame, row, "Omega dot", self.out["omega_dot"])
        row = self.add_output(output_frame, row, "Motor RPM", self.out["rpm"])
        row = self.add_output(output_frame, row, "No-load RPM at Vm", self.out["no_load_rpm"])

        row = self.add_separator(output_frame, row)

        row = self.add_output(output_frame, row, "Thrust / motor", self.out["thrust_per_motor"])
        row = self.add_output(output_frame, row, "Total thrust 4 motors", self.out["total_thrust"])
        row = self.add_output(output_frame, row, "Hover thrust / motor", self.out["hover_thrust_each"])
        row = self.add_output(output_frame, row, "Thrust / weight ratio", self.out["thrust_ratio"])

        row = self.add_separator(output_frame, row)

        row = self.add_output(output_frame, row, "Electrical power / motor", self.out["electrical_power_per_motor"])
        row = self.add_output(output_frame, row, "Electrical power total", self.out["electrical_power_total"])
        row = self.add_output(output_frame, row, "Mechanical power / motor", self.out["mechanical_power_per_motor"])
        row = self.add_output(output_frame, row, "Efficiency estimate", self.out["efficiency"])

        row = self.add_separator(output_frame, row)

        row = self.add_output(output_frame, row, "Battery SOC", self.out["battery_soc"])
        row = self.add_output(output_frame, row, "Battery Ah used", self.out["battery_ah_used"])
        row = self.add_output(output_frame, row, "Battery V open-circuit", self.out["battery_v_oc"])
        row = self.add_output(output_frame, row, "Battery V loaded", self.out["battery_v_loaded"])
        row = self.add_output(output_frame, row, "Estimated flight time", self.out["estimated_flight_time"])
        row = self.add_output(output_frame, row, "Simulation time", self.out["sim_time"])

        row = self.add_separator(output_frame, row)

        ttk.Label(output_frame, text="Status", font=("Helvetica", 10, "bold")).grid(row=row, column=0, sticky="w")
        ttk.Label(
            output_frame,
            textvariable=self.out["status"],
            font=("Helvetica", 10, "bold"),
            foreground="#0052cc",
        ).grid(row=row, column=1, sticky="w")

    def add_param(self, parent, row, label, variable):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=3)
        ttk.Entry(parent, textvariable=variable, width=16).grid(row=row, column=1, sticky="ew", pady=3)

    def add_output(self, parent, row, label, variable):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky="w", pady=2)
        ttk.Label(
            parent,
            textvariable=variable,
            font=("Courier", 10),
            foreground="#0052cc",
        ).grid(row=row, column=1, sticky="w", pady=2)
        return row + 1

    def add_separator(self, parent, row):
        ttk.Separator(parent).grid(row=row, column=0, columnspan=2, sticky="ew", pady=7)
        return row + 1

    def apply_parameters(self):
        # Motor params
        self.motor.kv = self.get_float(self.kv_var, 1100.0)
        self.motor.rm = self.get_float(self.rm_var, 0.073)
        self.motor.i0 = self.get_float(self.i0_var, 0.9)
        self.motor.i_max = self.get_float(self.imax_var, 30.0)
        self.motor.j_motor_prop = self.get_float(self.j_var, 2.5e-5)
        self.motor.kf = self.get_float(self.kf_var, 5.4e-6)
        self.motor.kq = self.get_float(self.kq_var, 1.0e-7)
        self.motor.update_motor_constants()

        # Battery params
        self.battery.cells = max(1, self.get_int(self.cells_var, 4))
        self.battery.capacity_ah = max(0.001, self.get_float(self.capacity_var, 5.3))
        self.battery.internal_resistance = max(0.0, self.get_float(self.r_internal_var, 0.035))
        self.battery.v_cell_full = self.get_float(self.v_cell_full_var, 4.2)
        self.battery.v_cell_empty = self.get_float(self.v_cell_empty_var, 3.3)

        # Recompute voltage after parameter changes
        self.battery.v_oc = self.battery.compute_open_circuit_voltage()
        self.battery.v_loaded = min(self.battery.v_loaded, self.battery.v_oc)
        self.battery.v_loaded = max(self.battery.v_loaded, self.battery.cells * 3.0)

    def toggle_run(self):
        self.running = not self.running
        self.last_time = time.perf_counter()

        if self.running:
            self.run_button.configure(text="Pause")
        else:
            self.run_button.configure(text="Start")

    def reset_motor(self):
        rpm = self.get_float(self.reset_rpm_var, 0.0)
        self.motor.reset(rpm)
        self.sim_time = 0.0
        self.last_time = time.perf_counter()

    def reset_battery(self):
        soc_percent = self.get_float(self.reset_soc_var, 100.0)
        soc = soc_percent / 100.0

        self.apply_parameters()

        self.battery.reset(soc=soc)
        self.sim_time = 0.0
        self.last_time = time.perf_counter()

    def update_labels(self):
        pwm = self.pwm_var.get()
        self.pwm_label.configure(text=f"{pwm:.0f} µs")

    def update_output_text(self, data):
        mass = self.get_float(self.mass_var, 1.5)
        g = 9.81

        thrust_each = data["thrust"]
        total_thrust = 4.0 * thrust_each
        hover_total = mass * g
        hover_each = hover_total / 4.0

        total_current = 4.0 * data["current"]

        thrust_ratio = total_thrust / hover_total if hover_total > 1e-6 else 0.0

        if thrust_ratio < 0.95:
            status = "Thieu luc nang, drone se roi"
        elif thrust_ratio > 1.05:
            status = "Du luc nang, drone se bay len"
        else:
            status = "Gan hover"

        # Estimate remaining flight time at current draw
        if total_current > 1e-6:
            remaining_ah = max(0.0, self.battery.capacity_ah - self.battery.ah_used)
            remaining_hours = remaining_ah / total_current
            remaining_minutes = remaining_hours * 60.0
            flight_time_text = f"{remaining_minutes:.2f} min"
        else:
            flight_time_text = "inf"

        self.out["u"].set(f"{data['u']:.3f} ({data['u'] * 100:.1f}%)")
        self.out["vm"].set(f"{data['vm']:.3f} V")

        self.out["current_per_motor"].set(f"{data['current']:.3f} A")
        self.out["total_current"].set(f"{total_current:.3f} A")

        self.out["torque_motor"].set(f"{data['torque_motor']:.5f} N·m")
        self.out["torque_load"].set(f"{data['torque_load']:.5f} N·m")
        self.out["omega_dot"].set(f"{data['omega_dot']:.2f} rad/s²")

        self.out["rpm"].set(f"{data['rpm']:.0f} RPM")
        self.out["no_load_rpm"].set(f"{data['no_load_rpm']:.0f} RPM")

        self.out["thrust_per_motor"].set(f"{thrust_each:.3f} N")
        self.out["total_thrust"].set(f"{total_thrust:.3f} N")
        self.out["hover_thrust_each"].set(f"{hover_each:.3f} N")
        self.out["thrust_ratio"].set(f"{thrust_ratio:.3f}")

        self.out["electrical_power_per_motor"].set(f"{data['electrical_power']:.2f} W")
        self.out["electrical_power_total"].set(f"{4.0 * data['electrical_power']:.2f} W")
        self.out["mechanical_power_per_motor"].set(f"{data['mechanical_power']:.2f} W")
        self.out["efficiency"].set(f"{data['efficiency'] * 100:.1f} %")

        self.out["battery_soc"].set(f"{self.battery.soc * 100:.2f} %")
        self.out["battery_ah_used"].set(f"{self.battery.ah_used:.4f} Ah")
        self.out["battery_v_oc"].set(f"{self.battery.v_oc:.3f} V")
        self.out["battery_v_loaded"].set(f"{self.battery.v_loaded:.3f} V")
        self.out["estimated_flight_time"].set(flight_time_text)

        self.out["sim_time"].set(f"{self.sim_time:.2f} s")
        self.out["status"].set(status)

    def loop(self):
        now = time.perf_counter()
        dt = now - self.last_time
        self.last_time = now

        # Avoid very large time step if window freezes
        dt = min(dt, 0.05)

        self.apply_parameters()
        self.update_labels()

        pwm = self.pwm_var.get()

        if self.running:
            # Use current loaded voltage for motor update
            vbat_now = self.battery.v_loaded

            data = self.motor.update(pwm, dt, vbat_now)

            # Total current of four identical motors
            total_current = 4.0 * data["current"]

            # Update battery SOC and voltage sag
            self.battery.update(total_current, dt)

            # Recompute output after battery voltage update
            data = self.motor.compute_outputs(pwm, self.battery.v_loaded)

            self.sim_time += dt
        else:
            data = self.motor.compute_outputs(pwm, self.battery.v_loaded)

        self.update_output_text(data)

        self.root.after(20, self.loop)


if __name__ == "__main__":
    root = tk.Tk()
    app = DroneMotorBatteryGUI(root)
    root.mainloop()