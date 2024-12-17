from typing import List, Optional, Tuple

import pygame

from smokesim.base import BaseProperty, BaseSim
from smokesim.particle import Particle, ParticleProperty


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


class Smoke(BaseSim):
    def __init__(self, screen: pygame.Surface, smoke_property: SmokeProperty):
        """
        Class to represent a smoke object. Smoke is made up of particles.

        Args:
        - screen (pygame.Surface): The screen to draw the smoke on.
        - smoke_property (SmokeProperty): The properties of the smoke.

        """
        super().__init__(smoke_property)
        self.origin = smoke_property.origin
        self.id = smoke_property.id
        self.screen = screen
        self.particle_count = smoke_property.particle_count
        self.color = smoke_property.color
        self.sprite_size = smoke_property.sprite_size
        self.lifetime = smoke_property.lifetime
        self.age = smoke_property.age
        self.particles: List[Particle] = []
        self.particles_until_now = 0
        self.particle_property = smoke_property.particle_property
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
            # print(p, particle_id)
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
                # particle.draw(self.screen)
                new_particles.append(particle)
            else:
                del particle
        if self.lifetime > 0 and self.age > self.lifetime:
            for p in self.particles:
                del p
            self.particles = []
        else:
            self.create_particles(self.particle_property)
        # print(f"ID: {self.id}, Num particles: {len(self.particles)}")

    def draw(self, screen: Optional[pygame.Surface] = None):
        screen = screen if screen else self.screen
        for particle in self.particles:
            particle.draw(screen)


class SmokeMachine:
    def __init__(
        self,
        screen: pygame.Surface,
        default_particle_count: int = 100,
        default_color: Tuple[int, int, int] = (24, 46, 48),
        default_sprite_size: int = 20,
        random_seed: int = 100,
        versbose: bool = False,
        auto_draw: bool = True,
    ):
        """
        A class to represent a smoke machine. The smoke machine creates and manages smoke objects.

        Args:
        - screen (pygame.Surface): The screen to draw the smoke on.
        - default_particle_count (int, optional): The default number of particles in the smoke. Defaults to 100.
        - default_color (Tuple[int, int, int], optional): The default color of the smoke. Defaults to (167, 167, 167).
        - default_sprite_size (int, optional): The default size of the sprite. Defaults to 20.

        """
        self.color = default_color
        self.sprite_size = default_sprite_size
        self.particle_count = default_particle_count
        self.screen = screen
        self.time_step = 0
        self.smokes: List[Smoke] = []
        self.last_smoke_id = -1
        self.random_seed = random_seed
        self.verbose = versbose
        self.auto_draw = auto_draw

    def add_smoke(self, args: dict):
        """
        A method to add smoke to the smoke machine.

        Args:
        - args (dict): The arguments to pass to the Smoke class.
            If `particle_args` is in the args, it will be passed to the ParticleProperty class.

        """

        if "color" not in args:
            args["color"] = self.color
        if "particle_count" not in args:
            args["particle_count"] = self.particle_count
        if "sprite_size" not in args:
            args["sprite_size"] = self.sprite_size
        if "id" not in args:
            args["id"] = self.last_smoke_id + 1
        if "random_seed" not in args:
            args["random_seed"] = self.random_seed
        if "particle_args" in args:
            particle_args = args["particle_args"]
            if particle_args.get("random_seed") is None:
                particle_args["random_seed"] = self.random_seed
            particle_property = ParticleProperty(**particle_args)
            # print(f"Particle property: {particle_property}")
            args["particle_property"] = particle_property
            del args["particle_args"]
        else:
            args["particle_property"] = ParticleProperty(random_seed=self.random_seed)
        smoke_property = SmokeProperty(**args)
        smoke = Smoke(self.screen, smoke_property)
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

        if self.auto_draw:
            self.draw()

    def draw(self, screen: Optional[pygame.Surface] = None):
        """
        A method to draw the smoke machine.

        Args:
        - screen (Optional[pygame.Surface], optional): The screen to draw the smoke machine on. Defaults to None.
        """
        screen = screen if screen else self.screen
        for smoke in self.smokes:
            smoke.draw(screen)
