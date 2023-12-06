import pygame
import sys
import random


#AI move


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (0, 255, 100)

class Player:
    def __init__(self):
        self.pos = [300, 300]
        self.radius = 15
        self.speed = 5

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.pos[0] > self.radius:
            self.pos[0] -= self.speed
        if keys[pygame.K_RIGHT] and self.pos[0] < WIDTH - self.radius:
            self.pos[0] += self.speed
        if keys[pygame.K_UP] and self.pos[1] > self.radius:
            self.pos[1] -= self.speed
        if keys[pygame.K_DOWN] and self.pos[1] < HEIGHT - self.radius:
            self.pos[1] += self.speed

class AI:
    def __init__(self):
        self.pos = [100, 100]
        self.radius = 15
        self.speed = 3
        self.direction_timer = 0
        self.change_direction_delay = 30

    def move(self):
        if self.direction_timer <= 0:
            directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            self.current_direction = random.choice(directions)
            self.direction_timer = self.change_direction_delay  # Reset timer
        else:
            self.direction_timer -= 1

        if self.current_direction == 'UP' and self.pos[1] > self.radius:
            self.pos[1] -= self.speed
        elif self.current_direction == 'DOWN' and self.pos[1] < HEIGHT - self.radius:
            self.pos[1] += self.speed
        elif self.current_direction == 'LEFT' and self.pos[0] > self.radius:
            self.pos[0] -= self.speed
        elif self.current_direction == 'RIGHT' and self.pos[0] < WIDTH - self.radius:
            self.pos[0] += self.speed

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dog Game")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.ai = AI()
        self.walls = [
            pygame.Rect(100, 50, 20, 200),
            pygame.Rect(250, 150, 300, 20),
            pygame.Rect(70, 400, 20, 150),
            pygame.Rect(400, 350, 20, 150),
            pygame.Rect(0, 0, 600, 15),
            pygame.Rect(0, 0, 15, 600),
            pygame.Rect(0, 585, 600, 14),
            pygame.Rect(585, 0, 15, 600)
        ]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    def check_collisions(self, keys):
        player_rect = pygame.Rect(self.player.pos[0] - self.player.radius, self.player.pos[1] - self.player.radius, self.player.radius * 2, self.player.radius * 2)
        for wall in self.walls:
            if player_rect.colliderect(wall):
                if keys[pygame.K_LEFT]:
                    self.player.pos[0] += self.player.speed
                if keys[pygame.K_RIGHT]:
                    self.player.pos[0] -= self.player.speed
                if keys[pygame.K_UP]:
                    self.player.pos[1] += self.player.speed
                if keys[pygame.K_DOWN]:
                    self.player.pos[1] -= self.player.speed
        
        ai_rect = pygame.Rect(self.ai.pos[0] - self.ai.radius, self.ai.pos[1] - self.ai.radius, self.ai.radius * 2, self.ai.radius * 2)
        for wall in self.walls:
            if ai_rect.colliderect(wall):
                if self.ai.current_direction == 'LEFT':
                    self.ai.pos[0] += 2 * self.ai.speed
                if self.ai.current_direction == 'RIGHT':
                    self.ai.pos[0] -=  2 * self.ai.speed
                if self.ai.current_direction == 'UP':
                    self.ai.pos[1] +=  2 * self.ai.speed
                if self.ai.current_direction == 'DOWN':
                    self.ai.pos[1] -= 2 *  self.ai.speed

    def run(self):
        running = True
        while running:
            self.win.fill(BLACK)

            keys = pygame.key.get_pressed()
            running = self.handle_events()
            self.player.move(keys)
            self.ai.move()
            self.check_collisions(keys)

            for wall in self.walls:
                pygame.draw.rect(self.win, WHITE, wall)
            
            pygame.draw.circle(self.win, YELLOW, self.player.pos, self.player.radius)
            pygame.draw.circle(self.win, RED, self.ai.pos, self.ai.radius)
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

game = Game()
game.run()