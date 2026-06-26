#!/usr/bin/env python3
"""
plot_trajectory_3d.py  --  F450 3D trajectory visualiser
=========================================================
Shows the drone's actual flight path vs target path in 3D space.

Static mode (default):
    python3 plot_trajectory_3d.py data/f450_tracking.csv

Live / animated mode (refreshes while sim is running):
    python3 plot_trajectory_3d.py data/f450_tracking.csv --live

Options:
    --output PATH       Save final figure to PATH (PNG/PDF/...)
    --show              Open the interactive plot window (static mode only)
    --live              Animate the figure, refreshing every --interval ms
    --interval MS       Refresh period for live mode  (default: 300)
    --wait              Block until the CSV file appears (useful with --live)
    --attitude          Overlay attitude arrows sampled every --attitude-step rows
    --attitude-step N   Rows between attitude arrow samples  (default: 20)
    --tail N            Keep only the last N samples in live mode  (0 = all)
    --max-points N      Downsample to at most N points for display  (0 = off)
"""

import argparse
import csv
import math
import os
import time as _time_mod

os.environ.setdefault("MPLCONFIGDIR", "/tmp/matplotlib")

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D          # noqa: F401  (needed for 3D)
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from matplotlib.animation import FuncAnimation


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="F450 3D trajectory: actual vs target."
    )
    p.add_argument("csv_path", help="CSV log created by F450 tracking logger.")
    p.add_argument("-o", "--output", default=None,
                   help="Save figure to this file. Default: <csv>_traj3d.png")
    p.add_argument("--show", action="store_true",
                   help="Open interactive window (static mode only).")
    p.add_argument("--live", action="store_true",
                   help="Animate – keep refreshing while the CSV grows.")
    p.add_argument("--interval", type=int, default=300,
                   help="Refresh interval in ms for live mode. Default: 300")
    p.add_argument("--wait", action="store_true",
                   help="Block until the CSV file appears.")
    p.add_argument("--attitude", action="store_true",
                   help="Draw attitude orientation arrows along the path.")
    p.add_argument("--attitude-step", type=int, default=20,
                   help="Rows between each attitude arrow. Default: 20")
    p.add_argument("--tail", type=int, default=0,
                   help="Live mode: keep only last N samples. 0 = all.")
    p.add_argument("--max-points", type=int, default=0,
                   help="Downsample for display if data is large. 0 = off.")

    # Plot limits. Default is fixed because live autoscale makes the 3D view
    # shrink/jump while the CSV is still being written.
    p.add_argument("--auto-limits", action="store_true",
                   help="Use automatic axis limits instead of fixed limits.")
    p.add_argument("--xy-limit", type=float, default=3.0,
                   help="Fixed XY half-range in metres. Default: 3.0")
    p.add_argument("--z-min", type=float, default=0.0,
                   help="Fixed Z lower limit. Default: 0.0")
    p.add_argument("--z-max", type=float, default=3.0,
                   help="Fixed Z upper limit. Default: 3.0")
    p.add_argument("--live-colorbar", action="store_true",
                   help="Show colorbar in live mode. Default: off to avoid axes shrinkage.")
    return p.parse_args()


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------

REQUIRED_COLS = {
    "time",
    "x", "x_target",
    "y", "y_target",
    "z", "z_target",
    "roll_rad", "pitch_rad", "yaw_rad",
}


def wait_for_file(csv_path):
    while not os.path.exists(csv_path):
        print("Waiting for CSV:", csv_path)
        _time_mod.sleep(1.0)


def read_csv(csv_path):
    """Read CSV into a dict of float lists. Returns None on any failure."""
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        return None
    try:
        with open(csv_path, newline="") as fh:
            reader = csv.DictReader(fh)
            rows = list(reader)
    except OSError:
        return None

    if not rows:
        return None

    if not REQUIRED_COLS.issubset(rows[0].keys()):
        missing = sorted(REQUIRED_COLS - rows[0].keys())
        print("CSV missing columns:", missing)
        return None

    data = {col: [] for col in rows[0].keys()}
    for row in rows:
        try:
            for col, val in row.items():
                data[col].append(float("nan") if val == "" else float(val))
        except ValueError:
            continue

    if not data.get("time"):
        return None
    return data


