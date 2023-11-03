import pygame
import sys

# Initialize pygame
pygame.init()

# Window Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electrical Conduction Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)

# Font
font = pygame.font.Font(None, 28)

# Input boxes
input_boxes = {
    "length": {"rect": pygame.Rect(180, 100, 195, 40), "text": "", "label": "Length (m):"},
    "diameter_mm": {"rect": pygame.Rect(180, 150, 195, 40), "text": "", "label": "Diameter (mm):"},
    "voltage": {"rect": pygame.Rect(180, 200, 195, 40), "text": "", "label": "Voltage (V):"}
}

# Dropdown menus
dropdowns = {
    "material": {"rect": pygame.Rect(500, 100, 200, 40), "options": ["Gold", "Silver", "Copper", "Aluminum", "Graphite"], "selected": None, "label": "Material:"},
    "awg": {"rect": pygame.Rect(530, 150, 200, 40), "options": ["AWG 10", "AWG 12", "AWG 14"], "selected": None, "label": "AWG:"}
}

active_box = None
# Variables adicionales
hovering_button = False

def draw_ui():
    screen.fill(WHITE)
    
    # Draw input boxes
    for key, box in input_boxes.items():
        pygame.draw.rect(screen, LIGHT_GRAY, box["rect"])
        txt_surface = font.render(box["text"], True, BLACK)
        screen.blit(txt_surface, (box["rect"].x + 5, box["rect"].y + 5))
        label_surface = font.render(box["label"], True, BLACK)
        screen.blit(label_surface, (box["rect"].x - 150, box["rect"].y + 5))
    
    # Draw dropdown menus
    for key, dropdown in dropdowns.items():
        pygame.draw.rect(screen, LIGHT_GRAY, dropdown["rect"])
        selected_text = dropdown["selected"] if dropdown["selected"] else "Select"
        txt_surface = font.render(selected_text, True, BLACK)
        screen.blit(txt_surface, (dropdown["rect"].x + 5, dropdown["rect"].y + 5))
        label_surface = font.render(dropdown["label"], True, BLACK)
        screen.blit(label_surface, (dropdown["rect"].x - 150, dropdown["rect"].y + 5))
    
    # Draw "Start Simulation" button
    btn_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    btn_color = BLUE if not hovering_button else (50, 150, 255)  # Cambiar color si el mouse está sobre el botón
    pygame.draw.rect(screen, btn_color, btn_rect)
    btn_surface = font.render("Start Simulation", True, WHITE)
    screen.blit(btn_surface, (btn_rect.x + 10, btn_rect.y + 10))

def main():
    global active_box, hovering_button
    running = True
    while running:
        hovering_button = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                for key, box in input_boxes.items():
                    if box["rect"].collidepoint(event.pos):
                        active_box = key
                        break
                else:
                    active_box = None
            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                else:
                    input_boxes[active_box]["text"] += event.unicode

        # Verificar si el mouse está sobre el botón
        mouse_pos = pygame.mouse.get_pos()
        btn_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
        if btn_rect.collidepoint(mouse_pos):
            hovering_button = True

        draw_ui()
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()