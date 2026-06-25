# F450 Tracking Plots

This folder contains scripts for plotting F450 tracking response.

The expected CSV is created from Isaac Script Editor with:

```python
f450_app.start_tracking_log("/tmp/f450_tracking.csv", sample_period=0.02)
```

After running the simulation, stop the log:

```python
f450_app.stop_tracking_log()
```

Then plot:

```bash
python3 src/data/plot_tracking.py /tmp/f450_tracking.csv
```

The plot contains target vs actual signals for:

- `x`
- `y`
- `z`
- `roll`
- `pitch`
- `yaw`

Position units are meters. Angle plots use degrees.
