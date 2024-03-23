from typing import Callable, Optional, List
import cv2
import numpy as np


class Canvas:
    def __init__(
        self,
        background: np.ndarray,
        dimensions: List,
        shake_every: float,
    ):
        self.background = background
        self.dimensions = dimensions
        self.shake_every = shake_every
        self._canvas = background

        self._foregrounds: Optional[List[np.ndarray]] = []
        self._frame = self.frame

    def draw_circle(self, center: List[int], radius: int, color: List[int]):
        frame = np.zeros_like(self._canvas, dtype=np.uint8)
        cv2.circle(frame, center, radius, color, -1)
        self._foregrounds.append(frame)

    @property
    def frame(self):
        for fg in self._foregrounds:
            self._canvas += fg  # [fg != [0, 0, 0]] = fg[fg != [0, 0, 0]]
        return self._canvas.astype(np.uint8)


class Particle:
    def __init__(
        self,
        x: int = 100,
        y: int = 100,
        z: int = 2,
        x_update: Optional[Callable] = lambda x, t: x * np.sin(t),
        y_update: Optional[Callable] = lambda x, t: x * np.cos(t),
        z_update: Optional[Callable] = lambda x, t: x / (t + 1),
        lifespan: int = 100,
        color: List[int] = [200, 200, 200],
        color_update: Optional[List[Callable]] = [lambda x, t: min(max(0, x - t), 255)],
        num_subparticles: Optional[int] = 2,
        subparticles_every: Optional[int] = 50,
    ) -> None:
        self._x = x
        self._y = y
        self._z = z
        self.x_update = x_update
        self.y_update = y_update
        self.z_update = z_update
        self.lifespan = lifespan
        self._color = color
        self._current_color = color
        self.color_update = color_update
        self._time = 0
        self.num_subparticles = num_subparticles
        self.subparticles_every = subparticles_every
        self.is_alive = True
        self._position = self.update_position(self._time)
        self.x, self.y, self.z = self.update_position(self._time)

    def update_position(self, time: float):
        x = self._x if self.x_update is None else self.x_update(self._x, time)
        y = self._y if self.y_update is None else self.y_update(self._y, time)
        z = self._z if self.z_update is None else self.z_update(self._z, time)

        return x, y, z

    def color(self, time: float):
        color = self._color
        if self.color_update is None:
            pass
        elif len(self.color_update) == 1:
            fxn = self.color_update[0]
            color = [fxn(c, time) for c in color]
        else:
            color = [upd(c, time) for upd, c in zip(self.color_update, color)]
        return [int(c) for c in color]

    def update(self):
        self._time += 1
        sub_particles = []
        if self._time <= self.lifespan:
            self._position = self.update_position(self._time)
            self._current_color = self.color(self._time)

            if self._time % self.subparticles_every == 0:
                if self.num_subparticles is not None:
                    for p in range(self.num_subparticles):
                        p = Particle(
                            self._position[0],
                            self._position[1],
                            self._position[2],
                            self.x_update,
                            self.y_update,
                            self.z_update,
                            self.lifespan,
                            self._current_color,
                            self.color_update,
                            self.num_subparticles,
                            self.subparticles_every,
                        )
                        sub_particles.append(p)
        else:
            self.is_alive = False
        return sub_particles


class Smoke:
    def __init__(
        self,
        origin: List = [(100, 100)],
        lifespan: int = 1000,
        start_particles: int = 10,
    ):
        self.origin = origin
        self.lifespan = lifespan
        self.start_particles = start_particles
        self.particles: Optional[List[Particle]] = []
        self._time = 0
        self.is_alive = True
        self._startup()

    def _startup(self):
        for sp in range(self.start_particles):
            p = self._create_particle()
            self.particles.append(p)

    def _create_particle(
        self,
        x: int = 100,
        y: int = 100,
        z: int = 20,
        x_update: Optional[Callable] = lambda x, t: x * np.sin(t),
        y_update: Optional[Callable] = lambda x, t: x * np.cos(t),
        z_update: Optional[Callable] = lambda x, t: x + 0 * t,
        lifespan: int = 1000,
        color: List[int] = [200, 200, 200],
        color_update: Optional[List[Callable]] = [
            lambda x, t: x + 0 * min(max(0, x - t), 255)
        ],
    ):
        return Particle(
            x, y, z, x_update, y_update, z_update, lifespan, color, color_update
        )

    def update(self):
        self._time += 1
        temp_particles = []
        if self.lifespan >= self._time:
            for particle in self.particles:
                res = particle.update()
                if len(res) > 0:
                    temp_particles.extend(res)
                if not particle.is_alive:
                    del particle
                else:
                    temp_particles.append(particle)
        else:
            self.is_alive = False
        self.particles = temp_particles
        return self.particles


class PlayGround:
    def __init__(
        self, max_frames: int = 1000, smoke_origins: List = [(350, 500), (200, 200)]
    ):
        self.max_frames = max_frames
        self.smoke_origins = smoke_origins
        self.canvas = Canvas(
            255 + np.zeros((700, 1000, 3), dtype=np.uint8),
            dimensions=[400, 500],
            shake_every=0,
        )
        self.smokes = [Smoke(orig) for orig in smoke_origins]
        self.current_frame = 0
        self.is_alive = True

    @property
    def frame(self):
        return self.canvas.frame

    def update_frame(self, smoke: Smoke):
        for particle in smoke.particles:
            x, y, z = [int(v) for v in particle._position]
            color = tuple([int(c) for c in particle._current_color])
            self.canvas.draw_circle((y, x), z, color)

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
while True:
    cv2.imshow("Canvas", pg.frame.astype(np.uint8))
    pg.update()
    key = cv2.waitKey(20)

    if key == ord("q") or not pg.is_alive:
        break

cv2.destroyAllWindows()