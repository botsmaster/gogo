import os
import pygame
from pygame.math import Vector2

import config
from snake import load_cube_image

class LooseCube:
    def __init__(self, value, pos):
        self.value = value
        self.pos = Vector2(pos)
        self.image = load_cube_image(value)
        self.rect = self.image.get_rect(center=self.pos)

    def draw(self, surface):
        self.rect = self.image.get_rect(center=self.pos)
        surface.blit(self.image, self.rect)
