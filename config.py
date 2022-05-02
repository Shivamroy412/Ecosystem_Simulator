import pygame
import map
import os

# Game Specifications
game_running = True

#Change initial_training to True if you change the neural network architecture
#or if you wish to start training from scratch and not leverage pre-trained weights
training = True 

SCREEN_WIDTH, SCREEN_HEIGHT =  1280, 768

days = 0
hunger_marker = False
spawn_near_mother = False

mutation_chance = 0.3

evolution = 0


#Fitness scores
edge_score = -1.0
eat_score = 10.0
eaten_death_score = -40.0
mating_score = 40.0
age_score = -0.25 #For normalising with newer generations, since the older creatures 
                 # would have survived longer and hence would have  higher scores

population_limit = 80

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

fox_initial_N = 15

# Grass
grass_image = pygame.image.load(os.path.join("img", "grass.png"))
grass_initial_quantity = 80


# Map
map = [[  'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em',  'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em', 'Em'],
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


#By what value are map edges represented in the matrices
edge_value_in_matrix = -0.1 


scroll_speed = 192
