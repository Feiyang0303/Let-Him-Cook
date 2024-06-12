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
    def __init__(self, game, pos: pg.Vector2, fontpath, size, color, justification=JUSTIFY_LEFT, text="default",
                 parentPanel=None):
        super().__init__(game, pos, parentPanel=parentPanel)

        self.font = pg.font.Font(fontpath, size)
        self.color = color
        self.justification = justification

        self.set_text(text)

    def set_text(self, text: str):
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
    def __init__(self, game, pos: pg.Vector2, imagepath: str, parentPanel=None):
        super().__init__(game, pos, parentPanel=parentPanel)

        self.image = pg.image.load(imagepath)

    def draw(self):
        self.game.screen.blit(self.img, (self.pos.x, self.pos.y))


class Button(UIElement):
    def __init__(self, game, pos, hitbox, call=lambda: print('button call'), parentPanel=None) -> None:
        super().__init__(game, pos, hitbox, parentPanel)
        self.call = call

        self.game.eventees.append(self)

        self.hovering = False
        self.clicking = False
        self.disabled = False

    def immuneUpdate(self):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        self.hovering = is_point_in_hitbox(mouse_pos, self.pos, self.hitbox)
        self.disabled == self.parentPanel == None or self.game.state != self.parentPanel.menu_state
    
    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering:
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False

    def disable(self):
        self.game.eventees.remove(self)

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
    def __init__(self, game, pos, hitbox, building_id: str, parentPanel=None):
        super().__init__(game, pos, hitbox, lambda: self.game.world_editor.place(building_id), parentPanel)
        self.building_id = building_id

        self.name_text = Text(game, pg.Vector2(pos.x + hitbox.x / 2, pos.y), "fonts/pixel-bit-advanced.ttf", 16,
                              (130, 149, 130), justification=JUSTIFY_CENTER, parentPanel=parentPanel)
        self.name_text.set_text(str(self.game.tile_library[self.building_id].price))

        building_sprite = self.game.tile_library[self.building_id].sprite
        scale = min(TILE_WIDTH / building_sprite.get_width(), TILE_HEIGHT / building_sprite.get_height())
        self.sprite = pg.transform.scale_by(self.game.tile_library[self.building_id].sprite, scale)

    def immuneUpdate(self):
        super().immuneUpdate()
        self.disabled = self.disabled or self.game.money < self.game.tile_library[self.building_id].price

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering and not self.disabled:
                self.game.money -= self.game.tile_library[self.building_id].price
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False

    def draw(self):
        super().draw()

        self.game.screen.blit(self.sprite, (self.pos.x + (self.hitbox.x - self.sprite.get_width()) / 2,
                                            self.pos.y + (self.hitbox.y - self.sprite.get_height()) / 2 + 8))
        self.name_text.draw()

class BuyItemButton(Button):
    def __init__(self, game, pos, hitbox, item_id: str, parentPanel=None):
        super().__init__(game, pos, hitbox, lambda: self.game.player.inventory.add_item(item_id), parentPanel)
        self.item_id = item_id

        self.name_text = Text(game, pg.Vector2(pos.x + hitbox.x / 2, pos.y), "fonts/pixel-bit-advanced.ttf", 16,
                              (130, 149, 130), justification=JUSTIFY_CENTER, parentPanel=parentPanel)
        self.name_text.set_text(str(self.game.item_library[self.item_id].buyprice))

        sprite = self.game.item_library[self.item_id].sprite
        scale = min(TILE_WIDTH / sprite.get_width(), TILE_HEIGHT / sprite.get_height())
        self.sprite = pg.transform.scale_by(self.game.item_library[self.item_id].sprite, scale)

    def immuneUpdate(self):
        super().immuneUpdate()
        self.disabled = self.disabled or self.game.money < self.game.item_library[self.item_id].buyprice or self.game.player.inventory.isFull()
        # law of demeter? snake_case?

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering and not self.disabled and self.game.state == self.parentPanel.menu_state:
                self.game.money -= self.game.item_library[self.item_id].buyprice
                self.clicking = True
                self.call()
        elif event.type == pg.MOUSEBUTTONUP:
            self.clicking = False

    def draw(self):
        super().draw()

        self.game.screen.blit(self.sprite, (self.pos.x + (self.hitbox.x - self.sprite.get_width()) / 2,
                                            self.pos.y + (self.hitbox.y - self.sprite.get_height()) / 2 + 8))
        self.name_text.draw()

