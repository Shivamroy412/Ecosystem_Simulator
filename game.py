import math
import config
import random
import organisms
import pygame


screen = pygame.display.set_mode((config.screen_width, config.screen_height))

# Object visible in screen
def object_appear(image, x, y):
    screen.blit(image, (x, y))



# Collision function
def isCollided(object1: object, object2_list: list):
    for object2 in object2_list:
        if object2.isAlive:
            distance = math.sqrt((object1.pos_X - object2.pos_X) ** 2 + (
                    object1.pos_Y - object2.pos_Y) ** 2)
            if object2 is not organisms.Grass:
                object2.reason_of_death = "Eaten by predator"
            if 40 > distance > 0:
                return object2

