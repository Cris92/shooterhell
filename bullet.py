import pygame

# Colori
WHITE = (255, 255, 255)

# Classe per i proiettili del giocatore
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, is_danger=False,damage=1,type = "single_bullet",screen_width=0,screen_height=0,owner=None):
        super().__init__()
        self.danger=is_danger
        self.type = type
        self.screen_height=screen_height
        self.screen_width=screen_width
        self.owner=owner
        if is_danger:
            img="img/enemy_bullet.png"
        else:
            img="img/ally_bullet.png"
        if self.type=="single_bullet":
            raw_image = pygame.image.load(img).convert_alpha()
            self.image = pygame.transform.scale(raw_image, (10, 10))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y
            self.speed_y = -10
            self.damage = damage
        elif self.type=="super_move_laser":
            img="img/super_laser.png"
            raw_image = pygame.image.load(img).convert_alpha()
            self.image = pygame.transform.scale(raw_image, (100,self.screen_height))
            self.rect = self.image.get_rect()
            self.rect.centerx = x
            self.rect.bottom = y -self.rect.height
            self.speed_y = 0
            self.damage = damage
            self.frame_duration = 1000
            self.frame_thrown = 0

    def update(self):
        if self.danger:
            self.rect.y -= self.speed_y
            if self.rect.bottom > self.screen_height:
               self.kill()
        else:
            if self.type=="single_bullet":
                self.rect.y += self.speed_y
                if self.rect.bottom < 0:
                    self.kill()
            else:
                self.rect.centerx =self.owner.rect.x
                self.rect.bottom =self.owner.rect.y
                if self.frame_duration==self.frame_thrown:
                    self.kill()
                else:
                    self.frame_thrown+=1
