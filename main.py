import pygame
from sys import exit
import random

from Entity import Entity

pygame.init()

screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

screen_width = screen.get_width() / 2
screen_height = screen.get_height() / 2

entity = Entity()
entity.spawn(screen_width, screen_height)
entity_out_of_screen = False
fruit_spawn_x = random.randrange(25, 615)
fruit_spawn_y = 0

player_pos = pygame.Vector2(screen_width, 0)
player_size = 25

gravity = 0


def movement():
    player_pos.x = pygame.mouse.get_pos()[0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player_pos.x -= 5
    if keys[pygame.K_d]:
        player_pos.x += 5


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        gravity += 1
        player_pos.y += gravity

        screen.fill("white")

        movement()
        entity.update()

    pygame.draw.circle(screen, "black", player_pos, player_size)

    pygame.display.update()
    clock.tick(60)
