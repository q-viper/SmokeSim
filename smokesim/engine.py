from enum import Enum
from typing import Optional, Tuple
from pathlib import Path
import numpy as np
from PIL import Image
import cv2


class EngineTypes(Enum):
    PYGAME = "pygame"
    PIL = "pil"


class BaseEngine:
    def __init__(self, engine_type: EngineTypes = EngineTypes.PYGAME):
        self.engine_type = engine_type

    def get_screen(self):
        pass


class Engine(BaseEngine):

    def __init__(
        self,
        screen_dim: Tuple[int, int] = (500, 700),
        engine_type: EngineTypes = EngineTypes.PYGAME,
    ):
        super().__init__(engine_type)
        self.screen_dim = screen_dim
        if engine_type == EngineTypes.PYGAME:
            import pygame

            self.engine = pygame
            self.screen: Optional[pygame.Surface] = None
        elif engine_type == EngineTypes.PIL:
            self.engine = Image
            self.screen: Optional[Image.Image] = None

    def blit(self, screen, image, pos):
        if self.engine_type == EngineTypes.PYGAME:
            screen.blit(image, pos)  # Pygame handles alpha blending automatically
        elif self.engine_type == EngineTypes.PIL:
            # Blend the image with the screen using alpha
            screen.paste(
                image, pos, mask=image.split()[-1]
            )  # Use the alpha channel as the mask

    def display_image(self, image):
        """
        A method to display the image on the screen.
        Args:
        - image: The image to display.
        """
        if image is None:
            raise ValueError(
                "Image is not initialized. Ensure `read_image` is called successfully."
            )

        # Ensure the screen is initialized
        if self.screen is None:
            self.screen = self.make_screen(self.screen_dim)

        if self.engine_type == EngineTypes.PYGAME:
            if self.screen_dim == image.get_size():
                self.screen.blit(image, (0, 0))
            else:
                image = self.engine.transform.scale(image, self.screen_dim)
            self.screen.blit(image, (0, 0))
        elif self.engine_type == EngineTypes.PIL:
            if self.screen_dim != image.size:
                image = image.resize(self.screen_dim)
            self.screen.paste(image, (0, 0))
        return self

    def make_screen(self, screen_dim: Tuple[int, int] = (500, 700)):
        self.screen_dim = screen_dim
        if self.engine_type == EngineTypes.PYGAME:
            self.engine.init()
            screen = self.engine.display.set_mode(
                self.screen_dim, flags=self.engine.HIDDEN
            )
            return screen
        elif self.engine_type == EngineTypes.PIL:
            return self.engine.new("RGBA", screen_dim, (0, 0, 0, 0))

    def make_surface(self, image: np.ndarray):
        if self.engine_type == EngineTypes.PYGAME:
            self.image = self.engine.surfarray.make_surface(image)
            self.image = self.engine.transform.scale(self.image, self.screen_dim)
        elif self.engine_type == EngineTypes.PIL:
            self.image = self.engine.fromarray(image)
            self.image = self.image.resize(self.screen_dim)
        return self.image

    def read_image(self, image_path: Optional[Path] = None):
        if self.engine_type == EngineTypes.PYGAME:
            if image_path is not None and image_path.exists():
                self.image = self.engine.image.load(str(image_path))
            else:
                # Create a blank image if the path is invalid or not provided
                self.image = np.zeros(
                    (self.screen_dim[1], self.screen_dim[0], 3), dtype=np.uint8
                )
                self.image = self.engine.surfarray.make_surface(self.image)

            self.image.set_alpha(255)
            self.image = self.engine.transform.scale(self.image, self.screen_dim)
            blank_image = self.engine.surfarray.make_surface(
                np.zeros((self.screen_dim[1], self.screen_dim[0], 3), dtype=np.uint8)
            )
            blank_image.set_alpha(255)
            self.blank_image = self.engine.transform.scale(blank_image, self.screen_dim)

        elif self.engine_type == EngineTypes.PIL:
            if image_path is not None and image_path.exists():
                self.image = self.engine.open(image_path)
            else:
                # Create a blank image if the path is invalid or not provided
                self.image = np.zeros(
                    (self.screen_dim[1], self.screen_dim[0], 3), dtype=np.uint8
                )
                self.image = self.engine.fromarray(self.image)
            self.image = self.image.resize(self.screen_dim)
            blank_image = self.engine.new("RGBA", self.screen_dim, (0, 0, 0, 0))
            self.blank_image = blank_image

    def paint_sprite(self, sprite):
        """
        A method to paint a sprite.

        Args:
        - sprite: The sprite to paint.

        Returns:
        - The painted sprite (Pygame Surface or PIL Image).
        """
        # Resize the opacity mask to match the sprite dimensions
        resized_opacity_mask = cv2.resize(
            sprite.opacity_mask,
            (sprite.width, sprite.height),
            interpolation=cv2.INTER_NEAREST,
        )

        if self.engine_type == EngineTypes.PYGAME:
            surface = self.engine.Surface(
                (sprite.width, sprite.height), self.engine.SRCALPHA
            )
            for x in range(sprite.width):
                for y in range(sprite.height):
                    alpha = int(resized_opacity_mask[y, x])
                    color = (*sprite.color, alpha)
                    surface.set_at((x, y), color)
            return surface

        elif self.engine_type == EngineTypes.PIL:
            from PIL import Image, ImageDraw

            surface = Image.new("RGBA", (sprite.width, sprite.height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(surface)
            for x in range(sprite.width):
                for y in range(sprite.height):
                    alpha = int(
                        resized_opacity_mask[y, x]
                    )  # Ensure alpha is an integer
                    color = tuple(map(int, sprite.color)) + (
                        alpha,
                    )  # Ensure all components are integers
                    draw.point((x, y), fill=color)
            return surface

    def end(self):
        if self.engine_type == EngineTypes.PYGAME:
            self.engine.quit()
        elif self.engine_type == EngineTypes.PIL:
            pass
