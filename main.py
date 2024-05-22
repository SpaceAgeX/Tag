import pygame
from utils import Player, Platform, TagSybol
from mapbuilder import Map
import random

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

player1_surf = pygame.Surface((50, 50))
player1_surf.fill((162, 62, 140))#pygame.image.load('Assets/sammy.png').convert_alpha()

player2_surf = pygame.Surface((50, 50))
player2_surf.fill((162, 62, 140))

TagSybolImage = pygame.image.load('Assets/TagSybol.png').convert_alpha()



def set_all_players(players):
    for player in players:
        player.set_players(players)
    
    chosen_index = random.randrange(0, len(players))
    players[chosen_index].set_it(True)
    #print(chosen_index)


class TagPlayer(Player):
    def __init__(self, screen, surf, platforms):
        super().__init__(screen, surf, platforms)
        self.opponents = None
        self.it = False
        self.id = random.random()
        self.collided = False
        self.sybol = TagSybol(TagSybolImage)


    def set_it(self, value):
        if value == True:
            self.it = True
            
        else:
            self.it = False
           
    

    def set_players(self, players):
        self.opponents = list(filter(lambda p: p.id != self.id, players))
    

    def update(self):
        super().update()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        opponent_rects = list(map(lambda o: o.rect, self.opponents))
        if self.it:
            self.sybol.draw(screen , (self.rect.midtop[0] - (self.sybol.image.get_width()/2), self.rect.midtop[1]- 32))
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
        

def main():
    current_map = Map.from_json("Assets/maps/default_map.json")
    current_map.generate_platforms()
    platforms = current_map.platforms


    player1 = TagPlayer(screen, player1_surf, platforms)

    player1.rect.topleft = ((WIDTH/2)- 128, (HEIGHT/2)-128)
    player1.controls = "wasd"

    player2 = TagPlayer(screen, player2_surf, platforms)
    player2.rect.topleft = ((WIDTH/2 + 128), (HEIGHT/2)-128)
    player2.controls = "arrow_keys"

    players = [player1, player2]
    set_all_players(players)

    running = True
    
   
    while running:    
        clock.tick(60)

        screen.fill((115,190,211))

        screen.blit((pygame.font.SysFont('arial', 30).render(str(int(clock.get_fps())), 1, pygame.Color((255,255,255)))), (0, 0))


        player1.update()
        player2.update()

        for platform in platforms:
            platform.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key==pygame.K_w:
                    player1.readyJump = True
                    player1.canJump = False
                if event.key==pygame.K_UP:
                    player2.readyJump = True
                    player2.canJump = False
            if event.type == pygame.KEYDOWN:
                if event.key==pygame.K_w and player1.readyJump:
                    player1.canJump = True
                    player1.readyJump = False
                if event.key==pygame.K_UP and player2.readyJump:
                    player2.canJump = True
                    player2.readyJump = False



        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()