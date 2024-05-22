import pygame
import math
import random

class TagSybol():

    def __init__(self, image):
        self.image = image

    def draw(self, surface, pos):
        surface.blit(self.image, pos)

   

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, controls, surf):
        super().__init__()

        self.image = surf
        
        self.rect = self.image.get_rect(topleft=(x, y))

        self.controls = controls

        self.vel_y = 0  
        self.vel_x = 0  

        self.speed = 7
        self.run_progress = 0
        self.acceleration = 0.5
        self.accelerating = True

        self.on_ground = False  
        self.jump_power = 16
        self.gravity_strength = 0.5

    def jump(self):
        if self.on_ground:  # Only jump if on the ground
            self.vel_y = -self.jump_power  # Upwards velocity
            self.on_ground = False

   
    def update(self, screen, platforms):


        keys = pygame.key.get_pressed()

        key_left = keys[pygame.K_a] if self.controls == "wasd" else keys[pygame.K_LEFT]
        key_right = keys[pygame.K_d] if self.controls == "wasd" else keys[pygame.K_RIGHT]
        

        if key_left == True:
            self.accelerating = True
            self.vel_x = -1*self.speed

        elif key_right == True:
            self.accelerating = True
            self.vel_x = 1*self.speed

        else:
            self.accelerating = False
            self.vel_x = 0



        self.vel_y += self.gravity_strength  
        if self.vel_y > 2.5:
            self.on_ground = False

        # Check vertical collisions
        self.rect.y += self.vel_y
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.vel_y = 0
                elif self.vel_y < 0:  # Moving up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Check horizontal collisions
        self.rect.x += self.vel_x
        for platform in platforms:
            if pygame.sprite.collide_rect(self, platform):
                if self.vel_x > 0:  # Moving right
                    self.rect.right = platform.rect.left
                    self.vel_x = 0
                elif self.vel_x < 0:  # Moving left
                    self.rect.left = platform.rect.right
                    self.vel_x = 0
        screen.blit(self.image, self.rect.topleft)





class TagPlayer(Player):
    def __init__(self, x, y, width, height, controls, surf, TagSybolImage):
        super().__init__(x, y, width, height, controls, surf)
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
    

    def update(self, screen, platforms):
        super().update(screen, platforms)
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
        