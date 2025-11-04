import pygame
import sys
import time

pygame.init()

# Screen
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple One-Player Pong")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Font
font = pygame.font.SysFont(None, 48)

# Ball
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_radius = 10
ball_dx, ball_dy = 2, 2

# Paddle
paddle_width, paddle_height = 80, 10
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 30
paddle_speed = 5

clock = pygame.time.Clock()
game_over = False

while True:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT]:
            paddle_x += paddle_speed

        # Keep paddle on screen
        paddle_x = max(0, min(WIDTH - paddle_width, paddle_x))

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Bounce off walls
        if ball_x - ball_radius <= 0 or ball_x + ball_radius >= WIDTH:
            ball_dx = -ball_dx
        if ball_y - ball_radius <= 0:
            ball_dy = -ball_dy

        # Bounce off paddle
        if (paddle_y <= ball_y + ball_radius <= paddle_y + paddle_height and
                paddle_x <= ball_x <= paddle_x + paddle_width):
            ball_dy = -ball_dy

        # Game over condition
        if ball_y - ball_radius > HEIGHT:
            game_over = True
            game_over_time = time.time()

    else:
        # Display game over text
        text = font.render("Game Over", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 24))

        # Wait 3 seconds, then quit
        if time.time() - game_over_time > 3:
            pygame.quit()
            sys.exit()

    # Draw ball and paddle (only if not game over)
    if not game_over:
        pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)
        pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    pygame.display.flip()
    clock.tick(60)
