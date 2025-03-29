from smokesim.base import BaseProperty
from smokesim.constants import CLOUD_MASK

import numpy as np
from typing import Optional, Tuple


class Sprite(BaseProperty):
    """
    A dataclass to represent a sprite.
    """

    width: int = 20
    height: int = 20
    opacity_mask: np.ndarray = CLOUD_MASK
    color: tuple = (255, 255, 255)

    class Config:
        arbitrary_types_allowed = True


class ParticleProperty(BaseProperty):
    """
    A dataclass to represent the arguments for a particle.


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

    startvx: Optional[float] = None
    startvy: Optional[float] = None
    scale: Optional[float] = None
    lifetime: Optional[int] = None
    age: int = 0
    min_vx: float = -4 / 100
    max_vx: float = 4 / 100
    min_vy: float = -4 / 10
    max_vy: float = -1 / 10
    # select random scale between min_scale and max_scale
    min_scale: int = 20
    max_scale: int = 40
    # select a final scale between 0.1 and 1.5 times the initial scale
    scale_range: Tuple[int, int] = (0.01, 1.5)
    min_lifetime: float = 2000
    max_lifetime: float = 8000
    color: Tuple[float, float, float] = (24, 46, 48)
    smoke_sprite_size: int = 20
    fade_speed: int = 1
    alpha: int = 255
    # seed:int = 100
    id: str = ""
