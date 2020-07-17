import pygame
import time
import life
import game
import map
from organisms import *


# Initialize pygame
pygame.init()
pygame.display.set_caption("Ecosystem Simulator")


#Pioneer Population
life.birth(Rabbit, config.rabbit_initial_N, config.rabbit_list)
life.birth(Grass, config.grass_initial_quantity, config.grass_list)


# Game_Loop

while config.game_running:

    game.screen.blit(game.universe_screen, (map.x_pos_map,map.y_pos_map))
    game.handle_events()
    map.Map.render_map()

    #Grass God
    Grass().grass_populator()
    Grass().new_grass_generator()

    #Rabbit God
    life.live(population_list=config.rabbit_list,
              food_list=config.grass_list, creature_class=Rabbit)

    # Days counter
    config.days += 1

    #print(config.days)

    time.sleep(0.2)

    pygame.display.update()
