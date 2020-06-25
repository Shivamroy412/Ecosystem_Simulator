import pygame
import random
import time
import math

# Initialize pygame

pygame.init()

# Game Screen

screen_width, screen_height = 1200, 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ecosystem Simulator")

# Rabbit

rabbit_image = pygame.image.load("./img/rabbit.png")
grass_image = pygame.image.load("./img/grass.png")
rabbit_initial_N = 10
grass_quantity = 15
rabbit_population = []
grass_list = []
days = 0


class Rabbit():
    def __init__(self):
        self.id = 0
        self.pos_X = 0
        self.pos_Y = 0
        self.age = 0
        self.gender = ''
        self.isAlive = True
        self.steps = 0
        self.random_speed = 0
        self.random_degree = 0

    def live(rabbit: object):
        # Rabbit appears
        object_appear(rabbit_image, rabbit.pos_X, rabbit.pos_Y)

        # Gender marker
        pygame.draw.circle(screen, (255, 47, 154) if rabbit.gender == 'F' else (
            51, 171, 249), (int(rabbit.pos_X) + 4, int(rabbit.pos_Y) + 4), 3)

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

        # Changes speed after every 15 steps
        if rabbit.steps % 15 == 0:
            rabbit.random_speed = random.randint(-100, 100) / 15

        rabbit.pos_X += rabbit.random_speed * math.cos(math.radians(
            rabbit.random_degree))
        rabbit.pos_Y += rabbit.random_speed * math.sin(math.radians(
            rabbit.random_degree))

        # Keeps the rabbit qithin boundaries
        if rabbit.pos_X <= 40:
            rabbit.pos_X = 40
            reverse()

        if rabbit.pos_X >= screen_width - 40:
            rabbit.pos_X = screen_width - 40
            reverse()

        if rabbit.pos_Y <= 40:
            rabbit.pos_Y = 40
            reverse()

        if rabbit.pos_Y >= screen_height - 40:
            rabbit.pos_Y = screen_height - 40
            reverse()

        # Step counter
        rabbit.steps += 1

        # Age counter
        rabbit.age += 1

        eaten_grass = isCollided(rabbit, grass_list)
        if eaten_grass:
            eaten_grass.isAlive = False


for i in range(rabbit_initial_N):
    gender = 'F' if random.randint(0, 12) % 2 == 0 else 'M'
    # Purposely slightly biased towards generating more females
    rabbit = Rabbit()
    rabbit.id = i
    rabbit.pos_X = random.randint(30, screen_width - 30)
    rabbit.pos_Y = random.randint(30, screen_height - 30)
    rabbit.gender = gender
    rabbit_population.append(rabbit)


# Grass
class Grass():
    def __init__(self):
        self.id = 0
        self.pos_X = 0
        self.pos_Y = 0
        self.isAlive = True

    def populate_grass(grass: object):
        object_appear(grass_image, grass.pos_X, grass.pos_Y)


def new_grass(old, new):
    for i in range(old, new):
        grass = Grass()
        grass.pos_X = random.randint(10, screen_width - 10)
        grass.pos_Y = random.randint(10, screen_height - 10)
        grass_list.append(grass)


# Initial grass generation
for i in range(grass_quantity):
    grass = Grass()
    grass.pos_X = random.randint(10, screen_width - 10)
    grass.pos_Y = random.randint(10, screen_height - 10)
    grass_list.append(grass)


# Collision function
def isCollided(object1: object, object2_list: list):
    for object2 in object2_list:
        distance = math.sqrt((object1.pos_X - object2.pos_X) ** 2 + (
                object1.pos_Y - object2.pos_Y) ** 2)
        if distance < 40 and distance > 0:
            return object2


# Object visible in screen
def object_appear(image, x, y):
    screen.blit(image, (x, y))


# Stats
def print_stats():
    for rabbit in rabbit_population:
        print(rabbit.id, rabbit.age, rabbit.steps, rabbit.gender,
              len(rabbit_population))


# Game_Loop

game_running = True

while game_running:

    screen.fill((11, 102, 35))  # Color of grass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print_stats()
            game_running = False

    # Rabbit appears at a random space
    for i in range(len(rabbit_population)):
        if rabbit_population[i].isAlive:
            Rabbit.live(rabbit_population[i])
    for i in range(len(grass_list)):
        if grass_list[i].isAlive:
            Grass.populate_grass(grass_list[i])

    # Grass generation every 15 days

    if days % 25 == 0:
        old_grass_quantity = grass_quantity
        new_grass_quantity = old_grass_quantity + random.randint(1, 5)
        new_grass(old_grass_quantity, new_grass_quantity)
        grass_quantity = new_grass_quantity

    # Days counter
    days += 1

    time.sleep(0.2)

    pygame.display.update()
