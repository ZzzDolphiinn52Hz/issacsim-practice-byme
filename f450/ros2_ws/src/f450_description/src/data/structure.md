# Cấu trúc vòng điều khiển PID - F450 Drone

## Tổng quan: 3 tầng cascade + 1 tầng độc lập

```
[Sensor: x,y,z, roll,pitch,yaw, vx,vy,vz, p,q,r]
         |
         v
   TANG 1: POSITION HOLD (PositionHoldPID)      <-- tầng ngoài cùng
         | output: roll_target, pitch_target
         v
   TANG 2: ATTITUDE HOLD (AttitudeHoldPID)      <-- tầng giữa
         | output: roll_corr, pitch_corr
         |
         +---> YAW HOLD (YawHoldPID)            <-- song song, độc lập
                      | output: yaw_corr
                      v
   TANG 3: ALTITUDE HOLD (AltitudeHoldPID)      <-- hoàn toàn độc lập
                      | output: pwm_base
                      v
              MIXER (QuadXPwmMixer)
              pwm[1..4] = f(pwm_base, roll_corr, pitch_corr, yaw_corr)
                      v
              MOTOR MODEL (MotorModel x4)
              thrust = Kf * omega^2
              reaction_torque = Kq * omega^2
```

---

## Chi tiết từng tầng

### Tầng 1 - Position Hold (`position_hold.py`)

Mục tiêu: giữ x, y trong không gian thế giới.

**Gains:** `kp_x=kp_y=0.55`, `kd_x=kd_y=1.30`, `ki_x=ki_y=0.03`

Cách hoạt động:
```
error_x = x_target - x
ax_cmd  = kp*error_x + kd*(vx_target - vx) + ki*integral_x
```

Sau đó chuyển sang góc nghiêng target (flat-earth model):
```
pitch_target = atan2(forward_accel, g)    # nghiêng trước/sau
roll_target  = -atan2(left_accel, g)      # nghiêng trái/phải
```

Có rotation sang body frame theo yaw hiện tại:
```
forward_accel = cos(yaw)*ax + sin(yaw)*ay
left_accel    = -sin(yaw)*ax + cos(yaw)*ay
```

**Giới hạn:** `accel_limit = 1.2 m/s²`, `angle_limit = 6.5 deg`
**Integral clamp:** `+/- 2.0`

Tầng 1 "ra lệnh" cho tầng 2 thông qua setpoint góc.

---

### Tầng 2 - Attitude Hold (`attitude_pid.py`)

Mục tiêu: bám theo `roll_target`, `pitch_target` từ tầng 1.

**Gains:** `kp=520`, `ki=25`, `kd=130` (roll và pitch dùng chung)

D-term dùng angular rate thực, KHÔNG phải đạo hàm error:
```
roll_corr  = kp*error_roll  + ki*integral_roll  - kd*p   # p = ang_vel.x
pitch_corr = kp*error_pitch + ki*integral_pitch - kd*q   # q = ang_vel.y
```

> Lý do: tránh derivative kick khi setpoint thay đổi đột ngột.
> Đây là kỹ thuật "derivative on measurement" phổ biến trong flight controller.

**Output:** PWM correction, giới hạn `pwm_limit = 260`.

---

### Tầng 2b - Yaw Hold (`yaw_hold.py`)

Song song với attitude, hoàn toàn độc lập (không cascade qua position).

**Gains:** `kp_yaw=95`, `ki_yaw=8`, `kd_yaw=28`

D-term dùng yaw_rate thực, không phải đạo hàm error:
```
yaw_corr = kp*error_yaw + ki*integral_yaw - kd*yaw_rate
```

`wrap_angle()` được dùng để tránh vấn đề góc vượt +/-180 deg.

**Output:** PWM correction, giới hạn `pwm_limit = 120`.

---

### Tầng 3 - Altitude Hold (`altitude_hold.py`)

Hoàn toàn độc lập với 3 tầng trên. Điều khiển chiều cao Z.

**Gains:** `kp_z=220`, `kd_z=150`, `ki_z=15`

```
pwm_base = pwm_hover + kp*error_z + kd*(vz_target - vz) + ki*integral_z
```

`pwm_hover = 1307` là feedforward (PWM giữ hover ổn định ở điểm cân bằng).
D-term dùng `vz` đo thực (`error_vz = 0 - vz`), tương đương derivative on measurement.

