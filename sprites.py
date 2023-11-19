import pygame

class Player:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.color = (0, 128, 255)

    def move(self, amount):
        self.y += amount

    def update(self, cam_x, cam_y):
        self.rect.x = self.x + cam_x
        self.rect.y = self.y + cam_y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Enemy:
    def __init__(self, x, y, w, h, speed):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, w, h)
        self.speed = speed
        self.color = (255, 0, 0)

    def update(self, cam_x, cam_y):
        self.rect.x = self.x + cam_x
        self.rect.y = self.y + cam_y
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    
    def move(self):
        self.x += self.speed
    
