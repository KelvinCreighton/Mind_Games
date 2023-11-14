import sys
import pygame
import random
import lib
import sprites

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mind Games")

# Game variables
GRAVITY = 0.04

# Primary colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_C = (0, 128, 255)
ENEMY_C = (255, 128, 0)

# Player setup
player = sprites.Player(WIDTH//2, HEIGHT//2, 50, 50)

# Enemy setup
enemy_count = 4
enemies = []
for i in range(enemy_count):
    enemy = sprites.Enemy(WIDTH + i*500, HEIGHT//2, 50, 50)
    enemy.vx = -7
    enemies.append(enemy)

clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Keydown events
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                player.jump()
        # Keyup events
        elif event.type == pygame.KEYUP:
            pass

    # Clear the screen
    screen.fill(BLACK)


    # PLAYER
    if player.on_ground:
        player.ay = 0
        player.vy = 0
    else:
        player.ay += GRAVITY

    player.update()
    player.draw(screen)
    
    if player.rect.y >= HEIGHT//2:
        player.on_ground = True
        player.rect.y = HEIGHT//2   # Temp solution for ground clipping
    else:
        player.on_ground = False


    # ENEMY
    for enemy in enemies:
        enemy.update()
        enemy.draw(screen)


    # Update game state
    pygame.display.flip()
    clock.tick(60)
