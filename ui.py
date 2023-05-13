import pygame

# Colori
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Classe per l'interfaccia utente
class UI:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 28)

    def show_score(self, screen, score):
        score_text = self.font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))

    def show_health_bar(self, screen, player):
        health_bar_width = 200
        health = player.HP
        max_health = player.max_hp
        health_percentage = health / max_health
        font = pygame.font.Font(None, 20)
        text = font.render("Health:", True, (255, 255, 255))
        screen.blit(text, (10, 40))
        bar_rect = pygame.Rect(60, 40, health_bar_width, 10)
        pygame.draw.rect(screen, BLACK, bar_rect)
        
        fill_width = health_percentage * health_bar_width
        fill_rect = pygame.Rect(60, 40, fill_width, 10)

        if health_percentage > 0.5:
            fill_color = GREEN
        else:
            fill_color = RED

        pygame.draw.rect(screen, fill_color, fill_rect)
    
    def show_super_bar(self,screen,player):
        font = pygame.font.Font(None, 20)
        text = font.render("Super:", True, (255, 255, 255))
        screen.blit(text, (10, 80))
        bar_width = int(player.last_frame_super / player.frame_for_super * 100)
        bar_rect = pygame.Rect(60, 80, 100, 10)
        pygame.draw.rect(screen, BLACK, bar_rect)
        pygame.draw.rect(screen, (0, 255, 0), (60, 80, bar_width, 10))


