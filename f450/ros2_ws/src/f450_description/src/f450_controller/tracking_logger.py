import csv
import math
import os


class TrackingLogger:
    def __init__(self, csv_path, sample_period=0.02):
        self.csv_path = os.path.abspath(os.path.expanduser(csv_path))
        self.sample_period = max(float(sample_period), 0.0)
        self.last_sample_time = None
        self.file = None
        self.writer = None

    def start(self):
        os.makedirs(os.path.dirname(self.csv_path), exist_ok=True)
        self.file = open(self.csv_path, "w", newline="")
        self.writer = csv.DictWriter(
            self.file,
            fieldnames=[
                "time",
                "x",
                "x_target",
                "y",
                "y_target",
                "z",
                "z_target",
                "roll_deg",
                "roll_target_deg",
                "pitch_deg",
                "pitch_target_deg",
                "yaw_deg",
                "yaw_target_deg",
                "roll_rad",
                "roll_target_rad",
                "pitch_rad",
                "pitch_target_rad",
                "yaw_rad",
                "yaw_target_rad",
            ],
        )
        self.writer.writeheader()
        self.file.flush()
        self.last_sample_time = None

    def stop(self):
        if self.file is None:
            return

        self.file.flush()
        self.file.close()
        self.file = None
        self.writer = None

    def log(
        self,
        sim_time,
        x,
        y,
        z,
        roll,
        pitch,
        yaw,
        x_target,
        y_target,
        z_target,
        roll_target,
        pitch_target,
        yaw_target,
    ):
        if self.writer is None:
            return

        if (
            self.last_sample_time is not None
            and sim_time - self.last_sample_time < self.sample_period
        ):
            return

        self.last_sample_time = sim_time
        self.writer.writerow(
            {
                "time": sim_time,
                "x": x,
                "x_target": x_target,
                "y": y,
                "y_target": y_target,
                "z": z,
                "z_target": z_target,
                "roll_deg": math.degrees(roll),
                "roll_target_deg": math.degrees(roll_target),
                "pitch_deg": math.degrees(pitch),
                "pitch_target_deg": math.degrees(pitch_target),
                "yaw_deg": math.degrees(yaw),
                "yaw_target_deg": math.degrees(yaw_target),
                "roll_rad": roll,
                "roll_target_rad": roll_target,
                "pitch_rad": pitch,
                "pitch_target_rad": pitch_target,
                "yaw_rad": yaw,
                "yaw_target_rad": yaw_target,
            }
        )
        self.file.flush()
