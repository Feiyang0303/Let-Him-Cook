import pygame as pg
from settings import *



class PreferenceScreen:
    
    def __init__(self, game) -> None:
        self.game = game

        self.faded_screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.faded_screen.fill((0, 0, 0))
        self.faded_screen.set_alpha(180) # 0 - 255

    def update(self):
        # make sliders
        pass


    
    def draw(self):
        self.game.screen.blit(self.faded_screen, (0, 0))
        # pg.draw.rect(self.game.screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA,32)
        
        # draw the background

        # draw pause text
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render("Game Paused", True, (225,225,225))
        self.game.screen.blit(text,(180,60))
        # draw the sliders

