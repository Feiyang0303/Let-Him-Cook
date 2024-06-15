import random as rd
import pygame as pg

from settings import *
from tools import *

# I <3 Python Object Oriented Programming (POOP)

class DayManager:
    def __init__(self, game) -> None:
        self.game = game

        self.current_wave = None
        self.wave_buffer = []

        self.quota = 100
        self.quota_add = [0, 10, 10, 10, 20, 30, 20]

        self.day = 0

        self.new_day()
    
    def update(self):
        self.current_wave.update()
    
    def new_day(self):
        self.quota += self.quota_add[self.day]
        self.day += 1

        # self.wave_buffer.append(TransitionWave(self.game, rd.choice(["It\'s a new day!", "Good Morning!", "Opening Time!", "WE ARE OPEN", "Let's cook!", "Morning Rush!", "8:00 AM"])))
        self.wave_buffer.append(CookWave(self.game, 60))
        # self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Time for a break..."])))
        self.wave_buffer.append(BreakWave(self.game, 20))

        # self.wave_buffer.append(TransitionWave(self.game, rd.choice(["It's lunch time!", "12:00 PM", "C'est midi.", "It's afternoon."])))
        self.wave_buffer.append(CookWave(self.game, 60))
        # self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Time for a break..."])))
        self.wave_buffer.append(BreakWave(self.game, 20))

        # self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Dinna time!", "Allez! Cuisine!", "It's Dinner Time!", "6:00 PM", "C'est apres midi.", "Bonne soiree."])))
        self.wave_buffer.append(CookWave(self.game, 120))
        # self.wave_buffer.append(TransitionWave(self.game, rd.choice(["Yeesh, time for a break..."])))
        self.wave_buffer.append(BreakWave(self.game, 40))

        # self.wave_buffer.append(SummaryWave(self.game, "That's a wrap, folks.", "mimimi...", "'night!", "12:00 AM", "I could really go for a drink.", "You cooked, brother."))

        self.current_wave = self.wave_buffer[0]
        self.current_wave.start()
    
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

class Wave:
    def __init__(self, game):
        self.game = game

    def start(self): pass

    def update(self): pass

    def finish(self): self.game.day_manager.next_wave()

class TimerWave(Wave):
    def __init__(self, game, delay):
        self.game = game
        self.delay = delay
        self.timer = 0

    def update(self):
        self.timer += self.game.DT
        if self.timer > self.delay: self.finish()

        self.game.timerText.set_text(format_time(self.delay - self.timer))

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
    def __init__(self, game, text):
        self.game = game

    def update(self):
        pass

class SummaryWave(Wave):
    def __init__(self, game, text):
        self.game = game

    def update(self):
        pass
