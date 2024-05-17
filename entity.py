#
# Base Entity Sprite for capstone game
#

import arcade
from helpers import load_texture_pair
from constants import RIGHT_FACING, CHARACTER_SCALING

class Entity(arcade.Sprite):
    def __init__(self, name_folder, name_file):
        super().__init__()

        # default to facing right
        self.facing_direction = RIGHT_FACING

        # used for image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        main_path = f":resources:images/animated_characters/{name_folder}/{name_file}"

        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}_jump.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}_fall.png")

        # load textures for walking
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture(f"{main_path}_climb0.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture(f"{main_path}_climb1.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used
        self.set_hit_box(self.texture.hit_box_points)
