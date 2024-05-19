import os
import math
import arcade
import win_views

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

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


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


class Enemy(Entity):
    def __init__(self, name_folder, name_file):

        # setup parent class
        super().__init__(name_folder, name_file)

        self.should_update_walk = 0
        self.health = 0

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        if self.should_update_walk == 3:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
            self.texture = self.walk_textures[self.cur_texture][self.facing_direction]
            self.should_update_walk = 0
            return

        self.should_update_walk += 1


class RobotEnemy(Enemy):
    def __init__(self):
        # Set up parent class
        super().__init__("robot", "robot")

        self.health = 100


class ZombieEnemy(Enemy):
    def __init__(self):

        # set up parent class
        super().__init__("zombie", "zombie")

        self.health = 50

class SuperZombie(Enemy):
    def __init__(self,):

        # set up parent class
        super().__init__("zombie", "zombie")

        self.scale = CHARACTER_SCALING * 2
        self.health = 300

class SuperRobot(Enemy):
    def __init__(self,):

        # set up parent class
        super().__init__("robot", "robot")

        self.scale = CHARACTER_SCALING * 3
        self.health = 10000


class PlayerCharacter(Entity):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__("male_adventurer", "maleAdventurer")

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.facing_direction]


class MainMenu(arcade.View):
    """Class that manages the 'menu' view."""

    def on_show_view(self):
        """Called when switching to this view."""
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        arcade.draw_text(
            "Main Menu - Click to play",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.BLACK,
            font_size=30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = MyGame()
        self.window.show_view(game_view)

class Heart(arcade.Sprite):
    def __init__(self, filename, scaling):
        super().__init__(filename, scaling)


class MyGame(arcade.View):
    """
    Main application class.
    """

    def __init__(self, level = 1, tries = 3, objectives = 0):

        # Call the parent class and set up the window
        super().__init__()

        # Set the path to start with this program
        self.file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(self.file_path)

        # List to hold heart sprites
        self.hearts = []

        # player health
        self.player_health = 3

        self.damage_timer = 0

        # Create hearts based on player's initial health
        for i in range(self.player_health):
            heart = Heart("./assets/images/HUD/hudHeart_full.png", HEART_SCALE)
            self.position = heart.width
            self.hearts.append(heart)

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.shoot_pressed = False
        self.jump_needs_reset = False

        # Our tilemap object
        self.tile_map = None

        # Scene Object
        self.scene = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        self.enemy_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Enemies physics engine
        # self.enemy_physics_engine = None

        # Camera
        self.camera = None

        # A camera that can be used to draw GUI elements
        self.gui_camera = None

        # Keep track of the score
        self.score = 0

        self.level_1_score = 0

        self.level_2_score = 0

        self.level_3_score = 0

        # Keep track of the objectives
        self.objectives = objectives

        self.level_1_objectives = 0
     
        self.level_2_objectives = 0

        self.level_3_objectives = 0

        self.level_4_objectives = 0

        self.level_5_objectives = 0

        # keep track of deaths

        self.tries = tries

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0

        # # Enemy shooting mechanics
        self.enemy_can_shoot = False
        self.enemy_shoot_timer = 0
       
        # Level
        self.level = level

        # Invincible timer
        self.invincible_timer = 0

        # super speed timer
        self.speed_timer = 0

        # super jump timer
        self.jump_timer = 0

        # keep track of buttons pressed
        self.buttons = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")

    def setup(self):
        """Set up the game here. Call this function to restart the game."""

        # Set up the camera
        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        # Name of map file to load
        my_map = f"{self.file_path}/assets/levels/platformer_level_{self.level}.json"
        # ":resources:tiled_maps/map_with_ladders.json"

        # Layer specific options from the tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True
            },
            # LAYER_NAME_INTERACTIVE_PLATFORMS: {
            #     "use_spatial_hash": True
            # },
            LAYER_NAME_MOVING_PLATFORMS: {
                "use_spatial_hash": False
            },
            LAYER_NAME_LADDERS: {
                "use_spatial_hash": True
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True
            },
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True
            },
            LAYER_NAME_POWER_UP: {
                "use_spatial_hash": True
            },
            LAYER_NAME_END_LEVEL: {
                "use_spatial_hash": True
            },
            LAYER_NAME_OBJECTIVE: {
                "use_spatial_hash": True
            },
            LAYER_NAME_INTERACTIVE: {
                "use_spatial_hash": True
            }
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(my_map, TILE_SCALING, layer_options)

        # Initialize scene with our tilemap, this will automatically add all layers
        # from the map as spritelists in the scene in the proper order
        self.scene = arcade.Scene.from_tilemap(self.tile_map)
        
        # self.enemy_sprite = Enemy()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = (
            self.tile_map.tile_width * TILE_SCALING * PLAYER_START_X
        )
        self.player_sprite.center_y = (
            self.tile_map.tile_height * TILE_SCALING * PLAYER_START_Y
        )
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE

        # enemies
        if LAYER_NAME_ENEMIES in self.tile_map.object_lists:
            enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

            for my_object in enemies_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )
                enemy_type = my_object.properties["type"]
                if enemy_type == "robot":
                    enemy = RobotEnemy()
                elif enemy_type == "zombie":
                    enemy = ZombieEnemy()
                elif enemy_type == "super zombie":
                    enemy = SuperZombie()
                elif enemy_type == "super robot":
                    enemy = SuperRobot()
                enemy.center_x = math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                )
                enemy.center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )
                if "boundary_left" in my_object.properties:
                    enemy.boundary_left = my_object.properties["boundary_left"]
                if "boundary_right" in my_object.properties:
                    enemy.boundary_right = my_object.properties["boundary_right"]
                if "change_x" in my_object.properties:
                    enemy.change_x = my_object.properties["change_x"]
                self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

        # Add bullet spritelist to Scene
        self.scene.add_sprite_list(LAYER_NAME_BULLETS)

        # --- other stuff
        # set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            platforms=self.scene[LAYER_NAME_MOVING_PLATFORMS],
            gravity_constant=GRAVITY,
            ladders=self.scene[LAYER_NAME_LADDERS],
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )


    def on_show_view(self):
        self.setup()

    def draw_hearts(self):
        xpos = SCREEN_WIDTH-30
        for i in range(self.player_health):
            self.hearts[i].position = (xpos, 30)
            self.hearts[i].draw()
            xpos -= 30

    def on_draw(self):
        """Render the screen."""

        # Activate the camera
        self.camera.use()

        # Clear the screen to the background color
        self.clear()

        # Draw our scene
        self.scene.draw()

        # Activate the GUI camera before drawing GUI elements
        self.gui_camera.use()

        # Draw our score on the screen, scrolling it with the viewport


        objective_text = f"Objectives: {self.objectives}/15"
        arcade.draw_text(
            objective_text,
            10,
            10,
            arcade.csscolor.BLACK,
            18,
        )

        life_text = f"Lives: {self.tries}"
        arcade.draw_text(
            life_text,
            10,
            620,
            arcade.csscolor.BLACK,
            18,
        )

        # Draw hearts
        self.draw_hearts()

        # Draw invincible timer
        if self.invincible_timer <= 0:
            pass
        else:
            invincible_text = f"Invincible: {int(self.invincible_timer)}"
            arcade.draw_text(
                invincible_text,
                10,
                40,
                arcade.csscolor.BLACK,
                18,
            )

        if self.speed_timer <= 0:
            pass
        else:
            speed_timer_text = f"Super Speed: {int(self.speed_timer)}"
            arcade.draw_text(
                speed_timer_text,
                10,
                70,
                arcade.csscolor.BLACK,
                18,
            )

        if self.jump_timer <= 0:
            pass
        else:
            jump_timer_text = f"Super Jump: {int(self.jump_timer)}"
            arcade.draw_text(
                jump_timer_text,
                10,
                70,
                arcade.csscolor.BLACK,
                18,
            )

    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset and self.jump_timer <= 0
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
            elif (
                self.physics_engine.can_jump(y_distance=10)
                and not self.jump_needs_reset
            ):
                self.player_sprite.change_y = PLAYER_JUMP_SPEED * 1.5
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            if self.speed_timer <= 0:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * 2
        elif self.left_pressed and not self.right_pressed:
            if self.speed_timer <= 0:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            else:
                self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED * 2
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        if key == arcade.key.Q:
            self.shoot_pressed = True

        if key == arcade.key.PLUS:
            self.camera.zoom(0.01)
        elif key == arcade.key.MINUS:
            self.camera.zoom(-0.01)

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key"""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        if key == arcade.key.Q:
            self.shoot_pressed = False

        self.process_keychange()

    def center_camera_to_player(self, speed=0.2):
        """Keeps camera centered on the player"""
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered, speed)

    def on_update(self, delta_time):
        """Movement and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()


        # self.enemy_physics_engine.update()

        # Update hearts
        # self.update_hearts()


        # Creates a timer for the invincible power up
        if self.invincible_timer > 0:
            self.invincible_timer -= delta_time
        elif self.invincible_timer <= 0:
            self.invincible_timer = 0

        # Creates a cool down timer after taking damage
        if self.damage_timer > 0:
            self.damage_timer -= delta_time
        elif self.damage_timer <= 0:
            self.damage_timer = 0

        # Creates a timer for super speed power up
        if self.speed_timer > 0:
            self.speed_timer -= delta_time
        elif self.speed_timer <= 0:
            self.speed_timer = 0

        # Creates a timer for the super jump ability
        if self.jump_timer > 0:
            self.jump_timer -= delta_time
        elif self.jump_timer <= 0:
            self.jump_timer = 0

        # Did the player fall off the map?
        if self.player_sprite.center_y < -100:
            self.tries -= 1
            if self.tries == 0:
                arcade.play_sound(self.game_over)
                game_over = GameOverView()
                self.window.show_view(game_over)
            elif self.tries > 0:
                arcade.play_sound(self.game_over)
                respawn = RespawnView(self.level, self.tries, self.objectives)
                self.window.show_view(respawn)

        # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
            self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            if self.invincible_timer > 0:
                pass
            else:
                self.tries -= 1
                if self.tries == 0:
                    arcade.play_sound(self.game_over)
                    game_over = GameOverView()
                    self.window.show_view(game_over)
                elif self.tries > 0:
                    arcade.play_sound(self.game_over)
                    respawn = RespawnView(self.level, self.tries, self.objectives)
                    self.window.show_view(respawn)
            


        # Update animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        # if self.enemy_can_shoot:
        #     enemy_type = my_object.properties["type"]
        #     if enemy_type == "super robot":
        #         if self.enemy_shoot_timer == SHOOT_SPEED:
        #             arcade.play_sound(self.shoot_sound)
        #             bullet = arcade.Sprite(
        #                 ":resources:images/space_shooter/laserBlue01.png",
        #                 SPRITE_SCALING_LASER,
        #             )

        #             if self.enemy_sprite.facing_direction == RIGHT_FACING:
        #                 bullet.change_x = BULLET_SPEED
        #             else:
        #                 bullet.change_x = -BULLET_SPEED

        #             bullet.center_x = self.enemy_sprite.center_x
        #             bullet.center_y = self.enemy_sprite.center_y

        #             self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

        #             if self.enemy_shoot_timer == 5:
        #                 self.enemy_can_shoot = False
        #             self.enemy_shoot_timer == 0

        #     else:
        #         pass
        # else:
        #     self.enemy_shoot_timer += delta_time
        #     if self.enemy_shoot_timer == SHOOT_SPEED:
        #         self.enemy_can_shoot = True
        #         self.enemy_shoot_timer = 0


        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite(
                    ":resources:images/space_shooter/laserBlue01.png",
                    SPRITE_SCALING_LASER,
                )

                if self.player_sprite.facing_direction == RIGHT_FACING:
                    bullet.change_x = BULLET_SPEED
                else:
                    bullet.change_x = -BULLET_SPEED

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y

                self.scene.add_sprite(LAYER_NAME_BULLETS, bullet)

                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0

        # update animations
        if LAYER_NAME_ENEMIES in self.tile_map.object_lists:
            self.scene.update_animation(
                delta_time,
                [
                    LAYER_NAME_COINS,
                    LAYER_NAME_BACKGROUND,
                    LAYER_NAME_PLAYER,
                    LAYER_NAME_ENEMIES,
                ],
            )
        else:
            self.scene.update_animation(
                delta_time, [LAYER_NAME_COINS, LAYER_NAME_BACKGROUND, LAYER_NAME_PLAYER]
            )

        # update moving platforms, enemies, and bullets
        if LAYER_NAME_ENEMIES in self.tile_map.object_lists:
            self.scene.update(
                [LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_ENEMIES, LAYER_NAME_BULLETS]
            )

            # see if the enemy hit a boundary and needs to reverse direction
            for enemy in self.scene[LAYER_NAME_ENEMIES]:
                if (
                    enemy.boundary_right
                    and enemy.right > enemy.boundary_right
                    and enemy.change_x > 0
                ):
                    enemy.change_x *= -1

                if (
                    enemy.boundary_left
                    and enemy.left < enemy.boundary_left
                    and enemy.change_x < 0
                ):
                    enemy.change_x *= -1
        else:
            self.scene.update([LAYER_NAME_MOVING_PLATFORMS, LAYER_NAME_BULLETS])

        for bullet in self.scene[LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene[LAYER_NAME_ENEMIES],
                    self.scene[LAYER_NAME_PLATFORMS],
                    # self.scene[LAYER_NAME_INTERACTIVE_PLATFORMS],
                    self.scene[LAYER_NAME_MOVING_PLATFORMS]
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                        # The collision was with an enemy
                        collision.health -= BULLET_DAMAGE

                        if collision.health <= 0:
                            self.score += 100
                            collision.remove_from_sprite_lists()
                            

                        # Hit sound
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                bullet.left
                > (self.tile_map.width * self.tile_map.tile_width) * TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()

        if LAYER_NAME_ENEMIES or LAYER_NAME_COINS or LAYER_NAME_POWER_UP or LAYER_NAME_END_LEVEL or LAYER_NAME_OBJECTIVE in self.tile_map.object_lists:
            player_collision_list = arcade.check_for_collision_with_lists(
                self.player_sprite,
                [
                self.scene[LAYER_NAME_ENEMIES], 
                self.scene[LAYER_NAME_COINS], 
                self.scene[LAYER_NAME_POWER_UP], 
                self.scene[LAYER_NAME_END_LEVEL],
                self.scene[LAYER_NAME_OBJECTIVE],
                self.scene[LAYER_NAME_INTERACTIVE]
                ]
            )

            # Loop through each coin we hit (if any) and remove it.
            # see if we hit any enemies.
            for collision in player_collision_list:
                if self.scene[LAYER_NAME_COINS] in collision.sprite_lists:
                    # Figure out how many points this coin is worth
                    if "Points" not in collision.properties:
                        print("warning, collected a coin without a Points property.")
                    else:
                        points = int(collision.properties["Points"])
                        self.score += points

                    # Remove the coin
                    collision.remove_from_sprite_lists()
                    arcade.play_sound(self.collect_coin_sound)

                elif self.scene[LAYER_NAME_POWER_UP] in collision.sprite_lists:
                    power_up_type = collision.properties["type"]
                    if power_up_type == "Invincible":
                        self.invincible_timer += 8
                        collision.remove_from_sprite_lists()
                        arcade.play_sound(self.collect_coin_sound)
                    elif power_up_type == "health":
                        if self.player_health >= 3:
                            pass
                        else:
                            self.player_health += 1
                            print(self.player_health)
                            collision.remove_from_sprite_lists()
                            arcade.play_sound(self.collect_coin_sound)
                    elif power_up_type == "speed":
                        self.speed_timer += 5
                        collision.remove_from_sprite_lists()
                        arcade.play_sound(self.collect_coin_sound)
                    elif power_up_type == "super jump":
                        self.jump_timer += 5
                        collision.remove_from_sprite_lists()
                        arcade.play_sound(self.collect_coin_sound)
                    elif power_up_type == "one up":
                        self.tries += 1
                        collision.remove_from_sprite_lists()
                        arcade.play_sound(self.collect_coin_sound)
                    else:
                        collision.remove_from_sprite_lists()
                        arcade.play_sound(self.collect_coin_sound)

                elif self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                    if self.invincible_timer > 0:  
                        collision.remove_from_sprite_lists()
                        self.score += 100
                        arcade.play_sound(self.hit_sound)
                    elif self.damage_timer > 0:
                        pass
                    else:
                        self.player_health -= 1
                        arcade.play_sound(self.hit_sound)
                        self.damage_timer += 1
                        print(self.player_health)
                        if self.player_health <= 0:
                            self.tries -= 1
                            if self.tries == 0:
                                arcade.play_sound(self.game_over)
                                game_over = GameOverView()
                                self.window.show_view(game_over)
                            elif self.tries > 0:
                                arcade.play_sound(self.game_over)
                                respawn = RespawnView(self.level, self.tries, self.objectives)
                                self.window.show_view(respawn)



                elif self.scene[LAYER_NAME_INTERACTIVE] in collision.sprite_lists:
                    self.buttons += 1
                    collision.remove_from_sprite_lists()
                    arcade.play_sound(self.hit_sound)
                    if self.buttons >= 3:
                        delete_list = []

                        for tile in self.scene[LAYER_NAME_MOVING_PLATFORMS]:
                            delete_list.append(tile)
                        for tile in delete_list:
                            tile.remove_from_sprite_lists()
                        
                        
                            
                        
                                           


                # handles changing levels
                elif self.scene[LAYER_NAME_END_LEVEL] in collision.sprite_lists:
                    if self.level < 5:
                        level_score_key = f"level_{self.level}_score"
                        self.__dict__[level_score_key] = self.__dict__.get(level_score_key, 0) + self.score
                        self.level += 1
                        self.setup()
                    else:
                        if self.objectives >= 12:    
                            win = win_views.Win(self.objectives)
                            self.window.show_view(win)
                        elif self.objectives >= 9:
                            almost_win = win_views.AlmostWin(self.objectives)
                            self.window.show_view(almost_win) 
                        elif self.objectives >= 6:
                            not_close_to_win = win_views.NotCloseToWin(self.objectives)
                            self.window.show_view(not_close_to_win) 
                        elif self.objectives >= 1:
                            pretty_bad_attempt = win_views.PrettyBadAttempt(self.objectives)
                            self.window.show_view(pretty_bad_attempt)
                        elif self.objectives == 0:
                            bad_attempt = win_views.BadAttempt(self.objectives)
                            self.window.show_view(bad_attempt)

                # handles objectives
                elif self.scene[LAYER_NAME_OBJECTIVE] in collision.sprite_lists:
                    if self.level == 1:
                        self.level_1_objectives += 1
                        self.objectives += 1
                    elif self.level == 2:
                        self.level_2_objectives += 1
                        self.objectives += 1
                    elif self.level == 3:
                        self.level_3_objectives += 1
                        self.objectives += 1
                    elif self.level == 4:
                        self.level_4_objectives += 1
                        self.objectives += 1
                    elif self.level == 5:
                        self.level_5_objectives += 1
                        self.objectives += 1
                    collision.remove_from_sprite_lists()
                    arcade.play_sound(self.collect_coin_sound)
                    print(self.objectives)

        # Position the camera
        self.center_camera_to_player()


class GameOverView(arcade.View):
    """Class to manage the game overview"""

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "Game Over - Click to restart",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = MyGame()
        self.window.show_view(game_view)

class RespawnView(arcade.View):
    """Class to manage the game overview"""

    def __init__(self, level, tries, objectives):
        super().__init__()
        self.level = level
        self.tries = tries
        self.objectives = objectives

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """Draw the game overview"""
        self.clear()
        arcade.draw_text(
            "You died - Click to restart the level",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 2,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view.""" 
        game_view = MyGame(self.level, self.tries, self.objectives)
        self.window.show_view(game_view)
        

def main():
    """Main function"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
