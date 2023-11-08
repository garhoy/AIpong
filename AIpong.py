import pygame
import random
import numpy as np
from pygame.locals import *

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong con Q-learning")

# Colores
WHITE = (255, 255, 255)

# Parámetros de Q-learning
LEARNING_RATE = 0.001
DISCOUNT_FACTOR = 0.99
EXPLORATION_RATE = 1.0
EXPLORATION_DECAY = 0.995
EXPLORATION_MIN = 0.01

# Inicialización de la tabla Q
q_table = {}

# Funciones de Q-learning
def get_state(ball, player):
    # Discretiza la posición y el movimiento de la bola y la posición de la paleta
    ball_x = discretize(ball.x, WIDTH)
    ball_y = discretize(ball.y, HEIGHT)
    player_y = discretize(player.y, HEIGHT)
    return (ball_x, ball_y, player_y, ball_speed_x, ball_speed_y)

def discretize(value, max_value, num_buckets=10):
    bucket_size = max_value // num_buckets
    discrete_value = value // bucket_size
    return min(discrete_value, num_buckets - 1)

def choose_action(state):
    global EXPLORATION_RATE
    if random.random() < EXPLORATION_RATE:
        return random.choice(['up', 'down', 'stay'])
    else:
        if state not in q_table:
            q_table[state] = [0, 0, 0]
        return ['up', 'down', 'stay'][np.argmax(q_table[state])]

def learn(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = [0, 0, 0]
    if next_state not in q_table:
        q_table[next_state] = [0, 0, 0]
    
    old_value = q_table[state][action]
    next_max = np.max(q_table[next_state])
    
    new_value = (1 - LEARNING_RATE) * old_value + LEARNING_RATE * (reward + DISCOUNT_FACTOR * next_max)
    q_table[state][action] = new_value

def update_exploration_rate():
    global EXPLORATION_RATE
    if EXPLORATION_RATE > EXPLORATION_MIN:
        EXPLORATION_RATE *= EXPLORATION_DECAY

# Mapeo de acciones a índices
action_to_index = {'up': 0, 'down': 1, 'stay': 2}

# Inicialización de objetos del juego
ball = pygame.Rect(WIDTH / 2 - 15, HEIGHT / 2 - 15, 30, 30)
player = pygame.Rect(WIDTH - 20, HEIGHT / 2 - 70, 10, 140)
opponent = pygame.Rect(10, HEIGHT / 2 - 70, 10, 140)
ball_speed_x = 3
ball_speed_y = 3
player_speed = 0
opponent_speed = 7
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)


def game_loop():
    global ball_speed_x, ball_speed_y, ball, player_speed, opponent_speed, EXPLORATION_RATE

    ongoing = True
    while ongoing:
        # Manejo de eventos de Pygame
        for event in pygame.event.get():
            if event.type == QUIT:
                ongoing = False
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    player_speed += 7
                elif event.key == K_UP:
                    player_speed -= 7
            if event.type == KEYUP:
                if event.key == K_DOWN or event.key == K_UP:
                    player_speed = 0

        # Movimiento de la paleta del jugador controlado por el usuario
        player.y += player_speed
        if player.top <= 0:
            player.top = 0
        if player.bottom >= HEIGHT:
            player.bottom = HEIGHT

        # Movimiento de la bola
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        # Movimiento y lógica de la IA para la paleta del oponente
        state = get_state(ball, opponent)
        action = choose_action(state)
        action_index = action_to_index[action]
        if action == 'up':
            opponent_speed = -7
        elif action == 'down':
            opponent_speed = 7
        else:
            opponent_speed = 0
        opponent.y += opponent_speed
        if opponent.top <= 0:
            opponent.top = 0
        if opponent.bottom >= HEIGHT:
            opponent.bottom = HEIGHT

        # Colisiones de la bola con las paredes
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        # Colisiones de la bola con las paletas
        if ball.colliderect(player) or ball.colliderect(opponent):
            ball_speed_x *= -1

        # Bola fuera de límites
        if ball.left <= 0 or ball.right >= WIDTH:
            ball.center = (WIDTH / 2, HEIGHT / 2)
            ball_speed_x *= -1
            # Recompensa y aprendizaje
            reward = -10000 if ball.left <= 0 else 100
            next_state = get_state(ball, opponent)
            learn(state, action_index, reward, next_state)
            # Actualizar tasa de exploración
            update_exploration_rate()

        # Dibujar en pantalla
        screen.fill(bg_color)
        pygame.draw.rect(screen, light_grey, player)
        pygame.draw.rect(screen, light_grey, opponent)
        pygame.draw.ellipse(screen, light_grey, ball)
        pygame.draw.aaline(screen, light_grey, (WIDTH / 2, 0), (WIDTH / 2, HEIGHT))

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()


if __name__ == '__main__':
    game_loop()
