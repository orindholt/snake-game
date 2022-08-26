from tkinter import E
import pygame
import random
import shelve

pygame.init()

hscore = 0

d = shelve.open("data")
try:
    d["high_score"]
    hscore = int(d["high_score"])
except:
    hscore = 0
print(hscore)
d.close()

char_size = 30
screen_width = char_size * 30
screen_height = char_size * 20

blue = 0, 0, 255
black = 0, 0, 0
white = 255, 255, 255
FPS = 10

monster_death_sounds = [
    pygame.mixer.Sound("assets/sounds/monster/death_01.wav"),
    pygame.mixer.Sound("assets/sounds/monster/death_02.wav"),
    pygame.mixer.Sound("assets/sounds/monster/death_03.wav")]


class CharAnimations:
    char_walk_front = [
        pygame.image.load("assets/char/front/player_01.png"),
        pygame.image.load("assets/char/front/player_02.png"),
        pygame.image.load("assets/char/front/player_01.png"),
        pygame.image.load("assets/char/front/player_03.png")]
    char_walk_side = [
        pygame.image.load("assets/char/side/player_01.png"),
        pygame.image.load("assets/char/side/player_02.png"),
        pygame.image.load("assets/char/side/player_01.png"),
        pygame.image.load("assets/char/side/player_03.png")]
    char_walk_back = [
        pygame.image.load("assets/char/back/player_01.png"),
        pygame.image.load("assets/char/back/player_02.png"),
        pygame.image.load("assets/char/back/player_01.png"),
        pygame.image.load("assets/char/back/player_03.png")]


char = CharAnimations().char_walk_front[1]
char = pygame.transform.scale(char, (char_size, char_size))
char_rect = char.get_rect()


class MonsterAnimations:
    spider_ani = [
        pygame.image.load("assets/monsters/spider/monster_01.png"),
        pygame.image.load("assets/monsters/spider/monster_02.png")]
    rat_ani = [
        pygame.image.load("assets/monsters/rat/monster_01.png"),
        pygame.image.load("assets/monsters/rat/monster_02.png")]
    snake_ani = [
        pygame.image.load("assets/monsters/snake/monster_01.png"),
        pygame.image.load("assets/monsters/snake/monster_02.png")]
    slime_ani = [
        pygame.image.load("assets/monsters/slime/monster_01.png"),
        pygame.image.load("assets/monsters/slime/monster_02.png")]


beep_sound = pygame.mixer.Sound("assets/sounds/beep.wav")

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.update()
pygame.display.set_caption("Snake game")

score_font = pygame.font.Font("assets/fonts/font_02.otf", 32)
title_font = pygame.font.Font("assets/fonts/font_01.ttf", 48)
plus_font = pygame.font.Font("assets/fonts/font_02.otf", 20)


def show_score(val):
    text = score_font.render(str(val), True, white)
    screen.blit(text, (10, 5))


def show_high_score(high_score):
    text = score_font.render("High score: " + str(high_score), True, white)
    screen.blit(text, (10, 5))


class Button():
    def __init__(self, x, y, text, size, color):
        self.arrow = pygame.image.load("assets/arrow.png").convert_alpha()
        self.arrow_rect = self.arrow.get_rect()
        font = pygame.font.Font("assets/fonts/font_02.otf", size)
        self.rendered = font.render(str(text), True, color)
        self.rect = self.rendered.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        self.arrow.set_alpha(0)
        if (self.rect.collidepoint(pos)):
            self.arrow.set_alpha(255)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                action = False
                self.clicked = False
        screen.blit(self.arrow, (self.rect.x - 30, self.rect.y + 15))
        screen.blit(self.rendered, (self.rect.x, self.rect.y))

        return action


start_button = Button(round(screen_width/2.5),
                      round(screen_height/2.25), "Start", 42, white)
exit_button = Button(round(screen_width/2.4),
                     round(screen_height/1.8), "Exit", 42, white)

monsters = [
    MonsterAnimations.spider_ani,
    MonsterAnimations.rat_ani,
    MonsterAnimations.snake_ani,
    MonsterAnimations.slime_ani]

randIndex = random.randrange(len(monsters))
monster = monsters[randIndex][0]
monster = pygame.transform.scale(monster, (char_size, char_size))
monster_rect = monster.get_rect()

grass = pygame.image.load("assets/grass.jpg")
grass = pygame.transform.scale(grass, (screen_width, screen_height))

game_menu = True


