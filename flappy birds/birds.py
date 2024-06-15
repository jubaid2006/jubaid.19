import pygame
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Game Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
PIPE_WIDTH = 80
PIPE_HEIGHT = 500
GAP = 150
GRAVITY = 0.5
FLAP_STRENGTH = -8
PIPE_SPEED = 5
CLOUD_SPEED_MIN = 1
CLOUD_SPEED_MAX = 3

# Load images
bird_image = pygame.image.load('bird.png')
pipe_image = pygame.image.load('pipe.png')
cloud_image = pygame.image.load('cloud.png')
hill_image = pygame.image.load('hill.png')

# Resize images
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))
cloud_image = pygame.transform.scale(cloud_image, (100, 60))
hill_image = pygame.transform.scale(hill_image, (300, 100))

# Setup the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load high score
high_score_file = 'highscore.txt'
if os.path.exists(high_score_file):
    with open(high_score_file, 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# Load background music
pygame.mixer.music.load('py music2.mp3')
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely

# Load font
font = pygame.font.SysFont(None, 24)

# Bird class
class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False

    def update(self):
        self.x -= PIPE_SPEED

    def draw(self, screen):
        screen.blit(pipe_image, (self.x, self.height - PIPE_HEIGHT))
        screen.blit(pygame.transform.flip(pipe_image, False, True), (self.x, self.height + GAP))

# Cloud class
class Cloud:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.speed = random.uniform(CLOUD_SPEED_MIN, CLOUD_SPEED_MAX)

    def update(self):
        self.x -= self.speed
        if self.x < -100:
            self.x = SCREEN_WIDTH
            self.y = random.randint(0, SCREEN_HEIGHT // 2)

    def draw(self, screen):
        screen.blit(cloud_image, (self.x, self.y))

# Initialize game variables
def init_game():
    global bird, pipes, clouds, score, game_over
    bird = Bird()
    pipes = [Pipe()]
    clouds = [Cloud() for _ in range(3)]
    score = 0
    game_over = False

# Display the start screen
def show_start_screen():
    start_button_rect = pygame.Rect((SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 25, 100, 50))

    while True:
        screen.fill((135, 206, 235))  # Sky blue background
        title_text = font.render('Flappy Bird', True, (0, 0, 0))
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Draw start button
        pygame.draw.rect(screen, (0, 0, 0), start_button_rect)
        start_text = font.render('Start', True, (255, 255, 255))
        screen.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2, start_button_rect.y + (start_button_rect.height - start_text.get_height()) // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    return

# Main game loop
def main():
    global game_over, score, high_score

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    init_game()

        if not game_over:
            # Update bird, pipes, and clouds
            bird.update()
            for cloud in clouds:
                cloud.update()
            for pipe in pipes:
                pipe.update()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    pipes.append(Pipe())
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    score += 1

            # Check for collisions
            if bird.y + BIRD_HEIGHT >= SCREEN_HEIGHT or bird.y <= 0:
                game_over = True
            for pipe in pipes:
                if bird.x + BIRD_WIDTH > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
                    if bird.y < pipe.height or bird.y + BIRD_HEIGHT > pipe.height + GAP:
                        game_over = True

            # Update high score
            if score > high_score:
                high_score = score
                with open(high_score_file, 'w') as file:
                    file.write(str(high_score))

        # Draw everything
        screen.fill((135, 206, 235))  # Sky blue background
        screen.blit(hill_image, (50, SCREEN_HEIGHT - 100))  # Draw hill
        for cloud in clouds:
            cloud.draw(screen)
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 30))

        # Draw high score
        high_score_text = font.render(f'High Score: {high_score}', True, (0, 0, 0))
        screen.blit(high_score_text, (10, 50))

        # Draw game over screen
        if game_over:
            game_over_text = font.render('Game Over!Press R', True, (255, 0, 0))
            screen.blit(game_over_text, (20, SCREEN_HEIGHT // 2))

        # Draw name
        name_text = font.render('creator: Jubaid', True, (0, 0, 100))
        screen.blit(name_text, (10, 10))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    show_start_screen()
    init_game()
    main()
