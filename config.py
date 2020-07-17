import pygame
import map

# Game Specifications
game_running = True
screen_width, screen_height = 1280, 768
days = 0
hunger_marker = False

# Rabbit
rabbit_image = [pygame.image.load("./img/rabbit_walk/rabbit" + str(i) +
                                  ".png") for i in range(1, 4)]
rabbit_image_quad1 = [pygame.image.load("./img/rabbit_walk/right_rabbit" + str(
    i) + ".png") for i in range(1, 4)]

rabbit_initial_N = 15
rabbit_list = []

# Grass
grass_image = pygame.image.load("./img/grass.png")
grass_initial_quantity = 50
grass_list = []

# Map

map = [
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
     'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G',
     'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'G', 'E'],
    ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E',
     'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']
]

tile_width = 64
tile_height = 64

map_tiles_list = []

universe_height = int(len(map) * tile_height)
universe_width = int(len(map[0]) * tile_width)

print(universe_width, universe_height)

print(universe_width, universe_height)

grass_land_image = pygame.image.load("./img/map/grass_land.png")
ground_land_image = pygame.image.load("./img/map/ground.png")

tile_image_mapping = {'E': ground_land_image,
                      'G': grass_land_image}

scroll_speed = 192
