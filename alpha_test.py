import pygame, sys

pygame.init()

window = pygame.display.set_mode((200, 200))
image = image2 = pygame.image.load('sprites/sugar.png')

image = image.convert()
rect = image.get_rect()

image2 = image2.convert_alpha()
rect2 = image2.get_rect()

rect2.left = rect.width + 1

i = 0
while True:
  for event in pygame.event.get():
    if event.type == 12:
      pygame.quit()
      sys.exit()

  image2.set_alpha(i)

  window.fill((255, 255, 255))
  window.blit(image2, (0, 0))

  if i == 255:
    i = 0
  else:
    i += 1

  pygame.display.update()
  pygame.time.Clock().tick(60)