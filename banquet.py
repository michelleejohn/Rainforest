import pygame
import sys
import os
import math
import subprocess

pygame.init()
pygame.mixer.init()

# window
WIDTH, HEIGHT = 950, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Banquet Hall")
clock = pygame.time.Clock()

# colors
BG_COLOR = (232, 239, 232)        # #e8efe8
BORDER_COLOR = (109, 143, 109)    # #6d8f6d
TITLE_BG = (217, 234, 217)        # #d9ead9
CHOICE_BG = (223, 240, 223)       # #dff0df
TEXT_DARK = (47, 79, 47)          # #2f4f2f
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_BG = (216, 216, 216)
BUTTON_HOVER = (191, 191, 191)

# assets
def load_image(filename, size=None):
    if not os.path.exists(filename):
        print(f"Missing image: {filename}")
        return None
    image = pygame.image.load(filename).convert_alpha()
    if size is not None:
        image = pygame.transform.smoothscale(image, size)
    return image

background = load_image("fairyforest.png", (WIDTH, HEIGHT))
keep_sound = pygame.mixer.Sound("yay_z.wav")

# fairy images and positions from your HTML
fairy_data = [
    {"file": "fairy1.png",   "x": int(WIDTH * 0.26), "y": 260, "w": 95},
    {"file": "fairy2.png",   "x": int(WIDTH * 0.38), "y": 245, "w": 95},
    {"file": "fairy3.png",   "x": int(WIDTH * 0.54), "y": 250, "w": 95},
    {"file": "fairiesss.png","x": int(WIDTH * 0.69), "y": 290, "w": 95},
    {"file": "fairy4.png",   "x": int(WIDTH * 0.15), "y": 315, "w": 95},
    {"file": "fairy5.png",   "x": int(WIDTH * 0.79), "y": 370, "w": 95},
]

fairies = []
for item in fairy_data:
    image = load_image(item["file"])
    if image:
        original_w, original_h = image.get_size()
        new_h = int(original_h * (item["w"] / original_w))
        image = pygame.transform.smoothscale(image, (item["w"], new_h))
    fairies.append({
        "image": image,
        "x": item["x"],
        "base_y": item["y"],
        "phase": item["x"] * 0.03
    })

# fonts
title_font = pygame.font.Font("Carattere-Regular.ttf", 30)
bubble_font = pygame.font.Font("Carattere-Regular.ttf", 26)
button_font = pygame.font.Font("Carattere-Regular.ttf", 14)
ending_font = pygame.font.Font("Carattere-Regular.ttf", 38)
small_font = pygame.font.Font("Carattere-Regular.ttf", 26)

# rectangles
title_rect = pygame.Rect(20, 20, 180, 55)

# main message bubble
bubble_rect = pygame.Rect(0, 90, 300, 140)
bubble_rect.centerx = WIDTH // 2

