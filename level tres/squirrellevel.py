import pygame
import random
import sys
import os

pygame.init()

# SCREEN
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🌳 Forest Tree Adventure")

font = pygame.font.SysFont("Arial", 30)
chat_font = pygame.font.SysFont("Arial", 24)

clock = pygame.time.Clock()

# GAME SETTINGS
TOTAL_NUTS = 5
TIME_LIMIT = 120
SPEED = 6

start_time = pygame.time.get_ticks()
score = 0

# TREE BASE POSITION
TREE_X = 600
TREE_Y = 120

# LOAD IMAGE FUNCTION
def load_image(path, w=None, h=None, fallback=(200,200,200)):
    try:
        img = pygame.image.load(os.path.join("images", path)).convert_alpha()
        if w and h:
            img = pygame.transform.scale(img, (w, h))
        return img
    except:
        surf = pygame.Surface((w or 50, h or 50))
        surf.fill(fallback)
        return surf

# IMAGES
bg = load_image("forest.png", WIDTH, HEIGHT)
nut_img = load_image("nut.png", 50, 50)
squirrel_img = load_image("squirrel.png", 120, 120)

branch_img = load_image("branch.png", 200, 50)
apple_img = load_image("apple.png", 60, 60)
owl_img = load_image("owl.png", 90, 90)
roach_img = load_image("roach.png", 70, 70)
snail_img = load_image("snail.png", 70, 70)

# FIXED FAIRY (pink fallback = missing file)
fairy_img = load_image("fairy.png", 120, 120, fallback=(255, 0, 255))
fairy_pos = (WIDTH - 180, HEIGHT - 180)

# CHATBOX
chatbox_rect = pygame.Rect(WIDTH//2 - 300, HEIGHT - 140, 600, 100)

def draw_chatbox(text):
    pygame.draw.rect(screen, (255,255,255), chatbox_rect, border_radius=12)
    pygame.draw.rect(screen, (0,0,0), chatbox_rect, 3, border_radius=12)

    words = text.split()
    lines = []
    line = ""

    for w in words:
        test = line + w + " "
        if chat_font.size(test)[0] < chatbox_rect.width - 20:
            line = test
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)

    y = chatbox_rect.y + 10
    for l in lines:
        screen.blit(chat_font.render(l, True, (0,0,0)), (chatbox_rect.x + 10, y))
        y += 25

# TREE OBJECTS

def create_obstacles():
    return [
        ("branch", pygame.Rect(TREE_X - 250, TREE_Y + 150, 300, 40)),
        ("branch", pygame.Rect(TREE_X + 50, TREE_Y + 250, 300, 40)),
        ("branch", pygame.Rect(TREE_X - 200, TREE_Y + 350, 300, 40)),
        ("branch", pygame.Rect(TREE_X - 120, TREE_Y + 80, 250, 40)),

        ("owl", pygame.Rect(TREE_X - 260, TREE_Y + 120, 90, 90)),
        ("owl", pygame.Rect(TREE_X + 220, TREE_Y + 200, 90, 90)),

        ("roach", pygame.Rect(300, 500, 70, 70)),
        ("snail", pygame.Rect(900, 450, 70, 70))
    ]

def nut_positions():
    return [
        pygame.Rect(TREE_X - 200, TREE_Y + 160, 50, 50),
        pygame.Rect(TREE_X + 100, TREE_Y + 160, 50, 50),
        pygame.Rect(TREE_X - 100, TREE_Y + 260, 50, 50),
        pygame.Rect(TREE_X + 200, TREE_Y + 260, 50, 50),
        pygame.Rect(TREE_X, TREE_Y + 350, 50, 50),
    ]

def apple_positions():
    return [
        pygame.Rect(TREE_X - 50, TREE_Y + 140, 60, 60),
        pygame.Rect(TREE_X + 220, TREE_Y + 240, 60, 60),
        pygame.Rect(TREE_X - 220, TREE_Y + 320, 60, 60),
    ]

obstacles = create_obstacles()
nuts = nut_positions()
apples = apple_positions()

# PLAYER
squirrel = pygame.Rect(WIDTH//2, HEIGHT-140, 120, 120)
target = None

def collision(rect):
    return any(rect.colliderect(o) for _, o in obstacles)

# RESET
def reset():
    global nuts, obstacles, squirrel, target, start_time, score
    nuts = nut_positions()
    obstacles = create_obstacles()
    squirrel.topleft = (WIDTH//2, HEIGHT-140)
    target = None
    start_time = pygame.time.get_ticks()
    score = 0

# LOOP
running = True
while running:

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            for n in nuts:
                if n.collidepoint(e.pos):
                    target = n
                    break

    # TIMER
    elapsed = (pygame.time.get_ticks() - start_time) // 1000
    remaining = TIME_LIMIT - elapsed

    if remaining <= 0:
        reset()

    # AI MOVEMENT
    if target:
        dx = target.x - squirrel.x
        dy = target.y - squirrel.y
        dist = (dx*dx + dy*dy) ** 0.5

        if dist < SPEED:
            squirrel.topleft = target.topleft
            nuts.remove(target)
            target = None
            score += 1

        else:
            mx = int(SPEED * dx / dist)
            my = int(SPEED * dy / dist)

            move = squirrel.move(mx, my)

            if not collision(move):
                squirrel = move
            else:
                if not collision(squirrel.move(mx, 0)):
                    squirrel.x += mx
                elif not collision(squirrel.move(0, my)):
                    squirrel.y += my
                else:
                    squirrel.x += random.choice([-SPEED, SPEED])
                    squirrel.y += random.choice([-SPEED, SPEED])

    if score == TOTAL_NUTS:
        reset()

    # DRAW
    screen.blit(bg, (0,0))

    # branches
    for name, r in obstacles:
        if name == "branch":
            screen.blit(branch_img, r)

    # apples
    for a in apples:
        screen.blit(apple_img, a)

    # nuts
    for n in nuts:
        screen.blit(nut_img, n)

    # animals
    for name, r in obstacles:
        if name == "owl":
            screen.blit(owl_img, r)
        elif name == "roach":
            screen.blit(roach_img, r)
        elif name == "snail":
            screen.blit(snail_img, r)

    # squirrel + fairy
    screen.blit(squirrel_img, squirrel)
    screen.blit(fairy_img, fairy_pos)

    # SCORE
    screen.blit(font.render(f"Nuts: {score}/{TOTAL_NUTS}", True, (0,0,0)), (20,20))

    # TIMER
    m, s = remaining // 60, remaining % 60
    screen.blit(font.render(f"Time: {m}:{s:02}", True, (0,0,0)), (WIDTH-170, 20))

    # CHAT
    draw_chatbox("Get ready for your surprise in the forest tree!",)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
