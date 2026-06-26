#!/usr/bin/env python3
"""
circle_trajectory.py  --  Isaac Sim Script Editor
==================================================
Cho drone F450 bay theo quỹ đạo hình tròn trong không gian.

Cach dung trong Isaac Script Editor:
  1. Chay setup block mot lan de khoi dong controller va logger.
  2. Vong lap on_physics_step se tu dong cap nhat setpoint theo thoi gian sim.
  3. Sau khi xong chay stop block de dung log.

Tham so chinh:
  CIRCLE_RADIUS   -- ban kinh vong tron (m)
  CIRCLE_Z        -- do cao bay (m)
  CIRCLE_PERIOD   -- thoi gian hoan thanh 1 vong (s)
  CIRCLE_CENTER_X -- tam X cua vong tron (m)
  CIRCLE_CENTER_Y -- tam Y cua vong tron (m)
  LOOKAHEAD_DT    -- drone nhan setpoint som hon mot chut de giam lag (s)
"""

import math
import sys
import os

# ---------------------------------------------------------------------------
# USER PARAMETERS  --  chinh o day
# ---------------------------------------------------------------------------

CIRCLE_RADIUS   = 2.0       # ban kinh (m)
CIRCLE_Z        = 1.5       # do cao bay (m), drone se len cao truoc
CIRCLE_PERIOD   = 20.0      # thoi gian 1 vong day (s)
CIRCLE_CENTER_X = 0.0       # tam X (m)
CIRCLE_CENTER_Y = 0.0       # tam Y (m)

# Drone se nhan setpoint som hon LOOKAHEAD_DT giay de bu lag controller
LOOKAHEAD_DT    = 0.18      # (s), chỉnh nho xuong neu drone overshoot

# Khi nao bat dau bay vong tron (de drone co thoi gian len do cao truoc)
TAKEOFF_TIME    = 5.0       # (s) -- sau thoi gian nay moi bat dau vong tron

# Tracking log
TRACKING_CSV    = (
    os.path.expanduser("~")
    + "/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src/data"
    + "/f450_tracking.csv"
)

# ---------------------------------------------------------------------------
# HELPER: tinh vi tri tren vong tron tai thoi diem t
# ---------------------------------------------------------------------------

def circle_setpoint(t, cx, cy, r, period, z, lookahead=0.0):
    """
    Tra ve (x_target, y_target, z_target) tren vong tron tai thoi diem t.
    lookahead dich chuyen setpoint theo chieu chuyển dong de giam pha tre.
    """
    t_eff   = t + lookahead
    angle   = 2.0 * math.pi * t_eff / period
    x_tgt   = cx + r * math.cos(angle)
    y_tgt   = cy + r * math.sin(angle)
    return x_tgt, y_tgt, z


# ---------------------------------------------------------------------------
# BLOCK 1 -- Chay trong Script Editor de KHOI DONG
# ---------------------------------------------------------------------------
# Paste doan nay vao Script Editor va nhan Run:
#
#   import importlib, sys, os
#   CONTROLLER_PATH = "/config/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description/src"
#   SCRIPT_PATH = CONTROLLER_PATH + "/scripr_editor"
#   for path in (CONTROLLER_PATH, SCRIPT_PATH):
#       if path not in sys.path:
#           sys.path.insert(0, path)
#   import circle_trajectory as ct
#   importlib.reload(ct)
#   ct.start(f450_app)
#
# ---------------------------------------------------------------------------

_sim_time_ref = [0.0]      # tong thoi gian sim tinh tu luc start()
_circle_started = [False]  # co hieu bay vong tron da bat dau chua
_orig_on_step   = [None]   # luu physics callback goc


