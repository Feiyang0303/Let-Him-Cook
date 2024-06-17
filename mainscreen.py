import pygame as pg
import sys
from userinterface import *
from settings import *
from worldrenderer import *


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.title_text = Text(game, pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4), "fonts/pixel-bit-advanced.ttf", 48, (255, 255, 255), justification=JUSTIFY_CENTER, text='LET HIM COOK')

        self.load_game_button = Button(game, pg.Vector2(0, SCREEN_HEIGHT / 4 + 200), pg.Vector2(SCREEN_WIDTH, 50), call=self.load_game)
        self.load_game_button_text = Text(game, pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 200), "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), justification=JUSTIFY_CENTER, text='LOAD GAME')

        self.new_game_button = Button(game, pg.Vector2(0, SCREEN_HEIGHT / 4 + 300), pg.Vector2(SCREEN_WIDTH, 50), call=self.new_game)
        self.new_game_button_text = Text(game, pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 300), "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), justification=JUSTIFY_CENTER, text='NEW GAME')

    def load_game(self):
        self.new_game_button.disable()
        self.load_game_button.disable()

        print("pressed load button")

        self.game.load_game()
        self.game.set_game_state(PLAY_STATE)
    
    def new_game(self):
        self.new_game_button.disable()
        self.load_game_button.disable()

        self.game.new_game()
        self.game.set_game_state(PLAY_STATE)

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.title_text.draw()

        self.load_game_button.draw()
        self.load_game_button_text.draw()
        self.new_game_button.draw()
        self.new_game_button_text.draw()

    def update(self):
        self.load_game_button.update()
        self.new_game_button.update()

    def immune_update(self):
        self.load_game_button.immune_update()
        self.new_game_button.immune_update()
