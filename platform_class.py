import pygame
import math




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