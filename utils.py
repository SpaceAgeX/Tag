import pygame
import math

class Player:
    def __init__(self, rendering_screen, player_surf, platforms):
        self.surf = player_surf
        self.rect = player_surf.get_rect()
        self.screen = rendering_screen
        self.platforms = platforms

        # Running Variables
        self.acceleration = 0.5
        self.accelerating = True
        self.running = False
        self.speed = 7
        self.run_progress = 0
        self.direction = 0
        
        # Jumping Variables
        self.gravity_strength = 0.5
        self.jumping = False
        self.jump_power = 16
        self.jump_progress = 0
        self.canJump = False
        self.readyJump = True

        self.controls = "wasd" # "arrow_keys" or "wasd"


    def draw(self):
        self.screen.blit(self.surf, self.rect)


    def is_on_floor(self):
        rects = list(map(lambda p: p.get_top(), self.platforms)) # Rects of all Platforms in Environment

        if self.rect.collideobjects(rects):
            return True
        elif self.rect.bottom >= self.screen.get_height():
            self.rect.bottom = self.screen.get_height()
            return True
        else:
            return False
    

    def update_jump(self):
        self.rect.move_ip(0, -self.jump_power+self.jump_progress)
        self.jump_progress += self.gravity_strength

        if self.is_on_floor():
            self.jumping = False
            self.jump_progress = 0
    

    def update_run(self):
        self.rect.move_ip(self.direction*self.run_progress, 0)

        if self.accelerating: self.run_progress += self.acceleration
        else: self.run_progress -= self.acceleration

        if self.run_progress > self.speed:
            self.run_progress = self.speed
        
        if self.run_progress < 0:
            self.run_progress = 0
            self.running = False
    

    def update(self):
        self.draw()
        keys = pygame.key.get_pressed()
        key_left = keys[pygame.K_a] if self.controls == "wasd" else keys[pygame.K_LEFT]
        key_right = keys[pygame.K_d] if self.controls == "wasd" else keys[pygame.K_RIGHT]
        key_up = self.canJump 
        

        mouse_clicked = pygame.mouse.get_pressed()[0]
    
        if self.jumping:
            self.update_jump()
        
        if self.running:
            self.update_run()

        # Debugging
        # if mouse_clicked:
        #     print("Jumping: ", self.jumping)
        #     print("Jump Progress: ", self.jump_progress)
        #     print("On Floor: ", self.is_on_floor())

        # Gravity
        if self.jumping == False and self.is_on_floor() == False:
            self.jump_progress = self.jump_power # Only Do the Descending Portion of the Jump
            self.jumping = True

        
        # Player Movement
        if key_left == True:
            if self.direction == 1: self.run_progress = 0
            self.running = True
            self.accelerating = True
            self.direction = -1
            
        elif key_right == True:
            if self.direction == -1: self.run_progress = 0
            self.running = True
            self.accelerating = True
            self.direction = 1
        else:
            self.accelerating = False
        if key_up:
            self.jumping = True
        

        # Platform Collision
        top_rects = list(map(lambda p: p.get_top(), self.platforms))
        bottom_rects = list(map(lambda p: p.get_bottom(), self.platforms))
        left_rects = list(map(lambda p: p.get_left(), self.platforms))
        right_rects = list(map(lambda p: p.get_right(), self.platforms))

        if rect := self.rect.collideobjects(left_rects):
            if abs(self.rect.right - rect.left) < self.speed+1:
                self.rect.right = rect.left-1

        if rect := self.rect.collideobjects(right_rects):
            if abs(self.rect.left - rect.right) < self.speed+1:
                self.rect.left = rect.right+1

        if rect := self.rect.collideobjects(top_rects):
            if abs(self.rect.bottom - rect.top) < self.speed+1:
                self.rect.bottom = rect.top+1

        if rect := self.rect.collideobjects(bottom_rects):
            self.rect.top = rect.bottom+1
            self.jump_progress = self.jump_power
            self.jumping = True
        self.canJump = False
        


class Platform:
    def __init__(self, screen, surf, pos):
        self.surf = surf
        self.rect = pygame.Rect(pos[0], pos[1], surf.get_width(), surf.get_height()-16)
        self.screen = screen
        self.pos = (pos[0], pos[1]- 5)
        self.direction = 1
    

    
    


    def get_top(self):
        top_rect = pygame.Rect(self.rect.x+2, self.rect.y, self.rect.w-4, 2)
        return top_rect
    

    def get_bottom(self):
        rect = pygame.Rect(self.rect.x+2, self.rect.y+self.rect.h-2, self.rect.w-4, 2)
        return rect

    def get_left(self):
        rect = pygame.Rect(self.rect.x, self.rect.y+2, 2, self.rect.h-4)
        return rect


    def get_right(self):
        rect = pygame.Rect(self.rect.x+self.rect.w-2, self.rect.y+2, 2, self.rect.h-4)
        return rect


    def draw(self):
        self.screen.blit(self.surf, self.pos)
    

    def update(self):
        self.rect.move_ip(self.direction, 0)

