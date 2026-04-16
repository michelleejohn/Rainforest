import pygame
import random
import time


pygame.init()

# game variables
GAME_WIDTH = 800
GAME_HEIGHT = 600
card_size = (100,150)
white = (255,255,255)
flip_delay = .5
button_width = 150
button_height = 50
timer_limit = 15
grid_size = 4

# make game window
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Potion Matching")

# get the images
background_image = pygame.image.load("potionbg.png").convert()
pink_potion_image = pygame.image.load("pinkpotion.png").convert_alpha()
purple_potion_image = pygame.image.load("purplepotion.png").convert_alpha()
orange_potion_image = pygame.image.load("orangepotion.png").convert_alpha()
fairy_image = pygame.image.load("purplefairy.png").convert_alpha()

card_images = []
card_images.append(pink_potion_image)
card_images.append(purple_potion_image)
card_images.append(orange_potion_image)

# duplicate the images to create pairs
card_images = card_images * 2
# shuffling cards
random.shuffle(card_images)

# list that stores the state of each card 
# true: face up, false means its face down
card_states = [False] * (grid_size**2)

# variables to keep track of flipped cards, pairs, moves +timet
flipped_cards = []
flipped_pairs = 0
moves = 0
timer_start_time = time.time()

font = pygame.font.Font('carattere-regular.ttf', 28)

def point_in_rect(point, rect):
    x, y = point
    rect_x, rect_y, rect_width, rect_height = rect
    return (rect_x <= x <= rect_x + rect_width) and (rect_y <= y <= rect_y + rect_height)

def draw_timer():
    elapsed_time = max(0, int(time.time() - timer_start_time))
    remaining_time = max(0, timer_limit - elapsed_time)
    timer_text = font.render(f"Time: {remaining_time}s", True, white)
    window.blit(timer_text, (GAME_WIDTH - 150, 10))

def display_message(message):
    message_text = font.render(message, True, white)
    text_rect = message_text.get_rect(center=(GAME_WIDTH//2, GAME_HEIGHT//2))
    window.blit(message_text, text_rect)

def draw_restart_button():
    restart_button_rect = (GAME_WIDTH - button_width - 20, 20, button_width, button_height)
    pygame.draw.rect(window, white, restart_button_rect)
    restart_text = font.render("Restart", True, (0, 0, 0))
    text_rect = restart_text.get_rect(center=(restart_button_rect[0] + button_width // 2, restart_button_rect[1] + button_height // 2))
    window.blit(restart_text, text_rect)

# main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            restart_button_rect = (
                GAME_WIDTH - button_width - 20, 20, button_width, button_height)
            if point_in_rect((mouse_x, mouse_y), restart_button_rect):
                random.shuffle(card_images)
                card_states = [False] * (grid_size ** 2)
                flipped_cards = []
                flipped_pairs = 0
                moves = 0
                timer_start_time = time.time()  # Restart the timer
            else:
                col = mouse_x // card_size[0]
                row = mouse_y // card_size[1]
                index = row * grid_size + col
                if index < len(card_states) and not card_states[index] and len(flipped_cards) < 2:
                    card_states[index] = True
                    flipped_cards.append(index)
                    moves += 1

    window.blit(background_image, (0, 0))

    # Draw grid of cards
    for i in range(grid_size):
        for j in range(grid_size):
            index = i * grid_size + j
            pygame.draw.rect(window, white, (j * card_size[0],
                                             i * card_size[1], card_size[0], card_size[1]))
            if card_states[index] or index in flipped_cards:
                card = card_images[index]
            else:
                card = pygame.Surface(card_size)
                card.fill((100, 100, 100))
            card = pygame.transform.scale(card, (card_size[0] - 8, card_size[1] - 8))
            window.blit(card, (j * card_size[0] + 4, i * card_size[1] + 4))

    # Render moves counter
    moves_text = font.render(f"Moves: {moves}", True, white)
    window.blit(moves_text, (10, 10))

    # Draw restart game button
    draw_restart_button()

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
    if flipped_pairs == grid_size ** 2 // 2:
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