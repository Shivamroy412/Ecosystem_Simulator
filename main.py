import pygame
import time
import game
import map
import statistics
from organisms import *
import numpy as np


# Initialize pygame
pygame.init()
pygame.display.set_caption("Ecosystem Simulator")
#Label Font
label_font = pygame.font.SysFont("Calibri", 20)


# Game_Loop

while config.game_running:

    game.screen.blit(game.universe_screen, (map.x_pos_map,map.y_pos_map))
    game.handle_events()
    map.Map.render_map()
    population_label = label_font.render(f"Present Rabbit Population: {len(Rabbit.rabbit_list)}", 1, (0,0,0))
    game.screen.blit(population_label, (10, 10))

    #Present Universe State
    Organism.universe_matrix = game.Universe(Grass.grass_list, Rabbit.rabbit_list, Fox.fox_list).universe_matrix

    #Grass God
    Grass.grass_populator()
    Grass.new_grass_generator()

    if not Rabbit.rabbit_list or not Fox.fox_list:

        Organism.birth(Rabbit, config.rabbit_initial_N, Rabbit.rabbit_list)
        Organism.birth(Fox, config.fox_initial_N, Fox.fox_list)

        if config.days == 0:
            Organism.birth(Grass, config.grass_initial_quantity, Grass.grass_list)

        config.evolution += 1
        config.days = 0 #This has to be defined here to reset days counter when new evolution occurs,
                        #while avoiding the new generation of pioneer Grass as defined in above condition

   
    Organism.Brain.universe_matrix = game.Universe().universe_matrix

    #Rabbit God
    Rabbit.live(population_list= Rabbit.rabbit_list,
              food_list=Grass.grass_list, creature_class=Rabbit)

    #Fox God
    Fox.live(population_list=Fox.fox_list, 
            food_list=Rabbit.rabbit_list, creature_class=Fox)  
        
    
    #Debugging all creatures accumulating to the left
    #print(np.mean([rabbit.degree for rabbit in Rabbit.rabbit_list]))


    # Days counter
    config.days += 1

    time.sleep(0.2)

    pygame.display.update()
