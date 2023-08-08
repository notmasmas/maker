
class Heart:
    def __init__(self, x, speed, image):
        self.image = image
        self.rect = self.image.get_rect(midtop=(x, -200))
        self.speed = speed

    def update(self):
        self.rect.y += self.speed
