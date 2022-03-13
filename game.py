import config
import pygame
import statistics
import map
from itertools import chain
import numpy as np


screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
universe_screen = pygame.Surface((config.universe_width,
                                  config.universe_height))

# Grass_area
bound_screen = pygame.Rect(config.TILE_DIM, config.TILE_DIM,
                           config.universe_width -
                           2 * config.TILE_DIM,
                           config.universe_height - 2 * config.TILE_DIM)

pygame.key.set_repeat()


# Object visible in screen
def object_appear(image, x, y):
    universe_screen.blit(image, (x, y))


class Universe:

    def __init__(self, *all_creature_lists):

        self.universe_width = config.universe_width
        self.universe_height = config.universe_height 
        self.edge_tiles_dim = config.TILE_DIM  

        self.day = config.days 

        self.creature_mapping = {'Grass': 1.0, 'RabbitM': 2.0, 'RabbitF' : 3.0, 
                                 'FoxM': 4.0, 'FoxF': 5.0}

        self.all_elements = list(chain(*all_creature_lists))
        #Python logic for the above line of code:
        # all_creature_lists is a tuple of the lists passed as argument
        # The above tuple is unwrapped using * and passed to itertools.chain
        # On unwrapping all the lists are passed as arguments to chain seperately
        # chain(*all_creature_lists) returns a chain yield object which contains all
        # elements of the list and then list() function converts the object to a list

        
    @property
    def universe_matrix(self):

        _matrix = np.full((self.universe_width, self.universe_height), fill_value = -0.1)    
        #Initialize with -1 for edge values and then replace inner universe cells with zero
        for row in range(self.edge_tiles_dim, self.universe_width - self.edge_tiles_dim):
            for col in range(self.edge_tiles_dim, self.universe_height - self.edge_tiles_dim):
                _matrix[row, col] = 0.0
           
            
        for element in self.all_elements:
             
            gender_str = element.gender if not element.__class__.__name__ == "Grass" else ""
            _matrix[int(element.pos_X), int(element.pos_Y)] =  self.creature_mapping[element.__class__.__name__ + gender_str]
            

        return _matrix










# Handle Events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.game_running = False
            statistics.print_stats()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if map.x_pos_map < 0:
            map.x_pos_map += config.scroll_speed

    if keys[pygame.K_RIGHT]:
        if map.x_pos_map > config.SCREEN_WIDTH - config.universe_width:
            map.x_pos_map -= config.scroll_speed

    if keys[pygame.K_UP]:
        if map.y_pos_map < 0:
            map.y_pos_map += config.scroll_speed

    if keys[pygame.K_DOWN]:
        if map.y_pos_map > config.SCREEN_HEIGHT - config.universe_height:
            map.y_pos_map -= config.scroll_speed
