import circle_trajectory as ct
importlib.reload(ct)

# Sua thong so quy dao o day neu muon.
ct.CIRCLE_RADIUS = 2.0
ct.CIRCLE_Z = 1.5
ct.CIRCLE_PERIOD = 20.0
ct.CIRCLE_CENTER_X = 0.0
ct.CIRCLE_CENTER_Y = 0.0
ct.TAKEOFF_TIME = 5.0
ct.LOOKAHEAD_DT = 0.18

# Dung chung file log voi controller chinh.
ct.TRACKING_CSV = TRACKING_CSV

ct.start(f450_app)
