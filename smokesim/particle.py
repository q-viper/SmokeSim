from smokesim.base import BaseSim, BaseProperty
from smokesim.constants import CLOUD_MASK

import pygame
import cv2
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
        self.sprite_paint = self.make_sprite()

    @property
    def position(self):
        return (self.x, self.y)

    def paint_sprite(self, sprite: Sprite) -> pygame.Surface:
        """
        A method to paint a sprite.

        Args:
        - sprite (Sprite): The sprite to paint.

        Returns:
        - pygame.Surface: The painted sprite.
        """
        surface = pygame.Surface((sprite.width, sprite.height), pygame.SRCALPHA)
        pixels = pygame.PixelArray(surface)
        opacities = cv2.resize(
            sprite.opacity_mask,
            (sprite.width, sprite.height),
            interpolation=cv2.INTER_NEAREST,
        )
        for x in range(sprite.width):
            for y in range(sprite.height):
                pixels[x, y] = (*sprite.color, opacities[x, y])
        del pixels
        # surface = pygame.transform.smoothscale(
        #     surface, (sprite.width // 2, sprite.height // 2)
        # )
        surface = pygame.transform.smoothscale(surface, (sprite.width, sprite.height))
        self.surface = surface
        return surface

    def make_sprite(self) -> pygame.Surface:
        """
        A method to make a sprite.

        Returns:
        - pygame.Surface: The sprite.
        """
        self.sprite = Sprite(
            color=self.color,
            width=self.scale,
            height=self.scale,
        )
        self.sprite_paint = self.paint_sprite(self.sprite)
        return self.sprite_paint

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
        # if self.scale > :
        # self.sprite.width = int(self.smoke_sprite_size * self.scale)
        # self.sprite.height = int(self.smoke_sprite_size * self.scale)
        # if self.sprite.width < 1 or self.sprite.height < 1:
        #     self.is_alive = False

        # surface = pygame.transform.smoothscale(
        #     self.surface, (self.sprite.width // 2, self.sprite.height // 2)
        # )
        surface = pygame.transform.smoothscale(self.surface, (height, width))
        self.sprite_paint = surface

    def draw(self, screen):
        """
        A method to draw the particle.

        Args:
        - screen (pygame.Surface): The screen to draw the particle on.
        """
        if self.is_alive:
            self.sprite_paint.set_alpha(self.alpha)
            screen.blit(self.sprite_paint, (int(self.x), int(self.y)))

        if (
            self.x < 0
            or self.y < 0
            or self.x > screen.get_width()
            or self.y > screen.get_height()
        ):
            self.is_alive = False

    def __del__(self):
        try:
            del self.sprite_paint
            del self.sprite
            del self.surface
        except AttributeError:
            pass
