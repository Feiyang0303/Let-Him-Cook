import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# class Button():
#     def __init__(self, x, y, image, scale):
#         width = image.get_width()
#         height = image.get_height()
#         self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
#         self.rect = self.image.get_rect()
#         self.rect.topleft = (x, y)
#         self.clicked = False

#     def draw(self, surface):
#         action = False
#         pygame.draw.rect(surface, (0, 0, 0),
#                          (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
#         bk = pygame.draw.rect(surface, (255, 255, 255),
#                               (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()), 3)

#         pos = pygame.mouse.get_pos()

#         if bk.collidepoint(pos):
#             if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
#                 self.clicked = True
#                 action = True
#                 pygame.draw.rect(surface, (0, 0, 255),
#                                  (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
#         if pygame.mouse.get_pressed()[0] == 0:
#             self.clicked = False

#         surface.blit(self.image, (self.rect.x, self.rect.y))

#         return action


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

game_paused = False
menu_state = "main"

# font = pygame.font

TEXT_COL = (255, 255, 255)

# resume_img = font.render
# options_img = font.render
# quit_img = font.render
# video_img = font.render
# audio_img = font.render
# keys_img = font.render
# back_img = font.render

while True:
    pass
