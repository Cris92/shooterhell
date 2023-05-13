import pygame
import time
from bullet import Bullet

# Colori
RED = (255, 0, 0)
SCREEN_WIDTH=0
SCREEN_HEIGHT=0
# Classe per il giocatore
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, HP=10):
        super().__init__()
        self.SCREEN_WIDTH=screen_width
        self.SCREEN_HEIGHT=screen_height
        raw_image = pygame.image.load("img/spaceship.png").convert_alpha()
        self.max_hp = 10
        self.HP = HP
        self.super_move_uses=3
        self.image = pygame.transform.scale(raw_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed_x = 0
        self.speed_y = 0
        self.last_hit_time = 0
        self.is_shooting=False
        self.hit_duration = 2  # Durata dell'effetto di colpo (in secondi)
        self.fade_duration = 0.5  # Durata del fading (in secondi)
        self.fade_alpha = 0  # Opacità corrente per il fading
        self.fade_start_time = 0  # Tempo di inizio del fading
        self.last_shot= time.time()
        self.shoot_type=""
        self.shoot_vel=0.5

    def update(self):
        current_time = time.time()
        if self.last_hit_time + self.hit_duration > current_time:
            # Se il personaggio è stato colpito di recente, esegui il fading
            if self.fade_alpha < 255:
                # Calcola l'opacità corrente in base al tempo trascorso
                elapsed_time = current_time - self.fade_start_time
                self.fade_alpha = int((elapsed_time / self.fade_duration) * 255)
                if self.fade_alpha > 255:
                    self.fade_alpha = 255

                # Applica l'opacità all'immagine
                self.image.set_alpha(self.fade_alpha)
        else:
            # Altrimenti, rendilo visibile
            self.image.set_alpha(255)

        self.speed_x = 0
        self.speed_y = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_DOWN]:
            self.speed_y = 5
        if keystate[pygame.K_UP]:
            self.speed_y = -5

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > self.screen_height:
            self.rect.bottom = self.screen_height

    def shoot(self):
        if self.super_move_uses>0 and self.shoot_type == "super_move_laser":
            self.super_move_uses-=1
        elif self.super_move_uses<=0 and self.shoot_type == "super_move_laser":
            return
        bullet = Bullet(self.rect.centerx, self.rect.top, is_danger=False,type = self.shoot_type,screen_height=self.SCREEN_HEIGHT)
        return bullet

    def hit(self, damage):
        current_time = time.time()
        

        if current_time > self.last_hit_time + self.hit_duration:
            self.HP -= damage
            self.last_hit_time = current_time
            self.fade_start_time = current_time
            self.fade_alpha = 0
            return True
        else:
            return False
