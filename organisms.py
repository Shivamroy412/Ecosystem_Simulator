import config
import random
import game
import math
import pygame

#print(help(config))


        
# Creature Birth
def birth(creature_class, creature_quantity, creature_population: list):
    present_population = len(creature_population)
    print("Birth happened: The present population is {}".format(present_population))
    for i in range(present_population, present_population + creature_quantity):
        creature = creature_class()
        
        creature.id = i
        creature.pos_X = random.randint(config.tile_width + 20,
                                        config.universe_width - config.tile_width - 20)
        creature.pos_Y = random.randint(config.tile_height + 20,
                                        config.universe_height - config.tile_height - 20)

                             
        if not isinstance(creature, Grass): 
            creature.gender = 'M' if random.random() < 0.45 else 'F'
            # Purposely slightly biased towards generating more females
            creature.life_span = random.randint(creature.life_span - 200,
                                                creature.life_span)
  
        creature_population.append(creature)


#Grass
class Grass:
    grass_list = []
    def __init__(self):
        self.pos_X = 0
        self.pos_Y = 0
        self.isAlive = True

    # Grass generation every 15 days
    def new_grass_generator():
        
        if config.days % 50 == 0:
            new_grass_quantity = random.randint(10, 15)
            birth(Grass, new_grass_quantity, Grass.grass_list)

    def grass_populator():
        for grass in Grass.grass_list:
            if grass.isAlive:
                game.object_appear(config.grass_image, grass.pos_X, grass.pos_Y)



class Organism:

    def __init__(self):
        self.id = 0
        self.pos_X = 0
        self.pos_Y = 0
        self.age = 0
        self.gender = ''
        self.isAlive = True
        self.steps = 0
        self.random_speed = 3
        self.random_degree = 0
        self.hunger = 0
        self.isPregnant = False
        self.gestation_days = 0
        self.isAdult = False
        self.life_span = 500 #max_life_span
        self.hunger_counter = 1
        self.gestation_period = 200
        self.childhood = 100
        # Also includes the time after birth to avoid inbreeding
        self.reason_of_death = ''




    def move_creature(self):
        creature = self
        if 90 < creature.random_degree <= 180:
            game.object_appear(pygame.transform.rotate(config.rabbit_image[
                                                        creature.steps % 3], 10),
                            creature.pos_X, creature.pos_Y)

        elif 180 < creature.random_degree <= 270:
            game.object_appear(
                pygame.transform.rotate(config.rabbit_image[creature.steps % 3],
                                        -10),
                creature.pos_X, creature.pos_Y)

        elif 0 < creature.random_degree <= 90:
            game.object_appear(pygame.transform.rotate(
                config.rabbit_image_quad1[creature.steps % 3],
                -10), creature.pos_X, creature.pos_Y)

        else:
            game.object_appear(pygame.transform.rotate(
                config.rabbit_image_quad1[creature.steps % 3], 10), creature.pos_X,
                creature.pos_Y)

        # Gender marker
        pygame.draw.circle(game.universe_screen,
                        (255, 47, 154) if creature.gender == 'F' else
                        (51, 171, 249),
                        (int(creature.pos_X) + 7, int(creature.pos_Y) + 6), 3)

        # Hunger marker
        if config.hunger_marker:
            pygame.draw.rect(game.universe_screen, (57, 255, 20, 0.3),
                            (creature.pos_X, creature.pos_Y - 5, 32, 3), 0)  # Base

            pygame.draw.rect(game.universe_screen, (255, 75, 0, 0.3),
                            (creature.pos_X, creature.pos_Y - 5,
                            (40 / 100) * creature.hunger, 3),
                            0)  # Marker

        # Movements

        # Changes direction after every 30 steps
        if creature.steps % 30 == 0:
            creature.random_degree = random.randint(0, 360)

        creature.pos_X += creature.random_speed * math.cos(math.radians(
            creature.random_degree))
        creature.pos_Y += creature.random_speed * math.sin(math.radians(
            creature.random_degree))

        # Reverses direction
        def reverse(creature):
            if creature.random_degree < 180:
                creature.random_degree += 180
            else:
                creature.random_degree -= 180

        # Keeps the rabbit within the boundaries
        if creature.pos_X <= game.bound_screen.left + 32:
            creature.pos_X = game.bound_screen.left + 32
            reverse(creature)

        if creature.pos_X >= game.bound_screen.right - 32:
            creature.pos_X = game.bound_screen.right - 32
            reverse(creature)

        if creature.pos_Y <= game.bound_screen.top + 32:
            creature.pos_Y = game.bound_screen.top + 32
            reverse(creature)

        if creature.pos_Y >= game.bound_screen.bottom - 32:
            creature.pos_Y = game.bound_screen.bottom - 32
            reverse(creature)





    def live(population_list, food_list, creature_class):
        #print(population_list)
        for creature in population_list:
            #print(creature.pos_X)
            #print(creature.id)
            if creature.isAlive:
                creature.move_creature()

                # Step counter
                creature.steps += 1

                # Age counter
                creature.age += 1

                # Hunger Counter
                creature.hunger += creature.hunger_counter
                if creature.hunger >= 100:
                    # creature.isAlive = False
                    creature.reason_of_death = "Hunger"

                # Creature eats only when hungry
                if creature.hunger > 50:
                    eaten_grass = game.isCollided(creature, food_list)
                    if eaten_grass:
                        eaten_grass.isAlive = False
                        creature.hunger = 0

                # Reproduction
                if creature.gender == 'M' and creature.isAdult:
                    mother = game.isCollided(creature, list(filter(lambda female: (
                            (female.gender == 'F' and not female.isPregnant) and
                            creature.isAdult), population_list)))
                    if mother:
                        mother.isPregnant = True
                        print("Rabbit got pregnant")

                if creature.isPregnant:
                    creature.gestation_days += 1

                if creature.isPregnant and creature.gestation_days == (
                        creature.gestation_period / 2):
                    litter_size = random.randint(5, 10)
                    creature.birth(creature_class, litter_size, population_list)

                if creature.gestation_days == creature.gestation_period:
                    creature.isPregnant = False
                    creature.gestation_days = 0

                if creature.age > creature.childhood:
                    creature.isAdult = True

                # Death
                if creature.age == creature.life_span:
                    creature.isAlive = False
                    creature.reason_of_death = "Age"







# Rabbit
class Rabbit(Organism):
    rabbit_list = []
    def __init__(self):
        super().__init__()



