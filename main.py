import sys
import pygame
import random
import lib

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mind Games")

# Primary colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PLAYER_C = (0, 128, 255)
ENEMY_C = (255, 128, 0)

# Player setup
player_size = 50
player_x = (WIDTH - player_size) // 2
player_y = HEIGHT // 2
player_rect = pygame.Rect(player_x, player_y, player_size, player_size)

# Enemy setup
enemy_size = 50
enemy_speed = 3
enemy_count = 4
enemies = []
for i in range(enemy_count):
    enemy_x = WIDTH + i*500
    enemy_y = HEIGHT // 2
    enemy_rect = pygame.Rect(enemy_x, enemy_y, enemy_size, enemy_size)
    enemies.append(enemy_rect)

clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Keydown events
        elif event.type == pygame.KEYDOWN:
            pass
        # Keyup events
        elif event.type == pygame.KEYUP:
            pass

    # Clear the screen
    screen.fill(BLACK)

    # PLAYER
    pygame.draw.rect(screen, PLAYER_C, player_rect)

    # ENEMY
    for enemy in enemies:
        enemy.x -= enemy_speed
        if lib.in_screen(screen, enemy):
            pygame.draw.rect(screen, ENEMY_C, enemy)

    # Update game state
    pygame.display.flip()
    clock.tick(60)
