import pygame
import random

# Colori
GREEN = (0, 255, 0)

# Classe per le ricompense
class Reward(pygame.sprite.Sprite):
    def __init__(self, enemy, screen_width, screen_height):
        super().__init__()
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.rewards_mapping = {
            "heal": "img/health_reward.png",
            "power_up": "img/powerup_reward.png",
            "speed_up": "img/speedup_reward.png"
        }  # Mappatura degli effetti alle immagini delle ricompense
        self.effects = list(self.rewards_mapping.keys())  # Lista degli effetti delle ricompense
        self.effect = random.choice(self.effects)  # Effetto casuale della ricompensa
        raw_image = pygame.image.load(self.rewards_mapping[self.effect]).convert_alpha()
        self.image = pygame.transform.scale(raw_image, (50,50))
        self.rect = self.image.get_rect()
        self.rect.centerx = enemy.rect.x
        self.rect.centery = enemy.rect.y
        self.speed_x = enemy.speed_x // 2  # Muoversi nella stessa direzione del nemico ma più lentamente
        self.speed_y = enemy.speed_y // 2
        print(self.rect)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.left < 0 or self.rect.right > self.screen_width or self.rect.top < 0 or self.rect.bottom > self.screen_height:
            self.kill()  # Rimuovi la ricompensa se esce dai limiti dello schermo

    def apply_effect(self, player):
        if self.effect == "heal":
            player.HP += 1  # Incrementa l'HP del giocatore di 1
        elif self.effect == "power_up":
            player.shoot_vel -=0.05
            # Applica l'effetto power-up al giocatore
            pass
        elif self.effect == "speed_up":
            player.speed_up +=0.1
            # Applica l'effetto speed-up al giocatore
            pass

        self.kill()  # Rimuovi la ricompensa dopo aver applicato l'effetto
