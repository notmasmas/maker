import random
import time

import pygame
from sys import exit

from fruit import Fruit
from bomb import Bomb

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Kiwi :D")
clock = pygame.time.Clock()

screen_width = screen.get_width() / 2
screen_height = screen.get_height() / 2

# Propriedades do kiwi (player)
kiwi_surf = pygame.image.load("graphics/kiwi.png")
kiwi_rect = kiwi_surf.get_rect(midbottom=(screen_width, 435))

# Propriedades dos objetos
fruit_surf = pygame.image.load("graphics/fruit.png")
bomb_image_path = "graphics/bomb.png"
objects = []

# Propriedades de icones
app_icon_path = "graphics/app_icon.png"
mouse_icon_path = "graphics/mouse_icon.png"
keyboard_icon_path = "graphics/keyboard_icon.png"
icon_pos = (screen_width + 265, screen_height + 195)

# Propriedades do chão
ground_height = 45
ground_color = (34, 139, 34)
ground = pygame.Rect(0, screen_height * 2 - ground_height, screen_width * 2, ground_height)

# Variáveis aleatórias ai sla
mouse_controls = True
initial_time = time.time()
current_time = initial_time
countdown = 0


# Essa função vai pegar a imagem e multiplicar por 3 (scale_factor) :thumbsup:
def load_image_and_scale(image_path, scale_factor):
    original_image = pygame.image.load(image_path)
    return pygame.transform.scale(original_image, (
        original_image.get_width() * scale_factor, original_image.get_height() * scale_factor))


mouse_icon = load_image_and_scale(mouse_icon_path, 3)
keyboard_icon = load_image_and_scale(keyboard_icon_path, 3)
app_icon = load_image_and_scale(app_icon_path, 3)
bomb_surf = load_image_and_scale(bomb_image_path, 3)


def render_ui():    # Função para caso vc precise renderizar alguma coisa relacionada a UI na tela :)
    if mouse_controls:
        screen.blit(mouse_icon, icon_pos)
    else:
        screen.blit(keyboard_icon, icon_pos)


def movement():
    if mouse_controls:
        kiwi_rect.x = pygame.mouse.get_pos()[0]

    if not mouse_controls:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            kiwi_rect.x -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            kiwi_rect.x += 5


def spawn_new_fruit():
    fruit_x_pos = random.randint(0, (screen_width * 2) - 36)
    fruit_speed = random.randint(1, 4)
    new_fruit = Fruit(fruit_x_pos, fruit_speed, fruit_surf)
    objects.append(new_fruit)


def spawn_new_bomb():
    bomb_x_pos = random.randint(0, (screen_width * 2) - 36)
    bomb_speed = random.randint(1, 4)
    new_bomb = Bomb(bomb_x_pos, bomb_speed, bomb_surf)
    objects.append(new_bomb)


def randomize_spawns():
    random_spawn_type = random.randint(0, 4)
    if random_spawn_type == 0:
        spawn_new_bomb()
    else:
        spawn_new_fruit()


while True:
    keys = pygame.key.get_pressed()  # n pergunta pq essa variavel ta aq
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif keys[pygame.K_e]:
            mouse_controls = not mouse_controls
            print(mouse_controls)

    screen.fill("lightblue")  # isolaaaaaaaaaaaaaaaaaadoooooos...... isolaaaaaaaaaaaaaaaaaaaadooooooooooos uuuuuuuuuuuuuuu

    current_time = time.time()

    if current_time >= countdown:
        for i in range(1, random.randint(1, 4)):
            randomize_spawns()
        countdown = current_time + random.randint(1, 2)

    # TODO: juntar as frutas e bombas em uma classe
    for fruit in objects:
        fruit.update()
        if fruit.rect.colliderect(ground):
            objects.remove(fruit)  # desenha as frutas

    for bomb in objects:
        bomb.update()
        if bomb.rect.colliderect(ground):
            objects.remove(bomb)

    movement()

    # se vc for fazer algo envolvendo adicionar mais coisas pra renderizar e tals, coloca de baixo dessa linha
    # pra ficar mais facil de ler o codigo, a logica e essas coisas deixa na parte de cima

    screen.blit(kiwi_surf, kiwi_rect)  # desenha o player
    pygame.draw.rect(screen, ground_color, ground)  # desenha o chao
    for fruit in objects:
        screen.blit(fruit.image, fruit.rect)
    for bomb in objects:
        screen.blit(bomb.image, bomb.rect)

    render_ui()

    pygame.display.update()
    clock.tick(60)
