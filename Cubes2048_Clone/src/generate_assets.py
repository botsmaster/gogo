"""Generate placeholder cube images for Cubes 2048 clone."""
import os
import pygame
from config import CUBE_COLORS, IMAGE_DIR, FONT_NAME

pygame.init()
FONT = pygame.font.Font(FONT_NAME, 32)

SIZE = 64
os.makedirs(IMAGE_DIR, exist_ok=True)

for value, color in CUBE_COLORS.items():
    surf = pygame.Surface((SIZE, SIZE), pygame.SRCALPHA)
    surf.fill(color)
    pygame.draw.rect(surf, (0, 0, 0), surf.get_rect(), 2)
    text = FONT.render(str(value), True, (0, 0, 0))
    rect = text.get_rect(center=(SIZE//2, SIZE//2))
    surf.blit(text, rect)
    pygame.image.save(surf, os.path.join(IMAGE_DIR, f"cube_{value}.png"))
print("Assets generated in", IMAGE_DIR)
