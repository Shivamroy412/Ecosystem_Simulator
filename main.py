import pygame
import random
import time

#Initialize pygame

pygame.init()


#Game Screen

screen = pygame.display.set_mode((900,700))
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

def rabbit_appear(x,y):
    screen.blit(rabbit_icon, (x, y))


for i in range(rabbit_initial_N):

    gender = 'M' if random.randint(0,1) == 1 else 'F'
    rabbit = Rabbit()
    rabbit.pos_X = random.randint(30, 870)
    rabbit.pos_Y = random.randint(30, 670)
    rabbit.gender = gender
    rabbit_population.append(rabbit)










#Game_Loop

game_running = True
while game_running:

    screen.fill((11, 102, 35))  # Color of grass

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False



    # Rabbit appears at a random space


    for i in range(rabbit_initial_N):

        rabbit_appear(rabbit_population[i].pos_X, rabbit_population[i].pos_Y)
        rabbit_speed_X = random.random()*6 - 3
        rabbit_speed_Y = random.random()*1 - 0.5
        rabbit_population[i].pos_X += rabbit_speed_X
        rabbit_population[i].pos_Y += rabbit_speed_Y
        print(rabbit_population[i].gender)


        # Keeping the rabbit within boundaries
        if rabbit_population[i].pos_X <= 0:
            rabbit_population[i].pos_X = 0
        if rabbit_population[i].pos_X >= 850:
            rabbit_population[i].pos_X = 850
        if rabbit_population[i].pos_Y <= 0:
            rabbit_population[i].pos_Y = 0
        if rabbit_population[i].pos_Y >= 650:
            rabbit_population[i].pos_Y = 650

    time.sleep(0.2)

    pygame.display.update()


