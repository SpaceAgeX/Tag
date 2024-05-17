import pygame
from utils import Player, Platform
import random

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

surf = pygame.Surface((50, 50))
surf.fill("green")


platforms = []

for i in range(10):
    platform = Platform.from_rect(screen, pygame.Rect(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), random.randrange(40, 100), 30), "blue")
    platforms.append(platform)


class TagPlayer(Player):
    def __init__(self, screen, surf, platforms, opponents: list[Player]):
        super().__init__(screen, surf, platforms)
        self.opponents = opponents
        self.it = False
    
    @staticmethod
    def empty():
        return TagPlayer(None, pygame.Surface((1,1)), [], [])

    def update(self):
        super().update()

        opponent_rects = list(map(lambda o: o.rect, self.opponents))
        if self.rect.collideobjects(opponent_rects):
            pass


player = TagPlayer.empty()
player2 = TagPlayer.empty()

player = TagPlayer(screen, surf, platforms, [player2])
player.controls = "wasd"

player2 = TagPlayer(screen, surf, platforms, [player])
player2.rect.topleft = (WIDTH/2, HEIGHT/2)
player2.controls = "arrow_keys"


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    player.update()
    player2.update()

    for platform in platforms:
        platform.draw()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
