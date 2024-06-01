import pygame as pg

from gameObject import *

JUSTIFY_LEFT = 0
JUSTIFY_CENTER = 1
JUSTIFY_RIGHT = 2

class Text:
    def __init__(self, game, fontpath, size, color, pos:pg.Vector2, justification=JUSTIFY_LEFT):
        self.game = game

        self.pos = pos
        self.font = pg.font.Font(fontpath, size)
        self.color = color
        self.justification = justification
        
        self.set_text("")
    
    def set_text(self, text:str):
        self.text = text
        self.img = self.font.render(self.text, False, self.color)

    def draw(self, surface:pg.Surface=None):
        if surface == None:
            self.game.screen.blit(self.img, (self.pos.x, self.pos.y))
        else:
            surface.blit(self.img, (self.pos.x, self.pos.y))


class Button:
    def __init__(self) -> None:
        pass


class Panel:
    def __init__(self) -> None:
        self.surface = None
        


# i could probably use a decorator for scroll bars...