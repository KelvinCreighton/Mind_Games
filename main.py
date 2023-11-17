import sys
import pygame
import random
import lib
import sprites

pygame.init()

#Set Screen Size
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#Set Screen Title
pygame.display.set_caption("Mind Games")

#Colors
white = (255, 255, 255)
black = (0, 0, 0)
player = (27, 250, 2)
key = (255, 225, 0)
goal = (255, 0, 0)

#Maze Pattern 1:Wall, 0:Path, 2:key, 3:player, 4:exit
MAZE = [
    [1, 1, 1, 1, 1, 4, 1, 3, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Define the block size
BLOCK_SIZE = HEIGHT // len(MAZE)

#Draw maze
def draw_maze(maze):
    for row_index, row in enumerate(maze):
        for col_index, item in enumerate(row):
            rect_x = col_index * BLOCK_SIZE
            rect_y = row_index * BLOCK_SIZE

            if item == 1:
                pygame.draw.rect(screen, black, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))
            if item == 0:
                pygame.draw.rect(screen, white, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))
            if item == 2:
                pygame.draw.rect(screen, key, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))
            if item == 3:
                pygame.draw.rect(screen, player, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))
            if item == 4:
                pygame.draw.rect(screen, goal, (rect_x, rect_y, BLOCK_SIZE, BLOCK_SIZE))

# Starting player position
player_x, player_y = 7, 0

#key position
key_x, key_y = 1, 12

# Function to handle player movement
def move_player(key, player_x, player_y):
    new_x, new_y = player_x, player_y

    if key == pygame.K_UP and MAZE[player_y - 1][player_x] != 1:
        new_y -= 1
    elif key == pygame.K_DOWN and MAZE[player_y + 1][player_x] != 1:
        new_y += 1
    elif key == pygame.K_LEFT and MAZE[player_y][player_x - 1] != 1:
        new_x -= 1
    elif key == pygame.K_RIGHT and MAZE[player_y][player_x + 1] != 1:
        new_x += 1

    return new_x, new_y

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            new_x, new_y = move_player(event.key, player_x, player_y)

            # Clear the old position and update the new position
            if (new_x, new_y) != (player_x, player_y):
                MAZE[player_y][player_x] = 0  # Clear old position
                player_x, player_y = new_x, new_y
                MAZE[player_y][player_x] = 3  # Set new position

    # Draw the maze
    screen.fill(white)  # Clear screen
    draw_maze(MAZE)
    pygame.display.flip()

    # Optional: control the frame rate
    pygame.time.delay(100)

pygame.quit()