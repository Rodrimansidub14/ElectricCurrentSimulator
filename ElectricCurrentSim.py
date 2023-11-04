import pygame
import sys
from Logica import calculate_resistance, calculate_current, calculate_power, drift_velocity, electron_travel_time 

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

# AWG to mm conversion (assuming some values for simplicity)
AWG_TO_MM = {
    "AWG 10": 2.588,
    "AWG 12": 2.053,
    "AWG 14": 1.628
}

# Particle density for materials (assuming some values for simplicity)
MATERIAL_DENSITY = {
    "Gold": "1.0 x 10^28",
    "Silver": "1.1 x 10^28",
    "Copper": "1.2 x 10^28",
    "Aluminum": "1.3 x 10^28",
    "Graphite": "1.4 x 10^28"
}

# Input boxes
input_boxes = {
    "length": {"rect": pygame.Rect(180, 100, 195, 40), "text": "", "label": "Length (m):"},
    "diameter_mm": {"rect": pygame.Rect(180, 200, 195, 40), "text": "", "label": "Diameter (mm):"},
    "voltage": {"rect": pygame.Rect(180, 250, 195, 40), "text": "", "label": "Voltage (V):"}
}

# Dropdown menus
dropdowns = {
    "diameter_unit": {"rect": pygame.Rect(180, 150, 195, 40), "options": ["mm", "AWG"], "selected": "mm", "label": "Unit:"},
    "material": {"rect": pygame.Rect(530, 100, 200, 40), "options": ["Gold", "Silver", "Copper", "Aluminum", "Graphite"], "selected": None, "label": "Material:"}
}

active_box = None
active_dropdown = None
hovering_button = False
def draw_awg_conversion():
    diameter_unit = dropdowns["diameter_unit"]["selected"]
    if diameter_unit == "AWG":
        awg_value = input_boxes["diameter_mm"]["text"]
        if awg_value in AWG_TO_MM:
            mm_value = AWG_TO_MM[awg_value]
            conversion_text = f"Conversion ({awg_value}): {mm_value} mm"
            conversion_surface = font.render(conversion_text, True, BLACK)
            screen.blit(conversion_surface, (WIDTH // 2 - conversion_surface.get_width() // 2, 280))

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

        # Draw particle density for selected material
    material = dropdowns["material"]["selected"]
    if material:
        density_text = f"Particle Density ({material}): {MATERIAL_DENSITY[material]}"
        density_surface = font.render(density_text, True, BLACK)
        screen.blit(density_surface, (WIDTH // 2 - density_surface.get_width() // 2, 530))
     

        # Draw AWG to mm conversion
        draw_awg_conversion()
    # Draw dropdown options if active
    if active_dropdown:
        dropdown = dropdowns[active_dropdown]
        for i, option in enumerate(dropdown["options"]):
            rect = pygame.Rect(dropdown["rect"].x, dropdown["rect"].y + (i+1)*40, dropdown["rect"].width, 40)
            pygame.draw.rect(screen, LIGHT_GRAY, rect)
            option_surface = font.render(option, True, BLACK)
            screen.blit(option_surface, (rect.x + 5, rect.y + 5))
            
    # Draw "Start Simulation" button
    btn_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
    btn_color = BLUE if not hovering_button else (50, 150, 255)
    pygame.draw.rect(screen, btn_color, btn_rect)
    btn_surface = font.render("Start Simulation", True, WHITE)
    screen.blit(btn_surface, (btn_rect.x + 10, btn_rect.y + 10))

def main():
    global active_box, active_dropdown, hovering_button
    running = True
    error_message = ""

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
                
                # Handle dropdowns
                for key, dropdown in dropdowns.items():
                    if dropdown["rect"].collidepoint(event.pos):
                        if active_dropdown == key:
                            active_dropdown = None
                        else:
                            active_dropdown = key
                        break
                    elif active_dropdown:
                        for i, option in enumerate(dropdowns[active_dropdown]["options"]):
                            rect = pygame.Rect(dropdown["rect"].x, dropdown["rect"].y + (i+1)*40, dropdown["rect"].width, 40)
                            if rect.collidepoint(event.pos):
                                dropdowns[active_dropdown]["selected"] = option
                                if active_dropdown == "diameter_unit" and option == "AWG":
                                    input_boxes["diameter_mm"]["text"] = ""  # Clear the diameter box
                                active_dropdown = None
                                break
            if event.type == pygame.KEYDOWN and active_box:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                else:
                    input_boxes[active_box]["text"] += event.unicode

        draw_ui()

        # Show error message if exists
        if error_message:
            error_surface = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (WIDTH // 2 - error_surface.get_width() // 2, 400))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()