import pygame
from sys import exit

pygame.init()

screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Kiwi :D")
clock = pygame.time.Clock()

screen_width = screen.get_width() / 2
screen_height = screen.get_height() / 2

# Propriedades do kiwi (player)
kiwi_surf = pygame.image.load("graphics/kiwi.png")
kiwi_rect = kiwi_surf.get_rect(midbottom=(screen_width, 435))

# Propriedades de icones
app_icon_path = "graphics/app_icon.png"
mouse_icon_path = "graphics/mouse_icon.png"
keyboard_icon_path = "graphics/keyboard_icon.png"
scale_factor = 3  # Favor não mudar (é sério)
icon_pos = (screen_width + 265, screen_height + 195)

# Propriedades do chão
ground_height = 45
ground_color = (34, 139, 34)
ground = pygame.Rect(0, screen_height * 2 - ground_height, screen_width * 2, ground_height)

# Variáveis aleatórias ai sla
mouse_controls = True


# Essa função vai pegar a imagem e multiplicar por 3 (scale_factor) :thumbsup:
def load_image_and_scale(image_path):
    original_image = pygame.image.load(image_path)
    return pygame.transform.scale(original_image, (
        original_image.get_width() * scale_factor, original_image.get_height() * scale_factor))


mouse_icon = load_image_and_scale(mouse_icon_path)
keyboard_icon = load_image_and_scale(keyboard_icon_path)
app_icon = load_image_and_scale(app_icon_path)

pygame.display.set_icon(app_icon)  # tem que ser antes do while True loop senão ele carrega depois que o jogo começa


def movement():
    if mouse_controls:
        kiwi_rect.x = pygame.mouse.get_pos()[0]
        screen.blit(mouse_icon, icon_pos)

    if not mouse_controls:
        if keys[pygame.K_a]:
            kiwi_rect.x -= 5
        if keys[pygame.K_d]:
            kiwi_rect.x += 5
        screen.blit(keyboard_icon, icon_pos)


while True:
    keys = pygame.key.get_pressed()  # n pergunta pq essa variavel ta aq
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif keys[pygame.K_e]:
            mouse_controls = not mouse_controls
            print(mouse_controls)

    screen.fill("white")
    pygame.draw.rect(screen, ground_color, ground)
    screen.blit(kiwi_surf, (kiwi_rect.x, kiwi_rect.y))

    movement()

    pygame.display.update()
    clock.tick(60)
