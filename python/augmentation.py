from smoke import SmokeMachine, SmokeProperty
from particle import ParticleProperty

import pygame
from typing import Optional, Tuple
from pathlib import Path
import numpy as np


class Augmentation:
    def __init__(self, image_path: Path = Path("assets/me.jpg"),
                 screen_dim: Optional[Tuple[int, int]] = None,
                 smoke_machine: Optional[SmokeMachine] = None):
        self.image_path = image_path
        self.image = None
        self.read_image(image_path)
        self.screen_dim = screen_dim if screen_dim else (
            self.image.get_width(), self.image.get_height())
        self.screen = smoke_machine.screen if smoke_machine else self.make_screen()
        self.smoke_machine = smoke_machine if smoke_machine else SmokeMachine(
            self.screen)
        self.display_image()

    def display_image(self):
        """
        A method to display the image on the screen.
        """
        if self.screen_dim == self.image.get_size():
            self.screen.blit(self.image, (0, 0))
        else:
            self.image = pygame.transform.scale(self.image, self.screen_dim)
        self.screen.blit(self.image, (0, 0))
        return self

    def read_image(self, image_path: Path) -> pygame.Surface:
        """
        A method to read an image.

        Args:
        - image_path (Path): The path to the image.

        Returns:
        - pygame.Surface: The image.        
        """

        self.image = pygame.image.load(str(image_path))
        return self

    def make_screen(self) -> pygame.Surface:
        """
        A method to make a screen.

        Returns:
        - pygame.Surface: The screen.
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        screen = pygame.display.set_mode(self.screen_dim, flags=pygame.HIDDEN)
        return screen

    def add_smoke(self, args: dict):
        """
        A method to add smoke to the screen.

        Args:
        - args (dict): The arguments to pass to the smoke machine.
        """
        self.smoke_machine.add_smoke(args)

    def agument(self, steps: int):
        """
        A method to augment the image with smoke.

        Args:
        - steps (int): The number of steps to augment the image.
        """
        for t in range(steps):
            self.screen.blit(self.image, (0, 0))
            self.smoke_machine.update(self.clock.tick(60))

        pygame.display.flip()

    def save_as(self, out_dir: Path = Path('assets/augmented_smoke.png')):
        """
        A method to save the augmented image.

        Args:
        - out_dir (Path, optional): The output directory to save the image. Defaults to Path('assets/augmented_smoke.png').

        """
        pygame.image.save(self.screen, str(out_dir))

    def end(self):
        """
        A method to end the pygame session.
        """
        pygame.quit()


if __name__ == "__main__":
    np.random.seed(100)
    WIDTH, HEIGHT = 700, 500
    augmentation = Augmentation(screen_dim=(WIDTH, HEIGHT))
    smoke_machine = augmentation.smoke_machine
    augmentation.add_smoke(dict(particle_count=15, sprite_size=25,
                                origin=(250, 500)))
    augmentation.add_smoke(dict(particle_count=15, sprite_size=25,
                                origin=(450, 500)))

    augmentation.agument(90)
    for i in range(5):
        augmentation.add_smoke(dict(color=smoke_machine.color, particle_count=1,
                                    origin=(np.random.randint(100, WIDTH), np.random.randint(100, HEIGHT)), lifetime=200,
                                    particle_args={'min_lifetime': 200,
                                                   'max_lifetime': 500,
                                                   'min_scale': 10,
                                                   'max_scale': 50,
                                                   'fade_speed': 50,
                                                   'scale': 50,
                                                   'smoke_sprite_size': 50,
                                                   'color': smoke_machine.color}))
    augmentation.agument(10)
    augmentation.save_as()
    augmentation.end()
