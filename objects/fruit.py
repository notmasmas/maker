import pygame


def scale_image(image_path, scale_factor):
    original_image = pygame.image.load(image_path)
    return pygame.transform.scale(original_image, (
        original_image.get_width() * scale_factor, original_image.get_height() * scale_factor))


class Fruit:
    kiwi = "graphics/fruit_kiwi.png"
    banana = "graphics/fruit_banana.png"
    orange = "graphics/fruit_orange.png"

    def __init__(self, x, speed, type):
        self.image = self.get_image_by_type(type)
        self.rect = self.image.get_rect(midtop=(x, -200))
        self.type = type
        self.speed = speed
        self.alpha = 255

    def update(self):
        self.rect.y += self.speed

    def death(self):
        self.alpha -= 50
        self.image.set_alpha(self.alpha)

    def is_done(self):
        return self.alpha <= 0

    def get_image_by_type(self, fruit_type):
        if fruit_type == 1:
            return scale_image(self.kiwi, 1)
        elif fruit_type == 2:
            return scale_image(self.banana, 3)
        elif fruit_type == 3:
            return scale_image(self.orange, 3)
