import pygame
import random


class Cloud:

    def __init__(self, y, speed, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(480, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
