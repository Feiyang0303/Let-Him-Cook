import random as rd
import pygame as pg

from settings import *
from tools import *
from userinterface import *

# I <3 Python Object Oriented Programming (POOP)

class DayManager:
    def __init__(self, game) -> None:
        self.game = game

        self.current_wave = None
        self.wave_buffer = []

        self.start_money = 0
        self.quota = 100
        self.quota_add = [0, 10, 10, 10, 20, 30, 20]

        self.day = 0

        self.new_day()
    
    def immune_update(self):
        if not self.game.is_paused:
            self.current_wave.update()

            self.game.quota_text.set_text(f"${self.game.money_made_today}/${self.quota}")
            if self.game.money_made_today >= self.quota:
                self.game.quota_text.set_color((0, 255, 0))
            else:
                self.game.quota_text.set_color((255, 0, 0))
    
    def draw(self):
        self.current_wave.draw()
    
    def new_day(self):
        self.game.money_made_today = 0
        self.quota += self.quota_add[self.day]
        self.day += 1

        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["It\'s a new day!", "Good Morning!", "6:00 AM"]), (85, 129, 130)))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["It's time to setup..."]), (109, 80, 90)))
        self.wave_buffer.append(BreakWave(self.game, 30))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Opening Time!", "WE ARE OPEN", "Let's cook!", "Morning Rush!", "8:00 AM"]), (109, 80, 90)))
        self.wave_buffer.append(CookWave(self.game, 60))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Time for a break..."]), (109, 80, 90)))
        self.wave_buffer.append(BreakWave(self.game, 20))

        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["It's lunch time!", "12:00 PM", "C'est midi.", "It's afternoon."]), (160, 133, 90)))
        self.wave_buffer.append(CookWave(self.game, 60))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Time for a break..."]), (109, 80, 90)))
        self.wave_buffer.append(BreakWave(self.game, 20))

        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Dinna time!", "Allez! Cuisine!", "It's Dinner Time!", "6:00 PM", "C'est apres midi.", "Bonne soiree."]), (160, 90, 90)))
        self.wave_buffer.append(CookWave(self.game, 120))

        self.wave_buffer.append(SummaryWave(self.game, rd.choice(["That's a wrap.", "mimimi...", "'night!", "12:00 AM", "You cooked."]), (38, 36, 31)))

        self.current_wave = self.wave_buffer[0]
        self.current_wave.start()
    
    def end_day(self):
        self.game.money += self.game.money_made_today - self.quota
        self.new_day()
    
    def new_friday(self):
        self.quota = 1000
        self.day += 1

        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["IT'S FRIDAY."])))
        self.wave_buffer.append(CookWave(self.game, 80))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Time for a short break..."])))
        self.wave_buffer.append(BreakWave(self.game, 15))

        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["FRIDAY AFTERNOON."])))
        self.wave_buffer.append(CookWave(self.game, 80))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Time for a short break..."])))
        self.wave_buffer.append(BreakWave(self.game, 15))

        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["FRIDAY NIGHT. GOOD LUCK."])))
        self.wave_buffer.append(CookWave(self.game, 180))
        self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Yeesh, time for a break..."])))
        self.wave_buffer.append(BreakWave(self.game, 40))

        self.wave_buffer.append(SummaryWave(self.game, "FRIDAY FINISHED."))

        self.current_wave = self.wave_buffer(0)
        self.current_wave.start()

    def next_wave(self):
        self.wave_buffer.pop(0)
        self.current_wave = self.wave_buffer[0]
        self.current_wave.start()

class Wave(GameObject):
    def __init__(self, game):
        self.game = game

    def start(self): pass

    def finish(self): self.game.day_manager.next_wave()

class TimerWave(Wave):
    def __init__(self, game, delay):
        self.game = game
        self.delay = delay
        self.timer = 0

    def update(self):
        self.timer += self.game.DT
        if self.timer > self.delay: self.finish()

        self.game.timer_text.set_text(format_time(self.delay - self.timer))

class CookWave(TimerWave):
    def __init__(self, game, delay):
        super().__init__(game, delay)
    
    def start(self):
        self.game.wave_state = COOK_WAVE

class BreakWave(TimerWave):
    def __init__(self, game, delay):
        super().__init__(game, delay)
    
    def start(self):
        self.game.wave_state = BREAK_WAVE

class TransitionWave(Wave):
    def __init__(self, game, text, color):
        self.game = game
        self.text = text
        self.color = color

    def start(self):
        self.panel = Panel(self.game, pg.Vector2((WORLD_WIDTH) * TILE_WIDTH, (WORLD_HEIGHT + WORLD_WALL_HEIGHT) * TILE_HEIGHT), self.color)
        self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2 + MARGIN, 200), "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), justification=JUSTIFY_CENTER, text=self.text))
        self.panel.elements.append(Button(self.game, pg.Vector2(0, 300), pg.Vector2(WORLD_WIDTH * TILE_WIDTH, 50), lambda:self.finish(), self.panel))
        self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2, 450), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_CENTER, text="okay"))

    def finish(self):
        self.panel.disable()
        super().finish()

    def update(self):
        self.panel.update()

    def immune_update(self):
        self.panel.immune_update()
    
    def draw(self):
        self.panel.draw()

class SummaryWave(Wave):
    def __init__(self, game, text, color):
        self.game = game
        self.text = text
        self.color = color

    def start(self):
        self.panel = Panel(self.game, pg.Vector2((WORLD_WIDTH) * TILE_WIDTH, (WORLD_HEIGHT + WORLD_WALL_HEIGHT) * TILE_HEIGHT), self.color)
        self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2 + MARGIN, 200), "fonts/pixel-bit-advanced.ttf", 32, (255, 255, 255), justification=JUSTIFY_CENTER, text=self.text))
        
        self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2 + MARGIN, 300), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_CENTER, 
                                        text=f"${self.game.money_made_today}/${self.game.day_manager.quota}"))
        
        if self.game.money_made_today-self.game.day_manager.quota > 0:
            self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2 + MARGIN, 340), "fonts/pixel-bit-advanced.ttf", 24, (0, 255, 0), justification=JUSTIFY_CENTER, 
                                            text=f"+${self.game.money_made_today-self.game.day_manager.quota}"))
            
            self.panel.elements.append(Button(self.game, pg.Vector2(0, 300), pg.Vector2(WORLD_WIDTH * TILE_WIDTH, 50), lambda:self.finish(), self.panel))
            self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2, 450), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_CENTER, text="okay"))

        else:
            self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2 + MARGIN, 340), "fonts/pixel-bit-advanced.ttf", 24, (255, 0, 0), justification=JUSTIFY_CENTER, 
                                            text=f"You failed to make quota."))
            
            self.panel.elements.append(Button(self.game, pg.Vector2(0, 300), pg.Vector2(WORLD_WIDTH * TILE_WIDTH, 50), lambda:self.game.new_game(), self.panel))
            self.panel.elements.append(Text(self.game, pg.Vector2(WORLD_WIDTH * TILE_WIDTH / 2, 450), "fonts/pixel-bit-advanced.ttf", 24, (255, 255, 255), justification=JUSTIFY_CENTER, text="new game"))
        
    def finish(self):
        self.panel.disable()
        self.game.day_manager.end_day()
        super().finish()

    def update(self):
        self.panel.update()

    def immune_update(self):
        self.panel.immune_update()
    
    def draw(self):
        self.panel.draw()
