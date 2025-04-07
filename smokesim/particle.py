from smokesim.base import BaseSim
from smokesim.defs.particle import ParticleProperty

from typing import Union, Tuple, Optional, Callable
import numpy as np


class Particle(BaseSim):
    def __init__(self, x: int, y: int, property: ParticleProperty):
        """
        A class to represent a particle. Particles are used to create smoke.

        Args:
         - x (int): The x coordinate of the particle.
        - y (int): The y coordinate of the particle.
        - property (ParticleProperty): The properties of the particle.
            - vx (Optional[float], optional): The x velocity of the particle. Defaults to None.
            - startvy (Optional[float], optional): The y velocity of the particle. Defaults to None.
            - scale (Optional[float], optional): The scale of the particle. Defaults to None.
            - lifetime (Optional[int], optional): The lifetime of the particle. Defaults to None.
            - age (int, optional): The age of the particle. Defaults to 0.
            - min_vx (float, optional): The minimum x velocity of the particle. Defaults to -4/100.
            - max_vx (float, optional): The maximum x velocity of the particle. Defaults to 4/100.
            - min_vy (float, optional): The minimum y velocity of the particle. Defaults to -4/10.
            - max_vy (float, optional): The maximum y velocity of the particle. Defaults to -1/10.
            - min_scale (int, optional): The minimum scale of the particle. Defaults to 20.
            - max_scale (int, optional): The maximum scale of the particle. Defaults to 40.
            - min_lifetime (float, optional): The minimum lifetime of the particle. Defaults to 2000.
            - max_lifetime (float, optional): The maximum lifetime of the particle. Defaults to 8000.
            - color (Tuple[float, float, float], optional): The color of the particle. Defaults to (167, 167, 167).
            - smoke_sprite_size (int, optional): The size of the sprite. Defaults to 20.
            - fade_speed (int, optional): The speed at which the particle fades. Defaults to 1.
            - alpha (int, optional): The alpha of the particle. Defaults to 255.
        """
        super().__init__(property)

        # self.seed = property.seed
        # self.float_in_range = lambda start, end, random_state: start + np.random.random() * (end - start)
        self.property = property
        self.x = x
        self.y = y
        self.startvx = (
            property.startvx
            if property.startvx is not None
            else self.float_in_range(property.min_vx, property.max_vx)
        )
        self.startvy = (
            property.startvy
            if property.startvy is not None
            else self.float_in_range(property.min_vy, property.max_vy)
        )
        self.scale = (
            property.smoke_sprite_size
            if property.scale is not None
            else int(self.float_in_range(property.min_scale, property.max_scale))
        )
        self.lifetime = (
            property.lifetime
            if property.lifetime is not None
            else self.float_in_range(property.min_lifetime, property.max_lifetime)
        )
        self.age = property.age
        self.color = property.color
        self.smoke_sprite_size = property.smoke_sprite_size
        self.final_scale = self.float_in_range(
            self.scale * property.scale_range[0], self.scale * property.scale_range[1]
        )
        self.scale_step = (self.final_scale - self.scale) / self.lifetime
        self.vy = self.startvy
        self.vx = self.startvx
        self.alpha = property.alpha
        self.fade_speed = property.fade_speed
        self.is_alive = True
        self.default_particle_mask: "np.ndarray" = None
        self.sprite_paint: "pygame.Surface" = None

    @property
    def position(self):
        return (self.x, self.y)

    def update(self, time_step: float = 1):
        """
        A method to update the particle.

        Args:
        - time_step (float, optional): The time_step to update the particle by. Defaults to 1.

        """
        self.age += time_step
        self.x += self.vx * time_step
        self.y += self.vy * time_step
        frac = self.age / self.lifetime
        frac = frac**0.5
        self.vy = (1 - frac) * self.startvy
        self.vx = (1 - frac) * self.startvx
        scale_frac = self.age * self.scale_step

        height = self.scale + scale_frac
        width = self.scale + scale_frac
        self.alpha -= self.fade_speed

        if (
            (self.alpha < 0)
            or (self.age > self.lifetime)
            or (self.scale < 1)
            or (height < 0)
            or (width < 0)
        ):
            self.is_alive = False
            return None
