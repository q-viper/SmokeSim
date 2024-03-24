class PlayGround:
    def __init__(
        self, max_frames: int = 1000, smoke_origins: List = [(350, 500), (200, 200)]
    ):
        self.max_frames = max_frames
        self.smoke_origins = smoke_origins
        self.canvas:Canvas = Canvas(
        )
        self.smokes = [Smoke(orig) for orig in smoke_origins]
        self.current_frame = 0
        self.is_alive = True

    @property
    def frame(self):
        return self.canvas.frame

    def update_frame(self, smoke: Smoke):
        points = []
        colors = []
        sizes = []
        # coord = [(x_update(x_orig, i), y_update(y_orig, i)) for i in range(1, pts)]
        # rad = [rad_update(rad_orig, i) for i in range(1, pts)]
        # color = [[color_update(c, i) for c in color_orig] for i in range(1, pts)]
        # canvas.scatter_points(coord, color, rad)
        for particle in smoke.particles:
            points.append(particle._position[:2])
            colors.append(particle._current_color)
            sizes.append(particle._position[2])
        self.canvas.scatter_points(points, colors, sizes)

    def update(self):
        temp_smokes = []
        if self.current_frame <= self.max_frames:
            for smoke in self.smokes:
                if not smoke.is_alive:
                    del smoke
                else:
                    temp_smokes.append(smoke)
                smoke.update()
                self.update_frame(smoke)
        else:
            self.is_alive = False
        return self.frame


pg = PlayGround()