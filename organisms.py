import config
import random
import game
import math
import pygame


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
            Organism.birth(Grass, new_grass_quantity, Grass.grass_list)

    def grass_populator():
        for grass in Grass.grass_list:
            if grass.isAlive:
                game.object_appear(config.grass_image, grass.pos_X, grass.pos_Y)



class Organism:

    def __init__(self):
        self.id = 0
        self.pos_X = 0
        self.pos_Y = 0
        self.image_roaster_left = []
        self.image_roaster_right = []
        self.age = 0
        self.gender = 'M' if random.random() < 0.45 else 'F' # Slightly biased towards generating more females
        self.isAlive = True
        self.steps = 0
        self.speed = 0
        self.degree = 0
        self.hunger = 0
        self.isPregnant = False
        self.partner = None
        self.mother = None
        self.father = None
        self.gestation_days = 0
        self.isAdult = False
        self.life_span = random.randint(150, 400) #max_life_span of particular creature
        self.hunger_counter = 1
        self.gestation_period = 200
        self.childhood = 100 # Also includes the time after birth to avoid inbreeding
        self.reason_of_death = ''
        self.litter_size = (3, 5)

        self.max_size_ratio = 1
        self.min_size_ratio = 0.35

    #Gradually increses size of creature with age
    @property
    def size_ratio(self):
        return min(self.min_size_ratio + (self.age/300), self.max_size_ratio)
        
    @property
    def img_intervals(self):
        return len(self.image_roaster_left) - 1    


    # Kinetics
    def move_creature(self):
        creature = self

        


        if 90 < creature.degree <= 180:

            game.object_appear(pygame.transform.rotozoom(self.image_roaster_left[
                                                        creature.steps % self.img_intervals], 10, 
                                                        creature.size_ratio),
                            creature.pos_X, creature.pos_Y)

        elif 180 < creature.degree <= 270:
            game.object_appear(
                pygame.transform.rotozoom(self.image_roaster_left[creature.steps % self.img_intervals],
                                        -10, creature.size_ratio),
                creature.pos_X, creature.pos_Y)

        elif 0 < creature.degree <= 90:
            game.object_appear(pygame.transform.rotozoom(
                self.image_roaster_right[creature.steps % self.img_intervals],
                -10, creature.size_ratio), creature.pos_X, creature.pos_Y)

        else:
            game.object_appear(pygame.transform.rotozoom(
                self.image_roaster_right[creature.steps % self.img_intervals], 10,
                 creature.size_ratio),
                 creature.pos_X, creature.pos_Y)

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
            creature.degree = random.randint(0, 360)

        creature.pos_X += creature.speed * math.cos(math.radians(
            creature.degree))
        creature.pos_Y += creature.speed * math.sin(math.radians(
            creature.degree))

        # Reverses direction
        def reverse(creature):
            if creature.degree < 180:
                creature.degree += 180
            else:
                creature.degree -= 180

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



    #Birth
    # Creature Birth
    def birth( creature_class, creature_quantity, creature_population: list, self = None):
   
        present_population = len(creature_population)

        for i in range(present_population, present_population + creature_quantity):
            creature = creature_class()
            creature.id = i
            
            if self:
                creature.mother = self
                creature.father = self.partner

                #Below traits are alreay assigned on birth, however this should be considered as a mutation
                #The creature has a 45%-45% chance of inheriting these traits from either parents and 10% 
                # through mutation
                creature.speed = random.choices([creature.father.speed, creature.mother.speed, creature.speed], 
                                                cum_weights= [0.45, 0.45, 0.1], k = 1)[0] #choices() returns a list
                creature.life_span = random.choices([creature.father.life_span, creature.mother.life_span, 
                                                    creature.life_span], cum_weights= [0.45, 0.45, 0.1], k = 1)[0]


                #New rabbits spawn near mother
                creature.pos_X = creature.mother.pos_X 
                creature.pos_Y = creature.mother.pos_Y


            else:           
                creature.pos_X = random.randint(config.tile_width + 20,
                                                config.universe_width - config.tile_width - 20)
                creature.pos_Y = random.randint(config.tile_height + 20,
                                                config.universe_height - config.tile_height - 20)

                                
            if not isinstance(creature, Grass): 
                print("Birth happened: The present population is {}".format(present_population))
                
                
                
            
            creature_population.append(creature)
 



    def death(self, population_list: list, reason = None):

        if not isinstance(self, Grass):
            self.reason_of_death = reason

        self.isAlive = False
        population_list.remove(self)







    @classmethod
    def live(cls, population_list, food_list, creature_class):
   
        for creature in population_list:
            
            if creature.isAlive:
                creature.move_creature()

                # Step counter
                creature.steps += 1

                # Age counter
                creature.age += 1

                # Hunger Counter
                creature.hunger += creature.hunger_counter
                if creature.hunger >= 200:                   #Max_Hunger 
                    creature.death(population_list, "Hunger")

                # Creature eats only when hungry
                if creature.hunger > 50:
                    eaten = game.isCollided(creature, food_list)
                    if eaten:
                        cls.death(eaten, food_list, "Eaten") 
                        #Calling death() as a classmethod and passing the instance since 
                        #Grass class does not have a death() method
                        creature.hunger = 0

                # Reproduction
                if creature.gender == 'M' and creature.isAdult:
                    mother = game.isCollided(creature, list(filter(lambda female: (
                            (female.gender == 'F' and not female.isPregnant) and
                            creature.isAdult), population_list)))
                    if mother:
                        mother.isPregnant = True
                        mother.partner = creature
                        print("Rabbit got pregnant")

                if creature.isPregnant:
                    creature.gestation_days += 1

                if creature.isPregnant and creature.gestation_days == (
                        creature.gestation_period / 2):
                    litter_size = random.randint(*creature.litter_size)
                    cls.birth(creature_class, litter_size, population_list, creature)

                if creature.gestation_days == creature.gestation_period:
                    creature.isPregnant = False
                    creature.gestation_days = 0

                if creature.age > creature.childhood:
                    creature.isAdult = True

                # Death
                if creature.age == creature.life_span:
                    creature.death(population_list, reason = "Age")




# Rabbit
class Rabbit(Organism):
    rabbit_list = []
    def __init__(self):
        super().__init__()
        
        self.image_roaster_left = config.rabbit_image_left
        self.image_roaster_right = config.rabbit_image_right

        self.litter_size = (5, 8)
        self.speed = random.uniform(1.0, 6.0)

        self.max_size_ratio = 0.85
        self.min_size_ratio = 0.35


#Fox
class Fox(Organism):
    fox_list = []
    def __init__(self):
        super().__init__()

        self.image_roaster_left = config.fox_image_left
        self.image_roaster_right = config.fox_image_right

        self.litter_size = (1, 3)
        self.speed = random.uniform(1.5, 3)

        self.max_size_ratio = 1.0
        self.min_size_ratio = 0.6
