# girls who code project

import pygame
import sys

pygame.init()


# Window
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rainforest Escape")

#load the images
start_bg = pygame.image.load("Rainforest_Background.png").convert()
settings_bg = pygame.image.load("Rainforest_Background.png").convert()
menu_bg = pygame.image.load("Rainforest_Background.png").convert()
Mariposa_= pygame.image.load("Mariposa.png").convert_alpha()
Mariposa_=pygame.transform.scale(Mariposa_,(100, 100))

def start_screen():
    screen.blit(start_bg, (0, 0))

# Colors
WHITE = (255, 255, 255)
GREEN = (95, 143, 97)
LIGHT_GREEN = (207, 227, 207)
DARK_GREEN = (74, 116, 80)
BLACK = (0, 0, 0)

# Load font (replace with your .ttf file if you have one)
try:
    font = pygame.font.Font("Carattere-Regular.ttf", 28)
    big_font = pygame.font.Font("Carattere-Regular.ttf", 44)
except:
    font = pygame.font.SysFont("arial", 28)
    big_font = pygame.font.SysFont("arial", 44)

# Game state
current_screen = "start"

# Settings values
volume = 0.5
brightness = 1.0


# Button class
class Button:
    def __init__(self, text, x, y, w, h, action):
        self.text = text
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect, border_radius=8)
        text_surf = font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.x + 20, self.rect.y + 12))

    def check_click(self, pos):
        if self.rect.collidepoint(pos):
            return self.action
        return None

# Slider class
class Slider:
    def __init__(self, x, y, w, min_val, max_val, value):
        self.rect = pygame.Rect(x, y, w, 6)
        self.knob_x = x + int((value - min_val)/(max_val - min_val) * w)
        self.min_val = min_val
        self.max_val = max_val
        self.value = value
        self.dragging = False

    def draw(self):
        pygame.draw.rect(screen, DARK_GREEN, self.rect)
        pygame.draw.circle(screen, GREEN, (self.knob_x, self.rect.y+3), 10)

    def update(self, mouse_pos, mouse_pressed):
        if mouse_pressed:
            if abs(mouse_pos[0] - self.knob_x) < 15 and abs(mouse_pos[1] - self.rect.y) < 15:
                self.dragging = True
        else:
            self.dragging = False

        if self.dragging:
            self.knob_x = max(self.rect.x, min(mouse_pos[0], self.rect.x + self.rect.w))
            ratio = (self.knob_x - self.rect.x) / self.rect.w
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

        return self.value

# Sliders
volume_slider = Slider(300, 220, 300, 0, 1, volume)
brightness_slider = Slider(300, 320, 300, 0.3, 1.5, brightness)

# Helper
def draw_text(text, x, y, font_obj=font):
    txt = font_obj.render(text, True, BLACK)
    screen.blit(txt, (x, y))

# Screens
def start_screen():
    screen.blit(start_bg, (0, 0))
    draw_text("Rainforest Escape", 325, 100, big_font)
    return [
        Button("Start Game", 350, 250, 200, 50, "story"),
        Button("Settings", 350, 320, 200, 50, "settings")
    ]

def settings_screen(mouse_pos, mouse_pressed):
    screen.blit(settings_bg, (0, 0))
    
    global volume, brightness

    draw_text("Settings", 325, 100, big_font)

    draw_text(f"Volume: {volume:.2f}", 300, 180)
    volume = volume_slider.update(mouse_pos, mouse_pressed)
    volume_slider.draw()

    draw_text(f"Brightness: {brightness:.2f}", 300, 280)
    brightness = brightness_slider.update(mouse_pos, mouse_pressed)
    brightness_slider.draw()

    return [Button("Back", 350, 420, 200, 50, "start")]

def story_screen():
    draw_text("Mariposa", 375, 100, big_font)
    screen.blit(Mariposa_,(400, 200))
    draw_text("The rainforest magic has been stolen!", 325, 300)
    draw_text("Help the fairies restore it.", 325, 340)
    return [Button("Continue", 350, 385, 200, 50, "menu")]

def menu_screen():
    screen.blit(menu_bg, (0, 0))
    draw_text("Choose a Level", 325, 100, big_font)
    return [
        Button("Level 1", 350, 200, 200, 50, "game1"),
        Button("Level 2", 350, 260, 200, 50, "game2"),
        Button("Level 3", 350, 320, 200, 50, "game3"),
        Button("Level 4", 350, 380, 200, 50, "game4"),
    ]

def game_screen(title, next_screen="menu"):
    draw_text(title, 250, 200)
    return [Button("Back", 350, 400, 200, 50, next_screen)]

def end_screen():
    draw_text("Congratulations!", 325, 150, big_font)
    draw_text("You restored the magic!", 350, 250)
    return [Button("Play Again", 350, 350, 200, 50, "start")]

# Brightness overlay
def apply_brightness():
    if brightness < 1:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(int((1 - brightness) * 200))
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
    elif brightness > 1:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(int((brightness - 1) * 120))
        overlay.fill((255, 255, 255))
        screen.blit(overlay, (0, 0))

# Main loop
clock = pygame.time.Clock()

while True:
    screen.fill(LIGHT_GREEN)

    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]

    # Screen logic
    if current_screen == "start":
        buttons = start_screen()
    elif current_screen == "settings":
        buttons = settings_screen(mouse_pos, mouse_pressed)
    elif current_screen == "story":
        buttons = story_screen()
    elif current_screen == "menu":
        buttons = menu_screen()
    elif current_screen == "game1":
        buttons = game_screen("Game 1 - Flappy Bird")
    elif current_screen == "game2":
        buttons = game_screen("Game 2 - Matching")
    elif current_screen == "game3":
        buttons = game_screen("Game 3 - Squirrel Nuts")
    elif current_screen == "game4":
        buttons = game_screen("Game 4 - Banquet", "end")
    elif current_screen == "end":
        buttons = end_screen()

    # Draw buttons
    for b in buttons:
        b.draw()

    # Apply brightness effect
    apply_brightness()

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            for b in buttons:
                result = b.check_click(mouse_pos)
                if result:
                    current_screen = result

    pygame.display.flip()
    clock.tick(60)
