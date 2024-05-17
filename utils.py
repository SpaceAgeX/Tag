import pygame
import math

class Player:
    def __init__(self, rendering_screen, player_surf, platforms):
        self.surf = player_surf
        self.rect = player_surf.get_rect()
        self.screen = rendering_screen
        self.platforms = platforms

        self.speed = 7
        self.gravity_strength = 0.25
        
        self.jumping = False
        self.jump_power = 10
        self.jump_progress = 0

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
    

    def update(self):
        self.draw()
        keys = pygame.key.get_pressed()
        mouse_clicked = pygame.mouse.get_pressed()[0]
    
        if self.jumping:
            self.update_jump()

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
        if self.controls == "wasd":
            if keys[pygame.K_a] == True:
                self.rect.move_ip(-self.speed, 0)
            elif keys[pygame.K_d] == True:
                self.rect.move_ip(self.speed, 0)
            if keys[pygame.K_SPACE] or keys[pygame.K_w]:
                self.jumping = True
        elif self.controls == "arrow_keys":
            if keys[pygame.K_LEFT] == True:
                self.rect.move_ip(-self.speed, 0)
            elif keys[pygame.K_RIGHT] == True:
                self.rect.move_ip(self.speed, 0)
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
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
        


class Platform:
    def __init__(self, screen, surf):
        self.surf = surf
        self.rect = surf.get_rect()
        self.screen = screen
    
    
    @staticmethod
    def from_rect(screen, rect: pygame.Rect, color):
        surf = pygame.Surface((rect.w, rect.h))
        platform = Platform(screen, surf)
        platform.surf.fill(color)
        platform.rect.x = rect.x
        platform.rect.y = rect.y
        return platform


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
        self.screen.blit(self.surf, self.rect)
    

    def update():
        pass

