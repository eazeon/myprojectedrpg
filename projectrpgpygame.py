import pygame
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Project RPG")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
FONT = pygame.font.Font(None, 36)

# Game variables
money = 1000
purchased_items = []
fusion_results = []
selected_items = []

fusion_recipes = {
    frozenset(["Coup simple", "Épée courte"]): "Coup d'estoc a l'épée",
    frozenset(["Coup simple", "Épée longue"]): "Coup droit a l'épée",
    frozenset(["Coup simple", "Dague"]): "Frappe de dague",
    # Add more recipes as needed...
}

itemshop_items = ["Potion de soin", "Potion de poison", "Bombe légère", "Bombe lourde", "Bombe fumigène", "Filet"]

def draw_text(text, color, x, y, center=False):
    rendered_text = FONT.render(text, True, color)
    rect = rendered_text.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(rendered_text, rect)

def fusion_window():
    global purchased_items, selected_items
    running = True

    while running:
        screen.fill(WHITE)
        draw_text("Fusion des compétences", BLACK, SCREEN_WIDTH // 2, 50, center=True)

        y_offset = 150
        item_buttons = []
        for idx, item in enumerate(purchased_items):
            button_rect = pygame.Rect(100, y_offset + idx * 50, 200, 40)
            pygame.draw.rect(screen, GRAY, button_rect)
            draw_text(item, BLACK, button_rect.centerx, button_rect.centery, center=True)
            item_buttons.append((button_rect, item))

        # Selected items display
        draw_text("Éléments sélectionnés:", BLACK, 400, 150)
        for idx, item in enumerate(selected_items):
            draw_text(item, BLACK, 400, 200 + idx * 40)

        # Back button
        back_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 100, 40)
        pygame.draw.rect(screen, RED, back_button_rect)
        draw_text("Retour", WHITE, 100, SCREEN_HEIGHT - 80, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if back_button_rect.collidepoint(x, y):
                    running = False
                for button_rect, item in item_buttons:
                    if button_rect.collidepoint(x, y):
                        if item in selected_items:
                            selected_items.remove(item)
                        else:
                            selected_items.append(item)

def inventory_window():
    global purchased_items
    running = True

    while running:
        screen.fill(WHITE)
        draw_text("Inventaire", BLACK, SCREEN_WIDTH // 2, 50, center=True)

        y_offset = 150
        if purchased_items:
            for idx, item in enumerate(purchased_items):
                draw_text(item, BLACK, 100, y_offset + idx * 40)
        else:
            draw_text("Aucun objet acheté.", BLACK, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, center=True)

        back_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 100, 40)
        pygame.draw.rect(screen, RED, back_button_rect)
        draw_text("Retour", WHITE, 100, SCREEN_HEIGHT - 80, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                if back_button_rect.collidepoint(x, y):
                    running = False

def shop_window(title, items):
    global money, purchased_items
    running = True

    while running:
        screen.fill(WHITE)
        draw_text(title, BLACK, SCREEN_WIDTH // 2, 50, center=True)
        draw_text(f"Argent: {money} deullars", BLACK, SCREEN_WIDTH // 2, 100, center=True)

        y_offset = 150
        buttons = []
        for idx, (item_name, cost) in enumerate(items):
            item_text = f"{item_name} : {cost}"
            draw_text(item_text, BLACK, 100, y_offset + idx * 50)
            button_rect = pygame.Rect(600, y_offset + idx * 50, 150, 30)
            pygame.draw.rect(screen, GRAY, button_rect)
            draw_text("Acheter", BLACK, 675, y_offset + idx * 50 + 15, center=True)
            buttons.append((button_rect, item_name, cost))

        back_button_rect = pygame.Rect(50, SCREEN_HEIGHT - 100, 100, 40)
        pygame.draw.rect(screen, RED, back_button_rect)
        draw_text("Retour", WHITE, 100, SCREEN_HEIGHT - 80, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for button_rect, item_name, cost in buttons:
                    if button_rect.collidepoint(x, y):
                        if money >= cost:
                            money -= cost
                            purchased_items.append(item_name)
                        else:
                            print("Not enough money!")
                if back_button_rect.collidepoint(x, y):
                    running = False

def main_menu():
    global money
    running = True

    buttons = [
        {"text": "Entraîneur militaire", "action": lambda: shop_window("Entraîneur militaire", [("Coup simple", 100), ("Coup puissant", 250), ("Parade", 250)])},
        {"text": "Maître magicien", "action": lambda: shop_window("Maître magicien", [("Magie élémentaire Feu", 200), ("Magie élémentaire Air", 200), ("Magie élémentaire Eau", 200), ("Magie élémentaire Terre", 200), ("Magie d'illusion", 300), ("Magie psychique", 300)])},
        {"text": "Marchand militaire", "action": lambda: shop_window("Marchand militaire", [("Épée courte", 200), ("Épée longue", 350), ("Dague", 200), ("Hache de guerre", 250), ("Arc", 250), ("Bouclier", 350)])},
        {"text": "Marchand d'objets", "action": lambda: shop_window("Marchand d'objets", [("Potion de soin", 50), ("Potion de poison", 50), ("Bombe légère", 100), ("Bombe lourde", 250), ("Bombe fumigène", 100), ("Filet", 100)])},
        {"text": "Fusion des compétences", "action": lambda: fusion_window()}
    ]

    inventory_button_rect = pygame.Rect(SCREEN_WIDTH - 150, 20, 130, 40)

    while running:
        screen.fill(WHITE)

        # Draw main menu options
        draw_text("Project RPG", BLACK, SCREEN_WIDTH // 2, 50, center=True)
        draw_text(f"Argent : {money} deullars", BLACK, SCREEN_WIDTH // 2, 100, center=True)

        y_offset = 200
        button_rects = []
        for idx, button in enumerate(buttons):
            text_width = FONT.size(button["text"])[0] + 20
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - text_width // 2, y_offset + idx * 70 + (50 if button["text"] == "Fusion des compétences" else 0), text_width, 40)
            pygame.draw.rect(screen, GRAY, button_rect)
            draw_text(button["text"], BLACK, SCREEN_WIDTH // 2, y_offset + idx * 70 + 20 + (50 if button["text"] == "Fusion des compétences" else 0), center=True)
            button_rects.append((button_rect, button["action"]))

        # Draw inventory button
        pygame.draw.rect(screen, BLUE, inventory_button_rect)
        draw_text("Inventaire", WHITE, SCREEN_WIDTH - 85, 40, center=True)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                for button_rect, action in button_rects:
                    if button_rect.collidepoint(x, y):
                        action()
                if inventory_button_rect.collidepoint(x, y):
                    inventory_window()

# Start the game
main_menu()