def gameLoop():
    global hscore
    global game_menu
    run = True
    score = 0

    char_x = round(screen_width/2)
    char_y = round(screen_height/2)
    char_chords = []
    char_surface = []
    direction = "down"

    char_walk_count = 0
    monster_ani_count = 0

    randIndex = random.randrange(len(monsters))
    char = CharAnimations.char_walk_front[0]

    char_chords.append((char_x, char_y))
    char_surface.append(char)

    def move_monster():
        random_x = round(random.randrange(0, screen_width, char_size))
        random_y = round(random.randrange(0, screen_height, char_size))
        monster_rect.x = random_x
        monster_rect.y = random_y
    move_monster()

    plus_text = plus_font.render(str("+1"), True, white).convert_alpha()
    plus_text.set_alpha(0)
    plus_rect = plus_text.get_rect()

    while run:
        while game_menu:
            screen.blit(grass, (0, 0))
            show_high_score(hscore)
            title = title_font.render("Snake Game", True, white)
            screen.blit(title, (screen_width/3.8, screen_height/3.8))

            if start_button.draw():
                game_menu = False
                gameLoop()
            if exit_button.draw():
                pygame.quit()
                quit()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # main event loop
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_w):
                    if len(char_chords) > 1 and direction != "down":
                        direction = "up"
                    elif len(char_chords) <= 1:
                        direction = "up"
                elif (event.key == pygame.K_s):
                    if len(char_chords) > 1 and direction != "up":
                        direction = "down"
                    elif len(char_chords) <= 1:
                        direction = "down"
                elif (event.key == pygame.K_d):
                    if len(char_chords) > 1 and direction != "left":
                        direction = "right"
                    elif len(char_chords) <= 1:
                        direction = "right"
                elif (event.key == pygame.K_a):
                    if len(char_chords) > 1 and direction != "right":
                        direction = "left"
                    elif len(char_chords) <= 1:
                        direction = "left"

        # walk and animations counts
        if char_walk_count < (len(CharAnimations.char_walk_front) - 1):
            char_walk_count += 1
        else:
            char_walk_count = 0

        if monster_ani_count < (len(MonsterAnimations.spider_ani) - 1):
            monster_ani_count += 1
        else:
            monster_ani_count = 0

        # moves char in direction
        if direction == "up":
            char_y -= char_size
            char = CharAnimations.char_walk_back[char_walk_count]
        elif direction == "down":
            char_y += char_size
            char = CharAnimations.char_walk_front[char_walk_count]
        elif direction == "right":
            char_x += char_size
            char = CharAnimations.char_walk_side[char_walk_count]
            char = pygame.transform.flip(char, True, False)
        elif direction == "left":
            char_x -= char_size
            char = CharAnimations.char_walk_side[char_walk_count]

        char_surface[0] = char
        char_rect.topleft = (char_x, char_y)

        # kills monster and +1 score
        if char_rect.x == monster_rect.x and char_rect.y == monster_rect.y:
            score += 1
            char_surface.insert(1, monster)
            randIndex = random.randrange(len(monsters))
            monster = monsters[randIndex][0]
            pygame.mixer.Sound.play(
                monster_death_sounds[random.randrange(len(monster_death_sounds))])
            pygame.mixer.Sound.play(
                monster_death_sounds[random.randrange(len(monster_death_sounds))])
            pygame.mixer.Sound.play(beep_sound)
            plus_rect.topleft = (monster_rect.x + char_size,
                                 monster_rect.y - char_size)
            plus_text.set_alpha(255)

            move_monster()
        monster = monsters[randIndex][monster_ani_count]
        monster = pygame.transform.scale(monster, (char_size, char_size))

        # remembers last positions
        char_chords.append((char_rect.x, char_rect.y))

        if (len(char_chords) > score + 1):
            char_chords.pop(0)

        # renders grass and monster
        screen.blit(grass, (0, 0))
        screen.blit(monster, monster_rect)

        # renders snake
        char_surface.reverse()

        for i, (x, y) in enumerate(char_chords):
            surface = pygame.transform.scale(
                char_surface[i], (char_size, char_size))
            screen.blit(surface, (x, y))

        char_surface.reverse()

        # +1 render
        if plus_text.get_alpha() > 0:
            plus_text.set_alpha(plus_text.get_alpha() - (255 / FPS))
        screen.blit(plus_text, (plus_rect.x, plus_rect.y))

        # death
        if char_x < 0 or char_x > (screen_width-char_size) or char_y < 0 or char_y > (screen_height-char_size) or char_chords.count(char_chords[0]) > 1:
            d = shelve.open("data")
            if(score > hscore):
                hscore = score
                d["high_score"] = str(score)
            d.close()
            game_menu = True

        show_score(score)

        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()


gameLoop()
