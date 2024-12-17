# the idea here is that I should be able to select an engine to draw the particles on a screen
# the screen could be a pygame screen or a PIL image
# an eninge could be pygame, or PIL
# hope is that the results from each engine will be the same

from enum import Enum
from typing import Optional, Tuple
from pathlib import Path
import numpy as np


class EngineTypes(Enum):
    PYGAME = "pygame"
    PIL = "pil"


class BaseEngine:
    def __init__(self, enigne_type: EngineTypes = EngineTypes.PYGAME):
        self.engine_type = enigne_type

    def get_screen(self):
        pass


class Engine(BaseEngine):
    def __init__(self, engine_type: EngineTypes = EngineTypes.PYGAME):
        super().__init__(engine_type)
        if engine_type == EngineTypes.PYGAME:
            import pygame

            self.engine = pygame
            self.screen: Optional[pygame.Surface] = None
        elif engine_type == EngineTypes.PIL:
            from PIL import Image

            self.engine = Image
            self.screen: Optional[Image.Image] = None

    def blit(self, screen, image, pos):
        if self.engine_type == EngineTypes.PYGAME:
            screen.blit(image, pos)
        elif self.engine_type == EngineTypes.PIL:
            screen.paste(image, pos)

    def display_image(self):
        if self.engine_type == EngineTypes.PYGAME:
            if self.screen_dim == self.image.get_size():
                self.screen.blit(self.image, (0, 0))
            else:
                self.image = self.engine.transform.scale(self.image, self.screen_dim)
            self.screen.blit(self.image, (0, 0))

        if self.engine_type == EngineTypes.PIL:
            if self.screen_dim == self.image.size:
                self.screen.paste(self.image, (0, 0))
            else:
                self.image = self.image.resize(self.screen_dim)
            self.screen.paste(self.image, (0, 0))

    def make_screen(self, screen_dim: Tuple[int, int] = (500, 700)):
        self.screen_dim = screen_dim
        if self.engine_type == EngineTypes.PYGAME:
            self.engine.init()
            screen = self.engine.display.set_mode(
                self.screen_dim, flags=self.engine.HIDDEN
            )
            return screen
        elif self.engine_type == EngineTypes.PIL:

            return self.engine.new("RGB", (500, 700), (0, 0, 0))

    def make_surface(self, image: np.ndarray):
        if self.engine_type == EngineTypes.PYGAME:
            self.image = self.engine.surfarray.make_surface(image)
            self.image = self.engine.transform.scale(self.image, self.screen_dim)
        elif self.engine_type == EngineTypes.PIL:
            self.image = self.engine.fromarray(image)
            self.image = self.image.resize(self.screen_dim)
        return self.image

    def read_image(self, image_path: Optional[Path] = None):
        """
        A method to read an image.

        Args:
        - image_path (Path): The path to the image.

        """
        if self.engine_type == EngineTypes.PYGAME:
            if image_path is not None:
                self.image = self.engine.image.load(str(image_path))
                if not image_path.exists():
                    Warning("No image path provided. Creating a blank image.")
                    image_path = None
            if image_path is None:
                self.image = np.zeros((self.screen_dim[0], self.screen_dim[1], 3))

                self.image = self.engine.surfarray.make_surface(self.image)

            self.image.set_alpha(255)

            self.image = self.engine.transform.scale(self.image, self.screen_dim)
            blank_image = self.engine.surfarray.make_surface(
                np.zeros((self.screen_dim[0], self.screen_dim[1], 3))
            )
            blank_image.set_alpha(255)
            self.blank_image = self.engine.transform.scale(blank_image, self.screen_dim)

        elif self.engine_type == EngineTypes.PIL:
            if image_path is not None:
                self.image = self.engine.open(image_path)
                if not image_path.exists():
                    Warning("No image path provided. Creating a blank image.")
                    image_path = None
            if image_path is None:
                self.image = np.zeros((self.screen_dim[0], self.screen_dim[1], 3))
                self.image = self.engine.fromarray(self.image)
            self.image.set_alpha(255)
            self.image = self.image.resize(self.screen_dim)
            blank_image = self.engine.new("RGB", (500, 700), (0, 0, 0))
            self.blank_image = blank_image.resize(self.screen_dim)

    def end(self):
        if self.engine_type == EngineTypes.PYGAME:
            self.engine.quit()
        elif self.engine_type == EngineTypes.PIL:
            pass
