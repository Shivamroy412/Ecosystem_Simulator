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


# Game_Loop

while config.game_running:

    game.screen.blit(game.universe_screen, (map.x_pos_map,map.y_pos_map))
    #game.handle_events() Disabled 
    map.Map.render_map()
    population_label = label_font.render(f"Evolution: {config.evolution} \
        Present Rabbit Population: {len(Rabbit.rabbit_list)}", 1, (0,0,0))
    game.screen.blit(population_label, (10, 10))

    #Present Universe State
    Organism.universe_matrix = game.Universe(Grass.grass_list, Rabbit.rabbit_list, Fox.fox_list).universe_matrix

    #Grass God
    Grass.grass_populator()
    Grass.new_grass_generator()

    for rabbit in Rabbit.rabbit_list:
        print(rabbit.id, rabbit.gender,  rabbit.fitness)

    # Population explosion kills all animals and jumps to next evolution
    # or when either Rabbits or Foxes are extinct or the System is started initially 
    if len(Rabbit.rabbit_list) >= config.population_limit or len(Fox.fox_list) >= config.population_limit \
         or not Rabbit.rabbit_list or not Fox.fox_list:
        
        Organism.dead_list.extend(Rabbit.rabbit_list)
        Rabbit.rabbit_list = []
        Organism.dead_list.extend(Fox.fox_list)
        Fox.fox_list = []

        if config.days > 0:
            Organism.save_fittest_creatures(Rabbit)
    
        Organism.birth(Rabbit, config.rabbit_initial_N, Rabbit.rabbit_list)
        Organism.birth(Fox, config.fox_initial_N, Fox.fox_list)

        if config.days == 0:
            Organism.birth(Grass, config.grass_initial_quantity, Grass.grass_list)

        config.evolution += 1
        config.days = 0 #This has to be defined here to reset days counter when new evolution occurs,
                        #while avoiding the new generation of pioneer Grass as defined in above condition

   
    #This is defining the universal state of the simulation as a matrix
    #Every intelligent creature then gets a slice from the Universal matrix based
    #on their position in the universe along with the radius of their vision
    Organism.Brain.universe_matrix = game.Universe().universe_matrix

    #Rabbit God
    Rabbit.live(population_list= Rabbit.rabbit_list,
              food_list=Grass.grass_list, creature_class=Rabbit)

    #Fox God
    Fox.live(population_list=Fox.fox_list, 
            food_list=Rabbit.rabbit_list, creature_class=Fox)  


    # Days counter
    config.days += 1


    #Check if simulation has been stopped manually
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            #This is done to handle the case of manually closing the simulation, 
            #since manually closing would mean that all creatures are not in dead_list
            Organism.dead_list.extend(Rabbit.rabbit_list)
            Organism.save_fittest_creatures(Rabbit)
            config.game_running = False
            statistics.print_stats()

    time.sleep(0.0001)

    pygame.display.update()
