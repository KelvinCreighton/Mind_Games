import pygame

class Player:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (0, 128, 255)

        self.on_ground = False

        # Acceleration and Velocity
        self.ax = 0
        self.ay = 0
        self.vx = 0
        self.vy = 0
    
    def jump(self):
        if not self.on_ground:
            return
        self.vy = -10
        self.ay = -0.04
        self.on_ground = False
    
    def update(self):
        self.vx += self.ax
        self.vy += self.ay
        self.rect.x += self.vx
        self.rect.y += self.vy

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
        if not self.in_screen(screen):
            return
        pygame.draw.rect(screen, self.color, self.rect)