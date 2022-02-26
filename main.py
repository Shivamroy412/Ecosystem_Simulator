import pygame
import time
import game
import map
from organisms import *


# Initialize pygame
pygame.init()
pygame.display.set_caption("Ecosystem Simulator")


#Pioneer Population
birth(Rabbit, config.rabbit_initial_N, Rabbit.rabbit_list)
birth(Grass, config.grass_initial_quantity, Grass.grass_list)


# Game_Loop

while config.game_running:

    game.screen.blit(game.universe_screen, (map.x_pos_map,map.y_pos_map))
    game.handle_events()
    map.Map.render_map()

    #Grass God
    Grass.grass_populator()
    Grass.new_grass_generator()

    #Rabbit God
    Rabbit.live(population_list= Rabbit.rabbit_list,
              food_list=Grass.grass_list, creature_class=Rabbit)

    # Days counter
    config.days += 1

    #print(config.days)

    time.sleep(0.2)

    pygame.display.update()
