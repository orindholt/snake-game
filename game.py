from ast import walk
from distutils.util import check_environ
import pygame
import random
pygame.init()

char_size = 30
walk_count = 0

screen_width = char_size * 30
screen_height = char_size * 20

blue = 0, 0, 255
black = 0, 0, 0
background = 220, 224, 193
FPS = 5

score = 0

run = True
direction = "down"

char_x = round(screen_width/2)
char_y = round(screen_height/2)

char_walk_front = [
    pygame.image.load("assets/char/front/player_02.png"),
    pygame.image.load("assets/char/front/player_03.png"), ]
char_walk_side = [pygame.image.load(
    "assets/char/side/player_01.png"), pygame.image.load("assets/char/side/player_02.png")]
char_walk_back = [pygame.image.load(
    "assets/char/back/player_01.png"), pygame.image.load("assets/char/back/player_01.png")]

char = pygame.image.load("assets/char/front/player_01.png")
char = pygame.transform.scale(char, (char_size, char_size))

char_rect = char.get_rect()


monster = pygame.image.load("assets/monsters/spider/monster_01.png")
monster = pygame.transform.scale(monster, (char_size, char_size))
monster_rect = monster.get_rect()

grass = pygame.image.load("assets/grass.jpg")
grass = pygame.transform.scale(grass, (screen_width, screen_height))

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()
pygame.display.set_caption("Snake game")


def move_food():
    x = round(random.randrange(0, screen_width, char_size))
    y = round(random.randrange(0, screen_height, char_size))
    monster_rect.x = x
    monster_rect.y = y
    screen.blit(monster, monster_rect)


move_food()


def move_char():
    char_rect.x = char_x
    char_rect.y = char_y


move_char()

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_w):
                direction = "up"
            elif(event.key == pygame.K_s):
                direction = "down"
            elif(event.key == pygame.K_d):
                direction = "right"
            elif(event.key == pygame.K_a):
                direction = "left"

    if char_x < 0 or char_x > (screen_width-char_size) or char_y < 0 or char_y > (screen_height-char_size):
        run = False

    if walk_count < 1:
        walk_count += 1
    else:
        walk_count = 0

    print(walk_count)
    if direction == "up":
        char_y -= char_size
        char = char_walk_back[walk_count]
    elif direction == "down":
        char_y += char_size
        char = char_walk_front[walk_count]
    elif direction == "right":
        char_x += char_size
        char = char_walk_side[walk_count]
        char = pygame.transform.flip(char, True, False)
    elif direction == "left":
        char_x -= char_size
        char = char_walk_side[walk_count]

    char = pygame.transform.scale(char, (char_size, char_size))
    move_char()

    if char_rect.x == monster_rect.x and char_rect.y == monster_rect.y:
        print("!")
        score += 1
        move_food()

    screen.blit(grass, (0, 0))
    screen.blit(monster, monster_rect)
    screen.blit(char, char_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
quit()
