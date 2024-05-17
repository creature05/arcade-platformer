# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
TILE_SCALING = 0.5
CHARACTER_SCALING = TILE_SCALING * 2
COIN_SCALING = TILE_SCALING
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Shooting Constants
SPRITE_SCALING_LASER = 0.8
SHOOT_SPEED = 10
BULLET_SPEED = 50
BULLET_DAMAGE = 25

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 30
GRAVITY = 1.5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

# Player starting position
PLAYER_START_X = 1
PLAYER_START_Y = 7

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# Constants for hearts
HEART_SCALE = 0.25

# Layer names from our tilemap
LAYER_NAME_MOVING_PLATFORMS = "Moving Platforms"
LAYER_NAME_PLATFORMS = "Platforms"
# LAYER_NAME_INTERACTIVE_PLATFORMS = "Interactive Platforms"
LAYER_NAME_COINS = "Coins"
LAYER_NAME_BACKGROUND = "Background"
LAYER_NAME_LADDERS = "Ladders"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Enemies"
LAYER_NAME_BULLETS = "Bullets"
LAYER_NAME_DONT_TOUCH = "Don't Touch"
LAYER_NAME_POWER_UP = "Power Up"
LAYER_NAME_END_LEVEL = "End Level"
LAYER_NAME_OBJECTIVE = "Objective"
LAYER_NAME_INTERACTIVE = "Interactive"

# PLATFORMS = [LAYER_NAME_PLATFORMS, LAYER_NAME_INTERACTIVE_PLATFORMS]
