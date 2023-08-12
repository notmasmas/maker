import pygame
import time
import random

from sys import exit

import image_loader
from objects.fruit import Fruit
from objects.bomb import Bomb
from objects.cloud import Cloud

pygame.mixer.init()

# Inicialização do pygame
pygame.init()

# Configuração da tela
screen_width = 640
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kiwi :D")

# Relógio para controle de frames
clock = pygame.time.Clock()

# Carregamento de fonte
load_score_font = pygame.font.Font("graphics/fonts/Daydream.ttf", 30)
load_text_font = pygame.font.Font("graphics/fonts/Daydream.ttf", 15)
load_fps_font = pygame.font.Font("graphics/fonts/Daydream.ttf", 20)

# Cálculo do centro da tela
center_x = screen_width / 2
center_y = screen_height / 2

# Caminhos dos sprites
player_image_path = "graphics/kiwi.png"
fruit_kiwi_image_path = "graphics/fruit_kiwi.png"
fruit_banana_image_path = "graphics/fruit_banana.png"
fruit_orange_image_path = "graphics/fruit_orange.png"
bomb_image_path = "graphics/bomb.png"
heart_image_path = "graphics/lifes1.png"
cloud_image_path = "graphics/cloud.png"

lifes1_path = "graphics/lifes1.png"

app_icon_path = "graphics/app_icon.png"
mouse_icon_path = "graphics/mouse_icon.png"
keyboard_icon_path = "graphics/keyboard_icon.png"
boom_path = "graphics/boom.png"

# Propriedades do kiwi (player)
player_surf = image_loader.load_image(player_image_path, 1)
kiwi_rect = player_surf.get_rect(midbottom=(center_x, 435))

# Propriedades dos objetos
fruit_types = ["kiwi", "banana", "orange"]
fruits = []
bombs = []
hearts = []
bomb_spawn_positions = [80, -80, 40, -40]
starting_text = load_text_font.render(str("Pegue uma fruta para iniciar"), False, "black")
starting_text_rect = starting_text.get_rect(midtop=(center_x, center_y))

# Propriedades do som
pygame.mixer.music.load("sounds/vine-boom.mp3")
pygame.mixer.music.set_volume(0.3)

# Propriedades da nuvem
cloud_surf = image_loader.load_image(cloud_image_path, 1)
clouds = []

# Propriedades dos ícones
icon_pos = (center_x + 265, center_y + 195)

# Propriedades do chão
ground_height = 45
ground_color = (34, 139, 34)
ground = pygame.Rect(0, center_y * 2 - ground_height, center_x * 2, ground_height)

# Variáveis aleatórias
background_color = (135, 206, 335)
mouse_controls = True
initial_time = time.time()
current_time = initial_time
countdown = 0
spawn_cloud_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_cloud_event, 5000)
first_fruit = False

score = 0
score_font = load_score_font.render(str(score), False, "black")
score_rect = score_font.get_rect(midtop=(center_x, 20))

fps = clock.get_fps()
fps_font = load_fps_font.render(str(fps), False, "black")
fps_rect = fps_font.get_rect(topright=(520, 20))
show_fps = False

lifes = 3
life_icon = image_loader.load_image(lifes1_path, 2)
life_rect = life_icon.get_rect(topleft=(20, 20))
life_spacing = 40
life_xpos = 50
lifes_list = [0, 1, 2]

mouse_icon = image_loader.load_image(mouse_icon_path, 3)
keyboard_icon = image_loader.load_image(keyboard_icon_path, 3)
app_icon = image_loader.load_image(app_icon_path, 3)
bomb_surf = image_loader.load_image(bomb_image_path, 3)
heart_surf = image_loader.load_image(heart_image_path, 3)
boom_surf = image_loader.load_image(boom_path, 3)

pygame.display.set_icon(app_icon)


def render_ui():  # Função para caso vc precise renderizar alguma coisa relacionada a UI na tela :)
    if mouse_controls:
        screen.blit(mouse_icon, icon_pos)
    else:
        screen.blit(keyboard_icon, icon_pos)

    global score_font
    score_font = load_score_font.render(str(score), False, "black")
    screen.blit(score_font, score_rect)

    global fps_font
    if show_fps:
        fps_font = load_fps_font.render(f"fps: {fps:.2f}", False, "black")
        screen.blit(fps_font, fps_rect)

    if not first_fruit:
        screen.blit(starting_text, starting_text_rect)

    for lives in enumerate(lifes_list):
        screen.blit(life_icon, (20 + life_spacing * lives[0], 20))


def movement():
    if mouse_controls:
        kiwi_rect.x = pygame.mouse.get_pos()[0]

    if not mouse_controls:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            kiwi_rect.x -= 5
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            kiwi_rect.x += 5


