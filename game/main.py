import sys
import pygame
import random
import sprites
import serial
import threading
import winsound


#Loading EEG prediction model
from joblib import load

# Load the model
model = load('csp_lda_model.joblib')
def EEGtoKeyStroke(eegDataInput):
    csp = model["csp"]
    lda = model["lda"]

    transformed_data = csp.transform(eegDataInput)
    prediction = lda.predict(transformed_data)
    # Convert prediction to keystroke

    if prediction == 0:  #left label
        #code to move sprite down
        return
    elif prediction == 1: #right label
        # code to move sprite up
        return


# Dev testing
ARDUINO_MODE = False

ser = ''
if ARDUINO_MODE:
    arduino_port = 'COM3'
    baud_rate = 115200
    ser = serial.Serial(arduino_port, baud_rate, timeout=1)
    breaking_case = False
sig1 = 0
sig2 = 0

def arduino_data():
# This function is going to keep running and fetch data from the arduino
    global sig1, sig2
    while not breaking_case:
        received = False
        while not received:
            try:
                ser_out = ser.readline().decode().strip().split(',')
                if not len(ser_out) == 2:
                    continue
                else:
                    received = True
                    sig1 = float(ser_out[0])
                    sig2 = float(ser_out[1])
            except Exception as e:  
                sig1 = 0
                sig2 = 0
                continue

if ARDUINO_MODE:
    arduino_data_thread = threading.Thread(target=arduino_data, daemon=True)
    arduino_data_thread.start()

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

game_score = 0
score_counter = 0

# Player setup
player_1 = sprites.Player(WIDTH//2-100, HEIGHT//2, 25, 25)
player_2 = sprites.Player(WIDTH//2+100, HEIGHT//2, 25, 25)

# Enemy setup
enemies = []
clock = pygame.time.Clock()

bg_music = pygame.mixer.music.load("game_music.wav")
pygame.mixer.music.play(-1)

hit_sound = pygame.mixer.Sound("game_over.wav")

def exit_code():
    print('='*24)
    print("Quitting py game")
    if ARDUINO_MODE:
        ser.close()
    print("closing serial connection")
    print("Exiting...")
    sys.exit()


def end_game():
    print('='*24)
    if player_1.lives > 0:
        print("PLAYER ONE WON!")
    else:
        print("PLAYER TWO WON!")
    print("Game score: ", game_score)
    exit_code()

while True:
    #print(f"left: {sig1}, right: {sig2}")
    for event in pygame.event.get():
        # Exit game
        if event.type == pygame.QUIT:
            pygame.quit()
            exit_code()
            
        elif event.type == pygame.KEYDOWN and not ARDUINO_MODE:
            if event.key == pygame.K_UP:
                player_1.move_y(-25)
            if event.key == pygame.K_DOWN:
                player_1.move_y(25)
            if event.key == pygame.K_w:
                player_2.move_y(-25)
            if event.key == pygame.K_s:
                player_2.move_y(25)
               
    if ARDUINO_MODE:
      player_speed = 25
      if cam_y%10 == 0:
          #Sig1 up sig2 down
          #if sig1 > 0 and sig2 > 0:
          #    print("forward")
          #   player_1.move_y(-player_speed)
          if sig1 > 0:
              print("up")
              player_1.move_y(-player_speed)
          elif sig2 > 0:
              print("down")
              player_1.move_y(player_speed)

        
    # Clear the screen
    screen.fill(BLACK)

    # Camera control
    cam_y += 1


    score_counter += 1
    if score_counter%10 == 0:
        game_score += 1

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
    
    
    # Update all enemies
    for enemy in enemies:
        enemy.move()
        enemy.update(cam_x, cam_y)
        enemy.draw(screen)

        if enemy.off_screen(HEIGHT):
            enemies.remove(enemy)
        # Check collision between players and enemies
        if player_1.collides_with(enemy):
            hit_sound.play()
            player_1.lives -= 1
            enemies.remove(enemy)
        if player_2.collides_with(enemy):
            hit_sound.play()
            player_2.lives -= 1
            enemies.remove(enemy)

    # Update all players (2)
    player_1.update(cam_x, cam_y)
    player_2.update(cam_x, cam_y)
    player_1.draw(screen)
    player_2.draw(screen)
    
    if player_1.out_of_bounds(WIDTH, HEIGHT):
        player_1.lives = 0
    if player_2.out_of_bounds(WIDTH, HEIGHT):
        player_2.lives = 0

    #print(player_1.lives, player_2.lives)
    if player_1.lives == 0 or player_2.lives == 0:
        pygame.quit()
        end_game()

    
    print("P1: "+str(player_1.lives) + "  P2: "+str(player_2.lives) + "  score: "+str(game_score))

    # Update game state
    pygame.display.flip()
    clock.tick(60)
