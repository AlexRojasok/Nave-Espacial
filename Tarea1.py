import pygame
import random
import os

# Inicializamos PyGame
pygame.init()

# Definimos el tamaño de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego de Nave Espacial")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Variables del jugador
player_width, player_height = 50, 40
player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10
player_speed = 5

# Variables del enemigo
enemy_width, enemy_height = 50, 40
enemy_speed = 5
enemy_list = []
enemy_increase_speed_timer = 0

# Variables de bloques de vida
life_block_width, life_block_height = 30, 30
life_block_list = []

# Variables de puntos
score = 0
lives = 3

# Fuente
font = pygame.font.SysFont("comicsans", 30)

# Función para dibujar la nave (jugador)
def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))

# Función para generar enemigos
def create_enemy():
    enemy_x = random.randint(0, WIDTH - enemy_width)
    enemy_y = -enemy_height
    enemy_list.append([enemy_x, enemy_y])

# Función para generar bloques de vida
def create_life_block():
    life_block_x = random.randint(0, WIDTH - life_block_width)
    life_block_y = -life_block_height
    life_block_list.append([life_block_x, life_block_y])

# Función para mover enemigos
def move_enemies():
    global enemy_speed
    for enemy in enemy_list[:]:
        enemy[1] += enemy_speed
        if enemy[1] > HEIGHT:
            enemy_list.remove(enemy)

# Función para mover bloques de vida
def move_life_blocks():
    for block in life_block_list[:]:
        block[1] += enemy_speed  # Los bloques de vida se mueven a la misma velocidad que los enemigos
        if block[1] > HEIGHT:
            life_block_list.remove(block)

# Función para dibujar enemigos
def draw_enemies():
    for enemy in enemy_list:
        pygame.draw.rect(screen, RED, (enemy[0], enemy[1], enemy_width, enemy_height))

# Función para dibujar bloques de vida
def draw_life_blocks():
    for block in life_block_list:
        pygame.draw.rect(screen, BLUE, (block[0], block[1], life_block_width, life_block_height))

# Función para detectar colisiones con enemigos
def check_collision(player_x, player_y, enemies):
    global score, lives
    for enemy in enemies[:]:
        if (player_x < enemy[0] + enemy_width and
            player_x + player_width > enemy[0] and
            player_y < enemy[1] + enemy_height and
            player_y + player_height > enemy[1]):
            enemies.remove(enemy)
            score -= 10  # Puntos negativos por colisión
            lives -= 1    # Pérdida de una vida

# Función para detectar colisiones con bloques de vida
def check_life_block_collision(player_x, player_y, life_blocks):
    global lives
    for block in life_blocks[:]:
        if (player_x < block[0] + life_block_width and
            player_x + player_width > block[0] and
            player_y < block[1] + life_block_height and
            player_y + player_height > block[1]):
            life_blocks.remove(block)
            lives += 1  # Sumar una vida

# Función para mostrar el puntaje y las vidas
def draw_score_and_lives():
    score_text = font.render(f"Puntos: {score}", True, WHITE)
    lives_text = font.render(f"Vidas: {lives}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 150, 10))

# Función para mostrar el menú principal
def show_menu():
    screen.fill(BLACK)
    title_text = font.render("Juego de Nave Espacial", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
    start_text = font.render("Presiona ENTER para comenzar", True, WHITE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()

# Función para el menú de pausa
def pause_menu():
    paused = True
    while paused:
        screen.fill(BLACK)
        pause_text = font.render("Juego en Pausa", True, WHITE)
        screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 3))
        resume_text = font.render("Presiona 'P' para continuar", True, WHITE)
        screen.blit(resume_text, (WIDTH // 2 - resume_text.get_width() // 2, HEIGHT // 2))
        restart_text = font.render("Presiona 'R' para reiniciar", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Continuar juego
                    paused = False
                if event.key == pygame.K_r:  # Reiniciar juego
                    restart_game()

# Función para reiniciar el juego
def restart_game():
    global player_x, player_y, score, lives, enemy_list, enemy_speed, life_block_list
    player_x, player_y = WIDTH // 2 - player_width // 2, HEIGHT - player_height - 10
    score = 0
    lives = 3
    enemy_list.clear()
    life_block_list.clear()
    enemy_speed = 5  # Reiniciamos la velocidad de los enemigos

# Función para mostrar pantalla de Game Over
def game_over():
    screen.fill(BLACK)
    over_text = font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
    retry_text = font.render("Presiona 'R' para reiniciar o 'Q' para salir", True, WHITE)
    screen.blit(retry_text, (WIDTH // 2 - retry_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

# Función principal del juego
def game_loop():
    global player_x, player_y, score, lives, enemy_speed, enemy_increase_speed_timer  # Declaramos las variables globales

    running = True
    menu = True
    clock = pygame.time.Clock()
    enemy_timer = 0
    life_block_timer = 0

    while running:
        clock.tick(60)  # 60 FPS
        screen.fill(BLACK)

        # Menú principal
        if menu:
            show_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    menu = False
            continue

        # Eventos dentro del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pausar el juego
                    pause_menu()

        # Movimiento del jugador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # Generar enemigos
        enemy_timer += 1
        if enemy_timer > 50:
            create_enemy()
            enemy_timer = 0

        # Generar bloques de vida cada 10 segundos
        life_block_timer += 1
        if life_block_timer > 600:  # 600 frames a 60 FPS son aproximadamente 10 segundos
            create_life_block()
            life_block_timer = 0

        # Mover y dibujar enemigos
        move_enemies()
        draw_enemies()

        # Mover y dibujar bloques de vida
        move_life_blocks()
        draw_life_blocks()

        # Detectar colisiones
        check_collision(player_x, player_y, enemy_list)
        check_life_block_collision(player_x, player_y, life_block_list)

        # Aumentar velocidad de enemigos progresivamente
        enemy_increase_speed_timer += 1
        if enemy_increase_speed_timer > 1000:  # Cada 1000 frames (~16.67 segundos a 60 FPS)
            enemy_speed += 0.5
            enemy_increase_speed_timer = 0

        # Dibujar el jugador
        draw_player(player_x, player_y)

        # Mostrar puntaje y vidas
        draw_score_and_lives()

        # Revisar si el jugador perdió todas las vidas
        if lives <= 0:
            game_over()

        pygame.display.update()

    pygame.quit()

# Iniciar el juego
if __name__ == "__main__":
    game_loop()
