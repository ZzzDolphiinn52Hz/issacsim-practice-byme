import carb


class TestDisturbance:
    def __init__(
        self,
        enabled=True,
        start_time=2.0,
        duration=0.25,
        force_y=3.0,
        z_offset=0.12,
    ):
        self.enabled = enabled
        self.start_time = float(start_time)
        self.duration = float(duration)
        self.force_y = float(force_y)
        self.z_offset = float(z_offset)

    def apply(self, dc, body_handle, sim_time):
        if not self.enabled:
            return

        if self.start_time <= sim_time <= self.start_time + self.duration:
            dc.apply_body_force(
                body_handle,
                carb.Float3(0.0, self.force_y, 0.0),
                carb.Float3(0.0, 0.0, self.z_offset),
                False,
            )
