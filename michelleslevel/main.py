import pygame
import random
import sys
import os
import heapq

pygame.init()
pygame.mixer.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌰 Forest Friend Rescue")

font = pygame.font.SysFont("Arial", 30)
carattere_font = pygame.font.SysFont("Arial", 24)

# Game settings
score = 0
TOTAL_NUTS = 5
TIME_LIMIT = 120
start_time = pygame.time.get_ticks()
SQUIRREL_SPEED = 4

clock = pygame.time.Clock()

# Dialogue
messages = [
"Hey there, I'm Prince Nutty the Squirrel!",
"I need your help to find all my hidden acorns - they're my treasure!",
"Watch out for tricky obstacless like apples, branches, and sneaky critters!",
"Move fast and steady so I don't miss a single acorn.",
"Let's find every acorn together and make this the best acorn hunt ever!"
]
message_index = 0
message_timer = pygame.time.get_ticks()

# Load image helper
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

# Load sound
def load_sound(path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(current_dir, path)
    try:
        return pygame.mixer.Sound(full_path)
    except:
        return None

collect_sound = load_sound("sounds/collect.wav")

# Load images
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

# Chatbox

def draw_chatbox(screen, text, font, rect):
    pygame.draw.rect(screen, (255,255,255), rect, border_radius=15)
    pygame.draw.rect(screen, (0,0,0), rect, 3, border_radius=15)

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

# Obstacles

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

# Grid pathfinding
GRID_SIZE = 40

def get_grid_pos(rect):
    return rect.x // GRID_SIZE, rect.y // GRID_SIZE


def is_blocked(x, y):
    test_rect = pygame.Rect(x*GRID_SIZE, y*GRID_SIZE, GRID_SIZE, GRID_SIZE)
    return any(test_rect.colliderect(o) for _, o in obstacles)


def astar(start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}
    g_score = {start:0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x,y = current
        neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

        for nx, ny in neighbors:
            if nx < 0 or ny < 0 or nx > WIDTH//GRID_SIZE or ny > HEIGHT//GRID_SIZE:
                continue

            if is_blocked(nx, ny):
                continue

            tentative = g_score[current] + 1

            if (nx,ny) not in g_score or tentative < g_score[(nx,ny)]:
                came_from[(nx,ny)] = current
                g_score[(nx,ny)] = tentative
                priority = tentative + abs(nx-goal[0]) + abs(ny-goal[1])
                heapq.heappush(open_set, (priority, (nx,ny)))

    return []

path = []
target_nut = None


def reset_level():
    global nut_positions, obstacles, squirrel_rect, target_nut, score, path, start_time
    nut_positions = random_nut_positions()
    obstacles = create_obstacles()
    squirrel_rect.topleft = (WIDTH//2, HEIGHT-140)
    target_nut = None
    score = 0
    path = []
    start_time = pygame.time.get_ticks()

# Game loop
running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            for nut in nut_positions:
                if nut.collidepoint(event.pos):
                    target_nut = nut
                    start = get_grid_pos(squirrel_rect)
                    goal = get_grid_pos(nut)
                    path = astar(start, goal)
                    break

    # Timer
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = TIME_LIMIT - elapsed

    if remaining <= 0:
        reset_level()

    # Dialogue cycling
    if pygame.time.get_ticks() - message_timer > 4000:
        message_index = (messages.index(messages[message_index]) + 1) % len(messages)
        message_timer = pygame.time.get_ticks()

    # Movement
    if path:
        next_cell = path[0]
        target_pos = (next_cell[0]*GRID_SIZE, next_cell[1]*GRID_SIZE)

        dx = target_pos[0] - squirrel_rect.x
        dy = target_pos[1] - squirrel_rect.y

        if abs(dx) < SQUIRREL_SPEED and abs(dy) < SQUIRREL_SPEED:
            path.pop(0)
        else:
            if dx != 0:
                squirrel_rect.x += SQUIRREL_SPEED if dx > 0 else -SQUIRREL_SPEED
            if dy != 0:
                squirrel_rect.y += SQUIRREL_SPEED if dy > 0 else -SQUIRREL_SPEED

    if target_nut and squirrel_rect.colliderect(target_nut):
        if collect_sound:
            collect_sound.play()

        nut_positions.remove(target_nut)
        target_nut = None
        path = []
        score += 1

    if score == TOTAL_NUTS:
        pygame.time.delay(500)
        reset_level()

    # Draw
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

    # Score
    screen.blit(font.render(f"Nuts: {score}/{TOTAL_NUTS}", True, (0,0,0)), (20, 20))

    # Timer display
    m, s = remaining // 60, remaining % 60
    screen.blit(font.render(f"Time: {m}:{s:02}", True, (0,0,0)), (WIDTH-170, 20))

    # Chatbox
    chat_rect = pygame.Rect(chatbox_pos[0], chatbox_pos[1], chatbox_size[0], chatbox_size[1])
    draw_chatbox(screen, messages[message_index], carattere_font, chat_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
