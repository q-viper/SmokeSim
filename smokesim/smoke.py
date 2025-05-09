from smokesim.particle import Particle
from smokesim.defs import Sprite, ParticleProperty, SmokeProperty
from smokesim.base import BaseSim
from smokesim.engine import EngineTypes, Engine
from smokesim.noise import PerlinNoise
from smokesim.defs.constants import CLOUD_MASK

from typing import Tuple, List, Optional
import numpy as np


class Smoke(BaseSim):
    def __init__(self, smoke_property: SmokeProperty):
        """
        Class to represent a smoke object. Smoke is made up of particles.

        Args:
        - smoke_property (SmokeProperty): The properties of the smoke.

        """
        super().__init__(smoke_property)
        self.origin = smoke_property.origin
        self.id = smoke_property.id
        self.particle_count = smoke_property.particle_count
        self.color = smoke_property.color
        self.sprite_size = smoke_property.sprite_size
        self.lifetime = smoke_property.lifetime
        self.age = smoke_property.age
        self.particles: List[Particle] = []
        self.particles_until_now = 0
        self.particle_property = smoke_property.particle_property
        smoke_property.use_perlin_rate = min(max(smoke_property.use_perlin_rate, 0), 1)

        if smoke_property.use_perlin_rate > self.random_state.random():
            self.noise = PerlinNoise(
                seed=self.random_state.randint(0, 100) * self.id,
                octaves=(1, 8),
                persistence=(0.2, 5.8),
                lacunarity=(0.5, 10.0),
            )
            self.default_particle_mask = self.noise.generate_cloud_mask(
                width=self.sprite_size,
                height=self.sprite_size,
                scale=self.sprite_size,
            )
        else:
            self.default_particle_mask = CLOUD_MASK
        self.create_particles(self.particle_property)

    def create_particles(self, particle_property: Optional[ParticleProperty] = None):
        """
        A method to create particles for the smoke.

        Args:
        - particle_property (Optional[ParticleProperty], optional): The properties of the particles. Defaults to None.
        """
        particles = []
        for p in range(self.particle_count):
            particle_id = f"{self.id}_{self.particles_until_now}"
            x, y = self.origin
            if particle_property:
                particle_property.random_seed = self.random_state.randint(0, 100000)
            else:
                particle_property = ParticleProperty(
                    color=self.color, smoke_sprite_size=self.sprite_size
                )
                particle_property.random_seed = self.random_state.randint(0, 100000)

            particle_property.id = particle_id
            particle = Particle(x, y, particle_property)

            particles.append(particle)
            self.particles_until_now += 1
        self.particles.extend(particles)

    def update(self, time_step: float = 30):
        """
        A method to update the smoke.

        Args:
        - time_step (float, optional): The time_step to update the smoke by. Defaults to 30.
        """
        self.age += time_step
        new_particles = []
        for particle in self.particles:
            particle.update(time_step)
            if particle.is_alive:
                new_particles.append(particle)
            else:
                del particle
        if self.lifetime > 0 and self.age > self.lifetime:
            for p in self.particles:
                del p
            self.particles = []
        else:
            self.create_particles(self.particle_property)


