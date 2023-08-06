import random
import time

import pygame
from sys import exit

from fruit import Fruit
from bomb import Bomb
from cloud import Cloud

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Kiwi :D")
clock = pygame.time.Clock()
font = pygame.font.Font("graphics/Minecrafter.Reg.ttf", 30)

screen_width = screen.get_width() / 2
screen_height = screen.get_height() / 2

# Propriedades do kiwi (player)
kiwi_surf = pygame.image.load("graphics/kiwi.png")
kiwi_rect = kiwi_surf.get_rect(midbottom=(screen_width, 435))

# Propriedades dos objetos
fruit_surf = pygame.image.load("graphics/fruit.png")
bomb_image_path = "graphics/bomb.png"
objects = []

# Propriedades nuvem
cloud_surf = pygame.image.load("graphics/cloud.png")
clouds = []
spawn_interval = 5000
last_spawn = 0

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

score = 0
score_font = font.render(str(score), False, "black")
score_rect = score_font.get_rect(midtop=(screen_width, 20))


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
    global score_font
    score_font = font.render(str(score), False, "black")


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


def spawn_new_cloud():
    y_pos = random.randint(20, 60)
    cloud_speed = random.randint(1, 2)
    new_cloud = Cloud(y_pos, cloud_speed, cloud_surf)
    clouds.append(new_cloud)


pygame.display.set_icon(app_icon)


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

    if current_time - last_spawn >= spawn_interval:
        spawn_new_cloud()
        last_spawn = current_time

    # TODO: juntar as frutas e bombas em uma classe
    for fruit in objects:
        fruit.update()
        if fruit.rect.colliderect(ground):
            objects.remove(fruit)  # desenha as frutas
        if fruit.rect.colliderect(kiwi_rect):
            if fruit in objects:
                objects.remove(fruit)
                score += 1

    for bomb in objects:
        bomb.update()
        if bomb.rect.colliderect(ground):
            objects.remove(bomb)

    for cloud in clouds:
        cloud.update()

    movement()

    # se vc for fazer algo envolvendo adicionar mais coisas pra renderizar e tals, coloca de baixo dessa linha
    # pra ficar mais facil de ler o codigo, a logica e essas coisas deixa na parte de cima

    # okay bjos <3

    screen.blit(kiwi_surf, kiwi_rect)  # desenha o player
    pygame.draw.rect(screen, ground_color, ground)  # desenha o chao
    for fruit in objects:
        screen.blit(fruit.image, fruit.rect)
    for bomb in objects:
        screen.blit(bomb.image, bomb.rect)

    for cloud in clouds:
        screen.blit(cloud.image, cloud.rect)

    screen.blit(score_font, score_rect)

    render_ui()

    pygame.display.update()
    clock.tick(60)
