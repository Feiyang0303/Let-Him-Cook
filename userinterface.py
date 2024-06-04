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
        if self.justification == JUSTIFY_LEFT:
            npos = self.pos
        elif self.justification == JUSTIFY_CENTER:
            npos = pg.Vector2(self.pos.x - self.img.get_width() / 2, self.pos.y)
        elif self.justification == JUSTIFY_RIGHT:
            npos = pg.Vector2(self.pos.x - self.img.get_width(), self.pos.y)

        if surface == None:
            self.game.screen.blit(self.img, (npos.x, npos.y))
        else:
            surface.blit(self.img, (npos.x, npos.y))

class Button(GameObject):
    def __init__(self, game, rect:pg.Rect, call=lambda:print('button call')) -> None:
        self.game = game
        self.rect = rect
        self.call = call

        self.game.eventees.append(self)

        self.hovering = False
        self.clicking = False

    def immuneUpdate(self):
        mouse_pos = pg.mouse.get_pos()
        self.hovering = self.rect.collidepoint(mouse_pos)

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering:
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False

    def draw(self):
        if self.clicking:
            pg.draw.rect(self.game.screen, (100, 100, 100), self.rect)
        elif self.hovering:
            pg.draw.rect(self.game.screen, (200, 200, 200), self.rect)
        else:
            pg.draw.rect(self.game.screen, (255, 255, 255), self.rect)

class BuyStructureButton(Button):
    def __init__(self, game, rect: pg.Rect, building_id:str) -> None:
        super().__init__(game, rect, lambda:world.build(building_id))

class Panel:
    def __init__(self) -> None:
        self.surface = None
        


# i could probably use a decorator for scroll bars...
# ideally i make a self-refferential ui_element class