**Integral clamp:** `+/- 12.0`

---

### Actuator Mixing (`motor_mixer.py`) - Quad X layout

```
Motor positions:
  M1 front-left:  (+x, +y)
  M2 front-right: (+x, -y)
  M3 rear-right:  (-x, -y)
  M4 rear-left:   (-x, +y)

Mixing:
  M1 = pwm_base + roll_corr - pitch_corr - yaw_corr
  M2 = pwm_base - roll_corr - pitch_corr + yaw_corr
  M3 = pwm_base - roll_corr + pitch_corr - yaw_corr
  M4 = pwm_base + roll_corr + pitch_corr + yaw_corr
```

Tăng M1+M4 (bên trái), giảm M2+M3 (bên phải) => roll sang phải.
Yaw dùng phản lực torque motor (CW vs CCW).

---

### Motor Model (`motor_model.py`)

Mô hình vật lý đầy đủ:

```
u    = (pwm - pwm_min) / (pwm_max - pwm_min)    # throttle 0..1
vm   = u * vbat                                   # ESC voltage
I    = (vm - Ke*omega) / Rm                       # BLDC current
T_motor = Kt * max(I - I0, 0)                     # motor torque
T_load  = Kq * omega^2                            # prop aerodynamic drag
omega_dot = (T_motor - T_load) / J               # rotor dynamics
thrust          = Kf * omega^2                    # thrust (N)
reaction_torque = Kq * omega^2                    # yaw torque (N.m)
```

Phản lực torque từng motor được tổng hợp và apply như một force couple vào thân drone để tạo yaw thực sự trong physics engine.

---

## Sơ đồ tín hiệu tóm tắt

```
x,y  ----[POS PID]----> roll_tgt, pitch_tgt ----[ATT PID]----> roll_corr, pitch_corr
                                                                         |
yaw  ----[YAW PID]----> yaw_corr ----------------------------------------+
                                                                         |
z    ----[ALT PID]----> pwm_base --------------------------------------------+
                                                                         |  |
                                                                    [MIXER]
                                                                   /  |  |  \
                                                                 M1  M2  M3  M4
                                                                   \  |  |  /
                                                              [MOTOR MODEL x4]
                                                          thrust + reaction_torque
                                                                         |
                                                               [Isaac Sim Physics]
                                                                         |
                                                                [Sensor readback]
```

---

## Bảng tổng hợp gains

| Controller    | File               | Kp          | Ki       | Kd          | Clamp output    |
|---------------|--------------------|-------------|----------|-------------|-----------------|
| Position X/Y  | position_hold.py   | 0.55        | 0.03     | 1.30        | angle ±6.5 deg  |
| Altitude Z    | altitude_hold.py   | 220.0       | 15.0     | 150.0       | PWM_MIN/MAX     |
| Attitude R/P  | attitude_pid.py    | 520.0       | 25.0     | 130.0       | ±260 PWM        |
| Yaw           | yaw_hold.py        | 95.0        | 8.0      | 28.0        | ±120 PWM        |

---

## Nhận xét & điểm đáng chú ý

1. **Cascade 2 tầng ngang (Position -> Attitude)** là kiến trúc chuẩn cho quadcopter. Bandwidth phải đảm bảo tầng attitude nhanh hơn tầng position ít nhất 5-10x. Với `kp_att=520` vs `kp_pos=0.55`, tỉ lệ này thỏa mãn.

2. **D-term dùng measured rate** thay vì derivative of error ở cả 3 controller (attitude, yaw, altitude). Thiết kế tốt, tránh derivative kick khi thay đổi setpoint.

3. **Altitude decoupled khỏi attitude** — đây là near-hover approximation (`cos(roll)cos(pitch) ≈ 1`). Khi drone nghiêng mạnh sẽ xuất hiện sai số altitude.

4. **Không có velocity loop riêng cho X/Y** — velocity error xử lý trực tiếp trong D-term của position PID (`kd * (vx_target - vx)`), không có tầng velocity PID riêng biệt.

5. **Yaw từ reaction torque** được mô hình hóa vật lý trong Isaac Sim thay vì chỉ delta PWM, khớp thực tế hơn.

6. **Integral limit** nhỏ ở position (`±2.0`) nhưng lớn hơn ở altitude (`±12.0`), phù hợp vì altitude cần chống ảnh hưởng của trọng lực liên tục.
