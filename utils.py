import pygame


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