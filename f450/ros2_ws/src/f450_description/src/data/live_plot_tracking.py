#!/usr/bin/env python3
import argparse
import csv
import os
import time

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


PLOTS = [
    ("x", "x_target", "x position", "m"),
    ("y", "y_target", "y position", "m"),
    ("z", "z_target", "z position", "m"),
    ("roll_deg", "roll_target_deg", "roll", "deg"),
    ("pitch_deg", "pitch_target_deg", "pitch", "deg"),
    ("yaw_deg", "yaw_target_deg", "yaw", "deg"),
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Live plot F450 target vs actual tracking from a CSV log."
    )
    parser.add_argument(
        "csv_path",
        help="CSV file written by F450AttitudeHold.start_tracking_log().",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=250,
        help="Refresh interval in milliseconds. Default: 250",
    )
    parser.add_argument(
        "--window",
        type=float,
        default=0.0,
        help="Show only the last N seconds. 0 means full history.",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait for the CSV file to appear instead of failing immediately.",
    )
    return parser.parse_args()


def wait_for_file(csv_path):
    while not os.path.exists(csv_path):
        print("Waiting for CSV:", csv_path)
        time.sleep(1.0)


def read_csv(csv_path):
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return None

    try:
        with open(csv_path, newline="") as csv_file:
            reader = csv.DictReader(csv_file)
            rows = list(reader)
    except OSError:
        return None

    if not rows:
        return None

    required = {"time"}
    for actual_name, target_name, _, _ in PLOTS:
        required.add(actual_name)
        required.add(target_name)

    if not required.issubset(rows[0].keys()):
        return None

    data = {name: [] for name in rows[0].keys()}

    for row in rows:
        try:
            for name, value in row.items():
                data[name].append(float(value) if value != "" else float("nan"))
        except ValueError:
            continue

    return data


def trim_window(data, window):
    if data is None or window <= 0.0:
        return data

    time_values = data["time"]
    if not time_values:
        return data

    min_time = time_values[-1] - window
    start_index = 0

    for index, value in enumerate(time_values):
        if value >= min_time:
            start_index = index
            break

    return {
        name: values[start_index:]
        for name, values in data.items()
    }


def build_plot():
    fig, axes = plt.subplots(3, 2, figsize=(14, 10), sharex=True)
    axes = axes.flatten()
    line_pairs = []

    for axis, (actual_name, target_name, title, unit) in zip(axes, PLOTS):
        target_line, = axis.plot([], [], "--", linewidth=1.6, label="target")
        actual_line, = axis.plot([], [], linewidth=1.4, label="actual")
        axis.set_title(title)
        axis.set_ylabel(unit)
        axis.grid(True, alpha=0.3)
        axis.legend(loc="best")
        line_pairs.append((axis, actual_line, target_line, actual_name, target_name))

    axes[-2].set_xlabel("time (s)")
    axes[-1].set_xlabel("time (s)")
    fig.suptitle("F450 live tracking response")
    fig.tight_layout()

    return fig, axes, line_pairs


def autoscale_axes(axes):
    for axis in axes:
        axis.relim()
        axis.autoscale_view()


def main():
    args = parse_args()

    if args.wait:
        wait_for_file(args.csv_path)

    fig, axes, line_pairs = build_plot()
    status_text = fig.text(0.01, 0.01, "Waiting for data...", fontsize=9)

    def update(_frame):
        data = trim_window(read_csv(args.csv_path), args.window)

        if data is None or not data.get("time"):
            status_text.set_text("Waiting for data...")
            return [status_text]

        time_values = data["time"]
        artists = [status_text]

        for axis, actual_line, target_line, actual_name, target_name in line_pairs:
            actual_line.set_data(time_values, data[actual_name])
            target_line.set_data(time_values, data[target_name])
            artists.extend([actual_line, target_line])

        autoscale_axes(axes)
        status_text.set_text(
            f"{os.path.basename(args.csv_path)} | "
            f"samples={len(time_values)} | "
            f"t={time_values[-1]:.2f}s"
        )
        return artists

    FuncAnimation(
        fig,
        update,
        interval=args.interval,
        cache_frame_data=False,
    )
    plt.show()


if __name__ == "__main__":
    main()
