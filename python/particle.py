from dataclasses import dataclass, field
from typing import Callable, List, Optional
import numpy as np

@dataclass
class Particle:
    x: int = 100
    y: int = 100
    z: int = 1
    x_update: Optional[Callable] = field(default=lambda x, t: x +t)
    y_update: Optional[Callable] = field(default=lambda x, t: x * np.cos((x+t)*np.pi/180))
    z_update: Optional[Callable] = field(default=lambda x, t: x-t/(x+2))
    lifespan: int = 100
    color: List[int] = field(default_factory=lambda: [200, 200, 200])
    color_update: Optional[List[Callable]] = field(default_factory=lambda: [lambda x, t: min(max(0, x - t), 255)])
    num_subparticles: Optional[int] = 2
    subparticles_every: Optional[int] = 2
    _time: int = 0
    _current_color: List[int] = field(init=False, default_factory=lambda: [200, 200, 200])
    _position: List[int] = field(init=False, default_factory=lambda: [100, 100, 2])
    is_alive: bool = True

    def update_position(self, time: float):
        x = self.x if self.x_update is None else self.x_update(self.x, time)
        y = self.y if self.y_update is None else self.y_update(self.y, time)
        z = self.z if self.z_update is None else self.z_update(self.z, time)

        return [x, y, z]

    def update_color(self, time: float):
        color = self.color
        if self.color_update is None:
            pass
        elif len(self.color_update) == 1:
            fxn = self.color_update[0]
            color = [fxn(c, time) for c in color]
        else:
            color = [upd(c, time) for upd, c in zip(self.color_update, color)]
        return [int(c) for c in color]

    def update(self):
        
        sub_particles = []
        if self._time <= self.lifespan:
            self._position = self.update_position(self._time)
            self._current_color = self.update_color(self._time)
            sub_particles = [self]
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
        self._time += 1
        return sub_particles

# Example usage:
particle = Particle()
particle.update()
print(particle)
