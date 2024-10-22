import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("sounds/bg_music_1.wav")

# Function to start background music
def start_bg_music():
    pygame.mixer.music.play(loops=-1)

# Function to stop background music
def stop_bg_music():
    pygame.mixer.music.stop()

# Set up display
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game by @Mostafa_Noaman")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Load background image
bk_ground = os.path.join("backgrounds", random.choice(os.listdir("backgrounds")))
background_img = pygame.image.load(bk_ground)
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load snake images
snake_head_img = os.path.join("snakes", random.choice(os.listdir("snakes")))
head_img = pygame.image.load(snake_head_img).convert_alpha()
head_img = pygame.transform.scale(head_img, (20, 20))

# Load apple image
apple = os.path.join("fruits", random.choice(os.listdir("fruits")))
food_img = pygame.image.load(apple).convert_alpha()
food_img = pygame.transform.scale(food_img, (20, 20))

# Obstacles
obstacle_color = RED
obstacles = []
for _ in range(10):
    x = random.randint(20, SCREEN_WIDTH - 20)
    y = random.randint(20, SCREEN_HEIGHT - 20)
    obstacles.append(pygame.Rect(x, y, 20, 20))

# Snake settings
snake_pos = [300, 300]
snake_body = [pygame.Rect(300, 300, 20, 20)]
direction = "STOP"
change_to = direction

# Food settings
food_pos = [random.randint(1, (SCREEN_WIDTH//20)) * 20, random.randint(1, (SCREEN_HEIGHT//20)) * 20]
food_spawn = True

# Game variables
score = 0
high_score = 0
delay = 0.1
mute = False

# Font settings
font = pygame.font.SysFont('courier', 24)
big_font = pygame.font.SysFont('courier', 36)

# Functions
def display_score():
    score_text = font.render(f"Score: {score}  High Score: {high_score}", True, WHITE)
    win.blit(score_text, [10, 10])

def game_over():
    game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
    game_over_sound.play()

    # Display game over message
    over_text = big_font.render("GAME OVER", True, WHITE)
    win.blit(over_text, [SCREEN_WIDTH // 4, SCREEN_HEIGHT // 3])
    pygame.display.flip()
    time.sleep(3)
    
    global score, snake_pos, snake_body, direction, food_spawn
    score = 0
    snake_pos = [300, 300]
    snake_body = [pygame.Rect(300, 300, 20, 20)]
    direction = "STOP"
    food_spawn = True

def mute_sound():
    global mute
    mute = True
    stop_bg_music()

def unmute_sound():
    global mute
    mute = False
    start_bg_music()

# Main game loop
clock = pygame.time.Clock()

running = True
while running:
    win.fill(BLACK)
    win.blit(background_img, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'
            elif event.key == pygame.K_x:
                mute_sound()
            elif event.key == pygame.K_c:
                unmute_sound()

    # Move the snake
    if direction == 'UP':
        snake_pos[1] -= 20
    if direction == 'DOWN':
        snake_pos[1] += 20
    if direction == 'LEFT':
        snake_pos[0] -= 20
    if direction == 'RIGHT':
        snake_pos[0] += 20

    # Snake growing mechanism
    snake_body.insert(0, pygame.Rect(snake_pos[0], snake_pos[1], 20, 20))
    if snake_pos == food_pos:
        score += 10
        if score > high_score:
            high_score = score

        eating_sound = pygame.mixer.Sound("sounds/heavy_swallow.wav")
        eating_sound.play()

        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randint(1, (SCREEN_WIDTH//20)) * 20, random.randint(1, (SCREEN_HEIGHT//20)) * 20]
    food_spawn = True

    # Draw snake
    for rect in snake_body:
        win.blit(head_img, rect.topleft)

    # Draw food
    win.blit(food_img, food_pos)

    # Draw obstacles
    for obstacle in obstacles:
        pygame.draw.rect(win, obstacle_color, obstacle)

    # Check for collisions
    if snake_pos[0] < 0 or snake_pos[0] >= SCREEN_WIDTH or snake_pos[1] < 0 or snake_pos[1] >= SCREEN_HEIGHT:
        game_over()

    for block in snake_body[1:]:
        if snake_body[0].colliderect(block):
            game_over()

    for obstacle in obstacles:
        if pygame.Rect(snake_pos[0], snake_pos[1], 20, 20).colliderect(obstacle):
            game_over()

    # Update display
    display_score()
    pygame.display.update()

    # Control game speed
    clock.tick(15)

pygame.quit()
