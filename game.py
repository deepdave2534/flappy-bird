import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
FLAP_STRENGTH = -7
PIPE_SPEED = 3
PIPE_GAP = 150
PIPE_FREQUENCY = 1500  # milliseconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')
clock = pygame.time.Clock()

class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 3
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = 30
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.y = self.y

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Pipe:
    def __init__(self):
        self.gap_y = random.randint(200, SCREEN_HEIGHT - 200)
        self.x = SCREEN_WIDTH
        self.width = 50
        self.passed = False
        
        # Create rectangles for collision detection
        self.top_pipe = pygame.Rect(self.x, 0, self.width, self.gap_y - PIPE_GAP // 2)
        self.bottom_pipe = pygame.Rect(self.x, self.gap_y + PIPE_GAP // 2, 
                                     self.width, SCREEN_HEIGHT - (self.gap_y + PIPE_GAP // 2))

    def update(self):
        self.x -= PIPE_SPEED
        self.top_pipe.x = self.x
        self.bottom_pipe.x = self.x

    def draw(self):
        # Draw top pipe
        pygame.draw.rect(screen, GREEN, self.top_pipe)
        # Draw bottom pipe
        pygame.draw.rect(screen, GREEN, self.bottom_pipe)

class Game:
    def __init__(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.last_pipe = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.__init__()
                    else:
                        self.bird.flap()

    def update(self):
        if not self.game_over:
            self.bird.update()
            
            # Generate new pipes
            current_time = pygame.time.get_ticks()
            if current_time - self.last_pipe > PIPE_FREQUENCY:
                self.pipes.append(Pipe())
                self.last_pipe = current_time

            # Update pipes
            for pipe in self.pipes[:]:
                pipe.update()
                
                # Check for score
                if not pipe.passed and pipe.x < self.bird.x:
                    pipe.passed = True
                    self.score += 1

                # Remove pipes that are off screen
                if pipe.x < -pipe.width:
                    self.pipes.remove(pipe)

            # Check for collisions
            if self.bird.y < 0 or self.bird.y > SCREEN_HEIGHT:
                self.game_over = True

            for pipe in self.pipes:
                if (self.bird.rect.colliderect(pipe.top_pipe) or 
                    self.bird.rect.colliderect(pipe.bottom_pipe)):
                    self.game_over = True

    def draw(self):
        screen.fill(BLUE)
        
        # Draw pipes
        for pipe in self.pipes:
            pipe.draw()
        
        # Draw bird
        self.bird.draw()
        
        # Draw score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        if self.game_over:
            game_over_text = self.font.render('Game Over! Press SPACE to restart', True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            screen.blit(game_over_text, text_rect)
        
        pygame.display.flip()

def main():
    game = Game()
    
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == '__main__':
    main()
