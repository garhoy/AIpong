import pygame
from pygame.locals import *
def game_loop():
    global ball_speed_x, ball_speed_y, ball, player_speed, opponent_speed

    ongoing = True
    while ongoing:
        # Handling input
        for event in pygame.event.get():
            if event.type == QUIT:
                ongoing = False
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

        # Ball collision with paddles
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1
        
        # Ball collision with walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
            
        # Check for ball going out of bounds on the left or right
        if ball.left <= 0 or ball.right >= WIDTH:
            ball.center = (WIDTH / 2, HEIGHT / 2)  # Reset ball to center
            ball_speed_x *= -1  # Change direction of ball
            ball_speed_y = 3 * (1 if ball_speed_y > 0 else -1)  # Reset y-speed but maintain direction
            player_speed = 0  # Reset player speed
            opponent_speed = 7  # Reset opponent speed (if needed)

        # Player paddle movement constraints
        if player.top <= 0:
            player.top = 0
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT

        # Opponent paddle AI (basic for now, it just follows the ball)
        if opponent.top < ball.y:
            opponent.top += opponent_speed
        if opponent.bottom > ball.y:
            opponent.bottom -= opponent_speed
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= HEIGHT:
            opponent.bottom = HEIGHT

        # Drawing everything
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        pygame.display.flip()
        # FPS
        pygame.time.Clock().tick(60)




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
    pygame.quit()