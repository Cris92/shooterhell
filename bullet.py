import pygame

# Colori
WHITE = (255, 255, 255)

# Classe per i proiettili del giocatore
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, color=WHITE,is_danger=False,damage=1):
        super().__init__()
        self.danger=is_danger
        if is_danger:
            img="img/enemy_bullet.png"
        else:
            img="img/ally_bullet.png"
        raw_image = pygame.image.load(img).convert_alpha()
        self.image = pygame.transform.scale(raw_image, (10, 10))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10
        self.damage = damage

    def update(self):
        if self.danger:
            self.rect.y -= self.speed_y
        else:
            self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()