# ---------------------------------------------------------------------------
# Downsampling
# ---------------------------------------------------------------------------

def downsample(data, max_points, tail=0):
    """Apply optional tail truncation then downsampling."""
    if data is None:
        return None

    n = len(data["time"])

    # Rolling tail
    start = 0
    if tail > 0 and n > tail:
        start = n - tail
    if start > 0:
        data = {col: vals[start:] for col, vals in data.items()}
        n = len(data["time"])

    # Downsampling
    if max_points and max_points > 0 and n > max_points:
        step = math.ceil(n / max_points)
        data = {col: vals[::step] for col, vals in data.items()}

    return data


# ---------------------------------------------------------------------------
# Attitude arrow helper
# ---------------------------------------------------------------------------

def _rotation_matrix(roll, pitch, yaw):
    """ZYX Euler -> rotation matrix (each arg in radians)."""
    cr, sr = math.cos(roll),  math.sin(roll)
    cp, sp = math.cos(pitch), math.sin(pitch)
    cy, sy = math.cos(yaw),   math.sin(yaw)

    # Body x-axis (forward) expressed in world frame
    fx = cy * cp
    fy = sy * cp
    fz = -sp

    # Body z-axis (up) expressed in world frame
    ux = cy * sp * sr - sy * cr
    uy = sy * sp * sr + cy * cr
    uz = cp * sr

    return (fx, fy, fz), (ux, uy, uz)


def draw_attitude_arrows(ax, data, step, scale=0.05, alpha=0.5):
    """Plot small forward (blue) and up (green) arrows along the path."""
    xs = data["x"]
    ys = data["y"]
    zs = data["z"]
    rolls  = data["roll_rad"]
    pitchs = data["pitch_rad"]
    yaws   = data["yaw_rad"]

    indices = range(0, len(xs), step)
    for i in indices:
        fwd, up = _rotation_matrix(rolls[i], pitchs[i], yaws[i])
        ax.quiver(xs[i], ys[i], zs[i],
                  fwd[0], fwd[1], fwd[2],
                  length=scale, color="steelblue", alpha=alpha,
                  arrow_length_ratio=0.3, linewidth=0.8)
        ax.quiver(xs[i], ys[i], zs[i],
                  up[0], up[1], up[2],
                  length=scale, color="limegreen", alpha=alpha,
                  arrow_length_ratio=0.3, linewidth=0.8)


# ---------------------------------------------------------------------------
# Colour-by-time line segments
# ---------------------------------------------------------------------------

def _make_segments(x, y, z):
    """Convert x,y,z arrays to array of [N-1, 2, 3] segments."""
    pts = np.array([x, y, z], dtype=float).T          # (N, 3)
    segs = np.stack([pts[:-1], pts[1:]], axis=1)       # (N-1, 2, 3)
    return segs


def _coloured_path(ax, xs, ys, zs, cmap_name="plasma", lw=2.0, alpha=0.9,
                   label=None):
    """Draw a 3D line coloured by time progress (0 -> 1)."""
    n = len(xs)
    if n < 2:
        return None
    segs = _make_segments(xs, ys, zs)
    t_norm = np.linspace(0.0, 1.0, n - 1)
    colours = matplotlib.colormaps[cmap_name](t_norm)
    lc = Line3DCollection(segs, colors=colours, linewidths=lw, alpha=alpha,
                          label=label)
    ax.add_collection3d(lc)
    return lc


# ---------------------------------------------------------------------------
# Axis padding helper
# ---------------------------------------------------------------------------

def _axis_lim(values, pad_frac=0.12, min_span=0.05):
    finite = [v for v in values if math.isfinite(v)]
    if not finite:
        return -1.0, 1.0
    lo, hi = min(finite), max(finite)
    span = hi - lo
    if span < min_span:
        mid = (lo + hi) / 2.0
        lo, hi = mid - min_span / 2, mid + min_span / 2
        span = min_span
    pad = pad_frac * span
    return lo - pad, hi + pad


