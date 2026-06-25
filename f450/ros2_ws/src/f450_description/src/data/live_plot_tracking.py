#!/usr/bin/env python3
import argparse
import csv
import os
import time
import math

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
        help="CSV file written by F450 tracking logger.",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=250,
        help="Refresh interval in milliseconds. Default: 250",
    )

    parser.add_argument(
        "--wait",
        action="store_true",
        help="Wait for the CSV file to appear instead of failing immediately.",
    )

    parser.add_argument(
        "--rolling",
        action="store_true",
        help="Use rolling time window mode. Default is full-history mode.",
    )

    parser.add_argument(
        "--window",
        type=float,
        default=20.0,
        help="Rolling window length in seconds, only used with --rolling.",
    )

    parser.add_argument(
        "--include-zero",
        action="store_true",
        default=True,
        help="Keep y=0 inside each subplot. Default: enabled.",
    )

    parser.add_argument(
        "--max-points",
        type=int,
        default=0,
        help="Downsample for display if data is very large. 0 means no limit.",
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
                if value == "":
                    data[name].append(float("nan"))
                else:
                    data[name].append(float(value))
        except ValueError:
            continue

    if not data.get("time"):
        return None

    return data


def normalize_time(data):
    """
    Convert raw log time to plotted time starting from 0.
    This guarantees the graph origin stays at t = 0.
    """
    if data is None or not data.get("time"):
        return data

    t0 = data["time"][0]
    data = {name: values[:] for name, values in data.items()}
    data["time_plot"] = [t - t0 for t in data["time"]]

    return data


def apply_display_mode(data, rolling=False, window=20.0, max_points=0):
    if data is None or not data.get("time_plot"):
        return data

    time_values = data["time_plot"]

    start_index = 0

    if rolling and window > 0.0:
        min_time = time_values[-1] - window
        for index, value in enumerate(time_values):
            if value >= min_time:
                start_index = index
                break

    data = {
        name: values[start_index:]
        for name, values in data.items()
    }

    if max_points and max_points > 0:
        n = len(data["time_plot"])
        if n > max_points:
            step = math.ceil(n / max_points)
            data = {
                name: values[::step]
                for name, values in data.items()
            }

    return data


def finite_values(values):
    return [
        value for value in values
        if value is not None and math.isfinite(value)
    ]


def set_axis_limits(axis, time_values, y_values, include_zero=True):
    if not time_values:
        return

    t_min = 0.0
    t_max = max(time_values[-1], 1.0)

    axis.set_xlim(t_min, t_max)

    valid_y = finite_values(y_values)

    if include_zero:
        valid_y.append(0.0)

    if not valid_y:
        return

    y_min = min(valid_y)
    y_max = max(valid_y)

    if abs(y_max - y_min) < 1e-9:
        margin = 1.0
    else:
        margin = 0.1 * (y_max - y_min)

    axis.set_ylim(y_min - margin, y_max + margin)


def build_plot():
    fig, axes = plt.subplots(3, 2, figsize=(14, 10), sharex=True)
    axes = axes.flatten()
    line_pairs = []

    for axis, (actual_name, target_name, title, unit) in zip(axes, PLOTS):
        target_line, = axis.plot([], [], "--", linewidth=1.6, label="target")
        actual_line, = axis.plot([], [], linewidth=1.4, label="actual")

        axis.axhline(0.0, linewidth=0.8, alpha=0.35)

        axis.set_title(title)
        axis.set_ylabel(unit)
        axis.grid(True, alpha=0.3)
        axis.legend(loc="best")

        line_pairs.append(
            (axis, actual_line, target_line, actual_name, target_name)
        )

    axes[-2].set_xlabel("time from start (s)")
    axes[-1].set_xlabel("time from start (s)")

    fig.suptitle("F450 live tracking response - full history")
    fig.tight_layout()

    return fig, axes, line_pairs


def main():
    args = parse_args()

    if args.wait:
        wait_for_file(args.csv_path)

    fig, axes, line_pairs = build_plot()
    status_text = fig.text(0.01, 0.01, "Waiting for data...", fontsize=9)

    def update(_frame):
        data = read_csv(args.csv_path)
        data = normalize_time(data)
        data = apply_display_mode(
            data,
            rolling=args.rolling,
            window=args.window,
            max_points=args.max_points,
        )

        if data is None or not data.get("time_plot"):
            status_text.set_text("Waiting for data...")
            return [status_text]

        time_values = data["time_plot"]
        artists = [status_text]

        for axis, actual_line, target_line, actual_name, target_name in line_pairs:
            actual_values = data[actual_name]
            target_values = data[target_name]

            actual_line.set_data(time_values, actual_values)
            target_line.set_data(time_values, target_values)

            combined_y = actual_values + target_values
            set_axis_limits(
                axis,
                time_values,
                combined_y,
                include_zero=args.include_zero,
            )

            artists.extend([actual_line, target_line])

        mode_text = "rolling" if args.rolling else "full-history"

        status_text.set_text(
            f"{os.path.basename(args.csv_path)} | "
            f"mode={mode_text} | "
            f"samples={len(time_values)} | "
            f"t={time_values[-1]:.2f}s"
        )

        return artists

    anim = FuncAnimation(
        fig,
        update,
        interval=args.interval,
        cache_frame_data=False,
    )

    fig._animation = anim

    plt.show()


if __name__ == "__main__":
    main()