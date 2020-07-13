import pygame

#Game Specifications
screen_width, screen_height = 1200, 780
days = 0

# Rabbit
rabbit_image = [pygame.image.load("./img/rabbit_walk/rabbit" + str(i) +
                                  ".png") for i in range(1, 4)]
rabbit_image_quad1 = [pygame.image.load("./img/rabbit_walk/right_rabbit" + str(
    i) + ".png") for i in range(1, 4)]
rabbit_initial_N = 10
rabbit_population = []
rabbit_gestation_period = 200
# Also includes the time after birth to avoid inbreeding
rabbit_childhood = 70


#Grass
grass_image = pygame.image.load("./img/grass.png")
grass_quantity = 130
grass_list = []


