
import pygame
import random
import time


pygame.init()

# game variables
GAME_WIDTH = 800
GAME_HEIGHT = 600
card_size = (150, 150)
white = (255, 255, 255)
black = (0, 0, 0)
flip_delay = 0.5
button_width = 150
button_height = 50
timer_limit = 60
grid_size = 3

grid_origin_x = (GAME_WIDTH - grid_size * card_size[0]) // 2
grid_origin_y = 50

# make game window
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Potion Matching")

# get the images
background_image = pygame.transform.scale(pygame.image.load("potionmatching.png").convert(), (GAME_WIDTH, GAME_HEIGHT))
pink_potion_image = pygame.image.load("pinkpotion.png").convert_alpha()
purple_potion_image = pygame.image.load("purplepotion.png").convert_alpha()
orange_potion_image = pygame.image.load("orangepotion.png").convert_alpha()
fairy_image = pygame.image.load("purplefairy.png").convert_alpha()
fairy_image = pygame.transform.scale(fairy_image, (120, 120))

cardback_image = pygame.image.load("cardback.png").convert_alpha()

card_images = [pink_potion_image, purple_potion_image, orange_potion_image] * 3
random.shuffle(card_images)

# list that stores the state of each card 
# true: face up, false means its face down
card_states = [False] * (grid_size**2)

# variables to keep track of flipped cards, pairs, moves + timer
flipped_cards = []
flipped_pairs = 0
target_pairs = 3
moves = 0
timer_start_time = None

font = pygame.font.Font('carattere-regular.ttf', 28)
show_intro = True
current_message_index = 0
intro_messages = [
    "Mix and Match Magical Potions!",
    "Tap two sparkling potion bottles to reveal their magical secrets.",
    "Find matching pairs bubbling with the same ingredients.",
    "Clear the board by matching all the potions."
]

def point_in_rect(point, rect):
    x, y = point
    rect_x, rect_y, rect_width, rect_height = rect
    return (rect_x <= x <= rect_x + rect_width) and (rect_y <= y <= rect_y + rect_height)

def draw_timer():
    elapsed_time = max(0, int(time.time() - timer_start_time))
    remaining_time = max(0, timer_limit - elapsed_time)
    timer_text = font.render(f"Time: {remaining_time}s", True, black)
    timer_rect = pygame.Rect(GAME_WIDTH - 200, 10, 180, 40)
    pygame.draw.rect(window, white, timer_rect)
    pygame.draw.rect(window, black, timer_rect, 2)
    text_rect = timer_text.get_rect(center=(timer_rect.centerx, timer_rect.centery))
    window.blit(timer_text, text_rect)

def display_message(message):
    message_text = font.render(message, True, white)
    text_rect = message_text.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2))
    window.blit(message_text, text_rect)

def draw_intro_screen():
    window.blit(background_image, (0, 0))
    overlay = pygame.Surface((GAME_WIDTH, GAME_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    window.blit(overlay, (0, 0))

    box_rect = pygame.Rect(0, GAME_HEIGHT - 180, GAME_WIDTH, 180)
    box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    box_surface.fill((255, 255, 255, 180))
    window.blit(box_surface, box_rect.topleft)
    pygame.draw.rect(window, black, box_rect, 3, border_radius=16)

    text_y = box_rect.y + 20
    line_height = 36

    intro_font = pygame.font.Font('carattere-regular.ttf', 28)
    line = intro_messages[current_message_index]
    line_surf = intro_font.render(line, True, black)
    text_rect = line_surf.get_rect(center=(GAME_WIDTH // 2, box_rect.centery))
    window.blit(line_surf, text_rect)

    hint_font = pygame.font.Font('carattere-regular.ttf', 18)
    if current_message_index < len(intro_messages) - 1:
        hint_text = "Click to continue"
    else:
        hint_text = "Press any key or click to start"
    hint_surf = hint_font.render(hint_text, True, black)
    hint_rect = hint_surf.get_rect(center=(GAME_WIDTH // 2, box_rect.bottom - 38))
    window.blit(hint_surf, hint_rect)

    window.blit(fairy_image, (20, box_rect.y + box_rect.height - fairy_image.get_height() - 10))


# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif show_intro and event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            if current_message_index < len(intro_messages) - 1:
                current_message_index += 1
            else:
                show_intro = False
                timer_start_time = time.time()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x = mouse_x - grid_origin_x
            rel_y = mouse_y - grid_origin_y
            if 0 <= rel_x < grid_size * card_size[0] and 0 <= rel_y < grid_size * card_size[1]:
                col = rel_x // card_size[0]
                row = rel_y // card_size[1]
                index = int(row) * grid_size + int(col)
                if index < len(card_states) and not card_states[index] and len(flipped_cards) < 2:
                    card_states[index] = True
                    flipped_cards.append(index)
                    moves += 1

    if show_intro:
        draw_intro_screen()
        pygame.display.flip()
        continue

    window.blit(background_image, (0, 0))

    # Draw grid of cards
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            card_rect = pygame.Rect(
                grid_origin_x + j * card_size[0],
                grid_origin_y + i * card_size[1],
                card_size[0],
                card_size[1]
            )
            pygame.draw.rect(window, white, card_rect)
            if card_states[index] or index in flipped_cards:
                card = card_images[index]
            else:
                card = cardback_image
            card = pygame.transform.scale(card, (card_size[0] - 8, card_size[1] - 8))
            window.blit(card, (card_rect.x + 4, card_rect.y + 4))

    # Render moves counter
    moves_text = font.render(f"Moves: {moves}", True, white)
    window.blit(moves_text, (10, 10))

    # Draw timer
    draw_timer()

    # Check for matched pairs
    if len(flipped_cards) == 2:
        time.sleep(flip_delay)
        if card_images[flipped_cards[0]] == card_images[flipped_cards[1]]:
            flipped_pairs += 1
            flipped_cards = []
        else:
            card_states[flipped_cards[0]] = False
            card_states[flipped_cards[1]] = False
            flipped_cards = []

    # Check for game over
    if flipped_pairs == target_pairs:
        display_message("Congratulations! You found all the pairs!")
        pygame.display.flip()
        time.sleep(2)  # Display the message for 2 seconds
        running = False

    # Check for time limit reached
    elapsed_time = time.time() - timer_start_time
    if elapsed_time >= timer_limit:
        display_message("Time's up! You lost the game.")
        pygame.display.flip()
        time.sleep(2)  # Display the message for 2 seconds
        running = False

    pygame.display.flip()

pygame.quit()
