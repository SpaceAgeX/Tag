import pygame
import math

class TagSybol():

    def __init__(self, image):
        self.image = image

    def draw(self, surface, pos):
        surface.blit(self.image, pos)


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

        # for event in events:
        #     if event.type == pygame.KEYUP:
        #         if (self.controls == "wasd" and event.key == pygame.K_w):
        #             self.readyJump = True
        #             self.canJump = False
        #         if (self.controls == "arrow_keys" and event.key == pygame.K_UP):
        #             self.readyJump = True
        #             self.canJump = False
        #     if event.type == pygame.KEYDOWN:
        #         if self.readyJump and  (self.controls == "wasd" and event.key == pygame.K_w): 
        #             self.canJump = True
        #             self.readyJump = False
        #         if self.readyJump and  (self.controls == "arrow_keys" and event.key == pygame.K_UP):
        #             self.canJump = True
        #             self.readyJump = False

    
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
        pass


class UIElement:
    def __init__(self, pos: tuple, dimensions: tuple):
        self.x = pos[0]
        self.y = pos[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, "black", self.rect)



class ColorPanel(UIElement):
    def __init__(self, pos: tuple, dimensions: tuple, color: pygame.Color):
        super().__init__(pos, dimensions)
        self.color = color


    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)



class Button(UIElement):
    def __init__(self, pos: tuple, dimensions: tuple, bg_color: pygame.Color, action):
        super().__init__(pos, dimensions)
        self.bg_color = bg_color

        self.click_action = action
        self.mouse_released = True

        self.text = ""
        self.text_color = (0, 0, 0)
        self.text_placement = "center"
        self.font = pygame.font.Font(None)

        self.surface = None
        

    def display(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.bg_color, self.rect)

        if self.surface != None:
            screen.blit(self.surface, self.rect)


        if self.text != "":
            text_surf = self.font.render(self.text, True, self.text_color, self.bg_color, self.width)
            text_rect = text_surf.get_rect()
            
            # Explanation of Line Below: (IF self.text_placement = "midleft" THEN text_rect.midleft = self.rect.midleft)
            setattr(text_rect, self.text_placement, getattr(self.rect, self.text_placement))
            screen.blit(text_surf, text_rect.topleft)

        self.is_clicked()
    

    def is_clicked(self):
        left_click = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()

        if left_click == False:
            self.mouse_released = True

        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]) and left_click and self.mouse_released:
            self.click_action()
            self.mouse_released = False
    

    def set_text(self, text: str, font: pygame.font.Font, color: pygame.Color, text_placement):
        self.text = text
        self.font = font
        self.text_color = color
        self.text_placement = text_placement
    

    def set_surface(self, surf):
        self.surface = surf