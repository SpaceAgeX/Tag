from utils import ColorPanel, Button
from platform_class import Platform
from tkinter.filedialog import asksaveasfilename
import pygame
import math
import json

WIDTH = 1280
HEIGHT = 720

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
selected_tile = 0

map_data = [[5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,0,0,0,0,0,2,4,0,0,0,0,0,0,0,0,6],
            [6,2,4,0,0,0,0,0,0,0,0,0,0,0,0,2,3,4,0,6],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,0,0,0,2,3,3,3,3,4,0,0,0,0,0,0,6],
            [6,0,0,0,0,2,4,0,0,0,0,0,0,1,0,0,0,0,0,6],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,6],
            [6,0,2,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,1,0,0,0,2,3,3,4,0,0,0,2,4,0,0,6],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [7,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,7]]


class Map:
    def __init__(self, data: list[list]):
        self.map_data = data
        self.dimensions = (len(data[0]), len(data))
        self.tile_images = [None]
        self.platforms = []

        for x in range(0, 7):
            self.tile_images.append(pygame.image.load('Assets/GrassTiles/GrassTile'+str(x+1)+'.png').convert_alpha())
    

    @staticmethod
    def from_json(file_path: str):
        f = open(file_path, "r")
        string_data = f.read()

        data = json.loads(string_data)["map_data"]
        return Map(data)


    
    def generate_platforms(self):
        self.platforms = []
        
        for row, i in enumerate(self.map_data):
            for tile, j in enumerate(i):
                if j > 0:
                    platform = Platform(screen, pygame.transform.scale_by(self.tile_images[j], 2), (tile*WIDTH/self.dimensions[0], row*HEIGHT/self.dimensions[1])) # (tile*64, (row*64)-8))
                    self.platforms.append(platform)


    def update_map_data(self, data):
        self.map_data = data
        self.dimensions = (len(data[0]), len(data))
        self.generate_platforms()
    

    def display(self):
        for platform in self.platforms:
            platform.draw()

        

def set_selected_tile(n):
    global selected_tile
    selected_tile = n
    print(selected_tile)


def save_layout(map_data):
    file_content = json.dumps({ "map_data": map_data })

    file_path = asksaveasfilename(filetypes=[('JSON Files', '*.json')], defaultextension=[('JSON Files', '*.json')])
    f = open(file_path, "w")
    f.write(file_content)

    print(f"Saved To {file_path}")




def main():
    running = True
    clock = pygame.time.Clock()

    current_map = Map(map_data)
    current_map.generate_platforms()
    

    # Instantiating UI Elements
    panel = ColorPanel((WIDTH-600, HEIGHT-200), (600, 150), "black")
    save_button = Button((panel.rect.x+225, HEIGHT-110), (150, 50), "indigo", lambda: save_layout(current_map.map_data))
    save_button.set_text("Save Layout", pygame.font.Font(None, 20), "white", "center")

    button0 = Button((panel.rect.x, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(0))
    button1 = Button((panel.rect.x+75, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(1))
    button2 = Button((panel.rect.x+75*2, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(2))
    button3 = Button((panel.rect.x+75*3, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(3))
    button4 = Button((panel.rect.x+75*4, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(4))
    button5 = Button((panel.rect.x+75*5, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(5))
    button6 = Button((panel.rect.x+75*6, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(6))
    button7 = Button((panel.rect.x+75*7, HEIGHT-180), (50, 50), "indigo", lambda: set_selected_tile(7))
    buttons = [button0, button1, button2, button3, button4, button5, button6, button7]
    
    for i, button in enumerate(buttons):
        button.set_text(str(i), pygame.font.Font(None, 20), "white", "center")
        button.set_surface(current_map.tile_images[i])


    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        screen.fill((115,190,211))
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()
        

        # Changing Tiles
        if mouse_clicked[0] and not panel.rect.collidepoint(mouse_pos):
            tile_x = math.floor(mouse_pos[0]/(WIDTH/current_map.dimensions[0])) #math.floor(mouse_pos[0]/64)
            tile_y = math.floor(mouse_pos[1]/(HEIGHT/current_map.dimensions[1])) #math.floor((mouse_pos[1]+8)/64)
            #print("Tile X: ", tile_x)
            #print("Tile Y: ", tile_y)

            new_map_data = current_map.map_data
            new_map_data[tile_y][tile_x] = selected_tile
            current_map.update_map_data(new_map_data)
            
        
        if mouse_clicked[2]:
            panel.rect.x = mouse_pos[0]
            panel.rect.y = mouse_pos[1]


        # Display Map
        current_map.display()

        # Displaying UI Elements
        panel.display(screen)
        save_button.display(screen)
        save_button.rect.x = panel.rect.x + 225
        save_button.rect.y = panel.rect.y + 90

        for i, button in enumerate(buttons):
            button.rect.x = panel.rect.x + 75 * i
            button.rect.y = panel.rect.y + 20
            button.display(screen)


        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()