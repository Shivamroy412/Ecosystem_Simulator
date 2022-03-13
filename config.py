import pygame
import map
import os

# Game Specifications
game_running = True
training = False 

SCREEN_WIDTH, SCREEN_HEIGHT =  1280, 768

days = 0
hunger_marker = True




# Rabbit
rabbit_image_left = [pygame.image.load(os.path.join('img', 'rabbit_walk',
                                "rabbit" + str(i) +
                                  ".png")) for i in range(1, 4)]
rabbit_image_right = [pygame.image.load(os.path.join('img', 'rabbit_walk',
                                "right_rabbit" + str(i) +
                                  ".png")) for i in range(1, 4)]
rabbit_initial_N = 25


#Fox
fox_image_left = [pygame.image.load(os.path.join('img', 'fox_walk',
                                "fox" + str(i) +
                                  ".png")) for i in range(1, 6)]

fox_image_right = [pygame.image.load(os.path.join('img', 'fox_walk',
                                "right_fox" + str(i) +
                                  ".png")) for i in range(1, 6)]

fox_initial_N = 10

# Grass
grass_image = pygame.image.load(os.path.join("img", "grass.png"))
grass_initial_quantity = 80


# Map
map = [
    ['Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Gm', 'Em'],
    ['Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em']]



TILE_DIM = 64

map_tiles_list = []

universe_height = int(len(map) * TILE_DIM)
universe_width = int(len(map[0]) * TILE_DIM)

print(universe_width, universe_height)

grass_land_image = pygame.image.load(os.path.join("img", "map", "grass_land.png"))
ground_land_image = pygame.image.load(os.path.join("img","map", "ground.png"))
#water_image = pygame.image.load("./img/map/water.png")

tile_image_mapping = {'Em': ground_land_image,
                      'Gm': grass_land_image,}

scroll_speed = 192
