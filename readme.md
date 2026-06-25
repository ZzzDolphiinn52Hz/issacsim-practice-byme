conda init

conda deactivate

conda activate env_isaaclab

issacsim

# script test

Ví dụ dùng:
ctrl = F450AttitudeHold(z_target=3.0)
ctrl.start()
Hoặc đặt target cụ thể:
ctrl = F450AttitudeHold(x_target=1.0, y_target=2.0, z_target=3.0)
ctrl.start()
Đổi target khi đang chạy:
ctrl.set_position_target(2.0, -1.0)
ctrl.set_xyz_target(0.0, 0.0, 4.0)
Tune PID XY:
ctrl.set_position_pid(kp_x=0.7, kd_x=1.0, kp_y=0.7, kd_y=1.0)
ctrl.position_angle_limit_deg = 8.0
ctrl.position_accel_limit = 1.5