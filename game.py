import math
import config
import pygame
import statistics
import map

screen = pygame.display.set_mode((config.screen_width, config.screen_height))
universe_screen = pygame.Surface((config.universe_width,
                                  config.universe_height))

# Grass_area
bound_screen = pygame.Rect(config.tile_width, config.tile_height,
                           config.universe_width -
                           2 * config.tile_width,
                           config.universe_height - 2 * config.tile_height)

pygame.key.set_repeat()


# Object visible in screen
def object_appear(image, x, y):
    universe_screen.blit(image, (x, y))


# Collision function
def isCollided(object1: object, object2_list: list):
    for object2 in object2_list:
        if object2.isAlive:
            distance = math.sqrt((object1.pos_X - object2.pos_X) ** 2 + (
                    object1.pos_Y - object2.pos_Y) ** 2)
            if 40 > distance > 0:
                return object2


# Handle Events
def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            config.game_running = False
            statistics.print_stats()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if map.x_pos_map < 0:
            map.x_pos_map += config.scroll_speed

    if keys[pygame.K_RIGHT]:
        if map.x_pos_map > config.screen_width - config.universe_width:
            map.x_pos_map -= config.scroll_speed

    if keys[pygame.K_UP]:
        if map.y_pos_map < 0:
            map.y_pos_map += config.scroll_speed

    if keys[pygame.K_DOWN]:
        if map.y_pos_map > config.screen_height - config.universe_height:
            map.y_pos_map -= config.scroll_speed