class StorageSlot(Button):
    def __init__(self, game, pos, hitbox, item, parentPanel=None):
        super().__init__(game, pos, hitbox, parentPanel)
        self.item=item
        self.name_text = Text(game, pg.Vector2(pos.x + hitbox.x / 2, pos.y), "fonts/pixel-bit-advanced.ttf", 16,
                              (130, 149, 130), justification=JUSTIFY_CENTER, parentPanel=parentPanel)
        self.name_text.set_text(self.item.name)
        scale = min(TILE_WIDTH / self.item.sprite.get_width(), TILE_HEIGHT / self.item.sprite.get_height())
        self.sprite = pg.transform.scale_by( self.item.sprite, (int(self.item.sprite.get_width() * scale), int(self.item.sprite.get_height() * scale)))

    def immuneUpdate(self):
        mouse_pos = pg.Vector2(pg.mouse.get_pos())
        self.hovering = is_point_in_hitbox(mouse_pos, self.pos, self.hitbox)

    def callEvent(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.hovering and not self.disabled and self.game.state == FRIDGE_STATE:
                self.clicking = True
                self.call()
            elif event.type == pg.MOUSEBUTTONUP:
                self.clicking = False
    def draw(self):
        super().draw()

        self.game.screen.blit(self.sprite, (self.pos.x + (self.hitbox.x - self.sprite.get_width()) / 2, self.pos.y + (self.hitbox.y - self.sprite.get_height()) / 2 + 8))
        self.name_text.draw()

    # def place_item(self):
    #     if self.game.player.inventory.items:
    #         self.item = self.game.player.inventory.items.pop(0)

    #def take_item(self):
    # if self.item:
    #     self.game.player.inventory.add(self.item)
    #     self.item = None
    #     self.name_text.set_text("Empty")



class Panel(GameObject):
    def __init__(self, game, hitbox: pg.Vector2):
        self.game = game

        self.hitbox = hitbox

        self.elements = []
        self.pos = pg.Vector2((SCREEN_WIDTH - hitbox.x) / 2, (SCREEN_HEIGHT - hitbox.y) / 2)

        self.menu_state = None

    def immuneUpdate(self):
        if self.game.state == self.menu_state:
            for element in self.elements:
                element.immuneUpdate()

    def update(self):
        if self.game.state == self.menu_state:
            for element in self.elements:
                element.update()

    def draw(self):
        if self.game.state == self.menu_state:
            pg.draw.rect(self.game.screen, (57, 59, 60), (self.pos.x, self.pos.y, self.hitbox.x, self.hitbox.y))
            for element in self.elements:
                element.draw()


class BuyMenu(Panel):
    BUTTON_WIDTH = 32 * PPU
    MARGIN = 4 * PPU

    def __init__(self, game, hitbox):
        super().__init__(game, hitbox)

        for i, building in enumerate(BUY_BUILDINGS):
            x = TILE_WIDTH / 2 + (BuyMenu.BUTTON_WIDTH + BuyMenu.MARGIN) * (i % 5)
            y = TILE_WIDTH / 2 + (BuyMenu.BUTTON_WIDTH + BuyMenu.MARGIN) * int(i/5)
            self.elements.append(
                BuyStructureButton(game, pg.Vector2(x, y), pg.Vector2(BuyMenu.BUTTON_WIDTH, BuyMenu.BUTTON_WIDTH),
                                   building, self))
            
        self.menu_state = BUY_STATE

class ItemBuyMenu(Panel):
    BUTTON_WIDTH = 32 * PPU
    MARGIN = 4 * PPU

    def __init__(self, game, hitbox):
        super().__init__(game, hitbox)

        for i, itemid in enumerate(BUY_ITEMS):
            x = TILE_WIDTH / 2 + (BuyMenu.BUTTON_WIDTH + BuyMenu.MARGIN) * (i % 5)
            y = TILE_WIDTH / 2 + (BuyMenu.BUTTON_WIDTH + BuyMenu.MARGIN) * int(i/5)
            self.elements.append(
                BuyItemButton(game, pg.Vector2(x, y), pg.Vector2(BuyMenu.BUTTON_WIDTH, BuyMenu.BUTTON_WIDTH),
                                   itemid, self))
        
        self.menu_state = BUY_ITEM_STATE

# i could probably use a decorator for scroll bars...
# ideally i make a self-refferential ui_element class

class StorageMenu(Panel):
    BUTTON_WIDTH = 25 * PPU
    MARGIN = 4 * PPU

    def __init__(self, game, hitbox):
        super().__init__(game, hitbox)
        self.storage = None

    def set(self, storage: Storage):
        self.elements.clear()
        self.storage = storage
        for i, item in enumerate(self.storage.items):
            x =(StorageMenu.BUTTON_WIDTH +StorageMenu.MARGIN) * i
            y =  0
            self.elements.append(StorageSlot(self.game, pg.Vector2(x, y),pg.Vector2(StorageMenu.BUTTON_WIDTH, StorageMenu.BUTTON_WIDTH), item, self))
        print(f"{self.item} is added to the fridge storage")

        self.menu_state = INVENTORY_STATE

    def draw(self):
        super().draw()
        for element in self.elements:
            element.draw()


