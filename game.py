import pygame
import pygame_menu
import random
from player import Player
from enemies import Enemy
from bullet import Bullet
from ui import UI
from game_logic import update_game
from game_logic import open_main_menu

# Dimensioni della finestra di gioco
WIDTH = 800
HEIGHT = 600

# Inizializzazione di Pygame
pygame.init()

# Classe per il gioco
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Bullet Hell")
        self.clock = pygame.time.Clock()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.ally_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()

        self.player = Player(WIDTH, HEIGHT,10)
        self.all_sprites.add(self.player)

        self.ui = UI(WIDTH, HEIGHT)

        self.background_image = pygame.image.load("img/Background.png")

        # Generazione iniziale di nemici
        for _ in range(8):
            enemy = Enemy(WIDTH, HEIGHT, self.all_sprites, self.enemy_bullets)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        # Variabili di stato del gioco
        self.game_over = False
        self.paused = False
        self.score = 0

        # Creazione del menu di Game Over
        self.game_over_menu = pygame_menu.Menu(width=400, height=600, title='Game Over', theme=pygame_menu.themes.THEME_BLUE)
        self.game_over_menu.add.button('Restart', self.restart_game)
        self.game_over_menu.add.button('Quit', self.quit_game)

        self.pause_over_menu = pygame_menu.Menu(width=400, height=600, title='Pause', theme=pygame_menu.themes.THEME_BLUE)
        self.pause_over_menu.add.button('Resume', self.resume_game)
        self.pause_over_menu.add.button('Quit', self.quit_game)

    # Creazione del menu iniziale
        self.main_menu = pygame_menu.Menu(
            width=400, height=600, title='Main Menu', theme=pygame_menu.themes.THEME_BLUE
        )
        self.main_menu.add.button('New Game', self.start_game)
        #self.main_menu.add.button('High Scores', self.show_high_scores)
        self.main_menu.add.button('Quit', self.quit_game)
        self.main_menu.set_onclose(self.handle_quit_event)

        self.main_menu.mainloop(self.screen)
    def open_main_menu_start(self):
        open_main_menu(self)

    def start_game(self):
        self.run()

    def run(self):
        while True:
            events = pygame.event.get()
            update_game(self, events)
            self.clock.tick(60)

    def restart_game(self, widget=None):
        self.all_sprites.empty()
        self.enemies.empty()
        self.ally_bullets.empty()
        self.enemy_bullets.empty()
        self.player = Player(self.WIDTH, self.HEIGHT)
        self.all_sprites.add(self.player)
        self.game_over = False
        self.score = 0

        for _ in range(8):
            enemy = Enemy(self.WIDTH, self.HEIGHT, self.all_sprites, self.enemy_bullets)
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

        self.game_over_menu.disable()

    def quit_game(self):
        pygame.quit()
        quit()

    def handle_quit_event(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def resume_game(self):
        self.paused = False
        self.pause_over_menu.disable()
