import pygame
import time
from enemies import Enemy
from player import Player
import random
import reward


def update_game(game, events):

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        elif event.type == pygame.KEYDOWN:
            if game.player.is_dead() == False:
                if event.key == pygame.K_SPACE:
                    game.player.is_shooting = True
                    game.player.shoot_type = "single_bullet"
                if event.key == pygame.K_LCTRL:
                    game.player.is_shooting = True
                    game.player.is_shooting_super = True
                    game.player.shoot_type = "super_move_laser"
                elif event.key == pygame.K_ESCAPE:
                    if not game.paused:
                        open_pause_menu(game)
                    else:
                        resume_game(game)
        elif event.type == pygame.KEYUP:
            if game.player.is_dead() == False:
                if event.key == pygame.K_SPACE or event.key == pygame.K_LCTRL:
                    game.player.is_shooting = False

    game.all_sprites.update()

    after_death_frame=10
    actual_after_death_frame=0

    # Fuoco continuo se il tasto spazio è premuto
    if game.player.is_shooting:
        if time.time()-game.player.last_shot > game.player.shoot_vel:
            bullet = game.player.shoot()
            if bullet is not None:
                game.all_sprites.add(bullet)
                game.ally_bullets.add(bullet)
                game.player.last_shot=time.time()


    # Collisioni tra proiettili e nemici
    hits = pygame.sprite.groupcollide(game.enemies, game.ally_bullets, False, False)
    for enemy,bullets in hits.items():
        if enemy.rect.x>=0 and enemy.rect.y>=0:
            enemy.is_hit=True
            game.score += 1
        for bullet in bullets:
            if bullet.type=="single_bullet":
                bullet.kill()            
        
    
    # Collisioni tra proiettili e proiettili amici
    hits = pygame.sprite.groupcollide(game.enemy_bullets, game.ally_bullets, True, False)
    for e_bullet,a_bullets in hits.items():
        for a_bullet in a_bullets:
            if a_bullet.type=="single_bullet":
                a_bullet.kill()

    # Collisioni tra giocatore e nemici
    hits = pygame.sprite.spritecollide(game.player, game.enemies, False)
    if hits:
        for hit_enemy in hits:
            #Gestione del nemico
            if hit_enemy.rect.x>=0 and hit_enemy.rect.y>=0:
                hit_enemy.is_hit=True
                game.score += 1
            #Gestione del player
            hit_done=game.player.hit(hit_enemy.damage)
            if hit_done:
                shake_screen(game,10, 0.2)
    
    # Collisioni tra giocatore e reward
    hits = pygame.sprite.spritecollide(game.player, game.rewards, False)
    if hits:
        for reward in hits:
           reward.apply_effect(game.player)

    # Collisioni tra giocatore e proiettili nemici
    hits = pygame.sprite.spritecollide(game.player, game.enemy_bullets, False)
    if hits:
        for hit_bullet in hits:
            hit_done=game.player.hit(hit_bullet.damage)
            if hit_done:
                shake_screen(game,10, 0.2)

    game.screen.blit(game.background_image, (0, 0))
    game.all_sprites.draw(game.screen)
    game.ui.show_score(game.screen, game.score)
    game.ui.show_health_bar(game.screen, game.player)
    game.ui.show_super_bar(game.screen, game.player)
    pygame.display.flip()

def open_main_menu(game):
    game.game_main_menu.enable()
    game.game_main_menu.mainloop(game.screen)

def open_pause_menu(game):
    game.paused = True
    game.pause_over_menu.enable()
    game.pause_over_menu.mainloop(game.screen)

def resume_game(game):
    game.paused = False
    game.game_over_menu.disable()

def restart_game(game, widget=None):
    game.all_sprites.empty()
    game.enemies.empty()
    game.ally_bullets.empty()
    game.enemy_bullets.empty()
    game.player = Player(game.WIDTH, game.HEIGHT,HP=10)
    game.player.HP = game.player.max_hp
    game.all_sprites.add(game.player)
    game.game_over = False
    game.score = 0

    for _ in range(8):
        enemy = Enemy(game.WIDTH, game.HEIGHT, game.all_sprites, game.enemy_bullets)
        game.all_sprites.add(enemy)
        game.enemies.add(enemy)

    game.paused = False
    game.game_over_menu.disable()


def quit_game(game):
        pygame.quit()
        quit()

def shake_screen(game, intensity, duration):
    original_pos = game.screen.get_rect().topleft
    shake_start_time = time.time()

    while time.time() - shake_start_time < duration:
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)

        temp_surface = pygame.Surface(game.screen.get_size())
        temp_surface.blit(game.background_image, (0, 0))

        for sprite in game.all_sprites:
            sprite_rect = sprite.rect.copy()
            sprite_rect.x += offset_x
            sprite_rect.y += offset_y
            temp_surface.blit(sprite.image, sprite_rect)

        game.screen.blit(temp_surface, (0, 0))
        pygame.display.flip()


def handle_quit_event(game):
    if game.paused:
        game.game_over_menu.disable()
        game.paused = False
    else:
        pygame.event.post(pygame.event.Event(pygame.QUIT))

def save_highscore(score):
    with open('highscores.txt', 'a') as file:
        file.write(str(score) + '\n')

def load_highscores():
    highscores = []
    with open('highscores.txt', 'r') as file:
        for line in file:
            highscores.append(int(line.strip()))
    return highscores