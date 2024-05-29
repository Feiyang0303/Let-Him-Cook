import pygame, math

# PYGAME

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Auto Tiling')

# GAME CORE

level_width = 16
level_height = 16

block_width = 50
block_height = 50

game_over = False

# BOARD

current_tile = 1
tile_images = ()
tiles = []
# 0 = empty, 1 = dirt, etc.
tiles.clear()
for h in range(level_height):
   tiles.append([])
   for w in range(level_width):
       tiles[h].append(0)

tile_ori = []
# 0-NW, 1-N, 2-NE
# 3-CW, 4-C, 5-CE
# 6-SW, 7-S, 8-SE
for h in range(level_height):
   tile_ori.append([])
   for w in range(level_width):
       tile_ori[h].append(0)

# INPUT

edit_mode = True

keys = [False, False, False, False, False]
mouse_down = False

player_width = 40  # 1 * block_width
player_height = 80  # 2 * block_height

collectibles = []

tile_x = 0
tile_y = 0

# PLAYER

spawn_x = 2 * block_width
spawn_y = level_height * block_height - 6 * block_height

player_x = spawn_x
player_y = spawn_y

vel_x = 0
acc_x = 0
kinetic_friction = 0.2
vel_y = 0
acc_y = 0
grav = 0.5

run_power = 3

jump_power = 15
jump_timer = 0  # delay until jump
jumped = False  # no double jumping
jump_leeway = 0  # let player jump if they press key right before hitting ground

bouncy_power = 20
bounce_delay = 0  # delay until bounce
bounce_timer = -1  # how long until player can bounce again

in_water = False

# EXTRA

coins = 0

tile_colors = (
   (169, 234, 243), (105, 189, 147), (245, 208, 73), (245, 124, 119), (169, 189, 196), (203, 181, 244),
   (224, 183, 167), (144, 215, 245))

# (77,67,48)

# CAMERA

scroll_x = -player_y + (SCREEN_HEIGHT / 2) - player_height / 2
scroll_y = player_x - (SCREEN_WIDTH / 2) + player_width / 2

min_xscroll = 0
max_xscroll = level_width * block_width - SCREEN_WIDTH
scroll_up = 2 * block_height
max_yscroll = -(level_height * block_height - SCREEN_HEIGHT) - scroll_up  # screen_height / 2 - scroll_up

# pygame.display.set_icon(pygame.image.load('E:\The Quest For Cake\coin_icon.png'))


class Collectible:

   def __init__(self, x, y, width=30, height=30):
       self.x, self.y, self.width, self.height = x, y, width, height
       self.collected = False

   def draw(self, color):
       pygame.draw.rect(screen, color, (int(self.x * block_width - scroll_x + (block_width - self.width) / 2),
                                        int(self.y * block_height + scroll_y + (block_height - self.height) / 2),
                                        self.width, self.height))


# def update_ori(tile_x, tile_y):
#    for y, x in []:
#        if (tile_x + x >= 0 and tile_x + x < level_width and tile_y + y >= 0 and tile_y + y < level_height):
#            tile_ori[tile_y + y][tile_x + x] = y * 3 + x


def is_rects_collis(rect1, rect2):
   return not (rect1[1] >= rect2[1] + rect2[3] or rect1[1] + rect1[3] <= rect2[1] or
               rect1[0] >= rect2[0] + rect2[2] or rect1[0] + rect1[2] <= rect2[0])


def is_rect_tri_collis(rect, tri):
   pass


def reset_level():
   global player_x, player_y, vel_x, vel_y, acc_x, acc_y, jump_timer, scroll_x, scroll_y, edit_mode, game_over, collectibles
   player_x = spawn_x
   player_y = spawn_y
   vel_x = acc_x = vel_y = acc_x = jump_timer = 0

   scroll_y = -spawn_y + (SCREEN_HEIGHT / 2) - player_height / 2
   scroll_x = spawn_x - (SCREEN_WIDTH / 2) + player_width / 2

   for coin in collectibles: coin.collected = False

   edit_mode = False
   game_over = False


