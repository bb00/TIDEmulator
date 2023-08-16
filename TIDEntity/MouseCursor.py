from pygame import sprite, Surface, draw, SRCALPHA

class MouseCursor(sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = Surface([400, 400], SRCALPHA, 32)
        self.rect = self.image.get_rect(center=(0,0))
        self.radius = 10
    def update(self, position):
        self.image.fill((0,0,0,0))
        draw.circle(self.image, (0, 255, 0), (200,200), 10, 1)
        self.rect.center = position
