import pygame
import random
import time
import math

# Initialize pygame

pygame.init()

# Game Screen

screen = pygame.display.set_mode((900, 700))
pygame.display.set_caption("Ecosystem Simulator")

# Rabbit

rabbit_icon = pygame.image.load("./img/rabbit.png")
rabbit_initial_N = 5
rabbit_population = []


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


def live(rabbit : object):

    # Rabbit appears
    rabbit_appear(rabbit.pos_X,rabbit.pos_Y)

    #Gender marker
    pygame.draw.circle(screen, (255, 47, 154) if rabbit.gender == 'F' else (
        51, 171, 249), (int(rabbit.pos_X) + 4, int(rabbit.pos_Y) + 4), 3)


    # Rabbit Movements

    #Reverses direction
    def reverse():
        if rabbit.random_degree < 180:
            rabbit.random_degree + 180
        else:
            rabbit.random_degree - 180

    # Changes direction after every 30 steps
    if rabbit.steps % 30 == 0:
        rabbit.random_degree = random.randint(0,360)


    # Changes speed after every 15 steps
    if rabbit.steps % 15 == 0:
        rabbit.random_speed = random.randint(-100,100) / 5

    rabbit.pos_X += rabbit.random_speed * math.cos(math.radians(
        rabbit.random_degree))
    rabbit.pos_Y += rabbit.random_speed * math.sin(math.radians(
        rabbit.random_degree))



    # Keeps the rabbit qithin boundaries
    if rabbit.pos_X <= 40:
        rabbit.pos_X = 40
        reverse()

    if rabbit.pos_X >= 860:
        rabbit.pos_X = 860
        reverse()

    if rabbit.pos_Y <= 40:
        rabbit.pos_Y = 40
        reverse()

    if rabbit.pos_Y >= 660:
        rabbit.pos_Y = 660
        reverse()


    #Step counter
    rabbit.steps += 1

    #Age counter
    rabbit.age += 1


def rabbit_appear(x, y):
    screen.blit(rabbit_icon, (x, y))


for i in range(rabbit_initial_N):
    gender = 'F' if random.randint(0, 10) % 2 == 0 else 'M'
    # Purposely slightly biased towards generating more females
    rabbit = Rabbit()
    rabbit.id = i
    rabbit.pos_X = random.randint(30, 870)
    rabbit.pos_Y = random.randint(30, 670)
    rabbit.gender = gender
    rabbit_population.append(rabbit)


def print_stats():
    for rabbit in rabbit_population:
        print(rabbit.id,rabbit.age, rabbit.steps, rabbit.gender, len(rabbit_population))


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
            live(rabbit_population[i])

    time.sleep(0.2)

    pygame.display.update()
