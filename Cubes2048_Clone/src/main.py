import pygame
import random
from pygame.math import Vector2

import config
from snake import Snake, AISnake
from objects import LooseCube


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("Cubes 2048 Clone")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(config.FONT_NAME, 24)
        self.world_rect = pygame.Rect(40, 40, config.SCREEN_WIDTH-80, config.SCREEN_HEIGHT-80)
        self.reset()

    def reset(self):
        self.player = Snake(2, self.world_rect.center)
        self.ais = [AISnake(2, (random.randint(self.world_rect.left, self.world_rect.right),
                                random.randint(self.world_rect.top, self.world_rect.bottom)), self.world_rect)
                    for _ in range(3)]
        self.loose_cubes = []
        self.spawn_timer = 0
        self.game_over = False

    def spawn_cube(self):
        value = random.choice([2, 4])
        x = random.randint(self.world_rect.left, self.world_rect.right)
        y = random.randint(self.world_rect.top, self.world_rect.bottom)
        self.loose_cubes.append(LooseCube(value, (x, y)))

    def handle_collisions(self):
        # player with loose cubes
        head_rect = self.player.head().image.get_rect(center=self.player.head().pos)
        for cube in self.loose_cubes[:]:
            if head_rect.colliderect(cube.rect):
                if cube.value == self.player.head().value:
                    self.player.head().value *= 2
                else:
                    self.player.add_cube(cube.value)
                self.loose_cubes.remove(cube)

        # player with boundaries
        if not self.world_rect.contains(head_rect):
            self.game_over = True
            return

        # collisions with AI
        for ai in self.ais[:]:
            ai_head_rect = ai.head().image.get_rect(center=ai.head().pos)
            # player hits ai
            for seg in ai.segments:
                seg_rect = seg.image.get_rect(center=seg.pos)
                if head_rect.colliderect(seg_rect):
                    if self.player.head().value >= seg.value:
                        # destroy ai
                        for seg2 in ai.segments:
                            self.loose_cubes.append(LooseCube(seg2.value, seg2.pos))
                        self.ais.remove(ai)
                    else:
                        self.game_over = True
                    return

            # ai hits player
            player_segments = self.player.segments
            for seg in player_segments:
                seg_rect = seg.image.get_rect(center=seg.pos)
                if ai_head_rect.colliderect(seg_rect):
                    if ai.head().value >= seg.value:
                        self.game_over = True
                        return
                    else:
                        for seg2 in ai.segments:
                            self.loose_cubes.append(LooseCube(seg2.value, seg2.pos))
                        self.ais.remove(ai)
                        break

    def update(self, dt):
        if self.game_over:
            return
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_cube()
            self.spawn_timer = 1.0
        mx, my = pygame.mouse.get_pos()
        self.player.set_target((mx, my))
        self.player.boost = pygame.mouse.get_pressed()[0]
        self.player.update(dt)
        for ai in self.ais:
            ai.update(dt, self.loose_cubes, self.player.head().value)
        self.handle_collisions()

    def draw_background(self):
        self.screen.fill(config.BG_COLOR)
        for x in range(self.world_rect.left, self.world_rect.right, 40):
            pygame.draw.line(self.screen, config.GRID_COLOR, (x, self.world_rect.top), (x, self.world_rect.bottom))
        for y in range(self.world_rect.top, self.world_rect.bottom, 40):
            pygame.draw.line(self.screen, config.GRID_COLOR, (self.world_rect.left, y), (self.world_rect.right, y))
        pygame.draw.rect(self.screen, (80, 80, 80), self.world_rect, 2)

    def draw(self):
        self.draw_background()
        for cube in self.loose_cubes:
            cube.draw(self.screen)
        for ai in self.ais:
            ai.draw(self.screen)
            name = self.font.render("AI", True, config.TEXT_COLOR)
            rect = name.get_rect(center=(ai.head().pos.x, ai.head().pos.y-40))
            self.screen.blit(name, rect)
        self.player.draw(self.screen)
        name = self.font.render("You", True, config.TEXT_COLOR)
        rect = name.get_rect(center=(self.player.head().pos.x, self.player.head().pos.y-40))
        self.screen.blit(name, rect)

        score = self.font.render(f"Score: {self.player.get_score()}", True, config.TEXT_COLOR)
        self.screen.blit(score, (10, 10))
        # leaderboard
        entries = [("You", self.player.get_score())] + [("AI", ai.get_score()) for ai in self.ais]
        entries.sort(key=lambda e: e[1], reverse=True)
        for i, (name_txt, val) in enumerate(entries[:3]):
            text = self.font.render(f"{i+1}. {name_txt} {val}", True, config.TEXT_COLOR)
            rect = text.get_rect(topright=(config.SCREEN_WIDTH-10, 10 + i*25))
            self.screen.blit(text, rect)

        if self.game_over:
            overlay = self.font.render("GAME OVER - Press R", True, (255,0,0))
            rect = overlay.get_rect(center=(config.SCREEN_WIDTH//2, config.SCREEN_HEIGHT//2))
            self.screen.blit(overlay, rect)

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(config.FPS) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and self.game_over and event.key == pygame.K_r:
                    self.reset()
            self.update(dt)
            self.draw()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    Game().run()
