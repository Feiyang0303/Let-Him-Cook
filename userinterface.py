import pygame as pg

from gameObject import *

JUSTIFY_LEFT = 0
JUSTIFY_CENTER = 1
JUSTIFY_RIGHT = 2

class UIElement(GameObject):
    def __init__(self, game, pos: pg.Vector2, hitbox=pg.Vector2(0, 0), parentPanel=None) -> None:
        self.parentPanel = parentPanel

        if not parentPanel == None:
            super().__init__(game, parentPanel.pos + pos, hitbox)
        else:
            super().__init__(game, pos, hitbox)


class Text(UIElement):
    def __init__(self, game, pos:pg.Vector2, fontpath, size, color, justification=JUSTIFY_LEFT, text="default", parentPanel=None):
        super().__init__(game, pos, parentPanel)
        
        self.font = pg.font.Font(fontpath, size)
        self.color = color
        self.justification = justification
        
        self.set_text(text)
    
    def set_text(self, text:str):
        self.text = text
        self.img = self.font.render(self.text, False, self.color)

    def draw(self, surf:pg.Surface=None):
        if self.justification == JUSTIFY_LEFT:
            npos = self.pos
        elif self.justification == JUSTIFY_CENTER:
            npos = pg.Vector2(self.pos.x - self.img.get_width() / 2, self.pos.y)
        elif self.justification == JUSTIFY_RIGHT:
            npos = pg.Vector2(self.pos.x - self.img.get_width(), self.pos.y)

        if surf == None:
            self.game.screen.blit(self.img, (npos.x, npos.y))
        else:
            surf.blit(self.img, (npos.x, npos.y))


class Button(UIElement):
    def __init__(self, game, pos, hitbox, call=lambda:print('button call'), parentPanel=None) -> None:
        super().__init__(game, pos, hitbox, parentPanel)
        self.call = call

        self.game.eventees.append(self)

        self.hovering = False
        self.clicking = False
        self.disabled = False

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

    def draw(self, surf=None):
        surf = self.game.screen if surf == None else surf

        if self.disabled:
            pg.draw.rect(surf, (60, 60, 60), self.rect)
        elif self.clicking:
            pg.draw.rect(surf, (100, 100, 100), self.rect)
        elif self.hovering:
            pg.draw.rect(surf, (200, 200, 200), self.rect)
        else:
            pg.draw.rect(surf, (255, 255, 255), self.rect)


class BuyStructureButton(Button):
    def __init__(self, game, pos, hitbox, building_id:str, parentPanel=None):
        super().__init__(game, pos, hitbox, lambda:self.game.world_editor.place(building_id), parentPanel)
        self.building_id = building_id

        self.name_text = Text(game, "fonts/pixel-bit-advanced.ttf", 12, (0, 0, 0), pg.Vector2(rect.center[0], rect.y + 12), justification=JUSTIFY_CENTER)
        self.name_text.set_text(building_id)

        self.disabled = False
    
    def immuneUpdate(self):
        super().immuneUpdate()
        self.disabled = self.game.money < self.game.tile_library[self.building_id].price

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering and not self.disabled:
                self.game.money -= self.game.tile_library[self.building_id].price
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False
    
    def draw(self, surf=None):
        surf = self.game.screen if surf == None else surf

        super().draw(surf)
        # icon
        surf.blit(self.game.tile_library[self.building_id].sprite, (self.rect.x + TILE_WIDTH/2, self.rect.y + TILE_HEIGHT/2))
        # name
        self.name_text.draw(surf)


class Panel(GameObject):
    def __init__(self, game, hitbox:pg.Vector2):
        self.game = game

        self.surface = pg.Surface((width, height))
        self.elements = []

        self.pos = pg.Vector2((SCREEN_WIDTH - hitbox.x)/2, (SCREEN_HEIGHT - hitbox.y)/2)

    def immuneUpdate(self):
        for element in self.elements:
            element.immuneUpdate()

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self):
        for element in self.elements:
            element.draw()
        
        self.game.screen.blit(self.surface, self.pos)
        

class BuyMenu(Panel):
    def __init__(self, game, width, height):
        super().__init__(game, width, height)
        self.elements.append(BuyStructureButton(game, pg.Rect(0, 0, TILE_WIDTH, TILE_HEIGHT), "counter"))
        self.elements.append(BuyStructureButton(game, pg.Rect(TILE_WIDTH, 0, TILE_WIDTH, TILE_HEIGHT), "fridge"))

# i could probably use a decorator for scroll bars...
# ideally i make a self-refferential ui_element class