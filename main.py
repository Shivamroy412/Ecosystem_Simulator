import pygame
import time
import game
import map
import statistics
from organisms import *


# Initialize pygame
pygame.init()
pygame.display.set_caption("Ecosystem Simulator")
#Label Font
label_font = pygame.font.SysFont("Calibri", 20)

#Pioneer Population
Organism.birth(Grass, config.grass_initial_quantity, Grass.grass_list)
Organism.birth(Rabbit, config.rabbit_initial_N, Rabbit.rabbit_list)
Organism.birth(Fox, config.fox_initial_N, Fox.fox_list)


# Game_Loop

while config.game_running:

    game.screen.blit(game.universe_screen, (map.x_pos_map,map.y_pos_map))
    game.handle_events()
    map.Map.render_map()
    population_label = label_font.render(f"Present Rabbit Population: {len(Rabbit.rabbit_list)}", 1, (0,0,0))
    game.screen.blit(population_label, (10, 10))

    #Grass God
    Grass.grass_populator()
    Grass.new_grass_generator()

    #Rabbit God
    Rabbit.live(population_list= Rabbit.rabbit_list,
              food_list=Grass.grass_list, creature_class=Rabbit)

    #Fox God
    Fox.live(population_list=Fox.fox_list, 
            food_list=Rabbit.rabbit_list, creature_class=Fox)

    # Days counter
    config.days += 1

    time.sleep(0.2)

    pygame.display.update()
