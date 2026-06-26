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


2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:                        
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:                       ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Warning] [omni.isaac.dynamic_control.plugin] Failed to find articulation at '/f450_simple'
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:                        
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:                       ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:                        
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:  File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:    x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:                       ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Warning] [omni.kit.window.script_editor.editor_tab] Failed to parse error, please report a bug. Error:RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:18  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 994 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 145, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     lookahead=LOOKAHEAD_DT,
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/opt/miniconda3/envs/env_isaaclab/lib/python3.11/site-packages/isaacsim/kit/kernel/py/omni/kit/app/_impl/__init__.py", line 128, in write
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     func(f"[py {self._name}]: {text}")
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/opt/miniconda3/envs/env_isaaclab/lib/python3.11/site-packages/isaacsim/kit/kernel/py/carb/__init__.py", line 56, in log_info
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     file, lno, func, mod = _get_caller_info()
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                            ^^^^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:19  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:20  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: Traceback (most recent call last):
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 154, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     print(
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: ^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   [Previous line repeated 995 more times]
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 132, in _circle_step
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     t = _sim_time_ref[0]
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:                         
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:   File "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/scripr_editor/circle_trajectory.py", line 59, in circle_setpoint
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:     x_tgt   = cx + r * math.cos(angle)
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]:                        ^^^^^^^^^^^^^^^
2026-06-26 07:06:21  [Error] [omni.kit.app._impl] [py stderr]: RecursionError: maximum recursion depth exceeded while calling a Python object
