import pygame
import sys
import math


pygame.init()


# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Fashion Surprise Game")


# Load images
background_img_raw = pygame.image.load('background.png').convert()
character_base_img = pygame.image.load('character.png').convert_alpha()
mushroom_img = pygame.image.load('mushroom.png').convert_alpha()
fairy_img_raw = pygame.image.load('fairy.png').convert_alpha()


# Example: 7 outfits (adjust as needed)
outfit_images_raw = [
    pygame.image.load('outfit1.png').convert_alpha(),
    pygame.image.load('outfit2.png').convert_alpha(),
    pygame.image.load('outfit3.png').convert_alpha(),
    pygame.image.load('outfit4.png').convert_alpha(),
    pygame.image.load('outfit5.png').convert_alpha(),
    pygame.image.load('outfit6.png').convert_alpha(),
    pygame.image.load('outfit7.png').convert_alpha(),
]


# Sizes
character_size = (160, 240)  # Player size
mushroom_size = (180, 140)
fairy_size = (110, 110)
outfit_size = (140, 210)     # Outfit size to fit character


# Scale images
background_img = pygame.transform.scale(background_img_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
character_base_img = pygame.transform.scale(character_base_img, character_size)
mushroom_img = pygame.transform.scale(mushroom_img, mushroom_size)
fairy_img = pygame.transform.scale(fairy_img_raw, fairy_size)
outfit_images = [pygame.transform.scale(img, outfit_size) for img in outfit_images_raw]


# Load Carattere font
carattere_font = pygame.font.Font('Carattere.ttf', 28)


# Positions
# Left half center for mushroom + player
left_area_width = SCREEN_WIDTH // 2
combined_height = character_size[1] + mushroom_size[1] - 40  # overlap adjustment
middle_y = (SCREEN_HEIGHT - combined_height) // 2


mushroom_pos = (
    (left_area_width - mushroom_size[0]) // 2,
    middle_y + character_size[1] - 40
)
character_pos = (
    (left_area_width - character_size[0]) // 2,
    middle_y
)


# Fairy bottom left corner with margin
fairy_margin = 20
fairy_base_pos = (fairy_margin, SCREEN_HEIGHT - fairy_size[1] - fairy_margin)


# Chatbox smaller and right of fairy, vertically centered with fairy
chatbox_height = 40
chatbox_width = SCREEN_WIDTH - fairy_base_pos[0] - fairy_size[0] - 3 * fairy_margin
chatbox_pos = (
    int(fairy_base_pos[0] + fairy_size[0] + 10),
    int(fairy_base_pos[1] + (fairy_size[1] - chatbox_height) // 2)
)
chatbox_size = (int(chatbox_width), int(chatbox_height))

num_outfits = 4
cols = 2
rows = 2


# Calculate vertical spacing so all fit in right half with some top/bottom margin
right_area_top = 80
right_area_bottom = SCREEN_HEIGHT - 80
available_height = right_area_bottom - right_area_top
outfit_spacing_y = 15
total_outfit_height = rows * outfit_size[1] + (rows - 1) * outfit_spacing_y


# If total outfit height is larger than available height, reduce spacing
if total_outfit_height > available_height:
    outfit_spacing_y = max(5, (available_height - rows * outfit_size[1]) // (rows - 1))


# Horizontal positions for two columns in right half
right_area_left = SCREEN_WIDTH // 2 + 50
outfits_start_x_left = right_area_left
outfits_start_x_right = right_area_left + outfit_size[0] + 40
outfits_start_y = right_area_top


selected_outfit_index = None

# Create clickable rectangles for 6 outfits only
clickable_padding = 5
outfit_rects = []
for i in range(num_outfits):
    col = i % cols
    row = i // cols
    x = outfits_start_x_left if col == 0 else outfits_start_x_right
    y = outfits_start_y + row * (outfit_size[1] + outfit_spacing_y)
    rect = pygame.Rect(
        x - clickable_padding,
        y - clickable_padding,
        outfit_size[0] + 2 * clickable_padding,
        outfit_size[1] + 2 * clickable_padding
    )
    outfit_rects.append(rect)





# Outfit offset relative to character for perfect fit (adjust as needed)
outfit_offset_x = 10  # Adjust this value to fit the outfit on the character
outfit_offset_y = 13  # Adjust this value to fit the outfit on the character
outfit_pos_on_character = (
    character_pos[0] + outfit_offset_x,
    character_pos[1] + outfit_offset_y
)


def draw_chatbox(surface, text, font, rect, bg_color=(255, 255, 255, 180), text_color=(0, 0, 0)):
    chat_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(chat_surf, bg_color, chat_surf.get_rect(), border_radius=5)
    surface.blit(chat_surf, (rect.x, rect.y))


    rendered_text = font.render(text, True, text_color)
    surface.blit(rendered_text, (rect.x + 10, rect.y + (rect.height - rendered_text.get_height()) // 2))

# Calculate clickable rects slightly bigger than outfits
clickable_padding = 5
outfit_rects = []
for i in range(num_outfits):
    col = i % cols
    row = i // cols
    x = outfits_start_x_left if col == 0 else outfits_start_x_right
    y = outfits_start_y + row * (outfit_size[1] + outfit_spacing_y)
    rect = pygame.Rect(
        x - clickable_padding,
        y - clickable_padding,
        outfit_size[0] + 2 * clickable_padding,
        outfit_size[1] + 2 * clickable_padding
    )
    outfit_rects.append(rect)


clock = pygame.time.Clock()
running = True
start_ticks = pygame.time.get_ticks()


while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(outfit_rects):
                if rect.collidepoint(mouse_pos):
                    selected_outfit_index = i
                    break


    # Fairy bobbing animation
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000
    bob_offset = int(5 * math.sin(seconds * 2 * math.pi))
    fairy_pos = (fairy_base_pos[0], fairy_base_pos[1] + bob_offset)


    # Draw everything
    screen.blit(background_img, (0, 0))
    screen.blit(mushroom_img, mushroom_pos)
    screen.blit(character_base_img, character_pos)


    # Draw selected outfit on character with offset
    if selected_outfit_index is not None:
        outfit_pos_on_character = (
            character_pos[0] + outfit_offset_x,
            character_pos[1] + outfit_offset_y
        )
        screen.blit(outfit_images[selected_outfit_index], outfit_pos_on_character)


    # Draw outfits with translucent colored backgrounds and borders
    for i, rect in enumerate(outfit_rects):
        if i == selected_outfit_index:
            bg_color = (0, 255, 0, 100)  # translucent green
            border_color = (0, 255, 0)
            border_thickness = 4
        elif rect.collidepoint(mouse_pos):
            bg_color = (255, 255, 0, 100)  # translucent yellow
            border_color = (255, 255, 0)
            border_thickness = 3
        else:
            bg_color = (100, 100, 100, 60)  # translucent gray
            border_color = (200, 200, 200)
            border_thickness = 2


        bg_surf = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surf, bg_color, bg_surf.get_rect(), border_radius=8)
        screen.blit(bg_surf, rect.topleft)


        # Center outfit image inside clickable box
        outfit_img = outfit_images[i]
        img_x = rect.x + (rect.width - outfit_img.get_width()) // 2
        img_y = rect.y + (rect.height - outfit_img.get_height()) // 2
        screen.blit(outfit_img, (img_x, img_y))


        pygame.draw.rect(screen, border_color, rect, border_thickness, border_radius=8)


    # Draw fairy and chatbox
    screen.blit(fairy_img, fairy_pos)


    chatbox_rect = pygame.Rect(
        chatbox_pos[0],
        chatbox_pos[1],
        chatbox_size[0],
        chatbox_size[1]
    )
    chat_text = "Get ready for your surprise!"
    draw_chatbox(screen, chat_text, carattere_font, chatbox_rect)


    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()

