# Simple Snake Game in Python 3 for Beginners
# By @Mostafa_Noaman

import os
import turtle
import time
import random
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("sounds/bg_music_1.wav")



# Function to start background music
def start_bg_music():
    pygame.mixer.music.play(loops=-1)

# Function to stop background music
def stop_bg_music():
    pygame.mixer.music.stop()


delay = 0.1

# Score
score = 0
high_score = 0

# Set up the screen
bk_ground = os.path.join("backgrounds",random.choice(os.listdir("backgrounds")))
wn = turtle.Screen()
wn.bgpic(bk_ground)  # Set the background image
wn.title("Snake Game by @Mostafa_Noaman")
wn.setup(width=600, height=600)
wn.tracer(0)  # Turns off the screen updates

# Snake head
snake_head = os.path.join("snakes",random.choice(os.listdir("snakes")))
wn.addshape(snake_head)
head = turtle.Turtle()
head.speed(0)
head.shape(snake_head)
head.penup()
head.goto(0,0)
head.direction = "stop"

# Obstacles
obstacles = []
for _ in range(10):  # Create 5 obstacles
    obstacle = turtle.Turtle()
    obstacle.shape("square")
    obstacle.color("red")
    obstacle.penup()
    x = random.randint(-290, 290)
    y = random.randint(-290, 290)
    obstacle.goto(x, y)
    obstacles.append(obstacle)

# Snake food
apple = os.path.join("fruits",random.choice(os.listdir("fruits")))
wn.addshape(apple)
food = turtle.Turtle()
food.speed(0)
food.shape(apple)
food.penup()
food.goto(0, 100)
segments = []

# Pen
type_color = "white" if not bk_ground.endswith("1.gif") else "black"
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color(type_color)
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))

# Functions
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# Game Over
def game_over():
    # Clear the screen
    head.goto(0, 0)
    head.direction = "stop"

    # Hide the food and segments
    food.goto(1000, 1000)
    for segment in segments:
        segment.goto(1000, 1000)
    segments.clear()

    # play game over sound
    game_over_sound = pygame.mixer.Sound("sounds/game_over.wav")
    game_over_sound.play()

    # Display Game Over message
    pen.goto(0, 0)
    pen.write("GAME OVER", align="center", font=("Courier", 36, "normal"))

    # Pause for a few seconds
    time.sleep(3)

    # Reset the score and game state
    global score
    score = 0
    pen.clear()
    pen.goto(0, 260)
    pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    # Reset the position of the head and food
    head.goto(0, 0)
    food.goto(0, 100)


# Function to check if the position is far enough from obstacles
def is_food_position_valid(x, y, obstacles, min_distance=50):
    for obstacle in obstacles:
        if obstacle.distance(x, y) < min_distance:
            return False
    return True

# Function to generate food away from obstacles and walls
def generate_food_position(wn_width, wn_height, obstacles, margin=40, min_distance_from_obstacles=30):
    while True:
        x = random.randint(-wn_width//2 + margin, wn_width//2 - margin)
        y = random.randint(-wn_height//2 + margin, wn_height//2 - margin)
        if is_food_position_valid(x, y, obstacles, min_distance_from_obstacles):
            return x, y

# Keyboard bindings
wn.listen()
wn.onkeypress(go_up, 'Up')
wn.onkeypress(go_down, 'Down')
wn.onkeypress(go_left, 'Left')
wn.onkeypress(go_right, 'Right')


# Main game loop
while True:
    wn.update()

    # Start background music if it is not already playing
    if not pygame.mixer.music.get_busy():
        start_bg_music()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        head.goto(0,0)
        head.direction = "stop"

        # play collusion sound
        stop_bg_music()  # Stop background music when game is reset
        collision_sound = pygame.mixer.Sound("sounds/crash.wav")
        collision_sound.play()
        time.sleep(2)

        # Hide the segments
        for segment in segments:
            segment.goto(1000, 1000)
        
        # Clear the segments list
        segments.clear()

        # Reset the score
        score = 0

        # Reset the delay
        delay = 0.1

        game_over()
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 


    # Check for collision with obstacles
    for obstacle in obstacles:
        if head.distance(obstacle) < 20:  # Collision detection
            head.goto(0, 0)
            head.direction = "stop"
            stop_bg_music()
            collision_sound = pygame.mixer.Sound("sounds/crash.wav")
            collision_sound.play()
            time.sleep(2)
            game_over()
            head.goto(0, 0)  # Reset position
            break

    # Check for a collision with the food (eating)
    if head.distance(food) < 20:
        # Move the food to a random spot
        food_x, food_y = generate_food_position(600, 600, obstacles, margin=40)
        food.goto(food_x, food_y)

        # Add a segment
        body = os.path.join("body",random.choice(os.listdir("body")))
        wn.addshape(body)
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape(body)
        new_segment.penup()
        segments.append(new_segment)

        # Shorten the delay
        delay -= 0.001

        # Increase the score
        score += 10

        if score > high_score:
            high_score = score
        
        eating_sound = pygame.mixer.Sound("sounds/heavy_swallow.wav")
        eating_sound.play()

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            head.goto(0,0)
            head.direction = "stop"
        
            # Hide the segments
            for segment in segments:
                segment.goto(1000, 1000)
        
            # Clear the segments list
            segments.clear()

            # Reset the score
            score = 0

            # Reset the delay
            delay = 0.1
        
            stop_bg_music()  # Stop background music when game is reset
            eating_sound = pygame.mixer.Sound("sounds/bite.wav")
            eating_sound.play()
            time.sleep(1)

            # Update the score display
            game_over()
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()
