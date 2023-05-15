import pygame
import time
from bullet import Bullet
# Colori
RED = (255, 0, 0)

# Classe per il giocatore
class Player(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, MAX_HP=1,game=None):
        super().__init__()
        self.SCREEN_WIDTH=screen_width
        self.SCREEN_HEIGHT=screen_height
        raw_image = pygame.image.load("img/spaceship.png").convert_alpha()
        self.max_hp = MAX_HP
        self.HP = self.max_hp
        self.super_move_uses=1
        self.image = pygame.transform.scale(raw_image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.speed_up=1
        self.speed_x = 0 * self.speed_up
        self.speed_y = 0 * self.speed_up
        self.last_hit_time = 0
        self.is_shooting=False
        self.hit_duration = 2  # Durata dell'effetto di colpo (in secondi)
        self.fade_duration = 0.5  # Durata del fading (in secondi)
        self.frame_for_super = 500
        self.last_frame_super = 0
        self.fade_alpha = 0  # Opacità corrente per il fading
        self.fade_start_time = 0  # Tempo di inizio del fading
        self.last_shot= time.time()
        self.super_to_charge=True
        self.shoot_type=""
        self.shoot_vel=0.5
        self.explosion_frames = []
        self.is_hit = False
        self.frame_counter = 0
        self.frame_delay = 10  
        self.explosion_frames=[]
        self.game=game
        for i in range(1,7):
            raw_image = pygame.image.load(f"img/explosion/explosion ({i}).png").convert_alpha()
            image=pygame.transform.scale(raw_image,(50,50))
            self.explosion_frames.append(image)

    def update(self):
        if self.is_dead():
            self.explode()
            return

        if self.last_frame_super!=self.frame_for_super:
            self.last_frame_super+=1
        else:
            if self.super_to_charge:
                self.super_move_uses+=1
                self.super_to_charge=False
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
        if not self.is_dead():
            if keystate[pygame.K_LEFT]:
                self.speed_x = -5
            if keystate[pygame.K_RIGHT]:
                self.speed_x = 5
            if keystate[pygame.K_DOWN]:
                self.speed_y = 5
            if keystate[pygame.K_UP]:
                self.speed_y = -5

        self.rect.x += self.speed_x *self.speed_up
        self.rect.y += self.speed_y *self.speed_up

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
            self.last_frame_super=0
            self.super_to_charge=True
        elif self.super_move_uses<=0 and self.shoot_type == "super_move_laser":
            return
        bullet = Bullet(self.rect.centerx, self.rect.top, is_danger=False,type = self.shoot_type,screen_width=self.screen_width,screen_height=self.screen_height,owner=self)
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
    
    def is_dead(self):
        if self.HP <= 0:
            return True
        else:
            return False
        
    def explode(self):
        if self.frame_counter < len(self.explosion_frames) * self.frame_delay:
            self.image = self.explosion_frames[self.frame_counter // self.frame_delay]
            self.frame_counter += 1
        else:
            self.kill()
            self.open_game_over_menu(self.game)
        
    def open_game_over_menu(self,game):
        game.paused = True
        game.game_over_menu.enable()
        game.game_over_menu.mainloop(game.screen)

