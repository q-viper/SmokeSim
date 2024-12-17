# the idea here is that I should be able to select an engine to draw the particles on a screen
# the screen could be a pygame screen or a PIL image
# an eninge could be pygame, or PIL
# hope is that the results from each engine will be the same

from enum import Enum
from typing import Optional, Tuple


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
        self.screen = self.get_screen()

    def get_screen(self):
        if self.engine_type == EngineTypes.PYGAME:
            import pygame

            return pygame.display.set_mode((500, 700))
        elif self.engine_type == EngineTypes.PIL:
            from PIL import Image

            return Image.new("RGB", (500, 700), (255, 255, 255))
