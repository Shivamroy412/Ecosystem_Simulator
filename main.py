import pygame
import time
import life
import game
import statistics
from organisms import *


# Initialize pygame
pygame.init()
pygame.display.set_caption("Ecosystem Simulator")


#Pioneer Population
life.birth(Rabbit, config.rabbit_initial_N, config.rabbit_population)
life.birth(Grass, config.grass_initial_quantity, config.grass_list)


# Game_Loop
game_running = True

while game_running:

    game.screen.fill((11, 102, 35))  # Color of grass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
            statistics.print_stats()

    #Grass God
    Grass().grass_populator()
    Grass().new_grass_generator()

    #Rabbit God
    life.live(population_list=config.rabbit_population,
              gestation_period=config.rabbit_gestation_period,
              food_list=config.grass_list, creature_class=Rabbit)

    # Days counter
    config.days += 1

    print(config.days)

    time.sleep(0.2)

    pygame.display.update()
