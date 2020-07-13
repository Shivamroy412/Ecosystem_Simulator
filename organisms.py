import config
import random
import game
import life

#Grass
class Grass():
    def __init__(self):
        self.pos_X = 0
        self.pos_Y = 0
        self.isAlive = True

        # Grass generation every 15 days
    def new_grass_generator(self):
        if config.days % 50 == 0:
            new_grass_quantity = random.randint(10, 15)
            life.birth(Grass, new_grass_quantity, config.grass_list)

    def grass_populator(self):
        for grass in config.grass_list:
            if grass.isAlive:
                game.object_appear(config.grass_image, grass.pos_X, grass.pos_Y)

# Rabbit
class Rabbit():
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
        self.life_span = 300
        self.reason_of_death = ''




