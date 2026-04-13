import pygame
import sys
import os

pygame.init()

# window
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("End Screen")
clock = pygame.time.Clock()

# colors
BG_COLOR = (232, 239, 232)      # #e8efe8
BORDER_COLOR = (109, 143, 109)  # #6d8f6d
BOX_BG = (217, 234, 217)        # #d9ead9
TEXT_DARK = (47, 79, 47)        # #2f4f2f

# load background
def load_image(filename, size=None):
    if not os.path.exists(filename):
        print(f"Missing image: {filename}")
        return None
    image = pygame.image.load(filename).convert()
    if size is not None:
        image = pygame.transform.smoothscale(image, size)
    return image

background = load_image("fairyforest.png", (WIDTH, HEIGHT))

# fonts
title_font = pygame.font.SysFont("segoescript,brushscriptmt,lucidahandwriting,arial", 22)
congrats_font = pygame.font.SysFont("segoescript,brushscriptmt,lucidahandwriting,arial", 32)
message_font = pygame.font.SysFont("segoescript,brushscriptmt,lucidahandwriting,arial", 18)
credits_font = pygame.font.SysFont("segoescript,brushscriptmt,lucidahandwriting,arial", 14)

# rectangles
title_rect = pygame.Rect(20, 20, 190, 60)

congrats_rect = pygame.Rect(0, 90, 550, 80)
congrats_rect.centerx = WIDTH // 2

message_rect = pygame.Rect(0, 270, 220, 110)
message_rect.centerx = WIDTH // 2

credits_rect = pygame.Rect(0, 450, 220, 140)
credits_rect.centerx = WIDTH // 2

def draw_box(surface, rect):
    pygame.draw.rect(surface, BOX_BG, rect)
    pygame.draw.rect(surface, BORDER_COLOR, rect, width=3)

def draw_text(surface, text, font, color, x, y, center=False):
    rendered = font.render(text, True, color)
    text_rect = rendered.get_rect()
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
    surface.blit(rendered, text_rect)

def draw_multiline_text(surface, lines, font, color, rect, line_spacing=8):
    rendered_lines = [font.render(line, True, color) for line in lines]
    total_height = sum(line.get_height() for line in rendered_lines) + line_spacing * (len(rendered_lines) - 1)
    y = rect.centery - total_height // 2

    for line in rendered_lines:
        line_rect = line.get_rect(center=(rect.centerx, y + line.get_height() // 2))
        surface.blit(line, line_rect)
        y += line.get_height() + line_spacing

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)

    if background:
        screen.blit(background, (0, 0))

    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), width=3)

    # title box
    draw_box(screen, title_rect)
    draw_text(screen, "End Screen", title_font, TEXT_DARK, title_rect.x + 15, title_rect.y + 10)

    # congratulations box
    draw_box(screen, congrats_rect)
    draw_text(screen, "Congratulations", congrats_font, TEXT_DARK,
              congrats_rect.centerx, congrats_rect.centery, center=True)

    # message box
    draw_box(screen, message_rect)
    message_lines = [
        "Thanks for",
        "playing!"
    ]
    draw_multiline_text(screen, message_lines, message_font, TEXT_DARK, message_rect, line_spacing=10)

    # credits box
    draw_box(screen, credits_rect)
    credits_lines = [
        "Credits:",
        "Michelle",
        "Zoe",
        "Leesie",
        "Patricia"
    ]
    draw_multiline_text(screen, credits_lines, credits_font, TEXT_DARK, credits_rect, line_spacing=6)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()