#
# Helper functions for capstone game
#
import arcade

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]
