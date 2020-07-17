import math
import random
import pygame
import game
import config


def move_creature(creature: object):
    if 90 < creature.random_degree <= 180:
        game.object_appear(pygame.transform.rotate(config.rabbit_image[
                                                       creature.steps % 3], 10),
                           creature.pos_X, creature.pos_Y)

    elif 180 < creature.random_degree <= 270:
        game.object_appear(
            pygame.transform.rotate(config.rabbit_image[creature.steps % 3],
                                    -10),
            creature.pos_X, creature.pos_Y)

    elif 0 < creature.random_degree <= 90:
        game.object_appear(pygame.transform.rotate(
            config.rabbit_image_quad1[creature.steps % 3],
            -10), creature.pos_X, creature.pos_Y)

    else:
        game.object_appear(pygame.transform.rotate(
            config.rabbit_image_quad1[creature.steps % 3], 10), creature.pos_X,
            creature.pos_Y)

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
        creature.random_degree = random.randint(0, 360)

    creature.pos_X += creature.random_speed * math.cos(math.radians(
        creature.random_degree))
    creature.pos_Y += creature.random_speed * math.sin(math.radians(
        creature.random_degree))

    # Reverses direction
    def reverse():
        if creature.random_degree < 180:
            creature.random_degree += 180
        else:
            creature.random_degree -= 180

    # Keeps the rabbit within the boundaries
    if creature.pos_X <= game.bound_screen.left + 32:
        creature.pos_X = game.bound_screen.left + 32
        reverse()

    if creature.pos_X >= game.bound_screen.right - 32:
        creature.pos_X = game.bound_screen.right - 32
        reverse()

    if creature.pos_Y <= game.bound_screen.top + 32:
        creature.pos_Y = game.bound_screen.top + 32
        reverse()

    if creature.pos_Y >= game.bound_screen.bottom - 32:
        creature.pos_Y = game.bound_screen.bottom - 32
        reverse()
