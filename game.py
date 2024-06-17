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
from mainscreen import *
from waves import *


class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("LET HIM COOK")
        self.FPS = 60
        self.DT = 1 / self.FPS
        self.clock = pg.time.Clock()

        self.eventees = []

        self.is_frozen = False
        self.is_paused = False
        self.state = MAIN_MENU_STATE

        self.do_lag_compensation = True

        self.mainscreen = MainMenu(self)

    def new_game(self):
        self.eventees.clear()

        self.item_library = {
            "package": Package(self, "package", "new-sprites/items/milk.png"),
            "alfredo": Item(self, "alfredo", "new-sprites/items/alfredo.png"),
            "apple": Item(self, "apple", "new-sprites/items/apple.png"),
            "bread": Item(self, "bread", "new-sprites/items/bread.png"),
            "burger": Item(self, "burger", "new-sprites/items/Burger.png"),
            "butter": Item(self, "butter", "new-sprites/items/butter.png"),
            "cake_batter": Item(self, "cake_batter", "new-sprites/items/cake_batter.png"),
            "caramel": Item(self, "caramel", "new-sprites/items/caramel.png"),
            "cheese": Item(self, "cheese", "new-sprites/items/cheese.png"),
            "chili": Item(self, "chili", "new-sprites/items/Chili.png"),
            "chocolate": Item(self, "chocolate", "new-sprites/items/chocolate.png"),
            "chopped-apple": Item(self, "chopped-apple", "new-sprites/items/chopped_apple.png"),
            "chopped-chocolate": Item(self, "chopped-chocolate", "new-sprites/items/chopped_chocolate.png"),
            "cookie-batter": Item(self, "cookie-batter", "new-sprites/items/cookie_batter.png"),
            "cookie": Item(self, "cookie", "new-sprites/items/cookie.png", sellprice=50),
            "flour": Item(self, "flour", "new-sprites/items/flour.png"),
            "fries": Item(self, "fries", "new-sprites/items/Fries.png"),
            "hot-dog": Item(self, "hot-dog", "new-sprites/items/Hot Dog.png"),
            "ice-cream": Item(self, "ice_cream", "new-sprites/items/ice_cream.png"),
            "lettuce": Item(self, "lettuce", "new-sprites/items/Lettuce.png"),
            "meat": Item(self, "meat", "new-sprites/items/Meat.png"),
            "milk": Item(self, "milk", "new-sprites/items/milk.png"),
            "pasta": Item(self, "pasta", "new-sprites/items/Pasta.png"),
            "potato-slices": Item(self, "potato-slices", "new-sprites/items/Potato Slices.png"),
            "potato": Item(self, "potato", "new-sprites/items/Potato.png"),
            "poutine": Item(self, "poutine", "new-sprites/items/Poutine.png"),
            "rice": Item(self, "rice", "new-sprites/items/rice.png"),
            "salad": Item(self, "salad", "new-sprites/items/salad.png"),
            "spaghetti-meatballs": Item(self, "spaghetti-meatball", "new-sprites/items/spaghetti meatballs.png"),
            "sugar": Item(self, "sugar", "new-sprites/items/sugar.png"),
            "supreme-burger": Item(self, "supreme-burger", "new-sprites/items/Supreme Burger.png"),
            "tomato-slice": Item(self, "tomato-slice", "new-sprites/items/Tomato Slice.png"),
            "tomato": Item(self, "tomato", "new-sprites/items/Tomato.png"),
            "weiner": Item(self, "weiner", "new-sprites/items/Weiner.png")
        }
        self.counter_recipes = {
            "cookie-batter": ("sugar", "flour", "chocolate", "butter"),
            "burger":("bread","meat","lettuce"),
            "supreme-burger" :("bread", "meat","lettuce","cheese","chopped-tomato"),
            "poutine" : ("fries","meat","cheese"),
            "chili" : ("tomato","milk","meat","cheese"),
            "hot-dog" : ("weiner","bread"),
            "lettuce" :("lettuce"),
            "salad" : ("tomato", "lettuce","cheese"),
            "ice-cream" : ("milk","sugar","chocolate")
            
        }
        self.oven_recipes = {
            "cookie": ("cookie-batter",),
            "bread": ("flour", "sugar","milk","butter"),
            "fries" : ("chopped-potato"),
            "spaghetti-meatball" : ("chopped-tomato","pasta","meat"),
            "cake" : ("flour","milk","sugar","chocolate")
        }
        self.chopper_recipes = {
            "chopped-potato" :("potato"),
            "chopped-tomato" : ("tomato")
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
        self.buy_menu = BuyMenu(self, pg.Vector2(12 * TILE_WIDTH, 10 * TILE_HEIGHT))
        self.storage_menu = StorageMenu(self, pg.Vector2(12 * TILE_WIDTH, 10 * TILE_HEIGHT))
        self.buy_item_menu = ItemBuyMenu(self, pg.Vector2(12 * TILE_WIDTH, 10 * TILE_HEIGHT))

        self.money_text = Text(self, pg.Vector2(MARGIN, MARGIN), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), text=f"${STARTING_MONEY}")
        self.quota_text = Text(self, pg.Vector2(MARGIN, MARGIN * 3), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), text=f"$0/${100}")

        self.wave_text = Text(self, pg.Vector2(SCREEN_WIDTH - MARGIN, MARGIN), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_RIGHT, text="break")
        self.timer_text = Text(self, pg.Vector2(SCREEN_WIDTH - MARGIN, MARGIN * 3), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_RIGHT, text="1:00")
        
        self.money = STARTING_MONEY
        self.money_made_today = 0
        self.sold_items = []

        self.day_manager = DayManager(self)
        self.wave_state = COOK_WAVE

    def load_game(self):
        self.new_game()
        if not load_game_state(self):
            self.new_game()

    def set_game_state(self, state):
        print(state)
        self.state = state
        self.is_frozen = self.state != PLAY_STATE

    def check_freeze(self):
        self.is_frozen = self.is_paused or (self.state != PLAY_STATE)

    def events(self):
        self.do_lag_compensation = True

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
                        self.is_paused = not self.is_paused

            for eventee in self.eventees:
                eventee.call_event(event)

    def update(self):
        if self.state == MAIN_MENU_STATE:
            self.mainscreen.update()
        else:
            self.world.update()
            for particle in self.particles: particle.update()
            self.player.update()
            self.player2.update()
            self.buy_menu.update()
            self.storage_menu.update()
            self.world_editor.update()

    def immune_update(self):
        if self.state==MAIN_MENU_STATE:
            self.mainscreen.immune_update()
        else:
            self.world.immune_update()
            for particle in self.particles: particle.immune_update()
            self.player.immune_update()
            self.player2.immune_update()
            self.buy_menu.immune_update()
            self.buy_item_menu.immune_update()
            self.storage_menu.immune_update()
            self.world_editor.immune_update()
            self.day_manager.immune_update()
            
            self.money_text.set_text(f"${self.money}")
            self.wave_text.set_text("break time" if self.wave_state == BREAK_WAVE else "cookin time")

    def draw(self):
        if self.state==MAIN_MENU_STATE:
            self.mainscreen.draw()
        else:
            self.screen.fill(BACKGROUND_COLOUR)
            self.world.draw()
            self.player.draw()
            self.player2.draw()
            for particle in self.particles: particle.draw()
            self.world_renderer.draw()
            self.world_editor.draw()
            self.money_text.draw()
            self.quota_text.draw()
            self.timer_text.draw()
            self.wave_text.draw()
            self.day_manager.draw()

            # these menus should really be handling that themselves....
            # ...whatever.
            # k i fixed it
            self.buy_menu.draw()
            self.storage_menu.draw()
            self.buy_item_menu.draw()

            if self.is_paused:
                self.pause_screen.draw()

        pg.display.update()

    def run(self):
        while True:
            self.events()
            self.DT = min(self.clock.tick(self.FPS) / 1000, 1 / 12)

            self.check_freeze()
            if not self.is_frozen:
                self.update()
            self.immune_update()
            self.draw()
