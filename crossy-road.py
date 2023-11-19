import pygame
import sys
import random
import sys
import pygame
import random
import sprites

# Initialize Pygame
pygame.init()

#Loading EEG prediction model
from joblib import load

# Load the model
model = load('game/csp_lda_model.joblib')
def EEGtoKeyStroke(eegDataInput):
    csp = model["csp"]
    lda = model["lda"]

    transformed_data = csp.transform(eegDataInput)
    prediction = lda.predict(transformed_data)
    # Convert prediction to keystroke

    if prediction == 0:  #left label
        pygame.KEYLEFT
    elif prediction == 1: #right label
        pygame.KEYRIGHT



# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 40
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
OBSTACLE_WIDTH = 50
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 5

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crossy Road Jump")

# Player variables
player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
player_y = SCREEN_HEIGHT - PLAYER_SIZE * 2
player_velocity = 0
player_jump = False

# Obstacle variables
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - OBSTACLE_HEIGHT * 2
obstacle_passed = True

# Constants for jump
JUMP_FORCE = 14
GRAVITY = 0.6

# Function to create a new obstacle
def create_obstacle():
    global obstacle_x, obstacle_passed
    obstacle_x = SCREEN_WIDTH
    obstacle_passed = False

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not player_jump:
                        player_jump = True
                        player_velocity = -JUMP_FORCE
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Reset game variables
                    game_over = False
                    player_y = SCREEN_HEIGHT - PLAYER_SIZE * 2
                    player_jump = False
                    player_velocity = 0
                    obstacle_passed = True
                    create_obstacle()

    if not game_over:
        # Apply gravity
        if player_jump:
            player_velocity += GRAVITY
            player_y += player_velocity

            if player_y >= SCREEN_HEIGHT - PLAYER_SIZE * 2:
                player_y = SCREEN_HEIGHT - PLAYER_SIZE * 2
                player_jump = False

        # Move obstacle
        obstacle_x -= OBSTACLE_SPEED

        # Check collision with obstacle
        if (
            obstacle_x < player_x + PLAYER_SIZE
            and obstacle_x + OBSTACLE_WIDTH > player_x
            and player_y + PLAYER_SIZE > obstacle_y
        ):
            game_over = True

        # Check if the obstacle has passed
        if obstacle_x + OBSTACLE_WIDTH < 0:
            obstacle_passed = True

        # Create a new obstacle if the previous one passed
        if obstacle_passed:
            create_obstacle()

        # Clear screen
        screen.fill(WHITE)

        # Draw player
        pygame.draw.rect(screen, RED, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

        # Draw obstacle
        pygame.draw.rect(screen, GREEN, (obstacle_x, obstacle_y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

        # Update display
        pygame.display.flip()
        clock.tick(60)  # Limit frame rate

    else:  # Game over screen
        screen.fill(WHITE)
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Move Left Hand to restart", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

# Quit Pygame properly
pygame.quit()
sys.exit()
