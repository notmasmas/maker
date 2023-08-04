import pygame
from sys import exit

from pygame import surface

# teste

# import random
# from entity import *

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Kiwi :D")
clock = pygame.time.Clock()

screen_width = screen.get_width() / 2
screen_height = screen.get_height() / 2

kiwi_surf = pygame.image.load("graphics/kiwi.png")
kiwi_rect = kiwi_surf.get_rect(midbottom=(screen_width, 440))

ground_height = 40
ground_color = (34, 139, 34)
ground = pygame.Rect(0, screen_height * 2 - ground_height, screen_width * 2, ground_height)


def movement():
    kiwi_rect.x = pygame.mouse.get_pos()[0]
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        kiwi_rect.x -= 5
    if keys[pygame.K_d]:
        kiwi_rect.x += 5


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill("white")
    pygame.draw.rect(screen, ground_color, ground)
    screen.blit(kiwi_surf, (kiwi_rect.x, kiwi_rect.y))
    movement()

    pygame.display.update()
    clock.tick(60)
