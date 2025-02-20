import pygame
import sys
import random
import time
import tkinter as tk
from tkinter import ttk
from pygame.locals import KEYDOWN, KEYUP, QUIT, K_UP, K_DOWN, K_w, K_s, K_LEFT, K_RIGHT
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Selection Tool")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Difficulty levels
difficulty = {
    "Easy": 5,
    "Medium": 10,
    "Hard": 15
}

selected_game = "Snake"
selected_difficulty = "Easy"

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def run_pygame():
    if selected_game == "Snake":
        snake_game()
    elif selected_game == "Car Race":
        car_race_game()
    elif selected_game == "Pong":
        pong_game()

def snake_game():
    global selected_difficulty
    speed = difficulty[selected_difficulty]

    # Snake settings
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    score = 0

    # Food settings
    food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    food_spawn = True

    # Game over function
    def game_over():
        screen.fill(BLACK)
        draw_text(f'Your Score: {score}', font, RED, screen, WIDTH // 4, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(2)
        show_game_over_gif()

    # Main logic
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # If two keys pressed simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # Move snake
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        # Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WIDTH // 10)) * 10, random.randrange(1, (HEIGHT // 10)) * 10]

        food_spawn = True
        screen.fill(BLACK)

        for pos in snake_body:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(screen, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Game Over conditions
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - 10:
            game_over()
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - 10:
            game_over()

        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()

        draw_text(f'Score: {score}', font, WHITE, screen, 20, 20)

        pygame.display.update()
        pygame.time.Clock().tick(speed)

def car_race_game():
    global selected_difficulty

    # Set the dimensions of the window
    display_width = 800
    display_height = 600

    # Set colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)

    # Road parameters
    road_center_x = display_width // 2
    road_center_y = display_height // 2
    road_radius_x = 187
    road_radius_y = 198

    # Set the directory for resources
    current_dir = os.path.dirname(]brook/ocrpy)
    resource_dir = os.path.join(current_dir, 'image')
    music_dir = os.path.join(current_dir, 'music')

    # Load images
    car_img = pygame.image.load(os.path.join(resource_dir, 'car1.png'))
    road_img = pygame.image.load(os.path.join(resource_dir, 'road.png'))
    obstacle_imgs = [
        pygame.image.load(os.path.join(resource_dir, 'car2.png')),
        pygame.image.load(os.path.join(resource_dir, 'car3.png')),
        pygame.image.load(os.path.join(resource_dir, 'car4.png'))
    ]

    # Scale images
    car_img = pygame.transform.scale(car_img, (50, 100))
    obstacle_imgs = [pygame.transform.scale(img, (50, 100)) for img in obstacle_imgs]
    road_img = pygame.transform.scale(road_img, (display_width, display_height))

    car_width = car_img.get_width()
    car_height = car_img.get_height()

    # Define the road boundaries
    road_left = road_center_x - road_radius_x
    road_right = road_center_x + road_radius_x - car_width

    # Initialize display
    gameDisplay = pygame.display.set_mode((display_width, display_height))
    pygame.display.set_caption('A bit Racey')

    # Clock for controlling the frame rate
    clock = pygame.time.Clock()

    # Load sound files
    crash_sound = pygame.mixer.Sound(os.path.join(music_dir, 'crash.wav'))
    car_sound = pygame.mixer.Sound(os.path.join(music_dir, 'car.wav'))

    # Function to display the car
    def car(x, y):
        gameDisplay.blit(car_img, (x, y))

    # Function to display text
    def text_objects(text, font):
        text_surface = font.render(text, True, black)
        return text_surface, text_surface.get_rect()

    def message_display(text):
        large_text = pygame.font.Font('freesansbold.ttf', 115)
        text_surf, text_rect = text_objects(text, large_text)
        text_rect.center = ((display_width / 2), (display_height / 2))
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(2)
        game_loop()

    # Function to handle crashes
    def crash():
        pygame.mixer.Sound.play(crash_sound)
        message_display('You Crashed \nPress any key to restart')

    # Function to draw obstacles
    def obstacles(obx, oby, image):
        gameDisplay.blit(image, (obx, oby))

    # Function to draw background
    def draw_background(y_offset):
        rel_y = y_offset % display_height
        gameDisplay.blit(road_img, (0, rel_y - display_height))
        if rel_y < display_height:
            gameDisplay.blit(road_img, (0, rel_y))

    # Function to display score
    def display_score(score):
        font = pygame.font.SysFont(None, 35)
        text = font.render("Score: " + str(score), True, black)
        gameDisplay.blit(text, (0, 0))

    # Main game loop
    def game_loop():
        pygame.mixer.Sound.play(car_sound, loops=-1)  # Play the car sound in a loop

        x = (display_width * 0.45)
        y = (display_height * 0.8)
        x_change = 0
        y_offset = 0

        obstacle_startx = random.randrange(road_left, road_right, 50)
        obstacle_starty = -600
        obstacle_speed = difficulty[selected_difficulty]
        obstacle_img = random.choice(obstacle_imgs)

        dodged = 0

        game_exit = False

        while not game_exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x_change = -5
                    elif event.key == pygame.K_RIGHT:
                        x_change = 5
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        x_change = 0

            x += x_change
            y_offset += obstacle_speed

            draw_background(y_offset)

            obstacles(obstacle_startx, obstacle_starty, obstacle_img)
            obstacle_starty += obstacle_speed
            car(x, y)
            display_score(dodged)

            if x > display_width - car_width or x < 0:
                crash()

            if obstacle_starty > display_height:
                obstacle_starty = 0 - car_height
                obstacle_startx = random.randrange(road_left, road_right, 50)
                obstacle_img = random.choice(obstacle_imgs)
                dodged += 1
                obstacle_speed += 1

            if y < obstacle_starty + car_height:
                if (x > obstacle_startx and x < obstacle_startx + car_width) or (
                        x + car_width > obstacle_startx and x + car_width < obstacle_startx + car_width):
                    crash()

            pygame.display.update()
            clock.tick(60)

        pygame.mixer.Sound.stop(car_sound)

    game_loop()
    pygame.quit()
    quit()

def pong_game():
    global selected_difficulty

    # Pong game parameters
    WIDTH = 600
    HEIGHT = 400
    BALL_RADIUS = 20
    PAD_WIDTH = 8
    PAD_HEIGHT = 80
    HALF_PAD_WIDTH = PAD_WIDTH / 2
    HALF_PAD_HEIGHT = PAD_HEIGHT / 2

    ball_pos = [0, 0]
    ball_vel = [0, 0]
    paddle1_vel = 0
    paddle2_vel = 0
    l_score = 0
    r_score = 0

    window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption('Pong Game')

    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT / 2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT / 2]

    def ball_init(right):
        nonlocal ball_pos, ball_vel
        ball_pos = [WIDTH / 2, HEIGHT / 2]
        horz = random.randrange(2, 4)
        vert = random.randrange(1, 3)
        if not right:
            horz = -horz
        ball_vel = [horz, -vert]

    def init():
        nonlocal l_score, r_score
        l_score = 0
        r_score = 0
        if random.randrange(0, 2) == 0:
            ball_init(True)
        else:
            ball_init(False)

    def draw(canvas):
        nonlocal paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score
        canvas.fill(BLACK)
        pygame.draw.line(canvas, WHITE, [WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1)
        pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
        pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)
        pygame.draw.circle(canvas, WHITE, [WIDTH // 2, HEIGHT // 2], 70, 1)

        if paddle1_pos[1] > HALF_PAD_HEIGHT and paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            paddle1_pos[1] += paddle1_vel
        elif paddle1_pos[1] == HALF_PAD_HEIGHT and paddle1_vel > 0:
            paddle1_pos[1] += paddle1_vel
        elif paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle1_vel < 0:
            paddle1_pos[1] += paddle1_vel

        if paddle2_pos[1] > HALF_PAD_HEIGHT and paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT:
            paddle2_pos[1] += paddle2_vel
        elif paddle2_pos[1] == HALF_PAD_HEIGHT and paddle2_vel > 0:
            paddle2_pos[1] += paddle2_vel
        elif paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT and paddle2_vel < 0:
            paddle2_pos[1] += paddle2_vel

        ball_pos[0] += int(ball_vel[0])
        ball_pos[1] += int(ball_vel[1])

        pygame.draw.circle(canvas, RED, ball_pos, BALL_RADIUS, 0)
        pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT],
                                            [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT],
                                            [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
        pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT],
                                            [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT],
                                            [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

        if int(ball_pos[1]) <= BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]
        if int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS:
            ball_vel[1] = -ball_vel[1]

        if int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH:
            if paddle1_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle1_pos[1] + HALF_PAD_HEIGHT:
                ball_vel[0] = -ball_vel[0]
                ball_vel[0] *= 1.1
                ball_vel[1] *= 1.1
            else:
                r_score += 1
                ball_init(True)

        if int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            if paddle2_pos[1] - HALF_PAD_HEIGHT <= ball_pos[1] <= paddle2_pos[1] + HALF_PAD_HEIGHT:
                ball_vel[0] = -ball_vel[0]
                ball_vel[0] *= 1.1
                ball_vel[1] *= 1.1
            else:
                l_score += 1
                ball_init(False)

        myfont1 = pygame.font.SysFont("Comic Sans MS", 20)
        label1 = myfont1.render("Score " + str(l_score), 1, (255, 255, 0))
        canvas.blit(label1, (50, 20))

        myfont2 = pygame.font.SysFont("Comic Sans MS", 20)
        label2 = myfont2.render("Score " + str(r_score), 1, (255, 255, 0))
        canvas.blit(label2, (470, 20))

    def keydown(event):
        nonlocal paddle1_vel, paddle2_vel
        if event.key == K_UP:
            paddle2_vel = -8
        elif event.key == K_DOWN:
            paddle2_vel = 8
        elif event.key == K_w:
            paddle1_vel = -8
        elif event.key == K_s:
            paddle1_vel = 8

    def keyup(event):
        nonlocal paddle1_vel, paddle2_vel
        if event.key in (K_w, K_s):
            paddle1_vel = 0
        elif event.key in (K_UP, K_DOWN):
            paddle2_vel = 0

    init()

    while True:
        draw(window)
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                keydown(event)
            elif event.type == KEYUP:
                keyup(event)
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        pygame.time.Clock().tick(60)

def show_game_over_gif():
    # Load the GIF and display it
    gif = pygame.image.load('path_to_gameover.gif')  # Update this path to the actual file path
    screen.fill(BLACK)
    screen.blit(gif, (WIDTH//2 - gif.get_width()//2, HEIGHT//2 - gif.get_height()//2))
    pygame.display.flip()
    time.sleep(3)
    main_menu()

def main_menu():
    root = tk.Tk()
    root.title("Game Selection Tool")

    def start_game():
        global selected_game, selected_difficulty
        selected_game = game_var.get()
        selected_difficulty = difficulty_var.get()
        root.destroy()
        run_pygame()

    tk.Label(root, text="Select Game:", font=("Helvetica", 16)).pack(pady=10)
    
    game_var = tk.StringVar(value="Snake")
    tk.Radiobutton(root, text="Snake", variable=game_var, value="Snake", font=("Helvetica", 14)).pack(anchor="w")
    tk.Radiobutton(root, text="Car Race", variable=game_var, value="Car Race", font=("Helvetica", 14)).pack(anchor="w")
    tk.Radiobutton(root, text="Pong", variable=game_var, value="Pong", font=("Helvetica", 14)).pack(anchor="w")
    
    tk.Label(root, text="Select Difficulty:", font=("Helvetica", 16)).pack(pady=10)

    difficulty_var = tk.StringVar(value="Easy")
    tk.Radiobutton(root, text="Easy", variable=difficulty_var, value="Easy", font=("Helvetica", 14)).pack(anchor="w")
    tk.Radiobutton(root, text="Medium", variable=difficulty_var, value="Medium", font=("Helvetica", 14)).pack(anchor="w")
    tk.Radiobutton(root, text="Hard", variable=difficulty_var, value="Hard", font=("Helvetica", 14)).pack(anchor="w")

    tk.Button(root, text="Start Game", command=start_game, font=("Helvetica", 16)).pack(pady=20)

    root.mainloop()

main_menu()
