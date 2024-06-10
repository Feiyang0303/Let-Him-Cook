import pygame as pg
import sys
from userinterface import *
from settings import *
from worldrenderer import *


class MainMenu:
    def __init__(self, game):
        self.game = game
        self.title_text = Text(game, pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4), "fonts/pixel-bit-advanced.ttf",
                               56, (255, 255, 255), justification=JUSTIFY_CENTER, text='LET HIM COOK')
        self.start_button = Button(game, pg.Vector2(SCREEN_WIDTH / 2 - 100, SCREEN_HEIGHT / 4 + 200),
                                   pg.Vector2(200, 50), call=self.start_game)
        self.start_button_text = Text(game, pg.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4 + 200),
                                      "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), justification=JUSTIFY_CENTER,
                                      text='START')

    def start_game(self):
        print("GAME START!")
        # self.game.new_game()
        self.game.set_game_state(PLAY_STATE)
        self.start_button.disable()

    def draw(self):
        self.game.screen.fill((0, 0, 0))
        self.title_text.draw()
        self.start_button.draw()
        self.start_button_text.draw()

    def update(self):
        self.start_button.update()


    def immuneUpdate(self):
        self.start_button.immuneUpdate()
