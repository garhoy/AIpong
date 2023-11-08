import pygame
from pygame.locals import *

def game_loop():
    global ball_speed_x, ball_speed_y,ball,player_speed,opponent_speed
    while True:
        # Handling input
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    player_speed += 7
                if event.key == K_UP:
                    player_speed -= 7
            if event.type == KEYUP:
                if event.key == K_DOWN:
                    player_speed -= 7
                if event.key == K_UP:
                    player_speed += 7

        ball.x += ball_speed_x
        ball.y += ball_speed_y

        player.y += player_speed

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed_x *= -1

        if player.top <= 0:
            player.top = 0
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT

        # Drawing everything
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        pygame.display.flip()
        # FPS
        pygame.time.Clock().tick(60)

# pygame.quit()


if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()

    # Setting up the display
    WIDTH, HEIGHT = 640, 480
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong")

    # Game variables
    ball_speed_x = 3
    ball_speed_y = 3
    player_speed = 0
    opponent_speed = 7
    ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)
    player = pygame.Rect(WIDTH - 20, HEIGHT / 2 - 70, 10, 140)
    opponent = pygame.Rect(10, HEIGHT / 2 - 70, 10, 140)
    bg_color = pygame.Color('grey12')
    light_grey = (200, 200, 200)


    game_loop()