def extend_level_width(blocks, left=False):
   global level_width, max_xscroll, spawn_x, player_x, scroll_x, tiles, collectibles
   level_width += blocks
   max_xscroll = level_width * block_width - SCREEN_WIDTH
   if left:
       if blocks > 0:
           for row in tiles:
               for i in range(blocks): row.insert(0, 0)
       elif blocks < 0:
           for row in range(level_height):
               tiles[row] = tiles[row][-blocks:]
       for coin in collectibles:
           coin.x += blocks
       spawn_x += blocks * block_width
       player_x += blocks * block_width
       scroll_x += blocks * block_width
   else:
       if blocks > 0:
           for row in tiles:
               for i in range(blocks): row.append(0)
       elif blocks < 0:
           for row in tiles:
               row = row[:level_width + blocks]


def extend_level_height(blocks, up=False):
   global level_height, max_yscroll, spawn_y, player_y, scroll_y, tiles, collectibles

   level_height += blocks
   if up:
       if blocks > 0:
           empty_row = [0] * level_width
           for i in range(blocks):
               tiles.insert(0, empty_row.copy())
       elif blocks < 0:
           tiles = tiles[-blocks:]

       for coin in collectibles:
           coin.y += blocks

       spawn_y += blocks * block_height
       player_y += blocks * block_height
       scroll_y += -blocks * block_height
   else:
       if blocks > 0:
           empty_row = [0] * level_width
           for i in range(blocks):
               tiles.append(empty_row.copy())
       elif blocks < 0:
           tiles = tiles[:level_height]

       max_yscroll = -(level_height * block_height - SCREEN_HEIGHT) - scroll_up


def is_column_empty(column):
   for row in tiles[0:level_height]:
       if row[column] != 0:
           return False
   return True


def is_row_empty(row):
   for tile in tiles[row]:
       if tile != 0:
           return False
   return True


def find_cols_erase(range, min):
   columns_empty = 0
   for column in range:
       if level_width - columns_empty <= min: return columns_empty  # minimum level width

       if is_column_empty(column):
           columns_empty += 1
       else:
           return columns_empty


def find_rows_erase(range, min):
   rows_empty = 0
   for row in range:
       if level_height - rows_empty <= min: return rows_empty  # minimum level height

       if is_row_empty(row):
           rows_empty += 1
       else:
           return rows_empty


clock = pygame.time.Clock()

