
import pygame as pg
from gameObject import *

# could add a ton of particles
# impact particles when placing and destroying buildings
# debris particles when chopping
# flame and smoke particles on cooking elements
# footstep trails...
# would add a whole lot of polish and movement to an unanimated game

class SellParticle(GameObject):
    def __init__(self, game, pos: pg.Vector2, font="fonts/pixel-bit-advanced.ttf", text="+10", size=16, color=(80, 255, 0)) -> None:
        sprite = pg.font.Font(font, size).render(text, False, color)

        super().__init__(game, pos, pg.Vector2(1, 1), sprite)
        self.z = 0
        self.velz = 8

    def update(self):
        self.z += self.velz * self.game.DT
        self.velz *= 0.92
        if self.velz <= 1 * self.game.DT:
            self.destroy()
    
    def destroy(self):
        if self in self.game.particles:
            self.game.particles.remove(self)
    
    def draw(self):
        self.game.world_renderer.draw_object(self, z=self.z)
    