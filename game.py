import pygame as pg
import math, sys, random

from gameObject import *
from savesystem import *
from player import *
from world import *
from worldEditor import *
from settings import *
from userinterface import *
from items import Storage, Inventory
from worldrenderer import *

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
        self.gameState = PLAY_STATE

        self.lagCompensation = True

    def new_game(self):
        self.world = World(self)
        self.player = Player(self)
        self.world_renderer = WorldRenderer(self)

        # UI
        self.debug_button = Button(self, pg.Rect(SCREEN_HEIGHT/2, SCREEN_WIDTH/2, 80, 80))

        self.scoreText = Text(self, "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), pg.Vector2(MARGIN, MARGIN))
        self.scoreText.set_text(f"${MONEY}")

        self.timerText = Text(self, "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), pg.Vector2(SCREEN_WIDTH - MARGIN, MARGIN), justification=JUSTIFY_RIGHT)
        self.timerText.set_text(f"1:00")

    def load_game(self):
        self.new_game()
        load_game_state(self)

    def set_game_state(self, state):
        self.gameState = state
        self.isFreezed = self.gameState != PLAY_STATE
    
    def check_freeze(self):
        self.isFreezed = self.isPaused or (self.gameState != PLAY_STATE)

    def events(self):
        self.lagCompensation = True

        for event in pg.event.get():
            if event.type == pg.QUIT:
                save_game_state(self)
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.isPaused = not self.isPaused
            # elif event.type == pg.VIDEOEXPOSE:
            #     print("MOVIGN WINDOW BEEP BEEP")
            #     self.lagCompensation = False
            #     self.DT = 1/self.FPS

            for eventee in self.eventees:
                eventee.callEvent(event)

    def update(self):
        self.world.update()
        self.player.update()
        self.debug_button.update()
    
    def immuneUpdate(self):
        self.world.immuneUpdate()
        self.player.immuneUpdate()
        self.debug_button.immuneUpdate()

    def draw(self):
        self.screen.fill(BACKGROUND_COLOUR)
        self.world.draw()
        self.player.draw()
        self.world_renderer.draw()

        if self.player.show_storage:
            self.storage.draw(self.screen)

        self.scoreText.draw()
        self.timerText.draw()
        self.debug_button.draw()

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
