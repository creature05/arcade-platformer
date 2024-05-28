# Capstone Game

## Requirements

All requirements are listed in the `requirements.txt` file.

### Python Version
Minimum of Python 3.11.4

### Arcade Version
Minimum of arcade 2.6.17

### Installation

After cloning the repo into a new folder, perform the following:
```shell
$ cd new-folder
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

To run the game:
```shell
$ python capstone_game.py 
```

## Game Instructions

### Objective
Your objective is to survive all 5 levels and collect all 15 gems. To continue to the next level you need to reach the flag at the end of the current level. You start with 3 lives and you have three hit points before you lose a life. If you lose all of your lives then you get a Game Over. Good luck!

### Controls
Jump: W or ↑  
Move Left: A or ←  
Move Right: D or →  
Shoot: Q  

### Power-Ups
Invincibility: if you pick up a star you become immune to damage for 8 seconds. any enemy you run into dies instantly.

Super Jump: if you pick up a red mushroom with dots then you can jump extra high for five seconds.

Heart: if you find a heart on the map and you have less than 3 hit points, you gain another hit point.

1UP: if you pick up a brown mushroom then you get an extra life.






