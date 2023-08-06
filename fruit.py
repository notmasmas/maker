import pygame


class Fruit:

    kiwi = pygame.image.load("graphics/fruit_kiwi.png")

    def __init__(self, x, speed, type):
        self.image = self.get_image_by_type(type)
        self.type = type
        self.rect = self.image.get_rect(midtop=(x, -200))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed

    def get_image_by_type(self, fruit_type):
        if fruit_type == 1:
            return self.kiwi
        elif fruit_type == 2:
            return self.kiwi
        elif fruit_type == 3:
            return self.kiwi
