import pygame
import os
from pygame.math import Vector2
from random import choice, random

import config


def load_cube_image(value):
    path = os.path.join(config.IMAGE_DIR, f"cube_{value}.png")
    if not os.path.exists(path):
        # Generate a simple surface on the fly
        surf = pygame.Surface((64, 64), pygame.SRCALPHA)
        color = config.CUBE_COLORS.get(value, (200, 200, 200))
        surf.fill(color)
        pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
        font = pygame.font.Font(config.FONT_NAME, 32)
        text = font.render(str(value), True, (0, 0, 0))
        rect = text.get_rect(center=(32, 32))
        surf.blit(text, rect)
        pygame.image.save(surf, path)
    return pygame.image.load(path).convert_alpha()


class Segment:
    def __init__(self, value, pos):
        self.value = value
        self.pos = Vector2(pos)

    @property
    def image(self):
        return load_cube_image(self.value)


class Snake:
    def __init__(self, value, pos):
        self.segments = [Segment(value, pos)]
        self.direction = Vector2(1, 0)
        self.speed = config.SNAKE_SPEED
        self.boost = False
        self.target = Vector2(pos)

    def head(self):
        return self.segments[0]

    def update(self, dt):
        speed = self.speed * (config.BOOST_MULTIPLIER if self.boost else 1)
        head = self.head()
        direction = (self.target - head.pos)
        if direction.length() != 0:
            direction = direction.normalize()
        move = direction * speed * dt
        head.pos += move
        # keep segments following
        for i in range(1, len(self.segments)):
            prev = self.segments[i-1]
            seg = self.segments[i]
            dist = prev.pos.distance_to(seg.pos)
            if dist > config.SEGMENT_DISTANCE:
                seg.pos += (prev.pos - seg.pos).normalize() * (dist - config.SEGMENT_DISTANCE)

    def draw(self, surface):
        for seg in reversed(self.segments):
            img = seg.image
            rect = img.get_rect(center=seg.pos)
            surface.blit(img, rect)

    def set_target(self, pos):
        self.target = Vector2(pos)

    def add_cube(self, value):
        tail = self.segments[-1]
        new_seg = Segment(value, tail.pos)
        self.segments.append(new_seg)
        self.merge_segments()

    def merge_segments(self):
        merged = True
        while merged:
            merged = False
            for i in range(len(self.segments)-1, 0, -1):
                if self.segments[i].value == self.segments[i-1].value:
                    self.segments[i-1].value *= 2
                    del self.segments[i]
                    merged = True
                    break

    def get_score(self):
        return self.head().value


class AISnake(Snake):
    def __init__(self, value, pos, world_rect):
        super().__init__(value, pos)
        self.world_rect = world_rect
        self.change_dir_time = 0

    def update(self, dt, loose_cubes, player_head_value):
        self.change_dir_time -= dt
        if self.change_dir_time <= 0:
            # random new target
            if loose_cubes and random() < 0.7:
                cube = choice(loose_cubes)
                self.set_target(cube.pos)
            else:
                x = random() * self.world_rect.width + self.world_rect.left
                y = random() * self.world_rect.height + self.world_rect.top
                self.set_target((x, y))
            self.change_dir_time = 1.0 + random()*2
        super().update(dt)
        # clamp to world
        head = self.head()
        head.pos.x = max(self.world_rect.left, min(head.pos.x, self.world_rect.right))
        head.pos.y = max(self.world_rect.top, min(head.pos.y, self.world_rect.bottom))
