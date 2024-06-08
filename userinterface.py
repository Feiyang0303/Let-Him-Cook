import pygame as pg

from gameObject import *
from tools import *
from items import *

JUSTIFY_LEFT = 0
JUSTIFY_CENTER = 1
JUSTIFY_RIGHT = 2

class UIElement(GameObject):
    def __init__(self, game, pos: pg.Vector2, hitbox=pg.Vector2(1, 1), parentPanel=None) -> None:
        self.parentPanel = parentPanel

        if not parentPanel == None:
            super().__init__(game, parentPanel.pos + pos, hitbox)
        else:
            super().__init__(game, pos, hitbox)


class Text(UIElement):
    def __init__(self, game, pos:pg.Vector2, fontpath, size, color, justification=JUSTIFY_LEFT, text="default", parentPanel=None):
        super().__init__(game, pos, parentPanel=parentPanel)
        
        self.font = pg.font.Font(fontpath, size)
        self.color = color
        self.justification = justification
        
        self.set_text(text)
    
    def set_text(self, text:str):
        self.text = text
        self.img = self.font.render(self.text, False, self.color)

    def draw(self):
        if self.justification == JUSTIFY_LEFT:
            npos = self.pos
        elif self.justification == JUSTIFY_CENTER:
            npos = pg.Vector2(self.pos.x - self.img.get_width() / 2, self.pos.y)
        elif self.justification == JUSTIFY_RIGHT:
            npos = pg.Vector2(self.pos.x - self.img.get_width(), self.pos.y)

        self.game.screen.blit(self.img, (npos.x, npos.y))

class Image(UIElement):
    def __init__(self, game, pos:pg.Vector2, imagepath:str, parentPanel=None):
        super().__init__(game, pos, parentPanel=parentPanel)
        
        self.image = pg.image.load(imagepath)

    def draw(self):
        self.game.screen.blit(self.img, (self.pos.x, self.pos.y))

