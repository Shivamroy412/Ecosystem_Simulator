import pygame
import random
import time

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
        self.pos_X = 0
        self.pos_Y = 0
        self.age = 0
        self.gender = ''
        self.isAlive = True
        self.steps = 0
        self.direction_randomiser = 0


def movement(rabbit: object):
    rabbit_appear(rabbit.pos_X, rabbit.pos_Y)

    if rabbit.steps % 15 is 0:
        rabbit.direction_randomiser = random.randint(1,4)

    rabbit_speed_X_right = random.randint(-99, 199) / 35
    rabbit_speed_X_left = random.randint(-199, 99) / 35
    rabbit_speed_Y_top = random.randint(-199, 99) / 35
    rabbit_speed_Y_bottom = random.randint(-99, 199) / 35

    if rabbit.direction_randomiser == 1:
        rabbit.pos_X += rabbit_speed_X_right
    if rabbit.direction_randomiser == 2:
        rabbit.pos_X += rabbit_speed_X_left
    if rabbit.direction_randomiser == 3:
        rabbit.pos_Y += rabbit_speed_Y_bottom
    if rabbit.direction_randomiser == 4:
        rabbit.pos_Y += rabbit_speed_Y_top

    # print(rabbit_population[i].gender)

    # Keeping the rabbit within boundaries
    if rabbit.pos_X <= 0:
        rabbit.pos_X = 0
    if rabbit.pos_X >= 850:
        rabbit.pos_X = 850
    if rabbit.pos_Y <= 0:
        rabbit.pos_Y = 0
    if rabbit.pos_Y >= 650:
        rabbit.pos_Y = 650

    print(rabbit.direction_randomiser)
    rabbit.steps += 1

def rabbit_appear(x, y):
    screen.blit(rabbit_icon, (x, y))


for i in range(rabbit_initial_N):
    gender = 'M' if random.randint(0, 1) == 1 else 'F'
    rabbit = Rabbit()
    rabbit.pos_X = random.randint(30, 870)
    rabbit.pos_Y = random.randint(30, 670)
    rabbit.gender = gender
    rabbit_population.append(rabbit)

# Game_Loop

game_running = True
while game_running:

    screen.fill((11, 102, 35))  # Color of grass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Rabbit appears at a random space
    for i in range(len(rabbit_population)):
        movement(rabbit_population[i])

    time.sleep(0.2)

    pygame.display.update()
