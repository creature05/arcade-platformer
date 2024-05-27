import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

class BadAttempt(arcade.View):

    def __init__(self, objectives, score):
        super().__init__()
        self.objectives = objectives
        self.score = score
        

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.DARK_GREEN)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Do Better!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 1.5,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
        arcade.draw_text(
            f"You've finished the game and didn't collect a single gem.",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                25,
                anchor_x="center",
            )
        
        arcade.draw_text(
            f"Score: {self.score}",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2.5,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )

class PrettyBadAttempt(arcade.View):

    def __init__(self, objectives, score):
        super().__init__()
        self.objectives = objectives
        self.score = score

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.DARK_GREEN)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Try again!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 1.5,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
        arcade.draw_text(
            f"You've finished the game but only collected {self.objectives} out of 15 gems.",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                25,
                anchor_x="center",
            )

        arcade.draw_text(
            f"Score: {self.score}",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2.5,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = MyGame()
        self.window.show_view(game_view)

class NotCloseToWin(arcade.View):

    def __init__(self, objectives, score):
        super().__init__()
        self.objectives = objectives
        self.score = score

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.DARK_GREEN)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "you can do better!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 1.5,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
        arcade.draw_text(
            f"You've finished the game but only collected {self.objectives} out of 15 gems.",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                25,
                anchor_x="center",
            )

        arcade.draw_text(
            f"Score: {self.score}",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2.5,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )
    
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        game_view = MyGame()
        self.window.show_view(game_view)

class AlmostWin(arcade.View):

    def __init__(self, objectives, score):
        super().__init__()
        self.objectives = objectives
        self.score = score

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.DARK_GREEN)
    
    def on_draw(self):
        self.clear()
        arcade.draw_text(
            "Good Job!",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 1.5,
                arcade.color.WHITE,
                30,
                anchor_x="center",
            )
        arcade.draw_text(
            f"You've finished the game and collected {self.objectives} out of 15 gems.",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                25,
                anchor_x="center",
            )

        arcade.draw_text(
            f"Score: {self.score}",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2.5,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        arcade.close_window()


class Win(arcade.View):
    """Class to manage the game overview"""

    def __init__(self, objectives, score):
        super().__init__()
        self.objectives = objectives
        self.score = score

    def on_show_view(self):
        """Called when switching to this view"""
        arcade.set_background_color(arcade.color.DARK_GREEN)

    def on_draw(self):
        """Draw the game overview"""    
        self.clear()
        arcade.draw_text(
            "You Win!",
            SCREEN_WIDTH / 2,
            SCREEN_HEIGHT / 1.5,
            arcade.color.WHITE,
            30,
            anchor_x="center",
        )
        arcade.draw_text(
            f"You've finished the game and collected all 15 gems, great job.",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2,
                arcade.color.WHITE,
                25,
                anchor_x="center",
            )
        arcade.draw_text(
            f"Score: {self.score}",
                SCREEN_WIDTH / 2,
                SCREEN_HEIGHT / 2.5,
                arcade.color.WHITE,
                20,
                anchor_x="center",
            )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """Use a mouse press to advance to the 'game' view."""
        arcade.close_window()
