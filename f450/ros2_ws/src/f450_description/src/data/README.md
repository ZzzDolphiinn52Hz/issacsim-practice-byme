# F450 Tracking Plots

This folder contains scripts and output data for F450 tracking response.

Use this path in Isaac Script Editor:

```python
DATA_DIR = CONTROLLER_PATH + "/data"
TRACKING_CSV = DATA_DIR + "/f450_tracking.csv"
f450_app.start_tracking_log(TRACKING_CSV, sample_period=0.02)
```

For realtime plotting, run this in another terminal while Isaac Sim is running:

```bash
python3 ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/live_plot_tracking.py \
  ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/f450_tracking.csv \
  --wait \
  --max-points 2000
```

After running the simulation, stop the log in Isaac:

```python
f450_app.stop_tracking_log()
```

Then create the final static plot:

```bash
python3 ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/plot_tracking.py \
  ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/f450_tracking.csv
```

## 3D trajectory viewer

Static (after simulation):

```bash
python3 ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/plot_trajectory_3d.py \
  ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/f450_tracking.csv \
  --show
```

Live (while Isaac Sim is running):

```bash
python3 ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/plot_trajectory_3d.py \
  ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data/f450_tracking.csv \
  --live --wait --interval 500
```

With attitude arrows (forward + up vectors along the path):

```bash
python3 plot_trajectory_3d.py f450_tracking.csv --show --attitude --attitude-step 15
```

Output: `<csv>_traj3d.png` (default) or specify with `-o path.png`.

---

## 2D tracking plots

The 2D plots contain target vs actual signals for:

- `x`
- `y`
- `z`
- `roll`
- `pitch`
- `yaw`

Position units are meters. Angle plots use degrees.
