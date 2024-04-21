import time
import pygame_gui
import pygame
import cv2
import random
import numpy as np
from dataclasses import dataclass
from constants import CLOUD_MASK
from typing import Optional, Tuple, List


def float_in_range(start, end):
    return start + random.random() * (end - start)


@dataclass
class Sprite:
    width: int = 20
    height: int = 20
    opacity_mask: np.ndarray = CLOUD_MASK
    color: tuple = (255, 255, 255)


class Particle:
    def __init__(self, x: int, y: int, vx: Optional[float] = None,
                 startvy: Optional[float] = None, scale: Optional[float] = None,
                 lifetime: Optional[int] = None, age: int = 0,
                 min_vx: float = -4/100, max_vx: float = 4/100,
                 min_vy: float = -4/10, max_vy: float = -1/10,
                 min_scale: int = 20, max_scale: int = 40,
                 min_lifetime: float = 2000, max_lifetime: float = 8000,
                 color: Tuple[float, float, float] = (167, 167, 167),
                 smoke_sprite_size: int = 20, fade_speed: int = 1
                 ):
        self.x = x
        self.y = y
        self.vx = vx if vx is not None else float_in_range(min_vx, max_vx)
        self.startvy = startvy if startvy is not None else float_in_range(
            min_vy, max_vy)
        self.scale = smoke_sprite_size if scale is not None else float_in_range(
            min_scale, max_scale)
        self.lifetime = lifetime if lifetime is not None else float_in_range(
            min_lifetime, max_lifetime)
        self.age = age
        self.color = color
        self.smoke_sprite_size = smoke_sprite_size
        self.final_scale = float_in_range(self.scale * 0.1,
                                          self.scale*1.5)
        self.scale_step = (self.final_scale - self.scale) / self.lifetime

        self.vy = self.startvy
        self.alpha = 255
        self.fade_speed = fade_speed
        self.is_alive = True
        self.sprite_paint = self.make_sprite()

    def paint_sprite(self, sprite: Sprite) -> pygame.Surface:
        surface = pygame.Surface(
            (sprite.width, sprite.height), pygame.SRCALPHA)
        pixels = pygame.PixelArray(surface)
        opacities = cv2.resize(
            sprite.opacity_mask, (sprite.width, sprite.height), interpolation=cv2.INTER_NEAREST)
        for x in range(sprite.width):
            for y in range(sprite.height):
                pixels[x, y] = (*sprite.color, opacities[x, y])
        del pixels
        surface = pygame.transform.smoothscale(
            surface, (sprite.width // 2, sprite.height // 2))
        surface = pygame.transform.smoothscale(
            surface, (sprite.width, sprite.height))
        self.surface = surface
        return surface

    def make_sprite(self):
        self.sprite = Sprite(
            color=self.color, width=self.smoke_sprite_size, height=self.smoke_sprite_size)
        self.sprite_paint = self.paint_sprite(self.sprite)
        return self.sprite_paint

    def update(self, time: float = 1):
        self.age += time
        self.x += self.vx * time
        self.y += self.vy * time
        frac = (self.age / self.lifetime) ** 0.5
        self.vy = (1 - frac) * self.startvy
        self.scale += time * self.scale_step
        self.alpha -= self.fade_speed
        if self.alpha < 0 or self.age > self.lifetime or self.scale < 1:
            self.is_alive = False
        if self.scale > 1:
            self.sprite.width = int(self.scale)
            self.sprite.height = int(self.scale)
            if self.sprite.width < 1 or self.sprite.height < 1:
                self.is_alive = False

            surface = pygame.transform.smoothscale(
                self.surface, (self.sprite.width // 2, self.sprite.height // 2))
            surface = pygame.transform.smoothscale(
                self.surface, (self.sprite.width, self.sprite.height))
            self.sprite_paint = surface
            pass

    def draw(self, screen):
        self.sprite_paint.set_alpha(self.alpha)
        screen.blit(self.sprite_paint, (int(self.x), int(self.y)))

    def __del__(self):
        del self.sprite_paint
        del self.sprite
        del self.surface