# choice box
choice_rect = pygame.Rect(0, 0, 180, 100)
choice_rect.midbottom = (WIDTH // 2, HEIGHT - 20)

button_width = 130
button_height = 30
button_gap = 10

keep_button = pygame.Rect(
    choice_rect.centerx - button_width // 2,
    choice_rect.y + 18,
    button_width,
    button_height
)

return_button = pygame.Rect(
    choice_rect.centerx - button_width // 2,
    keep_button.bottom + button_gap,
    button_width,
    button_height
)

# screen state
current_screen = "banquet"
screen_start_time = pygame.time.get_ticks()

# text helpers
def draw_text(surface, text, font, color, x, y, center=False):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    surface.blit(rendered, rect)

def draw_wrapped_text(surface, lines, font, color, rect):
    line_height = font.get_height() + 8
    total_height = len(lines) * line_height
    start_y = rect.centery - total_height // 2 + 20

    for i, line in enumerate(lines):
        text = font.render(line, True, color)
        text_rect = text.get_rect(center=(rect.centerx, start_y + i * line_height))
        surface.blit(text, text_rect)

def draw_button(surface, rect, text, mouse_pos):
    hovered = rect.collidepoint(mouse_pos)
    color = BUTTON_HOVER if hovered else BUTTON_BG
    pygame.draw.rect(surface, color, rect, border_radius=6)
    pygame.draw.rect(surface, BLACK, rect, width=2, border_radius=6)
    draw_text(surface, text, button_font, TEXT_DARK, rect.centerx, rect.centery, center=True)

def draw_scene(time_ms):
    screen.fill(BG_COLOR)

    if background:
        screen.blit(background, (0, 0))

    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), width=3)

    # title box
    pygame.draw.rect(screen, TITLE_BG, title_rect)
    pygame.draw.rect(screen, BORDER_COLOR, title_rect, width=3)
    draw_text(screen, "Banquet Hall", title_font, TEXT_DARK, title_rect.x + 12, title_rect.y + 8)

    # floating fairies
    seconds = time_ms / 1000.0
    for fairy in fairies:
        if fairy["image"]:
            float_offset = int(math.sin(seconds * 2.0 + fairy["phase"]) * 12)

            img_rect = fairy["image"].get_rect(
                topleft=(fairy["x"], fairy["base_y"] + float_offset)
            )

            glow = pygame.Surface((img_rect.width + 20, img_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.ellipse(glow, (255, 255, 255, 55), glow.get_rect())
            screen.blit(glow, (img_rect.x - 10, img_rect.y - 10))

            screen.blit(fairy["image"], img_rect.topleft)

    # popup animation
    popup_delay = 250
    pop_duration = 400
    elapsed = time_ms - screen_start_time

    if elapsed >= popup_delay:
        animation_time = elapsed - popup_delay
        progress = min(animation_time / pop_duration, 1)

        # pop effect
        scale = 0.2 + (0.8 * progress)

        bubble_w = int(bubble_rect.width * scale)
        bubble_h = int(bubble_rect.height * scale)

        animated_bubble = pygame.Rect(0, 0, bubble_w, bubble_h)
        animated_bubble.center = bubble_rect.center

        # draw speech bubble only when big enough
        if bubble_w > 20 and bubble_h > 20:
            temp = pygame.Surface((bubble_w, bubble_h), pygame.SRCALPHA)
            for i in range(bubble_h):
                t = i / max(bubble_h - 1, 1)
                r = int(79 + (166 - 79) * t)
                g = int(138 + (208 - 138) * t)
                b = int(79 + (141 - 79) * t)
                pygame.draw.line(temp, (r, g, b), (0, i), (bubble_w, i))

            rounded_mask = pygame.Surface((bubble_w, bubble_h), pygame.SRCALPHA)
            pygame.draw.rect(rounded_mask, (255, 255, 255), rounded_mask.get_rect(), border_radius=15)
            temp.blit(rounded_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(temp, animated_bubble.topleft)

            # speech arrow
            arrow_width = max(10, int(18 * scale))
            arrow_height = max(8, int(18 * scale))
            arrow_points = [
                (animated_bubble.centerx - arrow_width, animated_bubble.bottom),
                (animated_bubble.centerx + arrow_width, animated_bubble.bottom),
                (animated_bubble.centerx, animated_bubble.bottom + arrow_height)
            ]
            pygame.draw.polygon(screen, (166, 208, 141), arrow_points)

        # show text and buttons after popup finishes

        if progress > 0.95:
            bubble_lines = [
                "Thank you for helping Mariposa.",
                "We would like to reward you!",
                "Would you like to become a fairy?"
            ]
            draw_wrapped_text(screen, bubble_lines, bubble_font, WHITE, bubble_rect)

            # delay before showing buttons
            button_delay = 2000   # 👈 CHANGE THIS

            if animation_time > button_delay:
                pygame.draw.rect(screen, CHOICE_BG, choice_rect, border_radius=8)
                pygame.draw.rect(screen, BORDER_COLOR, choice_rect, width=3, border_radius=8)

                mouse_pos = pygame.mouse.get_pos()
                draw_button(screen, keep_button, "Keep Wings", mouse_pos)
                draw_button(screen, return_button, "Return to Human", mouse_pos)

def draw_keep_screen():
    if background:
        screen.blit(background, (0, 0))
    else:
        screen.fill(BG_COLOR)

    pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), width=3)

    # top left title
    end_title_box = pygame.Rect(20, 20, 190, 60)
    pygame.draw.rect(screen, TITLE_BG, end_title_box)
    pygame.draw.rect(screen, BORDER_COLOR, end_title_box, width=3)
    draw_text(screen, "End Screen", title_font, TEXT_DARK,
              end_title_box.x + 12, end_title_box.y + 12)

    # congratulations box
    congrats_box = pygame.Rect(0, 85, 550, 75)
    congrats_box.centerx = WIDTH // 2
    pygame.draw.rect(screen, TITLE_BG, congrats_box)
    pygame.draw.rect(screen, BORDER_COLOR, congrats_box, width=3)
    draw_text(screen, "Congratulations! You kept your wings!", ending_font, TEXT_DARK,
              congrats_box.centerx, congrats_box.centery, center=True)

    # thanks box
    thanks_box = pygame.Rect(0, 275, 220, 110)
    thanks_box.centerx = WIDTH // 2
    pygame.draw.rect(screen, TITLE_BG, thanks_box)
    pygame.draw.rect(screen, BORDER_COLOR, thanks_box, width=3)
    draw_text(screen, "Thanks for", small_font, TEXT_DARK,
              thanks_box.centerx, thanks_box.y + 28, center=True)
    draw_text(screen, "playing!", small_font, TEXT_DARK,
              thanks_box.centerx, thanks_box.y + 68, center=True)

    # credits box
    credits_box = pygame.Rect(0, 470, 220, 140)
    credits_box.centerx = WIDTH // 2 + 20
    pygame.draw.rect(screen, TITLE_BG, credits_box)
    pygame.draw.rect(screen, BORDER_COLOR, credits_box, width=3)

    credits_lines = ["Credits:", "Michelle", "Zoe", "Leesie", "Patricia"]
    for i, line in enumerate(credits_lines):
        draw_text(screen, line, small_font, TEXT_DARK,
                  credits_box.centerx,
                  credits_box.y + 15 + i * 24,
                  center=True)

def draw_return_screen():
    screen.fill((255, 240, 245))
    draw_text(screen, "You returned to human form.", ending_font, TEXT_DARK, WIDTH // 2, 220, center=True)
    draw_text(screen, "Thank you for helping Mariposa.", small_font, TEXT_DARK, WIDTH // 2, 290, center=True)

running = True
while running:
    time_ms = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_screen == "banquet":
                popup_delay = 0
                pop_duration = 250
                elapsed = time_ms - screen_start_time
                button_delay = 2000

                if elapsed >= popup_delay + pop_duration + button_delay:
                    if keep_button.collidepoint(event.pos):
                         current_screen = "keep"
                         keep_sound.play()
                    elif return_button.collidepoint(event.pos):
                        subprocess.Popen(["python", "fairies.py"])
                        running = False

    if current_screen == "banquet":
        draw_scene(time_ms)
    elif current_screen == "keep":
        draw_keep_screen()
    elif current_screen == "return":
        draw_return_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()