import pygame
import random
import sys
import os

pygame.init()

# Screen
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌰 Forest Friend Rescue")

font = pygame.font.SysFont("Arial", 30)
carattere_font = pygame.font.SysFont("Arial", 24)

# Game settings
score = 0
TOTAL_NUTS = 5
TIME_LIMIT = 120
start_time = pygame.time.get_ticks()
SQUIRREL_SPEED = 6

clock = pygame.time.Clock()

# Load images
def load_image(path, width=None, height=None, fallback_color=(100,100,100)):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, path)
    try:
        image = pygame.image.load(full_path).convert_alpha()
        if width and height:
            image = pygame.transform.scale(image, (width, height))
        return image
    except:
        surf = pygame.Surface((width or 50, height or 50))
        surf.fill(fallback_color)
        return surf

background = load_image("images/forest.png", WIDTH, HEIGHT)
nut_image = load_image("images/nut.png", 60, 60)
squirrel_image = load_image("images/squirrel.png", 120, 120)

roach = load_image("images/roach.png", 80, 80)
owl = load_image("images/owl.png", 100, 100)
branch = load_image("images/branch.png", 140, 60)
apple = load_image("images/apple.png", 60, 60)
snail = load_image("images/snail.png", 70, 70)

fairy_img = load_image("images/fairy.png", 120, 120)

# Positions
fairy_pos = (WIDTH - 180, HEIGHT - 180)

chatbox_pos = (WIDTH//2 - 300, HEIGHT - 150)
chatbox_size = (600, 100)

# Chatbox function
def draw_chatbox(screen, text, font, rect):
    pygame.draw.rect(screen, (255, 255, 255), rect, border_radius=15)
    pygame.draw.rect(screen, (0, 0, 0), rect, 3, border_radius=15)

    words = text.split(" ")
    lines = []
    current = ""

    for word in words:
        test = current + word + " "
        if font.size(test)[0] < rect.width - 20:
            current = test
        else:
            lines.append(current)
            current = word + " "
    lines.append(current)

    y = rect.y + 10
    for line in lines:
        screen.blit(font.render(line, True, (0,0,0)), (rect.x + 10, y))
        y += font.get_height()

# Nuts
def random_nut_positions():
    return [
        pygame.Rect(
            random.randint(50, WIDTH-110),
            random.randint(100, HEIGHT-160),
            60, 60
        )
        for _ in range(TOTAL_NUTS)
    ]

# Aesthetic obstacle layout
def create_obstacles():
    return [
        ("branch", pygame.Rect(400, 250, 140, 60)),
        ("branch", pygame.Rect(600, 350, 140, 60)),
        ("branch", pygame.Rect(800, 250, 140, 60)),

        ("owl", pygame.Rect(300, 150, 100, 100)),
        ("owl", pygame.Rect(900, 150, 100, 100)),

        ("roach", pygame.Rect(500, 500, 80, 80)),
        ("roach", pygame.Rect(700, 500, 80, 80)),

        ("snail", pygame.Rect(200, 400, 70, 70)),
        ("apple", pygame.Rect(1000, 450, 60, 60))
    ]

obstacles = create_obstacles()
nut_positions = random_nut_positions()

squirrel_rect = pygame.Rect(WIDTH//2, HEIGHT-140, 120, 120)
target_nut = None

def check_collision(rect, obstacles):
    return any(rect.colliderect(o) for _, o in obstacles)

def reset_level():
    global nut_positions, obstacles, squirrel_rect, target_nut, start_time, score
    nut_positions = random_nut_positions()
    obstacles = create_obstacles()
    squirrel_rect.topleft = (WIDTH//2, HEIGHT-140)
    target_nut = None
    start_time = pygame.time.get_ticks()
    score = 0

# GAME LOOP
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for nut in nut_positions:
                if nut.collidepoint(event.pos):
                    target_nut = nut
                    break

    # Timer
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = TIME_LIMIT - elapsed

    if remaining <= 0:
        reset_level()

    # SMART AI MOVEMENT
    if target_nut:
        dx = target_nut.x - squirrel_rect.x
        dy = target_nut.y - squirrel_rect.y
        dist = (dx*dx + dy*dy) ** 0.5

        if dist < SQUIRREL_SPEED:
            squirrel_rect.topleft = target_nut.topleft
            nut_positions.remove(target_nut)
            target_nut = None
            score += 1

        else:
            mx = int(SQUIRREL_SPEED * dx / dist)
            my = int(SQUIRREL_SPEED * dy / dist)

            new_rect = squirrel_rect.move(mx, my)

            if not check_collision(new_rect, obstacles):
                squirrel_rect = new_rect
            else:
                # try axis movement
                if not check_collision(squirrel_rect.move(mx, 0), obstacles):
                    squirrel_rect.x += mx
                elif not check_collision(squirrel_rect.move(0, my), obstacles):
                    squirrel_rect.y += my
                else:
                    squirrel_rect.x += random.choice([-SQUIRREL_SPEED, SQUIRREL_SPEED])
                    squirrel_rect.y += random.choice([-SQUIRREL_SPEED, SQUIRREL_SPEED])

    if score == TOTAL_NUTS:
        pygame.time.delay(500)
        reset_level()

    # DRAW
    screen.blit(background, (0,0))

    for nut in nut_positions:
        screen.blit(nut_image, nut)

    for name, rect in obstacles:
        img = {
            "branch": branch,
            "owl": owl,
            "roach": roach,
            "snail": snail,
            "apple": apple
        }[name]
        screen.blit(img, rect)

    screen.blit(squirrel_image, squirrel_rect)
    screen.blit(fairy_img, fairy_pos)

    # SCORE
    screen.blit(font.render(f"Nuts: {score}/{TOTAL_NUTS}", True, (0,0,0)), (20, 20))

    # TIMER MM:SS
    m, s = remaining // 60, remaining % 60
    screen.blit(font.render(f"Time: {m}:{s:02}", True, (0,0,0)), (WIDTH-170, 20))

    # CHATBOX
    chat_rect = pygame.Rect(chatbox_pos[0], chatbox_pos[1], chatbox_size[0], chatbox_size[1])
    draw_chatbox(screen, "Get ready for your surprise!", carattere_font, chat_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
