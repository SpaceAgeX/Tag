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


player = Player(screen, surf, platforms)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    player.update()
    for platform in platforms:
        platform.draw()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
