import pygame
import sys
import random


# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
DOG = (189,154,130)

class Player:
    def __init__(self):
        self.pos = [300, 300]
        self.radius = 15
        self.speed = 2

    #Player movement using arrow keys
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
        self.pos = [500, 100]
        self.radius = 15
        self.speed = 3
        self.direction_timer = 0
        self.change_direction_delay = 100
        directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
        self.current_direction = random.choice(directions)
        self.previous_y = 0
        self.previous_x = 0
        self.fsm = FSM('RIGHT') #Initialize FSM for AI
        self.init_fsm()
    
    def init_fsm(self):
        self.fsm.add_transition('RECT_COLLISION', 'LEFT', self.collide_left, 'DOWN')
        self.fsm.add_transition('RECT_COLLISION', 'RIGHT', self.collide_right, 'UP')
        self.fsm.add_transition('RECT_COLLISION', 'UP', self.collide_up, 'LEFT')
        self.fsm.add_transition('RECT_COLLISION', 'DOWN', self.collide_down, 'RIGHT')
    
    def get_state(self):
        return self.fsm.current_state

    def update(self):
        # Update FSM based on collision, input is always colliding with rectangle, uses current direction state to determine which new direction state and action
        self.fsm.process('RECT_COLLISION')
        self.previous_y = self.pos[0]
        self.previous_x = self.pos[1]

    def collide_left(self):
        self.pos[0] += 10
        self.current_direction = self.fsm.current_state

    def collide_right(self):
        self.pos[0] -= 10
        self.current_direction = self.fsm.current_state

    def collide_up(self):
        self.pos[1] += 10
        self.current_direction = self.fsm.current_state

    def collide_down(self):
        self.pos[1] -= 10
        self.current_direction = self.fsm.current_state

    #AI random movement, after some time chooses new direction, if AI postion is same as before (stuck in wall) reset it to start position
    def move(self):
        if self.direction_timer <= 0:
            self.direction_timer = self.change_direction_delay
            directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
            self.current_direction = random.choice(directions)
            if self. previous_y == self.pos[0] and self.previous_x == self.pos[1]:
                self.pos[0] = 500
                self.pos[1] = 100    
        else:
            self.direction_timer -= 1

        if self.current_direction == 'UP' and self.pos[1] > self.radius:
            self.pos[1] -= self.speed
        elif self.current_direction == 'DOWN' and self.pos[1] < HEIGHT - 5 - self.radius:
            self.pos[1] += self.speed
        elif self.current_direction == 'LEFT' and self.pos[0] > self.radius:
            self.pos[0] -= self.speed
        elif self.current_direction == 'RIGHT' and self.pos[0] < WIDTH - 5 - self.radius:
            self.pos[0] += self.speed

#FSM class
class FSM:
    def __init__(self, initial_state):
        self.state_transitions = {}
        self.current_state = initial_state

    def add_transition(self, input_symbol, state, action=None, next_state=None):
        if next_state is None:
            self.state_transitions[(input_symbol, state)] = (action, state)
        else:
            self.state_transitions[(input_symbol, state)] = (action, next_state)

    def get_transition(self, input_symbol, state):
        return self.state_transitions[(input_symbol, state)]

    def process(self, input_symbol):
        action, new_state = self.get_transition(input_symbol, self.current_state)
        self.current_state = new_state
        if action is not None:
            action()

class Game:
    def __init__(self):
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dog Game")
        self.clock = pygame.time.Clock()
        self.player = Player()
        self.ai = AI()

        #Paste images onto ai and player objects
        self.player_image = pygame.image.load('pixelMan.png')
        self.player_image = pygame.transform.scale(self.player_image, (self.player.radius * 2, self.player.radius * 2))
        self.ai_image = pygame.image.load('dogName.png')
        self.ai_image = pygame.transform.scale(self.ai_image, (self.ai.radius * 2, self.ai.radius * 2))

        #Obstacle Movement
        self.car_speed = 3
        self.cars = [] 
        for i in range(100, 600, 150,):
            self.cars.append(pygame.Rect(i, i - 20, 30, 30))

        self.walls = [
            pygame.Rect(0, 0, 600, 15),
            pygame.Rect(0, 0, 15, 600),
            pygame.Rect(0, 585, 600, 14),
            pygame.Rect(585, 0, 15, 600),
            pygame.Rect(325, 270, 20, 70),
            pygame.Rect(260, 270, 20, 70),
            pygame.Rect(0, 270, 100, 20),
            pygame.Rect(160, 270, 120, 20),
            pygame.Rect(325, 270, 110, 20),
            pygame.Rect(490, 270, 120, 20),
            pygame.Rect(0, 270, 120, 20), 
            pygame.Rect(65, 65,200, 20),
            pygame.Rect(330, 65, 200, 20),
            pygame.Rect(330, 65, 20, 50),
            pygame.Rect(265, 65, 20, 50),
            pygame.Rect(150, 155, 300, 20),
            pygame.Rect(330, 65, 20, 50),


        ]
        self.grass_color = (124, 252, 0)
        self.wall_color = (169, 169, 169)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True
    
    #Check collision for player and AI
    def check_collisions(self, keys):
        #1 - Check if player has collided with walls
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
        #2 Check if AI has collided with walls, if yes then call update to process FSM
        ai_rect = pygame.Rect(self.ai.pos[0] - self.ai.radius, self.ai.pos[1] - self.ai.radius, self.ai.radius * 2, self.ai.radius * 2)
        for wall in self.walls:
            if ai_rect.colliderect(wall):
                self.ai.update()  # Call AI's update method upon collision with a rectangle
        
        #IF player collides with AI then set true to end game
        if player_rect.colliderect(ai_rect):
            return True

    #Car movement
    def move_cars(self):
        for car in self.cars:
            car.x += self.car_speed
            if car.right > WIDTH: 
                car.left = 0

    def draw_cars(self):
        for car in self.cars:
            pygame.draw.rect(self.win, (255, 0, 0), car)

    def check_car_collision(self):
        player_rect = pygame.Rect(self.player.pos[0] - self.player.radius, self.player.pos[1] - self.player.radius, self.player.radius * 2, self.player.radius * 2)
        
        for car in self.cars:
            if player_rect.colliderect(car):
                return True
        return False

    def end_game(self):
        font = pygame.font.Font(None, 36)
        text = font.render('Game Over', True, (255, 0, 0))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.win.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)

    def run(self):
        running = True
        while running:
            self.win.fill(self.grass_color)

            keys = pygame.key.get_pressed()
            running = self.handle_events()
            self.player.move(keys)
            self.ai.move()
            self.check_collisions(keys)
            self.move_cars()
            self.draw_cars()

            car_collision = self.check_car_collision()  # Check collision with cars
            
            if car_collision:
                self.player.pos[0] = 300
                self.player.pos[1] = 300

            for wall in self.walls:
                pygame.draw.rect(self.win, self.wall_color, wall)

            self.win.blit(self.player_image, (self.player.pos[0] - self.player.radius, self.player.pos[1] - self.player.radius))
            self.win.blit(self.ai_image, (self.ai.pos[0] - self.ai.radius, self.ai.pos[1] - self.ai.radius))

            collision = self.check_collisions(keys)
            if collision:
                running = False
                self.end_game()
            
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

game = Game()
game.run()
