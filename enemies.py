#
# Enemy Sprite Code for Capstone Game
#

import arcade
from entity import Entity
from constants import RIGHT_FACING, LEFT_FACING, CHARACTER_SCALING


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
    def __init__(
        self,
    ):

        # set up parent class
        super().__init__("zombie", "zombie")

        self.scale = CHARACTER_SCALING * 2
        self.health = 300


class SuperRobot(Enemy):
    def __init__(
        self,
    ):

        # set up parent class
        super().__init__("robot", "robot")

        self.scale = CHARACTER_SCALING * 3
        self.health = 10000
