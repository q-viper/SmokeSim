
import pygame
from dataclasses import dataclass
from typing import Optional, Tuple, List
from smokesim.particle import Particle, ParticleProperty


@dataclass
class SmokeProperty:
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
    seed:int = 100


class Smoke:
    def __init__(self, screen: pygame.Surface, smoke_property: SmokeProperty):
        """
        Class to represent a smoke object. Smoke is made up of particles.

        Args:
        - screen (pygame.Surface): The screen to draw the smoke on.
        - smoke_property (SmokeProperty): The properties of the smoke.

        """
        self.origin = smoke_property.origin
        self.id = smoke_property.id
        self.screen = screen
        self.particle_count = smoke_property.particle_count
        self.color = smoke_property.color
        self.sprite_size = smoke_property.sprite_size
        self.lifetime = smoke_property.lifetime
        self.age = smoke_property.age
        self.particles: List[Particle] = []
        self.particle_property = smoke_property.particle_property
        self.create_particles(self.particle_property)

    def create_particles(self, particle_property: Optional[ParticleProperty] = None):
        """
        A method to create particles for the smoke.

        Args:
        - particle_property (Optional[ParticleProperty], optional): The properties of the particles. Defaults to None.
        """
        particles = []
        for _ in range(self.particle_count):
            x, y = self.origin
            if particle_property:

                particle = Particle(x, y, particle_property)
            else:
                particle_property = ParticleProperty(color=self.color,
                                                     smoke_sprite_size=self.sprite_size)
                particle = Particle(x, y, particle_property)

            particles.append(particle)
        self.particles.extend(particles)

    def update(self, time: float = 1):
        """
        A method to update the smoke.

        Args:
        - time (float, optional): The time to update the smoke by. Defaults to 1.
        """
        self.age += time
        new_particles = []
        for particle in self.particles:
            particle.update(time)
            if particle.is_alive:
                particle.draw(self.screen)
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


class SmokeMachine:
    def __init__(self, screen: pygame.Surface, default_particle_count: int = 100,
                 default_color: Tuple[int, int, int] = (24, 46, 48), default_sprite_size: int = 20):
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
        self.time = 0
        self.smokes: List[Smoke] = []
        self.last_smoke_id = -1

    def add_smoke(self, args: dict):
        """
        A method to add smoke to the smoke machine.

        Args:
        - args (dict): The arguments to pass to the Smoke class.

        """

        if 'color' not in args:
            args['color'] = self.color
        if 'particle_count' not in args:
            args['particle_count'] = self.particle_count
        if 'sprite_size' not in args:
            args['sprite_size'] = self.sprite_size
        if 'id' not in args:
            args['id'] = self.last_smoke_id+1
        if 'particle_args' in args:
            particle_args = args['particle_args']
            particle_property = ParticleProperty(**particle_args)
            args['particle_property'] = particle_property
            del args['particle_args']
        smoke_property = SmokeProperty(**args)
        smoke = Smoke(self.screen,
                      smoke_property)
        self.smokes.append(smoke)
        self.last_smoke_id += 1
        print(
            f"Added smoke with id: {smoke.id}, particles: {len(smoke.particles)}")

    def empty(self):
        """
        A method to empty the smoke machine.
        """
        print('Emptying smoke')
        for s in self.smokes:
            s.age = s.lifetime
            for p in s.particles:
                p.age = p.lifetime

                del p
            del s
        self.smokes = []

    def update(self, time: float = 1):
        """
        A method to update the smoke machine.

        Args:
        - time (float, optional): The time to update the smoke machine by. Defaults to 1.
        """
        self.time += time
        new_smokes = []
        for smoke in self.smokes:
            smoke.update(time)
            if smoke.age > smoke.lifetime and smoke.lifetime > 0:
                for p in smoke.particles:
                    p.age = p.lifetime
                    del p
                del smoke
            else:
                new_smokes.append(smoke)
        self.smokes = new_smokes
