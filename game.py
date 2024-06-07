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

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

        self.FPS = 60
        self.DT = 1/self.FPS
        self.clock = pg.time.Clock()
        self.storage = Storage()
        self.inventory= Inventory(Storage())

        self.eventees = []

        self.isFreezed = False
        self.isPaused = False
        self.state = PLAY_STATE

        self.money = AERSOL

        self.lagCompensation = True

    def new_game(self):
        self.world = World(self)
        self.player = Player(self)
        self.world_renderer = WorldRenderer(self)
        self.world_editor = WorldEditor(self)
        self.tile_library = self.world.tile_library

        self.pause_screen = PreferenceScreen(self)

        # UI
        self.buyMenu = BuyMenu(self, pg.Vector2(12*TILE_WIDTH, 10*TILE_HEIGHT))
        self.fridgeMenu = FridgeMenu(self, pg.Vector2(400, 300))

        self.scoreText = Text(self, pg.Vector2(MARGIN, MARGIN), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), text=f"${AERSOL}")

        self.timerText = Text(self, pg.Vector2(SCREEN_WIDTH - MARGIN, MARGIN), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_RIGHT, text="1:00")

    def load_game(self):
        self.new_game()
        load_game_state(self)

    def set_game_state(self, state):
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
        self.world.update()
        self.player.update()
        self.buyMenu.update()
        self.fridgeMenu.update()
        self.world_editor.update()
        self.scoreText.set_text(f"${self.money}")
    
    def immuneUpdate(self):
        self.world.immuneUpdate()
        self.player.immuneUpdate()
        self.buyMenu.immuneUpdate()
        self.world_editor.immuneUpdate()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOUR)
        self.world.draw()
        self.player.draw()
        self.world_renderer.draw()
        self.world_editor.draw()
        self.scoreText.draw()
        self.timerText.draw()


        # these menus should really be handling that themselves....
        if self.state == INVENTORY_STATE:
            self.storage.draw(self.screen)
        if self.isPaused:
            self.pause_screen.draw()
        if self.state == BUY_STATE:
            self.buyMenu.draw()
        elif self.state == FRIDGE_STATE:
            self.fridgeMenu.draw()

        pg.display.update()

    def run(self):
        while True:
            self.events()
            self.DT = min(self.clock.tick(self.FPS) / 1000, 1/12)
            
            self.check_freeze()
            if not self.isFreezed:
                self.update()
            self.immuneUpdate()
            self.draw()
