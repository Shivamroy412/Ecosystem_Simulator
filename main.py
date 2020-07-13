import pygame
import random
import time
import math
import config
import statistics

# Initialize pygame
pygame.init()

# Game Screen
screen = pygame.display.set_mode((config.screen_width, config.screen_height))
pygame.display.set_caption("Ecosystem Simulator")



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


    def live(rabbit: object):
        # Rabbit appears
        if 90 < rabbit.random_degree <= 180:
            object_appear(pygame.transform.rotate(config.rabbit_image[
                                                      rabbit.steps
                                                               %3], 10),
                rabbit.pos_X, rabbit.pos_Y)

        elif 180 < rabbit.random_degree <= 270:
            object_appear(pygame.transform.rotate(config.rabbit_image[
                                                      rabbit.steps
                                                               %3], -10),
                rabbit.pos_X,rabbit.pos_Y)

        elif 0 < rabbit.random_degree <= 90:
            object_appear(pygame.transform.rotate(config.rabbit_image_quad1[
                                                      rabbit.steps % 3],-10),
                  rabbit.pos_X,rabbit.pos_Y)

        else:
            object_appear(pygame.transform.rotate(config.rabbit_image_quad1[
                                                      rabbit.steps % 3],10),
                  rabbit.pos_X,rabbit.pos_Y)

        # Gender marker
        pygame.draw.circle(screen, (255, 47, 154) if rabbit.gender == 'F' else (
            51, 171, 249), (int(rabbit.pos_X) + 7, int(rabbit.pos_Y) + 6), 3)

        # Hunger marker
        # pygame.draw.rect(screen, ( 57,255,20, 0.3), (rabbit.pos_X,
        # rabbit.pos_Y - 5, 32, 3),0)  #Base
        #
        # pygame.draw.rect(screen, (255, 75, 0, 0.3), (rabbit.pos_X,
        # rabbit.pos_Y - 5, (40 / 100) * rabbit.hunger,3), 0) #Marker

        # Rabbit Movements

        # Reverses direction
        def reverse():
            if rabbit.random_degree < 180:
                rabbit.random_degree += 180
            else:
                rabbit.random_degree -= 180

        # Changes direction after every 30 steps
        if rabbit.steps % 30 == 0:
            rabbit.random_degree = random.randint(0, 360)

        rabbit.pos_X += rabbit.random_speed * math.cos(math.radians(
            rabbit.random_degree))
        rabbit.pos_Y += rabbit.random_speed * math.sin(math.radians(
            rabbit.random_degree))

        # Keeps the rabbit qithin boundaries
        if rabbit.pos_X <= 40:
            rabbit.pos_X = 40
            reverse()

        if rabbit.pos_X >= config.screen_width - 40:
            rabbit.pos_X = config.screen_width - 40
            reverse()

        if rabbit.pos_Y <= 40:
            rabbit.pos_Y = 40
            reverse()

        if rabbit.pos_Y >= config.screen_height - 40:
            rabbit.pos_Y = config.screen_height - 40
            reverse()

        # Step counter
        rabbit.steps += 1

        # Age counter
        rabbit.age += 1

        # Hunger Counter
        rabbit.hunger += 0.5
        if rabbit.hunger >= 100:
            rabbit.isAlive = False

        # Rabbit eats only when hungry
        if rabbit.hunger > 50:
            eaten_grass = isCollided(rabbit, config.grass_list)
            if eaten_grass:
                eaten_grass.isAlive = False
                rabbit.hunger = 0

        # Reproduction
        if rabbit.gender == 'M' and rabbit.isAdult:
            mother = isCollided(rabbit, list(filter(lambda female: (
                    (female.gender == 'F' and not female.isPregnant) and
                    rabbit.isAdult),config.rabbit_population)))
            if mother:
                mother.isPregnant = True
                print("Rabbit got pregnant")

        if rabbit.isPregnant:
            rabbit.gestation_days += 1

        if rabbit.isPregnant and rabbit.gestation_days == \
                config.rabbit_gestation_period/2:
            litter_size = random.randint(5,10)
            rabbit_birth(litter_size)

        if rabbit.gestation_days == config.rabbit_gestation_period:
            rabbit.isPregnant = False
            rabbit.gestation_days = 0


        #Rabbit Death

        if rabbit.age > config.rabbit_childhood:
            rabbit.isAdult = True
        if rabbit.age == rabbit.life_span:
            rabbit.isAlive = False



#Rabbit birth
def rabbit_birth(rabbit_quantity):
    present_rabbit_population = len(config.rabbit_population)
    print("birth", present_rabbit_population)
    for i in range(present_rabbit_population,
                   present_rabbit_population + rabbit_quantity):
        gender = 'M' if random.randint(1, 9) % 3 == 0 else 'F'
        # Purposely slightly biased towards generating more females
        rabbit = Rabbit()
        rabbit.id = i
        rabbit.pos_X = random.randint(30, config.screen_width - 30)
        rabbit.pos_Y = random.randint(30, config.screen_height - 30)
        rabbit.gender = gender
        rabbit.life_span = random.randint(450,500)
        config.rabbit_population.append(rabbit)



#Grass
class Grass():
    def __init__(self):
        self.pos_X = 0
        self.pos_Y = 0
        self.isAlive = True

    def populate_grass(grass: object):
        object_appear(config.grass_image, grass.pos_X, grass.pos_Y)


def new_grass(new):
    for i in range(new):
        grass = Grass()
        grass.pos_X = random.randint(10, config.screen_width - 10)
        grass.pos_Y = random.randint(10, config.screen_height - 10)
        config.grass_list.append(grass)




# Initial grass generation
for i in range(config.grass_quantity):
    grass = Grass()
    grass.pos_X = random.randint(10, config.screen_width - 10)
    grass.pos_Y = random.randint(10, config.screen_height - 10)
    config.grass_list.append(grass)


# Collision function
def isCollided(object1: object, object2_list: list):
    for object2 in object2_list:
        if object2.isAlive:
            distance = math.sqrt((object1.pos_X - object2.pos_X) ** 2 + (
                    object1.pos_Y - object2.pos_Y) ** 2)
            if 40 > distance > 0:
                return object2


# Object visible in screen
def object_appear(image, x, y):
    screen.blit(image, (x, y))


# def rabbit_appear(rabbit: object):
#     image = pygame.image.load("./img/rabbit_walk/rabbit" + str(image_index) + ".png")
#     screen.blit(image, (rabbit.pos_X, rabbit.pos_Y))
#     image_index += 1
#     if image_index == 4:
#         image_index = 1


# # Stats
# def print_stats():
#     for rabbit in config.rabbit_population:
#         print(rabbit.id, rabbit.age, rabbit.steps,
#               rabbit.gender)


# Game_Loop

game_running = True

while game_running:

    screen.fill((11, 102, 35))  # Color of grass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            statistics.print_stats()
            game_running = False


    # Grass appears at a random space
    for i in range(len(config.grass_list)):
        if config.grass_list[i].isAlive:
            Grass.populate_grass(config.grass_list[i])
    # Rabbit appears at a random space
    if config.days == 0:
        rabbit_birth(config.rabbit_initial_N)
    for i in range(len(config.rabbit_population)):
        if config.rabbit_population[i].isAlive:
            Rabbit.live(config.rabbit_population[i])


    # Grass generation every 15 days

    if config.days % 50 == 0:
        new_grass_quantity = random.randint(10,15)
        new_grass(new_grass_quantity)

    # Days counter
    config.days += 1

    time.sleep(0.2)

    pygame.display.update()
