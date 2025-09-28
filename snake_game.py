import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🐍 Snake Game")

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Clock
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 24)

def draw_text(text, size, color, x, y, center=True):
    font_obj = pygame.font.SysFont("Arial", size, bold=True)
    label = font_obj.render(text, True, color)
    rect = label.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(label, rect)

def start_screen():
    while True:
        screen.fill(BLACK)
        draw_text("🐍 Snake Game", 40, GREEN, WIDTH // 2, HEIGHT // 3)
        draw_text("Press SPACE to Start", 30, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Use W A S D to Move", 20, WHITE, WIDTH // 2, HEIGHT // 2 + 40)
        draw_text("Eat red food, avoid hitting walls!", 20, WHITE, WIDTH // 2, HEIGHT // 2 + 70)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", 40, RED, WIDTH // 2, HEIGHT // 3)
        draw_text(f"Final Score: {score}", 30, WHITE, WIDTH // 2, HEIGHT // 2)
        draw_text("Press SPACE to Play Again", 25, GREEN, WIDTH // 2, HEIGHT // 2 + 50)
        draw_text("Press ESC to Quit", 25, WHITE, WIDTH // 2, HEIGHT // 2 + 80)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def game_loop():
    snake = [(100, 100)]
    direction = (CELL_SIZE, 0)  # start moving right
    food = (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
            random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)
    score = 0
    lives = 3

    running = True
    while running:
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Controls (WASD instead of arrows)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and direction != (0, CELL_SIZE):
            direction = (0, -CELL_SIZE)
        elif keys[pygame.K_s] and direction != (0, -CELL_SIZE):
            direction = (0, CELL_SIZE)
        elif keys[pygame.K_a] and direction != (CELL_SIZE, 0):
            direction = (-CELL_SIZE, 0)
        elif keys[pygame.K_d] and direction != (-CELL_SIZE, 0):
            direction = (CELL_SIZE, 0)

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
            new_head[1] < 0 or new_head[1] >= HEIGHT or
            new_head in snake):
            lives -= 1
            if lives == 0:
                return score
            else:
                snake = [(100, 100)]
                direction = (CELL_SIZE, 0)
                continue

        snake.insert(0, new_head)

        # Check food collision
        if new_head == food:
            score += 1
            food = (random.randrange(0, WIDTH // CELL_SIZE) * CELL_SIZE,
                    random.randrange(0, HEIGHT // CELL_SIZE) * CELL_SIZE)
        else:
            snake.pop()

        # Drawing
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0], food[1], CELL_SIZE, CELL_SIZE))

        draw_text(f"Score: {score}", 20, WHITE, 5, 5, center=False)
        draw_text(f"Lives: {lives}", 20, WHITE, WIDTH - 100, 5, center=False)

        pygame.display.flip()

# Main loop
while True:
    start_screen()
    final_score = game_loop()
    game_over_screen(final_score)
