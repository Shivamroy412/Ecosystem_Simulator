import config
import random
import game
import math
import pygame
import numpy as np

class Organism:

    number_of_creatures = 0
    dead_list = []
    #Neural Network AI
    isIntelligent = None

    def __init__(self):
        self.id = ""
        self.pos_X = random.randint(config.TILE_DIM + 20,
                                    config.universe_width - config.TILE_DIM - 20)
        self.pos_Y = random.randint(config.TILE_DIM + 20,
                                    config.universe_height - config.TILE_DIM - 20)
        self.image_roaster_left = []
        self.image_roaster_right = []

        self.age = 0
        self.gender = 'M' if random.random() < 0.45 else 'F' # Slightly biased towards generating more females
        self.isAlive = True
        self.steps = 0
        self.speed = 0
        
        self.partner = None
        self.mother = None
        self.father = None
        self.generation = 0

        self.isPregnant = False
        self.gestation_days = 0
        self.isAdult = False
        self.life_span = 0 
        self.gestation_period = 200
        self.childhood = 100 # Also includes the time after birth to avoid inbreeding
        self.reason_of_death = ''
        self.degree = random.randint(0, 360) 

        self.hunger = 0
        self.again_hungry = 0 #Creature keeps eating since training 
        self.max_hunger_limit = 150
        
        self.litter_size_range = (3, 5)

        self.max_size_ratio = 1
        self.min_size_ratio = 0.35

        self.fitness = 0.0

    

    #Gradually increaes size of creature with age
    @property
    def size_ratio(self):
        return min(self.min_size_ratio + (self.age/300), self.max_size_ratio)
        
    @property
    def img_intervals(self):
        return len(self.image_roaster_left) - 1  

    @property 
    def brain(self):
        if self.isIntelligent:
            return Organism.Brain(creature = self)
        else:
            return None


    #The below parameter trait is alreay assigned on birth,however this should be considered as a 
    #mutation as it is random, The creature has a (1-mutation_chance)/2% chance of inheriting this 
    #trait from either parents and (mutation_chance)% through mutation
    def inheritance(self, trait, mutation_chance = 0.1):
        return random.choices([getattr(self.mother, trait), getattr(self.father, trait), 
                              getattr(self, trait)], 
                              [(1.0-mutation_chance)/2.0, (1.0-mutation_chance)/2.0, 
                              mutation_chance],k=1)[0]
                              # [0] since it returns a list


    # Kinetics
    def move_creature(self):
        creature = self

        # Changes direction after every 30 steps
        if self.steps % 30 == 0 and not self.isIntelligent:
            creature.degree = random.randint(0, 360)

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
                            (32 /creature.max_hunger_limit) * creature.hunger, 3),
                            0)  # Marker

        # Movements
        creature.pos_X += creature.speed * math.cos(math.radians(
            creature.degree))
        creature.pos_Y += creature.speed * math.sin(math.radians(
            creature.degree))

        # Reverses direction
        def reverse(creature):
            
            creature.fitness += config.edge_score
            #A creature reverses only upon going on the edge, discouraging it to 
            # move towards the edge with a slight penalty

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


    # Collision function
    def isCollided(self, object2_list: list, distance_formula = "Manhattan"):
        for object2 in object2_list:
            if object2.isAlive:

                if distance_formula == "Euclidean":
                    distance = math.sqrt((self.pos_X - object2.pos_X) ** 2 + (
                            self.pos_Y - object2.pos_Y) ** 2)
                    if 40 > distance > 0:
                        return object2
                
                if distance_formula == "Manhattan":       #Reduces computational overhead
                    distance = abs(self.pos_X - object2.pos_X) + abs(self.pos_Y - object2.pos_Y)
                    if 40 > distance > 0:
                        return object2



    #Birth
    # Creature Birth
    def birth( creature_class, creature_quantity, creature_population: list, self = None):
   
        present_population = len(creature_population)

        for _ in range(present_population, present_population + creature_quantity):
            
            creature = creature_class()
            
            #When the parents were already present in the universe, that is, not pioneers
            if self:
                #This condition implies that the creatures mated and therefore the mother creature
                #called this function. This would also mean that the inheritance of traits can be 
                #done through the the parent creatures already present in the simulation.
                
                creature.mother = self
                creature.father = self.partner

                creature.generation = max(creature.mother.generation, creature.father.generation) + 1

                #Since trait is an attribute it has to be passed as a string
                creature.speed = creature.inheritance("speed", 0.1)
                creature.life_span = creature.inheritance("life_span", 0.1)

                #New rabbits spawn near mother
                creature.pos_X = creature.mother.pos_X 
                creature.pos_Y = creature.mother.pos_Y

            else:
                #This condition would imply that new creatures need to be formed and this is the start of the
                #simulation or the next evolution and there would be a pioneer population created.
                pass
                                

            if not isinstance(creature, Grass):
                
                creature.id = "_".join(["Evol", str(config.evolution), "Num", str(creature_class.number_of_creatures)])

                creature_class.number_of_creatures += 1 #Keeps a count of the number of creatures    
                    
            
            creature_population.append(creature)


    def death(self, population_list: list, reason = None):

        if not isinstance(self, Grass):
            self.reason_of_death = reason
            Organism.dead_list.append(self)

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
                creature.hunger += 1
                if creature.hunger >= creature.max_hunger_limit:
                    
                    creature.fitness += config.dies_of_hunger_score
                    #Crearure couldn't find food, however there might be shortage of food, hence not
                    # the heaviest penalty

                    creature.death(population_list, "Hunger")
                    continue #Continue to the next element after death, since 
                             #creature gets removed from the list at this time
                             #This can cause problems if more than one death condition is met

                # Creature eats only when hungry, this has been made 0 while training
                if creature.hunger > creature.again_hungry:
                    eaten = creature.isCollided(food_list)
                    if eaten:

                        creature.fitness += config.eat_score #Eating is an essential activity

                        creature.hunger = 0

                        if not isinstance(eaten, Grass):
                            eaten.fitness = config.eaten_death_score #Got eaten

                        cls.death(eaten, food_list, "Eaten")
                        continue 
                        #Calling death() as a classmethod and passing the instance since 
                        #Grass class does not have a death() method
                        

                # Reproduction
                if creature.gender == 'M' and creature.isAdult: 
                    
                    mother = creature.isCollided(list(filter(lambda female: (
                            (female.gender == 'F' and not female.isPregnant) and
                            creature.isAdult), population_list)))

                    if mother:
                        mother.isPregnant = True
                        mother.partner = creature
                        (f"{creature_class.__name__} got pregnant")

                    # Since at present we don't show the above traits required to be a mother
                    # only herding tendencies can also be rewarded as it encourages mating
                    female_nearby =  creature.isCollided(list(filter(lambda female: 
                            female.gender == 'F', population_list)))

                    # Mating would acquire a high fitness score
                    if female_nearby:
                        creature.fitness        += config.mating_score
                        female_nearby.fitness   += config.mating_score

                if creature.isPregnant:
                    creature.gestation_days += 1

                if creature.isPregnant and creature.gestation_days == (
                        creature.gestation_period / 2):
                    litter_size = random.randint(*creature.litter_size_range)
                    cls.birth(creature_class, litter_size, population_list, creature)

                if creature.gestation_days == creature.gestation_period:
                    creature.isPregnant = False
                    creature.gestation_days = 0

                if creature.age > creature.childhood:
                    creature.isAdult = True

                # Death
                if creature.age == creature.life_span:
                    creature.death(population_list, reason = "Age")
                    continue


                #Neural_Network 
                if creature.isIntelligent: 

                    #print(creature.id, creature.degree,  creature.pos_X, creature.pos_Y)
                    creature.degree =  creature.brain.forward()   
                    

    
    class Brain:

        universe_matrix = None

        def __init__(self, creature,  vision_radius = 125, neurons_1 = 10, neurons_2 = 1):

            self.creature = creature
            self.vision_radius = vision_radius
            
            self.pos_X = int(self.creature.pos_X)
            self.pos_Y = int(self.creature.pos_Y)
            self.id = self.creature.id

            #Layer 1
            self.neurons_1 = neurons_1

            self.weight_1 = np.random.uniform(-1.0, 1.0, (self.vision_radius * 2 + 1, self.neurons_1))
            self.bias_1 = np.random.uniform(-1.0, 1.0, (1, self.neurons_1))

            #Layer 2
            self.neurons_2 = neurons_2

            self.weight_2 = np.random.uniform(-1.0, 1.0, (self.neurons_1, self.neurons_2))
            self.bias_2 = np.random.uniform(-1.0, 1.0, (1, self.neurons_2))


        def forward(self):

            #Multiplying weight and adding bias in Layer 1
            output = np.dot(self.view_matrix, self.weight_1) + self.bias_1 #Dim (vision_radius, neurons_1)

            #Activation function RelU
            output = np.maximum(0, output)   #Dim (vision_radius, neurons_1)

            #Multiplying weights and biases in Layer 2
            output = np.dot(output, self.weight_2) + self.bias_2   #Dim (vision_radius, neurons_2)

            #Activation function Sigmoid
            output = 1.0/(1.0 + np.exp(-output))

            return np.mean(output) * 360


        @property
        def view_matrix(self):
            # A complex logic had to be written for creatures wandering at the edges of the map
            #since their vision would spill-over of the map screen

            #Initialise the view_matrix with edge values
            _view_matrix = np.full((2*self.vision_radius+1, 2*self.vision_radius+1), config.edge_value_in_matrix)

            _universe_left = max(0,self.pos_X - self.vision_radius)
            _universe_right = min(config.SCREEN_WIDTH-1, self.pos_X + self.vision_radius)
            _universe_top = max(0, self.pos_Y - self.vision_radius)
            _universe_bottom = min(config.SCREEN_HEIGHT-1,self.pos_Y + self.vision_radius)

            #Dimensions of the part of the vision_matrix which overlaps the universe map
            _overlap_matrix_width  = _universe_right - _universe_left + 1
            _overlap_matrix_height = _universe_bottom - _universe_top + 1

            #Slicing idices of the overlapping matrix
            _overlap_left = (2*self.vision_radius+1)-_overlap_matrix_width if _universe_left == 0 else 0
            _overlap_right = _overlap_matrix_width if _universe_right == (config.SCREEN_WIDTH-1) else (2*self.vision_radius+1)
            _overlap_top = (2*self.vision_radius+1)- _overlap_matrix_height if _universe_top == 0 else 0
            _overlap_bottom = _overlap_matrix_height if _universe_bottom == (config.SCREEN_HEIGHT-1) else (2*self.vision_radius+1)

            #Slicing and specifying only the part of the vision matrix and universe that overlap
            _view_matrix[_overlap_left:_overlap_right, _overlap_top:_overlap_bottom] = self.universe_matrix[
                                                        _universe_left:_universe_right+1, _universe_top:_universe_bottom+1]


            return _view_matrix



