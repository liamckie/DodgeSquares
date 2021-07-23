from random import *
import pygame
import sys

pygame.init()

WIDTH = 800
HEIGHT = 600

RED = (255, 40, 0)  # Enemy
BLUE = (0, 60, 255)  # Player
GREEN = (20, 255, 20)   # Score Colour
BG_COLOUR = (0, 0, 0)

SPEED = 7

player_size = 50
player_pos = [WIDTH / 2, HEIGHT - 3 * player_size]

enemy_size = 50
enemy_pos = [randint(0, WIDTH - enemy_size), 0]
enemy_list = [enemy_pos]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Square Dogder")

game_over = False
score = 0
clock = pygame.time.Clock()
myFont = pygame.font.SysFont("Consolas", 35)


def set_level(score, SPEED):
    if score < 20 :
        SPEED = 5
    elif score < 40:
        SPEED = 7
    elif score < 60:
        SPEED = 9
    elif score < 80:
        SPEED = 11
    else:
        SPEED = 15
    return  SPEED


def drop_enemies(enemy_list):
    delay = random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = randint(0, WIDTH - enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, RED, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_pos(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += SPEED
        else:
            enemy_list.pop(idx)
            score += 1
    return score


def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos, player_pos):
            return True
    return False


def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
        if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
            return True
    return False


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            x = player_pos[0]
            y = player_pos[1]

            if event.key == pygame.K_LEFT:
                x -= player_size
            elif event.key == pygame.K_RIGHT:
                x += player_size
            elif event.key == pygame.K_UP:
                y -= player_size
            elif event.key == pygame.K_DOWN:
                y += player_size

            player_pos = [x, y]

    screen.fill(BG_COLOUR)

    if detect_collision(player_pos, enemy_pos):
        game_over = True
        break

    drop_enemies(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    SPEED = set_level(score, SPEED)

    text = "SCORE: " + str(score)
    label = myFont.render(text, 1, GREEN)
    screen.blit(label, (WIDTH - 200, HEIGHT - 40))

    if collision_check(enemy_list, player_pos):
        result = "Your score was : " + str(score)
        print(result)
        game_over = True

    draw_enemies(enemy_list)
    pygame.draw.rect(screen, BLUE, (player_pos[0], player_pos[1], player_size, player_size))

    clock.tick(30)

    pygame.display.update()

