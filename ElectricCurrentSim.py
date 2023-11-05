import pygame
import sys
from Logica import calculate_resistance, calculate_current, calculate_power, drift_velocity, electron_travel_time 

# Initialize pygame
pygame.init()

# Window Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Electrical Conduction Simulation")

btn_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 28)
# Cylinder representation
CYLINDER_RECT = pygame.Rect(WIDTH // 4, HEIGHT - 150, WIDTH // 2, 100)

# Random walk option
random_walk_option = {"rect": pygame.Rect(WIDTH // 4, HEIGHT - 200, 20, 20), "checked": False, "label": "Show Random Walk"}
# AWG to mm conversion (assuming some values for simplicity)
def awg_to_mm(awg):
    if awg == "0000":
        awg_num = -3
    elif awg == "000":
        awg_num = -2
    elif awg == "00":
        awg_num = -1
    else:
        awg_num = int(awg)
    return 0.127 * 92 ** ((36 - awg_num) / 39)

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
    "length": {"rect": pygame.Rect(180, 100, 195, 40), "text": "", "label": "Length (m):", "active": True},
    "diameter_mm": {"rect": pygame.Rect(180, 200, 195, 40), "text": "", "label": "Diameter (mm):", "active": True},
    "voltage": {"rect": pygame.Rect(180, 250, 195, 40), "text": "", "label": "Voltage (V):", "active": True},
    "awg": {"rect": pygame.Rect(530, 150, 195, 40), "text": "", "label": "AWG (000-40):", "active": False}
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

def start_simulation():
    simulation_running = True
    while simulation_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulation_running = False
                pygame.quit()
                sys.exit()

            # Check for random walk checkbox click
            if event.type == pygame.MOUSEBUTTONDOWN and random_walk_option["rect"].collidepoint(event.pos):
                random_walk_option["checked"] = not random_walk_option["checked"]

        # Aquí irá la lógica de la simulación y la visualización de los electrones

        # Dibuja la casilla de verificación de caminata aleatoria en la pantalla de simulación
        screen.fill(WHITE)  # Limpia la pantalla
        pygame.draw.rect(screen, BLACK, random_walk_option["rect"], 2)
        if random_walk_option["checked"]:
            pygame.draw.line(screen, BLACK, random_walk_option["rect"].topleft, random_walk_option["rect"].bottomright, 2)
            pygame.draw.line(screen, BLACK, random_walk_option["rect"].bottomleft, random_walk_option["rect"].topright, 2)
        label_surface = font.render("Show Random Walk", True, BLACK)
        screen.blit(label_surface, (random_walk_option["rect"].x + 30, random_walk_option["rect"].y))

        pygame.display.flip()

def draw_ui():
    screen.fill(WHITE)
    
    # Draw input boxes
    for key, box in input_boxes.items():
        box_color = LIGHT_GRAY if box["active"] else (220, 220, 220)  # Cambia el color si la caja está inactiva
        pygame.draw.rect(screen, box_color, box["rect"])
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
        awg_value = input_boxes["awg"]["text"]

    # Draw AWG to mm conversion
    awg_value = input_boxes["awg"]["text"]
    special_awgs = ["0000", "000", "00"]
    if awg_value.isdigit() and 0 <= int(awg_value) <= 40 or awg_value in special_awgs:
        diameter_mm = awg_to_mm(awg_value)
        conversion_text = f"Conversion (AWG {awg_value}): {diameter_mm:.2f} mm"
        conversion_surface = font.render(conversion_text, True, BLACK)
        screen.blit(conversion_surface, (WIDTH // 2 - conversion_surface.get_width() // 2, 480))



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
                # Check if the random walk option was clicked
                if random_walk_option["rect"].collidepoint(event.pos):
                    random_walk_option["checked"] = not random_walk_option["checked"]

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
                                    input_boxes["diameter_mm"]["active"] = False
                                    input_boxes["awg"]["active"] = True
                                else:
                                    input_boxes["awg"]["text"] = ""  # Clear the AWG box
                                    input_boxes["awg"]["active"] = False
                                    input_boxes["diameter_mm"]["active"] = True
                                active_dropdown = None
                                break
            if event.type == pygame.KEYDOWN and active_box and input_boxes[active_box]["active"]:
                if event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["text"] = input_boxes[active_box]["text"][:-1]
                else:
                    input_boxes[active_box]["text"] += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN and btn_rect.collidepoint(event.pos):
                start_simulation()

        draw_ui()

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