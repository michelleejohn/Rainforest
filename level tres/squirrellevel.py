import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Screen size
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌰 Forest Friend Rescue")

# Font
font = pygame.font.SysFont("Arial", 30)

# Score
score = 0
TOTAL_NUTS = 5

# Timer
TIME_LIMIT = 120  # 2 minutes
start_time = pygame.time.get_ticks()

# Lives
lives = 3

# Speed
SQUIRREL_SPEED = 6

clock = pygame.time.Clock()

# Load image function
def load_image(path, width=None, height=None, fallback_color=(100,100,100)):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except pygame.error:
        surf = pygame.Surface((width or 50, height or 50))
        surf.fill(fallback_color)
        return surf

# Load images
background = load_image("images/forest.png", WIDTH, HEIGHT)
nut_image = load_image("images/nut.png", 60, 60)
squirrel_image = load_image("images/squirrel.png", 120, 120)

# Obstacles
roach = load_image("images/roach.png", 80, 80)
owl = load_image("images/owl.png", 100, 100)
branch = load_image("images/branch.png", 140, 60)
apple = load_image("images/apple.png", 60, 60)
snail = load_image("images/snail.png", 70, 70)

# Heart image
heart = load_image("images/heart.png", 40, 40, fallback_color=(255,0,0))

# Nut positions
def random_nut_positions():
    positions = []
    for _ in range(TOTAL_NUTS):
        x = random.randint(50, WIDTH - 110)
        y = random.randint(100, HEIGHT - 160)
        positions.append(pygame.Rect(x, y, 60, 60))
    return positions

# Obstacles
def create_obstacles():
    obstacles = []

    for _ in range(2):
        obstacles.append(("branch", pygame.Rect(random.randint(100, WIDTH-200), random.randint(100, HEIGHT-200), 140, 60)))

    for _ in range(2):
        obstacles.append(("owl", pygame.Rect(random.randint(100, WIDTH-200), random.randint(100, HEIGHT-200), 100, 100)))

    for _ in range(2):
        obstacles.append(("roach", pygame.Rect(random.randint(100, WIDTH-200), random.randint(100, HEIGHT-200), 80, 80)))

    for _ in range(1):
        obstacles.append(("snail", pygame.Rect(random.randint(100, WIDTH-200), random.randint(100, HEIGHT-200), 70, 70)))

    for _ in range(2):
        obstacles.append(("apple", pygame.Rect(random.randint(100, WIDTH-200), random.randint(100, HEIGHT-200), 60, 60)))

    return obstacles

obstacles = create_obstacles()
nut_positions = random_nut_positions()

# Squirrel
squirrel_rect = pygame.Rect(WIDTH//2 - 60, HEIGHT - 140, 120, 120)
target_nut = None

# Check collision
def check_collision(rect, obstacles):
    for _, obs in obstacles:
        if rect.colliderect(obs):
            return True
    return False

# Reset level
def reset_level():
    global nut_positions, obstacles, squirrel_rect, target_nut, start_time, score
    nut_positions = random_nut_positions()
    obstacles = create_obstacles()
    squirrel_rect.x = WIDTH//2 - 60
    squirrel_rect.y = HEIGHT - 140
    target_nut = None
    start_time = pygame.time.get_ticks()
    score = 0

# Game loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for nut_rect in nut_positions:
                if nut_rect.collidepoint(mouse_pos):
                    target_nut = nut_rect
                    break

    # Timer
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = TIME_LIMIT - elapsed

    if remaining <= 0:
        lives -= 1
        reset_level()

    # Move squirrel
    if target_nut:
        dx = target_nut.x - squirrel_rect.x
        dy = target_nut.y - squirrel_rect.y
        dist = (dx**2 + dy**2) ** 0.5

        if dist < SQUIRREL_SPEED:
            squirrel_rect.x = target_nut.x
            squirrel_rect.y = target_nut.y
            nut_positions.remove(target_nut)
            score += 1
            target_nut = None

        else:
            new_x = squirrel_rect.x + int(SQUIRREL_SPEED * dx / dist)
            new_y = squirrel_rect.y + int(SQUIRREL_SPEED * dy / dist)

            new_rect = pygame.Rect(new_x, new_y, 120, 120)

            if not check_collision(new_rect, obstacles):
                squirrel_rect.x = new_x
                squirrel_rect.y = new_y

    # Win condition
    if score == TOTAL_NUTS:
        pygame.time.delay(500)
        reset_level()

    # Game over
    if lives <= 0:
        print("Game Over")
        pygame.quit()
        sys.exit()

    # Draw
    screen.blit(background, (0,0))

    # Draw nuts
    for nut_rect in nut_positions:
        screen.blit(nut_image, nut_rect)

    # Draw obstacles
    for name, rect in obstacles:
        if name == "branch":
            screen.blit(branch, rect)
        elif name == "owl":
            screen.blit(owl, rect)
        elif name == "roach":
            screen.blit(roach, rect)
        elif name == "snail":
            screen.blit(snail, rect)
        elif name == "apple":
            screen.blit(apple, rect)

    # Draw squirrel
    screen.blit(squirrel_image, squirrel_rect)

    # Draw score
    score_text = font.render(f"Nuts: {score}/{TOTAL_NUTS}", True, (0,0,0))
    screen.blit(score_text, (WIDTH//2 - 80, 20))

    # Draw timer
    timer_text = font.render(f"Time: {remaining}", True, (0,0,0))
    screen.blit(timer_text, (WIDTH - 150, 20))

    # Draw hearts
    for i in range(lives):
        screen.blit(heart, (20 + i * 50, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
