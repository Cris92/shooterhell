import pygame
import random
from bullet import Bullet
from reward import Reward

# Colori
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Classe per i nemici
class Enemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game=game
        raw_image = pygame.image.load("img/enemy1.png").convert_alpha()
        self.image = pygame.transform.scale(raw_image, (50, 50))
        self.rect = self.image.get_rect()
        self.screen_width = game.WIDTH  # Salva le dimensioni della finestra di gioco come attributi
        self.screen_height = game.HEIGHT
        self.rect.x = random.randint(0, game.WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)
        self.speed_x = random.randint(-2, 2)
        self.shoot_delay = 120  # Ritardo tra i colpi dei nemici
        self.last_shot = pygame.time.get_ticks()
        self.all_sprites = game.all_sprites  # Salva la variabile all_sprites
        self.enemy_bullets = game.enemy_bullets
        self.damage=3
        self.explosion_frames = []
        self.is_hit = False
        self.frame_counter = 0
        self.frame_delay = 5  
        self.stop_movement = False
        for i in range(1,7):
            raw_image = pygame.image.load(f"img/explosion/explosion ({i}).png").convert_alpha()
            image=pygame.transform.scale(raw_image,(50,50))
            self.explosion_frames.append(image)

    def update(self):
        if self.is_hit:
            self.game.enemies.remove(self)
            self.stop_movement = True
            if len(self.explosion_frames) >0:
                if self.frame_counter>= self.frame_delay:
                    self.image=self.explosion_frames.pop(0)
                    self.frame_counter=0
                else:
                    self.frame_counter+=1
            else:
                if self.rect.x>=0 and self.rect.y>=0:
                    enemy = Enemy(self.game)
                    self.game.all_sprites.add(enemy)
                    self.game.enemies.add(enemy)
                    # Dentro il ciclo principale del gioco, quando uccidi un nemico
                    if random.randint(1, 3) == 1:
                        reward = Reward(self, self.game.WIDTH, self.game.HEIGHT)
                        self.game.rewards.add(reward)
                        self.game.all_sprites.add(reward)
                    self.kill()
                
        if self.stop_movement == False:
            choice = random.randint(1,30)
            if choice ==3:
                self.speed_x=-self.speed_x
            self.rect.y += self.speed_y
            self.rect.x += self.speed_x
            if self.rect.top > self.screen_height + 10 or self.rect.left < -self.rect.width or self.rect.right > self.screen_width + self.rect.width:
                self.rect.y = random.randint(-100, -40)
                self.speed_y = random.randint(1, 3)
                self.rect.x = random.randint(0, self.screen_width - self.rect.width)
                self.speed_x = random.randint(-2, 2)
            if self.rect.right > self.screen_width or self.rect.left < 0:
                self.speed_x=-self.speed_x
                
            self.shoot()

    
    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now

            # Estrai casualmente un numero dalla lista [1, 2, 3, 4]
            choice = random.randint(1, 6)
            if choice == 3:
                bullet = Bullet(self.rect.centerx, self.rect.bottom, YELLOW,True,screen_height=self.screen_height,screen_width=self.screen_width)  # Creazione del proiettile dei nemici
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)  # Aggiungi il proiettile alla variabile all_sprites

    