class Button(UIElement):
    def __init__(self, game, pos, hitbox, call=lambda:print('button call'), parentPanel=None) -> None:
        super().__init__(game, pos, hitbox, parentPanel)
        self.call = call

        self.game.eventees.append(self)

        self.hovering = False
        self.clicking = False
        self.disabled = False

    def immuneUpdate(self):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        self.hovering = is_point_in_hitbox(mouse_pos, self.pos, self.hitbox)

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering:
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False

    def draw(self):
        if self.disabled:
            pg.draw.rect(self.game.screen, (60, 60, 60), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
        elif self.clicking:
            pg.draw.rect(self.game.screen, (100, 100, 100), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
        elif self.hovering:
            pg.draw.rect(self.game.screen, (200, 200, 200), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
        else:
            pg.draw.rect(self.game.screen, (89, 77, 81), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))


class BuyStructureButton(Button):
    def __init__(self, game, pos, hitbox, building_id:str, parentPanel=None):
        super().__init__(game, pos, hitbox, lambda:self.game.world_editor.place(building_id), parentPanel)
        self.building_id = building_id

        self.name_text = Text(game, pg.Vector2(pos.x + hitbox.x / 2, pos.y), "fonts/pixel-bit-advanced.ttf", 16, (130, 149, 130), justification=JUSTIFY_CENTER, parentPanel=parentPanel)
        self.name_text.set_text(str(self.game.tile_library[self.building_id].price))


        building_sprite = self.game.tile_library[self.building_id].sprite
        scale = min(TILE_WIDTH / building_sprite.get_width(), TILE_HEIGHT / building_sprite.get_height())
        self.sprite = pg.transform.scale_by(self.game.tile_library[self.building_id].sprite, scale)

        self.disabled = False
    
    def immuneUpdate(self):
        super().immuneUpdate()
        self.disabled = self.game.money < self.game.tile_library[self.building_id].price

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering and not self.disabled and self.game.state == BUY_STATE:
                self.game.money -= self.game.tile_library[self.building_id].price
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False
    
    def draw(self):
        super().draw()

        self.game.screen.blit(self.sprite, (self.pos.x + (self.hitbox.x - self.sprite.get_width()) / 2, self.pos.y + (self.hitbox.y - self.sprite.get_height()) / 2 + 8))
        self.name_text.draw()


class Panel(GameObject):
    def __init__(self, game, hitbox:pg.Vector2):
        self.game = game

        self.hitbox = hitbox

        self.elements = []
        self.pos = pg.Vector2((SCREEN_WIDTH - hitbox.x)/2, (SCREEN_HEIGHT - hitbox.y)/2)

    def immuneUpdate(self):
        if self.game.state == BUY_STATE:
            for element in self.elements:
                element.immuneUpdate()

    def update(self):
        if self.game.state == BUY_STATE:
            for element in self.elements:
                element.update()

    def draw(self):
        pg.draw.rect(self.game.screen, (57, 59, 60), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
        for element in self.elements:
            element.draw()
        

class BuyMenu(Panel):

    BUTTON_WIDTH = 32 * PPU
    MARGIN = 4 * PPU

    def __init__(self, game, hitbox):
        super().__init__(game, hitbox)
        buildings = ["counter", "fridge", "chopper", "oven"]

        for i, building in enumerate(buildings):
            x = TILE_WIDTH/2 + (BuyMenu.BUTTON_WIDTH + BuyMenu.MARGIN) * i
            y = TILE_WIDTH/2 + 0
            self.elements.append(BuyStructureButton(game, pg.Vector2(x, y), pg.Vector2(BuyMenu.BUTTON_WIDTH, BuyMenu.BUTTON_WIDTH), building, self))

# i could probably use a decorator for scroll bars...
# ideally i make a self-refferential ui_element class

# class FridgeOpenButton(Button):
#     def __init__(self, game, pos, hitbox, parentPanel=None):
#         super().__init__(game, pos, hitbox,self.toggle_fridge_menu, parentPanel)
#         self.sprite = pg.image.load("sprites/Fridge.png")
#         scale = min(TILE_WIDTH / building_sprite.get_width(), TILE_HEIGHT / building_sprite.get_height())
#         self.sprite = pg.transform.scale(self.sprite,
#                                          (int(self.sprite.get_width() * scale), int(self.sprite.get_height() * scale)))
#         self.disabled = False


#     def toggle_fridge_menu(self):
#         if self.game.state!=FRIDGE_STATE:
#             self.game.state=FRIDGE_STATE
#         else:
#             self.game.state=PLAY_STATE

#     def draw(self):
#         super().draw()
#         self.game.screen.blit(self.sprite, (self.pos.x + (self.hitbox.x - self.sprite.get_width()) / 2,

#                                             self.pos.y + (self.hitbox.y - self.sprite.get_height()) / 2))
# class FridgeItemButton(Button):
#     def __init__(self, game, pos, hitbox, item, parentPanel=None):
#         super().__init__(game, pos, hitbox, lambda: self.game.player.inventory.remove_item(item), parentPanel)
#         self.item=item
#         self.sprite = pg.image.load("sprites/Cookie.png")
#         scale = min(hitbox.x / self.sprite.get_width(), hitbox.y / self.sprite.get_height())
#         self.sprite = pg.transform.scale(self.sprite,
#                                          (int(self.sprite.get_width() * scale), int(self.sprite.get_height() * scale)))
#     def draw(self):
#         super().draw()
#         self.game.screen.blit(self.sprite, (self.pos.x + (self.hitbox.x - self.sprite.get_width()) / 2,
#                                             self.pos.y + (self.hitbox.y - self.sprite.get_height()) / 2))

class StorageMenu(Panel):
    def __init__(self, game, hitbox):
        super().__init__(game, hitbox)
        self.storage = None
    
    def set(self, storage:Storage):
        self.elements.clear()
        self.storage = storage

        for i, items in enumerate(self.storage.items):
            self.elements.append(Image(self.game, pg.Vector2(TILE_WIDTH * i, 0), ))


    # def update(self):
    #     self.elements.clear()
    #     for i, item in enumerate(self.game.player.inventory.items):
    #         x = TILE_WIDTH / 2 + (FridgeMenu.BUTTON_WIDTH + FridgeMenu.MARGIN) * i
            # y = TILE_WIDTH / 2 + 0
            # self.elements.append(FridgeItemButton(self.game, pg.Vector2(x, y), pg.Vector2(FridgeMenu.BUTTON_WIDTH, FridgeMenu.BUTTON_WIDTH),
            #                        item, self))

    # def draw(self, world_renderer):
    #     super().draw()
    #     for element in self.elements:
    #         element.draw()
    #     world_renderer.draw_fridge_menu(self)