# Rabbit
class Rabbit(Organism):
    rabbit_list = []

    isIntelligent = True

    def __init__(self):
        super().__init__()
        
        self.image_roaster_left = config.rabbit_image_left
        self.image_roaster_right = config.rabbit_image_right

        self.litter_size_range = (5, 8)
        self.speed = random.uniform(3.0, 8.0)
        self.life_span = random.randint(1500, 4000) 

        self.max_size_ratio = 0.85
        self.min_size_ratio = 0.35

        self.again_hungry = 0 #zero since training 
        self.max_hunger_limit = 500



#Fox
class Fox(Organism):
    fox_list = []

    isIntelligent = False

    def __init__(self):
        super().__init__()

        self.image_roaster_left = config.fox_image_left
        self.image_roaster_right = config.fox_image_right

        self.litter_size_range = (3, 6)
        self.speed = random.uniform(2.0, 4.0)
        self.life_span = random.randint(1200, 1500) 

        self.max_size_ratio = 1.0
        self.min_size_ratio = 0.6

        self.again_hungry = 150  #zero since training
        self.max_hunger_limit = 500




#Grass
class Grass:
    grass_list = []
    def __init__(self):
        self.pos_X = random.randint(config.TILE_DIM + 20,
                                    config.universe_width - config.TILE_DIM - 20)
        self.pos_Y = random.randint(config.TILE_DIM + 20,
                                    config.universe_height - config.TILE_DIM - 20)
        self.isAlive = True

    # Grass generation every 40 days
    def new_grass_generator():
        
        if config.days % 40 == 0:
            new_grass_quantity = random.randint(40, 70)
            Organism.birth(Grass, new_grass_quantity, Grass.grass_list)

    def grass_populator():
        for grass in Grass.grass_list:
            if grass.isAlive:
                game.object_appear(config.grass_image, grass.pos_X, grass.pos_Y)

