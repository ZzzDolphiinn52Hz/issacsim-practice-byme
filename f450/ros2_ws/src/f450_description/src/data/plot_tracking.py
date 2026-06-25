#!/usr/bin/env python3
import argparse
import csv
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib.pyplot as plt


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
        description="Plot F450 tracking response for x, y, z, roll, pitch, yaw."
    )
    parser.add_argument(
        "csv_path",
        help="CSV file created by F450AttitudeHold.start_tracking_log().",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=None,
        help="Output image path. Default: <csv_name>_tracking.png",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the plot window after saving.",
    )
    return parser.parse_args()


def read_csv(csv_path):
    with open(csv_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    if not rows:
        raise ValueError(f"No data rows found in {csv_path}")

    required = {"time"}
    for actual_name, target_name, _, _ in PLOTS:
        required.add(actual_name)
        required.add(target_name)

    missing = sorted(required - set(rows[0].keys()))
    if missing:
        raise ValueError(
            "CSV is missing required columns: " + ", ".join(missing)
        )

    data = {name: [] for name in rows[0].keys()}

    for row in rows:
        for name, value in row.items():
            if value == "":
                data[name].append(float("nan"))
            else:
                data[name].append(float(value))

    return data


def default_output_path(csv_path):
    root, _ = os.path.splitext(csv_path)
    return root + "_tracking.png"


def plot_tracking(data, output_path, show=False):
    time = data["time"]

    fig, axes = plt.subplots(3, 2, figsize=(14, 10), sharex=True)
    axes = axes.flatten()

    for axis, (actual_name, target_name, title, unit) in zip(axes, PLOTS):
        axis.plot(time, data[target_name], "--", linewidth=1.6, label="target")
        axis.plot(time, data[actual_name], linewidth=1.4, label="actual")
        axis.set_title(title)
        axis.set_ylabel(unit)
        axis.grid(True, alpha=0.3)
        axis.legend(loc="best")

    axes[-2].set_xlabel("time (s)")
    axes[-1].set_xlabel("time (s)")

    fig.suptitle("F450 tracking response")
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)

    if show:
        plt.show()
    else:
        plt.close(fig)


def main():
    args = parse_args()
    output_path = args.output or default_output_path(args.csv_path)
    data = read_csv(args.csv_path)
    plot_tracking(data, output_path, show=args.show)
    print("Saved plot:", output_path)


if __name__ == "__main__":
    main()
