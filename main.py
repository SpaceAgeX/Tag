import pygame
from player import Player, TagSybol, TagPlayer
from platform_class import Platform
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
player2_surf.fill((165, 48, 48))

TagSybolImage = pygame.image.load('Assets/TagSybol.png').convert_alpha()



def set_all_players(players):
    for player in players:
        player.set_players(players)
    
    chosen_index = random.randrange(0, len(players))
    players[chosen_index].set_it(True)
    #print(chosen_index)




def main():
    current_map = Map.from_json("Assets/maps/big_map.json")
    current_map.generate_platforms()
    platforms = current_map.platforms


    player1 = TagPlayer((WIDTH/2)- 128, (HEIGHT/2)-128, 50, 50, "wasd", player1_surf, TagSybolImage)
    player2 = TagPlayer((WIDTH/2)+ 128, (HEIGHT/2)-128, 50, 50, "arrow_keys", player2_surf, TagSybolImage)
    players = [player1, player2]
    set_all_players(players)

    running = True
    
   
    while running:    
        clock.tick(60)

        screen.fill((115,190,211))

        screen.blit((pygame.font.SysFont('arial', 30).render(str(int(clock.get_fps())), 1, pygame.Color((255,255,255)))), (0, 0))


        player1.update(screen,platforms)
        player2.update(screen,platforms)

        for platform in platforms:
            platform.draw()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.jump()
                if event.key == pygame.K_UP:
                    player2.jump()

            

            if event.type == pygame.QUIT:
                running = False


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()