class SmokeMachine:
    def __init__(
        self,
        engine_type: EngineTypes = EngineTypes.PYGAME,
        default_particle_count: int = 100,
        default_color: Tuple[int, int, int] = (24, 46, 48),
        default_sprite_size: int = 20,
        random_seed: int = 100,
        versbose: bool = False,
    ):
        self.engine_type = engine_type
        self.color = default_color
        self.sprite_size = default_sprite_size
        self.particle_count = default_particle_count
        self.time_step = 0
        self.smokes: List[Smoke] = []
        self.last_smoke_id = -1
        self.random_seed = random_seed
        self.random_state = np.random.RandomState(random_seed)
        self.verbose = versbose
        self.default_sprite = None
        self.default_smoke_property = SmokeProperty()

    def add_smoke(self, smoke_property: SmokeProperty):
        """
        A method to add smoke to the smoke machine.

        Args:
        - smoke_property: SmokeProperty, object containing the properties of the smoke.
        """
        # if the propert are default, then use from the smoke's property
        if self.default_smoke_property.color == smoke_property.color:
            smoke_property.color = self.color
        if self.default_smoke_property.sprite_size == smoke_property.sprite_size:
            smoke_property.sprite_size = self.sprite_size
        if self.default_smoke_property.particle_count == smoke_property.particle_count:
            smoke_property.particle_count = self.particle_count
        if self.default_smoke_property.id == smoke_property.id:
            smoke_property.id = self.last_smoke_id + 1
        if self.default_smoke_property.random_seed == smoke_property.random_seed:
            smoke_property.random_seed = self.random_seed
        if (
            self.default_smoke_property.particle_property
            == smoke_property.particle_property
        ):
            smoke_property.particle_property.random_seed = self.random_seed
        if self.default_smoke_property.lifetime == smoke_property.lifetime:
            smoke_property.lifetime = -1
        smoke = Smoke(smoke_property)
        self.smokes.append(smoke)

        self.last_smoke_id += 1
        if self.verbose:
            print(f"Added smoke with id: {smoke.id}, particles: {len(smoke.particles)}")

    def empty(self):
        """
        A method to empty the smoke machine.
        """
        print("Emptying smoke")
        for s in self.smokes:
            s.age = s.lifetime
            for p in s.particles:
                p.age = p.lifetime

                del p
            del s
        self.smokes = []

    def update(self, time_step: float = 30):
        """
        A method to update the smoke machine.

        Args:
        - time_step (float, optional): The time_step to update the smoke machine by. Defaults to 30.
        """
        self.time_step += time_step
        new_smokes = []
        for smoke in self.smokes:
            smoke.update(time_step)
            if smoke.age > smoke.lifetime and smoke.lifetime > 0:
                for p in smoke.particles:
                    p.age = p.lifetime
                    del p
                del smoke
            else:
                new_smokes.append(smoke)
        self.smokes = new_smokes

    def draw(self, screen, engine: Engine):
        """
        A method to draw the smoke machine.

        Args:
        - screen: The screen to draw the smoke machine on.
        - engine: The engine instance to handle rendering.
        """
        for smoke in self.smokes:
            self.draw_smoke(smoke, screen, engine)

    def make_sprite(self, particle: Particle, engine) -> object:
        """
        A method to make a sprite.

        Args:
        - particle (Particle): The particle to create a sprite for.
        - engine: The engine instance to handle rendering.

        Returns:
        - The sprite object (Pygame Surface or PIL Image).
        """
        sprite = Sprite(
            color=particle.color,
            width=particle.scale,
            height=particle.scale,
            mask=particle.default_particle_mask,
        )

        if engine.engine_type == EngineTypes.PYGAME:
            sprite_paint = engine.paint_sprite(sprite)
        elif engine.engine_type == EngineTypes.PIL:
            sprite_paint = engine.paint_sprite(sprite)
        return sprite_paint

    def draw_particle(self, particle: Particle, screen, engine: Engine):
        """
        A method to draw a particle.

        Args:
        - particle (Particle): The particle to draw.
        - screen: The screen to draw the particle on.
        - engine: The engine instance to handle rendering.
        """
        if particle.is_alive:
            if particle.sprite_paint is None:
                particle.sprite_paint = self.make_sprite(particle, engine)
            if particle.sprite_paint is None:
                raise ValueError(
                    "sprite_paint is None. Ensure make_sprite is working correctly."
                )
            if engine.engine_type == EngineTypes.PYGAME:
                particle.sprite_paint.set_alpha(particle.alpha)
            engine.blit(
                screen, particle.sprite_paint, (int(particle.x), int(particle.y))
            )

            # Mark particle as not alive if it goes out of bounds
            if (
                particle.x < 0
                or particle.x > engine.screen_dim[0]
                or particle.y < 0
                or particle.y > engine.screen_dim[1]
            ):
                particle.is_alive = False

    def draw_smoke(self, smoke: Smoke, screen, engine: Engine):
        """
        A method to draw a smoke.

        Args:
        - smoke (Smoke): The smoke to draw.
        - screen: The screen to draw the smoke on.
        """
        for particle in smoke.particles:
            if particle.sprite_paint is None:
                particle.default_particle_mask = smoke.default_particle_mask
                if self.default_sprite is None:
                    particle.sprite_paint = self.make_sprite(particle, engine)
                else:
                    particle.sprite_paint = self.default_sprite
            self.draw_particle(particle, screen, engine)