while True:

   keys[4] = False

   # INPUT =============================================

   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           quit()
       if event.type == pygame.MOUSEBUTTONDOWN:
           mouse_down = True
       if event.type == pygame.MOUSEBUTTONUP:
           mouse_down = False

       if event.type == pygame.KEYDOWN:
           key = event.key
           if pygame.key.name(key).isdigit() and int(pygame.key.name(key)) in (0, 1, 2, 3, 4, 5, 6, 7):
               current_tile = int(pygame.key.name(key))
           if key == pygame.K_d: keys[0] = True
           if key == pygame.K_a: keys[1] = True
           if key == pygame.K_w: keys[2] = True
           if key == pygame.K_s: keys[3] = True
           if key == pygame.K_r: keys[4] = True
           if key == pygame.K_q: edit_mode = not edit_mode

       if event.type == pygame.KEYUP:
           if event.key == pygame.K_d: keys[0] = False
           if event.key == pygame.K_a: keys[1] = False
           if event.key == pygame.K_w: keys[2] = False
           if event.key == pygame.K_s: keys[3] = False

   # LOGIC =============================================

   mouse_x, mouse_y = pygame.mouse.get_pos()

   if edit_mode:
       if pygame.mouse.get_focused() == 1:  # if mouse is in window

           # INPUT

           tile_x = int((mouse_x + scroll_x) // (block_width))
           tile_y = int((mouse_y - scroll_y) // (block_height))
           if mouse_down:

               # CHANGE LEVEL DIMENSIONS IF PLACEMENT GOES OUT OF BOUNDS

               if current_tile != 0:
                   if tile_x >= level_width:
                       extend_level_width(tile_x - level_width + 1)
                   elif tile_x < 0:
                       extend_level_width(-tile_x, True)
                       tile_x = int((mouse_x + scroll_x) // (block_width))  # recalculate to avoid flashing

                   if tile_y >= level_height:
                       extend_level_height(tile_y - level_height + 1)
                   elif tile_y < 0:

                       extend_level_height(-tile_y, True)
                       tile_y = int((mouse_y - scroll_y) // (block_height))  # recalculate to avoid flashing

               # PLACE TILES

               if tile_x < level_width and tile_x >= 0 and tile_y < level_height and tile_y >= 0:
                   # print(str(tile_x) + "," + str(tile_y))

                   if tiles[tile_y][tile_x] != current_tile:
                       if tiles[tile_y][tile_x] == 2:  # remove coin
                           for coin in collectibles:
                               if coin.x == tile_x and coin.y == tile_y:
                                   collectibles.remove(coin)
                       if current_tile == 2:
                           coin = Collectible(tile_x, tile_y)
                           collectibles.append(coin)
                       if current_tile == 5:
                           spawn_x = tile_x * block_width
                           spawn_y = tile_y * block_height
                       else:
                           tiles[tile_y][tile_x] = current_tile
                       # update_ori(tile_x, tile_y)

               # LEVEL ERASING WITH EMPTY ENDS

               if current_tile == 0:
                   if tile_x == 0:  # 'eraser' tile
                       columns_empty = find_cols_erase(range(0, level_width), 16)
                       extend_level_width(-columns_empty, True)
                       tile_x = int((mouse_x + scroll_x) // (block_width))  # recalculate to avoid flashing

                   elif tile_x == level_width - 1:  # 'eraser' tile
                       columns_empty = find_cols_erase(range(level_width - 1, -1, -1), 16)
                       extend_level_width(-columns_empty)

                   if tile_y == 0:  # 'eraser' tile
                       rows_empty = find_rows_erase(range(0, level_height), 16)
                       extend_level_height(-rows_empty, True)
                       tile_y = int((mouse_y - scroll_y) // (block_height))  # recalculate to avoid flashing

                   elif tile_y == level_height - 1:  # 'eraser' tile
                       rows_empty = find_rows_erase(range(level_height - 1, -1, -1), 16)
                       extend_level_height(-rows_empty)

               # PANNING

           mouse_x_center = mouse_x - SCREEN_WIDTH / 2
           mouse_y_center = mouse_y - SCREEN_HEIGHT / 2

           if abs(mouse_x_center) >= SCREEN_WIDTH / 2 - 200:
               scroll_x += ((mouse_x_center - 200) if mouse_x_center > 0 else (mouse_x_center + 200)) // 10
           if abs(mouse_y_center) >= SCREEN_HEIGHT / 2 - 200:
               scroll_y -= ((mouse_y_center - 200) if mouse_y_center > 0 else (mouse_y_center + 200)) // 10

       # FINE PANNING

       if keys[0]: scroll_x += 5
       if keys[1]: scroll_x -= 5
       if keys[2]: scroll_y += 5
       if keys[3]: scroll_y -= 5

   else:
       if keys[4]: reset_level()  # reset key

       if vel_y >= 30: vel_y = 30

       acc_y = 0
       acc_x = 0

       # INPUT LOGIC

       if not game_over:

           # RUNNING

           if player_x + player_width >= level_width * block_width:  # prevent going through border
               player_x = level_width * block_width - player_width
           elif keys[0]:
               # vel_x += run_power
               acc_x += run_power
           if player_x <= 0:  # prevent going through border
               player_x = 0
           elif keys[1]:
               # vel_x -= run_power
               acc_x -= run_power

               # JUMPING

           if keys[2]:
               if colliding_ground:
                   if bounce_delay == 0:
                       jump_power = 15
                       if not jumped and jump_timer <= 0: jump_timer = 6
                       if jump_leeway > 0:
                           jump_leeway = 0
                           jump_timer = 2
                   else:
                       jump_power = 4
                       jump_timer = bounce_delay


               elif not jumped:
                   jump_leeway = 50
               jumped = True
           else:
               jumped = False
           if jump_leeway > 0: jump_leeway -= 1

           if jump_timer > 0:
               jump_timer -= 1
               if jump_timer <= 0: acc_y -= jump_power

       elif player_y > SCREEN_HEIGHT + player_height:
           vel_y = 0
           player_y = SCREEN_HEIGHT - max_yscroll

       if bounce_delay > 0:
           bounce_delay -= 1
           if bounce_delay == 0:
               vel_y = -bouncy_power

       # GROUND COLLISION

       player_tile_x = int((player_x + player_width / 2) // block_width)  # x center of player
       player_tile_y = int((player_y + player_height / 2) // block_height)  # y center of player

       acc_y += grav  # GRAVITY

       colliding_ground = False
       colliding_ceil = False
       colliding_wall = False

       for y in range(player_tile_y - 1, player_tile_y + 2 + math.ceil(player_height // block_height)):
           # for y in range(level_height):
           if y < 0 or y >= level_height: continue

           for x in range(player_tile_x - 1, player_tile_x + 2 + math.ceil(player_width // block_width)):
               # for x in range(level_width):
               if x < -1 or x >= level_width: break

               tile = tiles[y][x]
               tile_rect = (x * block_width, y * block_height, block_width, block_height)

               y_collide = is_rects_collis((player_x, player_y + vel_y + acc_y, player_width, player_height),
                                           tile_rect)
               x_collide = is_rects_collis((player_x + vel_x + acc_x, player_y, player_width, player_height),
                                           tile_rect)
               collide = is_rects_collis((player_x, player_y, player_width, player_height), tile_rect)

               if bounce_timer > 0:
                   continue

               if tile == 0:
                   continue
               elif tile == 1:
                   if y_collide:
                       if vel_y + acc_y < 0:
                           colliding_ceil = True
                           player_y = (y + 1) * block_height  # RIGHT BELOW BLOCK
                           vel_y = 0
                       else:
                           colliding_ground = True
                           player_y = y * block_height - player_height  # RIGHT ABOVE BLOCK
                           vel_y = 0
                       x_collide = is_rects_collis(
                           (player_x + vel_x + acc_x, player_y, player_width, player_height), tile_rect)
                   if x_collide:
                       if vel_x + acc_x > 0 or vel_x + acc_x < 0:
                           colliding_wall = True
                           if vel_x + acc_x > 0:
                               player_x = x * block_width - player_width
                           else:
                               player_x = (x + 1) * block_width
                           vel_x = 0

               elif tile == 3:
                   if y_collide and vel_y + acc_y > 0 and bounce_delay == 0:
                       colliding_ground = True
                       bounce_delay = 4
                   elif y_collide and vel_y + acc_y < 0 and not collide:
                       colliding_ceil = True
                       player_y = (y + 1) * block_height  # RIGHT BELOW BLOCK
                       vel_y = 0
                       x_collide = is_rects_collis(
                           (player_x + vel_x + acc_x, player_y, player_width, player_height), tile_rect)

                   if x_collide and not collide:
                       if vel_x + acc_x > 0 or vel_x + acc_x < 0:
                           colliding_wall = True
                           if vel_x + acc_x > 0:
                               player_x = x * block_width - player_width
                           else:
                               player_x = (x + 1) * block_width
                           vel_x = 0

               elif tile == 4:
                   if collide: game_over = True

               elif tile == 6:
                   if y_collide and vel_y + acc_y > 0 and not x_collide and not collide and not keys[3]:
                       colliding_ground = True
                       player_y = y * block_height - player_height  # RIGHT ABOVE BLOCK
                       vel_y = 0
                       x_collide = is_rects_collis((player_x + vel_x + acc_x, player_y, player_width, player_height),
                                                   tile_rect)

               elif tile == 7:
                   if collide:
                       in_water = True

       # MOVE

       if not colliding_ground and not colliding_ceil: vel_y += acc_y
       if not colliding_wall: vel_x += acc_x

       player_y += vel_y
       if abs(vel_x) > 0.5:
           player_x += vel_x

       # FRICTION

       vel_x = round(vel_x * 0.6, 2)

       # SCROLL

       scroll_y += (-(player_y - (SCREEN_HEIGHT / 2) + (player_height / 2)) - scroll_y + scroll_up) // 10
       scroll_x += (player_x - (SCREEN_WIDTH / 2) + (player_width / 2) - scroll_x) // 10

       # SCROLL BOUNDARIES

       if scroll_x < min_xscroll:
           scroll_x = min_xscroll
       elif scroll_x > max_xscroll:
           scroll_x = max_xscroll
       if scroll_y < max_yscroll: scroll_y = max_yscroll  # screen_height/2+2*block_height

       # NOT SMOOTH
       # scroll_y = -player_y + (screen_height / 2) - player_height / 2
       # scroll_x = player_x - (screen_width / 2) + player_width / 2

       # FALL INTO DA VOID
       if player_y > level_height * block_height + scroll_up: game_over = True

       # COIN COLLECTION

       for coin in collectibles:
           if not coin.collected and is_rects_collis(
                   (player_x, player_y, player_width, player_height),
                   (coin.x * block_width, coin.y * block_height, coin.width, coin.height)):
               coin.collected = True
               coins += 1
               print('cha-ching\tmoolah: ', coins)

   # LOGIC =============================================

   # SCREEN PAINTING ============================================

   # FILL SKY

   screen.fill(tile_colors[0])

   # DRAW TILES

   curr_x = 0
   curr_y = 0
   for row in tiles:
       for tile in row:
           if tile == 0:
               pass
           elif tile == 4:
               start_x = int(curr_x - scroll_x)
               start_y = int(curr_y + scroll_y)
               points = [(start_x, start_y + block_height), (start_x + block_width, start_y + block_height),
                         (start_x + block_width / 2, start_y)]
               pygame.draw.polygon(screen, tile_colors[4], points)
           elif tile != 2:
               pygame.draw.rect(screen, tile_colors[tile],
                                (int(curr_x - scroll_x), int(curr_y + scroll_y), block_width, block_height))

           curr_x += block_width

       curr_y += block_height
       curr_x = 0

   # DRAW BOTTOM TILES
   curr_x = - scroll_x
   for tile in tiles[level_height - 1]:
       if tile == 1:
           curr_y = (level_height - 0) * block_height + scroll_y
           for i in range(math.ceil(scroll_up / block_height)):
               pygame.draw.rect(screen, tile_colors[tile],
                                (int(curr_x), int(curr_y), block_width, block_height))
               curr_y += block_height
       curr_x += block_width

       # COLLECTIBLES

   for coin in collectibles:
       if not coin.collected and edit_mode: coin.draw(tile_colors[2])  # show coins in edit mode

   # EDIT MODE

   if edit_mode:
       # DRAW GHOST BLOCK
       ghost_tile = pygame.Surface((block_width, block_height))  # per-pixel alpha
       ghost_tile.fill(tile_colors[current_tile])  # notice the alpha value in the color
       ghost_tile.set_alpha(160)

       screen.blit(ghost_tile, (int(tile_x * block_width - scroll_x), int(tile_y * block_height + scroll_y)))

       # not transparent
       # pygame.draw.rect(screen, tile_colors[current_tile], (tile_x*block_width-scroll_x, tile_y*block_height+scroll_y, block_width, block_height))

       # DRAW LEVEL BORDERS
       pygame.draw.rect(screen, (255, 255, 255), (int(0 - scroll_x), int(0 + scroll_y),
                                                  level_width * block_width, level_height * block_height), 2)

   # DRAW PLAYER

   pygame.draw.rect(screen, (203, 181, 244), (
       int(player_x - scroll_x), int(player_y + scroll_y), player_width, player_height))

   pygame.display.update()

   clock.tick(60)

