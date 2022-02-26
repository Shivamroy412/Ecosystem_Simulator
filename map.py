import config
import game

y_pos_map = 0
x_pos_map = 0


class Map:

    def __init__(self):
        self.tile_image = ''
        self.pos_X = 0
        self.pos_Y = 0
        self.terrain_type = ''

    def render_map():
        cam_y_pos_map = 0
        for row in config.map:
            cam_x_pos_map = 0
            for tile in row:
                if tile in config.tile_image_mapping:
                    map_tile_object = Map()
                    map_tile_object.tile_image = \
                        config.tile_image_mapping[tile]
                    map_tile_object.pos_X = cam_x_pos_map
                    map_tile_object.pos_Y = cam_y_pos_map
                    map_tile_object.terrain_type = tile
                    game.object_appear(map_tile_object.tile_image,
                                       map_tile_object.pos_X,
                                       map_tile_object.pos_Y)
                    config.map_tiles_list.append(map_tile_object)

                cam_x_pos_map += config.tile_width
            cam_y_pos_map += config.tile_height
