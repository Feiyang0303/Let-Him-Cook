import pygame as pg
import math, sys, random

from gameObject import *
from savesystem import *
from player import *
from world import *
from worldEditor import *
from settings import *
from userinterface import *
from items import *
from worldrenderer import *
from preferencescreen import *
from particle import *
from mainscreen import MainMenu


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("LET HIM COOK")
        self.FPS = 60
        self.DT = 1 / self.FPS
        self.clock = pg.time.Clock()

        self.eventees = []

        self.isFreezed = False
        self.isPaused = False
        self.state=MAIN_MENU_STATE
        # self.state = PLAY_STATE

        self.money = AERSOL

        self.lagCompensation = True
        self.mainscreen=MainMenu(self)

    def new_game(self):

        self.item_library = self.item_library = {
            "sugar": Item(self, "sugar", "new-sprites/items/sugar.png"),
            "butter": Item(self, "butter", "new-sprites/items/butter.png"),
            "flour": Item(self, "flour", "new-sprites/items/flour.png"),
            "cookie": Item(self, "cookie", "new-sprites/items/cookie.png", sellprice=50),
        }
        self.world = World(self)
        self.particles = []

        self.player = Player(self)
        self.player2 = Player(self, 1)

        self.world_renderer = WorldRenderer(self)
        self.world_editor = WorldEditor(self)
        self.tile_library = self.world.tile_library

        self.pause_screen = PreferenceScreen(self)

        # UI
        self.buyMenu = BuyMenu(self, pg.Vector2(12 * TILE_WIDTH, 10 * TILE_HEIGHT))
        self.storageMenu = StorageMenu(self, pg.Vector2(12 * TILE_WIDTH, 10 * TILE_HEIGHT))
        self.buyItemMenu = ItemBuyMenu(self, pg.Vector2(12 * TILE_WIDTH, 10 * TILE_HEIGHT))

        self.scoreText = Text(self, pg.Vector2(MARGIN, MARGIN), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255),
                              text=f"${AERSOL}")

        self.timerText = Text(self, pg.Vector2(SCREEN_WIDTH - MARGIN, MARGIN), "fonts/pixel-bit-advanced.ttf", 24,
                              (255, 255, 255), justification=JUSTIFY_RIGHT, text="1:00")

    def load_game(self):
        self.new_game()
        load_game_state(self)

    def set_game_state(self, state):
        print(state)
        self.state = state
        self.isFreezed = self.state != PLAY_STATE

    def check_freeze(self):
        self.isFreezed = self.isPaused or (self.state != PLAY_STATE)

    def events(self):
        self.lagCompensation = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_game_state(self)
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    if self.state != PLAY_STATE:
                        self.state = PLAY_STATE
                    else:
                        self.isPaused = not self.isPaused
                elif event.key == pg.K_i:
                    self.state = INVENTORY_STATE if self.state == PLAY_STATE else PLAY_STATE

            for eventee in self.eventees:
                eventee.callEvent(event)

    def update(self):
        if self.state == MAIN_MENU_STATE:
            self.mainscreen.update()
        else:
            self.world.update()
            for particle in self.particles: particle.update()
            self.player.update()
            self.player2.update()
            self.buyMenu.update()
            self.storageMenu.update()
            self.world_editor.update()

    def immuneUpdate(self):
        if self.state==MAIN_MENU_STATE:
            self.mainscreen.immuneUpdate()
        else:
            self.world.immuneUpdate()
            for particle in self.particles: particle.immuneUpdate()
            self.player.immuneUpdate()
            self.player2.immuneUpdate()
            self.buyMenu.immuneUpdate()
            self.buyItemMenu.immuneUpdate()
            self.storageMenu.immuneUpdate()
            self.world_editor.immuneUpdate()
            
            self.scoreText.set_text(f"${self.money}")

    def draw(self):
        if self.state==MAIN_MENU_STATE:
            self.mainscreen.draw()
        else:
            self.screen.fill(BACKGROUND_COLOUR)
            self.world.draw()
            for particle in self.particles: particle.draw()
            self.player.draw()
            self.player2.draw()
            self.world_renderer.draw()
            self.world_editor.draw()
            self.scoreText.draw()
            self.timerText.draw()

            # these menus should really be handling that themselves....
            # ...whatever.
            # k i fixed it
            self.buyMenu.draw()
            self.storageMenu.draw()
            self.buyItemMenu.draw()

            if self.isPaused:
                self.pause_screen.draw()

        pg.display.update()

    def run(self):
        while True:
            self.events()
            self.DT = min(self.clock.tick(self.FPS) / 1000, 1 / 12)

            self.check_freeze()
            if not self.isFreezed:
                self.update()
            self.immuneUpdate()
            self.draw()