# ---------------------------------------------------------------------------
# Figure builder
# ---------------------------------------------------------------------------

def build_figure():
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlabel("X  (m)")
    ax.set_ylabel("Y  (m)")
    ax.set_zlabel("Z  (m)")
    ax.set_title("F450 3D trajectory  -  actual vs target")
    return fig, ax


# ---------------------------------------------------------------------------
# Core renderer
# ---------------------------------------------------------------------------

def render_static(ax, data, show_attitude=False, attitude_step=20,
                  add_colorbar=True, stats_text_obj=None,
                  fixed_limits=True, xy_limit=3.0, z_min=0.0, z_max=3.0):
    """
    Draw 3D path geometry onto ax (clears first).

    Returns (cbar, stats_text_obj):
      cbar           -- matplotlib Colorbar object, or None if add_colorbar=False
      stats_text_obj -- the Figure Text object for the stats line (bottom-left)

    In live mode the caller should:
      - call cbar.remove() before the next frame to prevent axes shrinkage
      - pass the returned stats_text_obj back on the next call so it is
        updated in-place instead of creating a new Text artist each frame
    """
    ax.cla()

    ax.set_xlabel("X  (m)")
    ax.set_ylabel("Y  (m)")
    ax.set_zlabel("Z  (m)")
    ax.set_title("F450 3D trajectory  -  actual vs target")

    xs, ys, zs = data["x"], data["y"], data["z"]
    xt, yt, zt = data["x_target"], data["y_target"], data["z_target"]
    t       = data["time"]
    elapsed = t[-1] - t[0]

    # --- target path (dashed grey) ---
    ax.plot(xt, yt, zt,
            linestyle="--", color="grey", linewidth=1.4,
            alpha=0.7, label="target path")

    # --- actual path, colour-coded by time ---
    _coloured_path(ax, xs, ys, zs, cmap_name="plasma",
                   lw=2.2, alpha=0.9, label="actual path")

    # --- start / end markers ---
    ax.scatter([xs[0]],  [ys[0]],  [zs[0]],
               color="green", s=80, zorder=5, label="start")
    ax.scatter([xs[-1]], [ys[-1]], [zs[-1]],
               color="red",   s=80, zorder=5, label="end")
    ax.scatter([xt[-1]], [yt[-1]], [zt[-1]],
               color="grey", s=60, marker="x", zorder=5, label="target end")

    # --- attitude arrows ---
    if show_attitude and len(xs) > 1:
        draw_attitude_arrows(ax, data, step=attitude_step)

    # --- axis limits ---
    # In live mode, autoscale makes the plot jump/shrink as new CSV rows arrive.
    # Keep fixed axes by default so the circular trajectory is drawn in a stable frame.
    if fixed_limits:
        ax.set_xlim(-xy_limit, xy_limit)
        ax.set_ylim(-xy_limit, xy_limit)
        ax.set_zlim(z_min, z_max)
        ax.set_box_aspect((2.0 * xy_limit, 2.0 * xy_limit, max(z_max - z_min, 1e-6)))
    else:
        ax.set_xlim(*_axis_lim(xs + xt))
        ax.set_ylim(*_axis_lim(ys + yt))
        ax.set_zlim(*_axis_lim(zs + zt))
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()
        z0, z1 = ax.get_zlim()
        ax.set_box_aspect((x1 - x0, y1 - y0, max(z1 - z0, 1e-6)))

    ax.legend(loc="upper left", fontsize=9)

    # --- colorbar (caller manages lifecycle in live mode) ---
    cbar = None
    if add_colorbar:
        sm = plt.cm.ScalarMappable(
            cmap="plasma",
            norm=plt.Normalize(vmin=0.0, vmax=max(elapsed, 1e-3)),
        )
        sm.set_array([])
        cbar = ax.get_figure().colorbar(sm, ax=ax, shrink=0.55, pad=0.1)
        cbar.set_label("elapsed time (s)")

    # --- stats annotation (reuse existing Text object in live mode) ---
    dist = sum(
        math.sqrt((xs[i] - xs[i-1])**2 +
                  (ys[i] - ys[i-1])**2 +
                  (zs[i] - zs[i-1])**2)
        for i in range(1, len(xs))
    )
    stats_str = (
        f"samples={len(t)}  |  elapsed={elapsed:.2f}s"
        f"  |  path length={dist:.3f}m"
    )
    if stats_text_obj is None:
        stats_text_obj = ax.get_figure().text(
            0.01, 0.01, stats_str, fontsize=8, color="dimgrey"
        )
    else:
        stats_text_obj.set_text(stats_str)

    return cbar, stats_text_obj


