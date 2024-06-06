import pygame as pg
from settings import *



class PreferenceScreen:
    
    def __init__(self, game) -> None:
        self.game = game
        self.faded_screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)).convert_alpha()
        self.faded_screen.fill((0, 0, 0))
        self.faded_screen.set_alpha(180) # 0 - 255
        
        self.sliders = [
            Slider((280,475) , (200,30), 0.5, 0, 100)
        ]

    def update(self):
        # make sliders
        pass

    
    def draw(self):
        mouse_pos = pg.mouse.get_pos()
        mouse = pg.mouse.get_pressed()
        self.game.screen.blit(self.faded_screen, (0, 0))

        # pg.draw.rect(self.game.screen, (0, 0, 0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), pg.SRCALPHA,32)
        
        # draw the background

        # draw pause text
        font = pg.font.Font('freesansbold.ttf', 32)
        text = font.render("Game Paused", True, (225,225,225))
        self.game.screen.blit(text,(180,60))
        # draw the sliders
        
        for slider in self.sliders:
            if slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
                slider.move_slider(mouse_pos)
                print(slider.get_value())
            slider.render(self.game)

class Slider:
    def __init__(self, pos: tuple, size: tuple, initial_val: float, min: int, max: int) -> None:
        self.pos = pos
        self.size = size
        self.slider_left_pos = self.pos[0] - (size[0]//2)
        self.slider_right_pos = self.pos[0] + (size[0]//2)
        self.slider_top_pos = self.pos[1] - (size[1]//2)

        self.min = min
        self.max = max
        self.initial_val = (self.slider_right_pos-self.slider_left_pos)*initial_val # <- percentage

        self.container_rect = pg.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pg.Rect(self.slider_left_pos + self.initial_val - 5, self.slider_top_pos, 10, self.size[1])
    
    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def render(self, game):
        pg.draw.rect(game.screen, "white", self.container_rect)
        pg.draw.rect(game.screen, "blue", self.button_rect)
    def get_value(self):
        val_range = self.slider_right_pos - self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val/val_range)*(self.max-self.min)+self.min