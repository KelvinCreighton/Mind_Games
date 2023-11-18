import sys
import pygame
import random
import sprites

# For dev
USING_ARDUINO = False

if USING_ARDUINO:
    import arduino_data

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Arduino Crossy Road")

# Primary colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Camera
cam_x = 0
cam_y = 0

# Player setup
player = sprites.Player(WIDTH//2, HEIGHT//2, 25, 25)

# Enemy setup
enemies = []


clock = pygame.time.Clock()


while True:
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Keydown events
        elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE and not USING_ARDUINO:
                player.move(-25)
        # Keyup events
        elif event.type == pygame.KEYUP:
            pass

    
    if USING_ARDUINO:
        player_input_data = arduino_data.getdata()
        if not player_input_data:
            continue
        if not player_input_data[0]:
            continue
        if not player_input_data[1]:
            continue
        if not len(player_input_data) == 2:
            continue

        
    # Clear the screen
    screen.fill(BLACK)

    # Camera control
    cam_y += 1

    # Spawn enemies
    enemy_spawn_rate = 1
    enemy_count_limit = 25  # Match with the camera y to align it to a grid and prevent weird overlap
    for i in range(random.randint(1, enemy_spawn_rate)):
        if cam_y%enemy_count_limit == 0:
            rand_dir = random.randint(0, 1)
            size = enemy_count_limit
            x = -50
            if rand_dir == 1:
                x = WIDTH+50
            # Align y to a grid
            grid_height = enemy_count_limit
            grid_height_count = HEIGHT/grid_height
            y = random.randint(0, grid_height_count)*grid_height - cam_y
            speed = random.randint(1, 5)
            if rand_dir == 1:
                speed *= -1
            enemy = sprites.Enemy(x, y, size, size, speed)
            enemies.append(enemy)
    
    if USING_ARDUINO:
        print(player_input_data)
        
        if float(player_input_data[0]) > 0:
            player.move(-25)
    
    for enemy in enemies:
        enemy.move()
        enemy.update(cam_x, cam_y)
        enemy.draw(screen)

    player.update(cam_x, cam_y)
    player.draw(screen)


    # Update game state
    pygame.display.flip()
    clock.tick(60)