# ---------------------------------------------------------------------------
# Static entry point
# ---------------------------------------------------------------------------

def default_output(csv_path):
    root, _ = os.path.splitext(csv_path)
    return root + "_traj3d.png"


def run_static(args):
    data = read_csv(args.csv_path)
    if data is None:
        raise SystemExit("ERROR: Could not read data from " + args.csv_path)

    data = downsample(data, args.max_points)

    fig, ax = build_figure()
    render_static(ax, data,
                  show_attitude=args.attitude,
                  attitude_step=args.attitude_step,
                  fixed_limits=not args.auto_limits,
                  xy_limit=args.xy_limit,
                  z_min=args.z_min,
                  z_max=args.z_max)

    out = args.output or default_output(args.csv_path)
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    print("Saved:", out)

    if args.show:
        plt.show()
    else:
        plt.close(fig)


# ---------------------------------------------------------------------------
# Live / animated entry point
# ---------------------------------------------------------------------------

def run_live(args):
    if args.wait:
        wait_for_file(args.csv_path)

    fig, ax = build_figure()
    status = fig.text(0.5, 0.97, "Waiting for data...", fontsize=9,
                      ha="center", va="top", color="dimgrey")

    # Persistent objects reused across frames to prevent axes shrinkage.
    #   cbar       -- Colorbar; must call cbar.remove() before recreating
    #   stats_text -- Figure Text for bottom-left stats line
    _live = {"cbar": None, "stats_text": None}

    def update(_frame):
        # --- remove previous colorbar BEFORE ax.cla() inside render_static ---
        # Calling cbar.remove() frees the space it borrowed from the 3D axes.
        if _live["cbar"] is not None:
            try:
                _live["cbar"].remove()
            except Exception:
                pass
            _live["cbar"] = None

        data = read_csv(args.csv_path)
        if data is None:
            status.set_text("Waiting for data...")
            return

        data = downsample(data, args.max_points, tail=args.tail)
        if data is None or len(data.get("time", [])) < 2:
            status.set_text("Not enough data yet...")
            return

        cbar, stats_text = render_static(
            ax, data,
            show_attitude=args.attitude,
            attitude_step=args.attitude_step,
            # In live mode colorbar recreation can shrink/jitter the 3D axes.
            # Keep it off by default; enable with --live-colorbar if needed.
            add_colorbar=args.live_colorbar,
            stats_text_obj=_live["stats_text"],   # reuse, update in-place
            fixed_limits=not args.auto_limits,
            xy_limit=args.xy_limit,
            z_min=args.z_min,
            z_max=args.z_max,
        )
        _live["cbar"]       = cbar
        _live["stats_text"] = stats_text

        n  = len(data["time"])
        t0 = data["time"][0]
        tn = data["time"][-1]
        status.set_text(
            f"{os.path.basename(args.csv_path)}  |  "
            f"samples={n}  |  t={tn - t0:.2f}s"
        )

    anim = FuncAnimation(fig, update, interval=args.interval,
                         cache_frame_data=False)
    fig._anim_ref = anim   # keep alive

    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    args = parse_args()

    if args.wait and not args.live:
        wait_for_file(args.csv_path)

    if args.live:
        run_live(args)
    else:
        run_static(args)


if __name__ == "__main__":
    main()
