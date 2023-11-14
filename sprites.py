import pygame

class Player:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 128, 255)
        self.velocity_y = 0
    
    def update(self):
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Enemy:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (255, 0, 32)
        self.vx = 0
        self.vy = 0
    
    def in_screen(self, screen):
        screen_width, screen_height = screen.get_size()
        return 0 <= self.rect.left < screen_width and 0 <= self.rect.top < screen_height and \
           0 <= self.rect.right <= screen_width and 0 <= self.rect.bottom <= screen_height
    
    def update(self):
        self.rect.x += self.vx
        self.rect.y += self.vy

    def draw(self, screen):
        if self.in_screen(screen):
            pygame.draw.rect(screen, self.color, self.rect)