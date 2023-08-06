
class Cloud:

    def __init__(self, y, speed, image):
        self.image = image
        self.rect = self.image.get_rect(topleft=(800, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
