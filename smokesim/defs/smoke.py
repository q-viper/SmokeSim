from smokesim.defs.particle import ParticleProperty
from smokesim.base import BaseProperty

from typing import Optional, Tuple


class SmokeProperty(BaseProperty):
    """
    A dataclass to represent the arguments for a smoke.

    - origin (Tuple[int, int], optional): The origin of the smoke. Defaults to (100, 100).
    - particle_count (int, optional): The number of particles in the smoke. Defaults to 100.
    - color (Tuple[int, int, int], optional): The color of the smoke. Defaults to (167, 167, 167).
    - particle_args (dict, optional): Arguments to pass to the Particle class. Defaults to {}.
    - sprite_size (int, optional): The size of the sprite. Defaults to 20.
    - lifetime (int, optional): The lifetime of the smoke. Defaults to -1.
    - age (int, optional): The age of the smoke. Defaults to 0.
    - id (int, optional): The id of the smoke. Defaults to 0.
    """

    origin: Tuple[int, int] = (100, 100)
    particle_count: int = 100
    color: Tuple[int, int, int] = (24, 46, 48)
    particle_property: Optional[ParticleProperty] = ParticleProperty()
    sprite_size: int = 20
    lifetime: int = -1
    age: int = 0
    id: int = 0
    use_perlin_rate: float = 0.5