def spawn_new_fruit():
    fruit_x_pos = random.randint(0, (int(screen_width * 2) - 36))
    fruit_speed = random.randint(1, 6)
    fruit_type = random.randint(1, len(fruit_types))
    new_fruit = Fruit(fruit_x_pos, fruit_speed, fruit_type)
    fruits.append(new_fruit)

    if random.randint(1, 100) <= 30:
        spawn_new_bomb(fruit_x_pos)


def spawn_new_bomb(fruit_x_pos):
    bomb_x_pos = fruit_x_pos + random.choice(bomb_spawn_positions)
    bomb_speed = random.randint(2, 6)
    new_bomb = Bomb(bomb_x_pos, bomb_speed, bomb_surf)
    bombs.append(new_bomb)


def spawn_new_heart():
    heart_x_pos = random.randint(0, (int(screen_width * 2) - 36))
    heart_speed = random.randint(3, 7)
    new_heart = Bomb(heart_x_pos, heart_speed, heart_surf)
    hearts.append(new_heart)


def spawn_new_cloud():
    cloud_y_pos = random.randint(20, 100)
    cloud_speed = random.randint(1, 2)
    new_cloud = Cloud(cloud_y_pos, cloud_speed, cloud_surf)
    clouds.append(new_cloud)


def randomize_spawns():
    if random.randint(1, 100) <= 90:
        spawn_new_fruit()

    if random.randint(1, 100) <= 6:
        spawn_new_heart()


def add_life():
    global lifes
    lifes += 1
    lifes_list.append(0)


def lose_life():
    global lifes
    lifes -= 1
    if len(lifes_list) > 0:
        lifes_list.pop()


while True:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            pygame.mixer.quit()
            exit()
        elif keys[pygame.K_e]:
            mouse_controls = not mouse_controls
        elif event.type == spawn_cloud_event:
            spawn_new_cloud()
        elif keys[pygame.K_F3]:
            show_fps = not show_fps

    screen.fill("lightblue")

    current_time = time.time()

    if current_time >= countdown:
        for i in range(1, random.randint(1, 4)):
            randomize_spawns()
        countdown = current_time + random.randint(1, 2)

    if score <= -1 and first_fruit:
        print("You lose")
        pygame.quit()
        exit()

    if lifes <= -1:
        pygame.quit()
        exit()

    for fruit in fruits:
        fruit.update()
        if fruit.rect.colliderect(ground):
            #fruit.death()
            #fruit.is_done()        # bug bem de arrombado, eu quero colocar uma animação de fade out, funciona,
            #if fruit.is_done():    # mas como o objeto fica por mais um tempinho, a pontuação acaba sendo subtraida
            fruits.remove(fruit)    # mais do q deveria, ent em vez de ser -2, acaba sendo -10 (exemplo), pq
            if first_fruit:         # o objeto acaba entrando no chão e ficando ali por um tempo
                score -= 2
        if fruit.rect.colliderect(kiwi_rect):
            if fruit in fruits:
                fruits.remove(fruit)
                if first_fruit:
                    score += 1
                first_fruit = True

    for bomb in bombs:
        bomb.update()
        if bomb.rect.colliderect(ground):
            bombs.remove(bomb)
        if bomb.rect.colliderect(kiwi_rect):
            boom_rect = boom_surf.get_rect(topleft=(bomb.rect.x, bomb.rect.y))
            screen.blit(boom_surf, boom_rect)
            pygame.mixer.music.play()
            bombs.remove(bomb)
            lose_life()

    for heart in hearts:
        heart.update()
        if heart.rect.colliderect(ground):
            hearts.remove(heart)
        if heart.rect.colliderect(kiwi_rect):
            if lifes < 3:
                add_life()
            hearts.remove(heart)

    for cloud in clouds:
        cloud.update()
        if cloud.rect.x < -200:
            clouds.remove(cloud)

    movement()

    # se vc for fazer algo envolvendo adicionar mais coisas pra renderizar e tals, coloca de baixo dessa linha
    # pra ficar mais facil de ler o codigo, a logica e essas coisas deixa na parte de cima

    # okay bjos <3

    screen.blit(player_surf, kiwi_rect)  # desenha o player
    pygame.draw.rect(screen, ground_color, ground)  # desenha o chao

    for cloud in clouds:  # desenha as nuvens
        screen.blit(cloud.image, cloud.rect)

    for fruit in fruits:  # desenha as frutas
        screen.blit(fruit.image, fruit.rect)

    for bomb in bombs:  # desenha as bombas
        screen.blit(bomb.image, bomb.rect)

    for heart in hearts:
        screen.blit(heart.image, heart.rect)

    fps = clock.get_fps()

    render_ui()
    pygame.display.flip()
    life_xpos = 50

    pygame.display.update()
    clock.tick(60)
