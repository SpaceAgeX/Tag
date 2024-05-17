import pygame

class Player:
    def __init__(self, rendering_screen, player_surf, platforms):
        self.surf = player_surf
        self.rect = player_surf.get_rect()
        self.screen = rendering_screen
        self.platforms = platforms

        self.speed = 3
        
        self.jumping = False
        self.jump_power = 10
        self.jump_progress = 0


    def draw(self):
        self.screen.blit(self.surf, self.rect)


    def is_on_floor(self):
        rects = list(map(lambda p: p.get_top(), self.platforms)) # Rects of all Platforms in Environment

        if rect := self.rect.collideobjects(rects):
            #self.rect.bottom = rect.top+1
            return True
        elif self.rect.bottom >= self.screen.get_height():
            return True
        else:
            return False
    

    def update_jump(self):
        self.rect.move_ip(0, -self.jump_power+self.jump_progress)
        self.jump_progress += 0.25

        if self.is_on_floor():
            self.jumping = False
            self.jump_progress = 0
    

    def update(self):
        self.draw()
        keys = pygame.key.get_pressed()
        mouse_clicked = pygame.mouse.get_pressed()[0]

        # Debugging
        if mouse_clicked:
            print("Jumping: ", self.jumping)
            print("Jump Progress: ", self.jump_progress)
            print("On Floor: ", self.is_on_floor())

        # Gravity
        if self.jumping == False and self.is_on_floor() == False:
            self.jump_progress = self.jump_power # Only Do the Descending Portion of the Jump
            self.jumping = True

        # Jumping
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            self.jumping = True

        if self.jumping:
            self.update_jump()
        
        # Player Movement
        if keys[pygame.K_a] == True:
            self.rect.move_ip(-self.speed, 0)
        elif keys[pygame.K_d] == True:
            self.rect.move_ip(self.speed, 0)
        
        # Bottom Collision
        rects = list(map(lambda p: p.get_bottom(), self.platforms))
        if self.rect.collideobjects(rects):
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
        top_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.w, 2)
        return top_rect
    

    def get_bottom(self):
        rect = pygame.Rect(self.rect.x, self.rect.y+self.rect.h-2, self.rect.w, 2)
        return rect


    def draw(self):
        self.screen.blit(self.surf, self.rect)
    

    def update():
        pass