def start(app):
    """
    Goi ham nay trong Script Editor sau khi f450_app da duoc khoi tao.

    Vi du:
        import circle_trajectory as ct
        ct.start(f450_app)
    """
    global _app
    _app = app

    # Reset state
    _sim_time_ref[0]    = 0.0
    _circle_started[0]  = False

    # Cau hinh controller: bat position hold
    app.enable_position_hold = True
    app.enable_yaw_hold      = True

    # Dat muc tieu ban dau: dung yen tai tam, len do cao
    start_x, start_y, _ = circle_setpoint(0.0, CIRCLE_CENTER_X, CIRCLE_CENTER_Y,
                                           CIRCLE_RADIUS, CIRCLE_PERIOD, CIRCLE_Z)
    app.set_xyz_target(
        x_target=start_x,
        y_target=start_y,
        z_target=CIRCLE_Z,
    )

    # Bat dau ghi log
    app.start_tracking_log(TRACKING_CSV, sample_period=0.02)

    # Hook vao physics step de cap nhat setpoint tung frame
    # (Luu lai ham goc de restore khi stop)
    _orig_on_step[0] = app.on_physics_step

    def _circle_step(dt):
        _sim_time_ref[0] += dt
        t = _sim_time_ref[0]

        # Sau TAKEOFF_TIME giay moi bat dau bay vong tron
        if t >= TAKEOFF_TIME:
            if not _circle_started[0]:
                _circle_started[0] = True
                print(f"[circle] Bat dau vong tron tai t={t:.2f}s")

            t_circle = t - TAKEOFF_TIME
            x_tgt, y_tgt, z_tgt = circle_setpoint(
                t_circle,
                CIRCLE_CENTER_X, CIRCLE_CENTER_Y,
                CIRCLE_RADIUS, CIRCLE_PERIOD, CIRCLE_Z,
                lookahead=LOOKAHEAD_DT,
            )
            app.position_controller.x_target = x_tgt
            app.position_controller.y_target = y_tgt
            app.altitude_controller.z_target  = z_tgt

            # In progress moi 2 giay
            if int(t * 0.5) != int((t - dt) * 0.5):
                rounds = t_circle / CIRCLE_PERIOD
                print(
                    f"[circle] t={t:.1f}s  "
                    f"rounds={rounds:.2f}  "
                    f"setpoint=({x_tgt:.2f}, {y_tgt:.2f}, {z_tgt:.2f})"
                )

        # Goi controller goc
        orig = _orig_on_step[0]
        if orig is not None:
            orig(dt)

    app.on_physics_step = _circle_step
    app.start()

    print("=" * 60)
    print("circle_trajectory: STARTED")
    print(f"  radius={CIRCLE_RADIUS}m  z={CIRCLE_Z}m  period={CIRCLE_PERIOD}s")
    print(f"  center=({CIRCLE_CENTER_X}, {CIRCLE_CENTER_Y})")
    print(f"  takeoff_wait={TAKEOFF_TIME}s  lookahead={LOOKAHEAD_DT}s")
    print(f"  log -> {TRACKING_CSV}")
    print("=" * 60)


# ---------------------------------------------------------------------------
# BLOCK 2 -- Chay trong Script Editor de DUNG va luu log
# ---------------------------------------------------------------------------
# Paste doan nay vao Script Editor sau khi muon ket thuc:
#
#   import circle_trajectory as ct
#   ct.stop(f450_app)
#
# ---------------------------------------------------------------------------

def stop(app):
    """Restore physics callback goc va dung tracking log."""
    if _orig_on_step[0] is not None:
        app.on_physics_step = _orig_on_step[0]
        _orig_on_step[0]    = None
        app.start()

    app.stop_tracking_log()
    print("circle_trajectory: STOPPED")
    print("Log saved to:", TRACKING_CSV)
    print()
    print("Xem quy dao 3D:")
    print(
        f"  python3 ~/Desktop/IssacSim_TA/f450/ros2_ws/src/f450_description"
        f"/src/data/plot_trajectory_3d.py {TRACKING_CSV} --show"
    )


# ---------------------------------------------------------------------------
# STANDALONE TEST -- chay ngoai Isaac de kiem tra ham tinh toan setpoint
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Kiem tra circle_setpoint():")
    print(f"  radius={CIRCLE_RADIUS}m  period={CIRCLE_PERIOD}s  z={CIRCLE_Z}m")
    print()
    print(f"  {'t(s)':>6}  {'x_tgt':>8}  {'y_tgt':>8}  {'z_tgt':>6}  {'angle_deg':>10}")
    print("  " + "-" * 50)
    for step in range(9):
        t = step * CIRCLE_PERIOD / 8.0
        x, y, z = circle_setpoint(t, CIRCLE_CENTER_X, CIRCLE_CENTER_Y,
                                   CIRCLE_RADIUS, CIRCLE_PERIOD, CIRCLE_Z)
        angle_deg = math.degrees(2.0 * math.pi * t / CIRCLE_PERIOD)
        print(f"  {t:>6.2f}  {x:>8.3f}  {y:>8.3f}  {z:>6.2f}  {angle_deg:>10.1f}")

    # Kiem tra lookahead khong lam thay doi ban kinh
    errors = []
    for i in range(100):
        t = i * CIRCLE_PERIOD / 100.0
        x, y, z = circle_setpoint(t, CIRCLE_CENTER_X, CIRCLE_CENTER_Y,
                                   CIRCLE_RADIUS, CIRCLE_PERIOD, CIRCLE_Z,
                                   lookahead=LOOKAHEAD_DT)
        r = math.sqrt((x - CIRCLE_CENTER_X)**2 + (y - CIRCLE_CENTER_Y)**2)
        errors.append(abs(r - CIRCLE_RADIUS))

    max_err = max(errors)
    print()
    print(f"  Ban kinh sai so toi da (voi lookahead={LOOKAHEAD_DT}s): {max_err:.6f}m")
    assert max_err < 1e-9, "FAIL: lookahead lam thay doi ban kinh!"
    print("  PASS: lookahead khong anh huong ban kinh.")
