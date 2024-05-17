import pygame
from utils import Player, Platform
import random

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()
running = True

player1_surf = pygame.Surface((50, 50))
player1_surf.fill("indigo")
player2_surf = pygame.Surface((30, 50))
player2_surf.fill("indigo")


platforms = []

for i in range(10):
    platform = Platform.from_rect(screen, pygame.Rect(random.randrange(0, WIDTH), random.randrange(0, HEIGHT), random.randrange(40, 100), 30), "darkgreen")
    platforms.append(platform)


def set_all_players(players):
    for player in players:
        player.set_players(players)
    
    chosen_index = random.randrange(0, len(players))
    players[chosen_index].set_it(True)
    print(chosen_index)


class TagPlayer(Player):
    def __init__(self, screen, surf, platforms):
        super().__init__(screen, surf, platforms)
        self.opponents = None
        self.it = False
        self.id = random.random()
        self.collided = False
    

    def set_it(self, value):
        if value == True:
            self.it = True
            self.surf.fill("red")
        else:
            self.it = False
            self.surf.fill("indigo")
    

    def set_players(self, players):
        self.opponents = list(filter(lambda p: p.id != self.id, players))
    

    def update(self):
        super().update()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        opponent_rects = list(map(lambda o: o.rect, self.opponents))

        if self.rect.collideobjects(opponent_rects):
            if self.collided == False:
                self.collided = True

                if self.it:
                    self.set_it(False)
                else:
                    self.set_it(True)
        else:
            self.collided = False

        # Debugging
        if mouse_clicked:
            print(f"It ({self.id}): ", self.it)
        


player1 = TagPlayer(screen, player1_surf, platforms)
player1.controls = "wasd"

player2 = TagPlayer(screen, player2_surf, platforms)
player2.rect.topleft = (WIDTH/2, HEIGHT/2)
player2.controls = "arrow_keys"

players = [player1, player2]
set_all_players(players)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("deepskyblue3")

    player1.update()
    player2.update()

    for platform in platforms:
        platform.draw()

    pygame.display.update()
    clock.tick(60)


pygame.quit()
