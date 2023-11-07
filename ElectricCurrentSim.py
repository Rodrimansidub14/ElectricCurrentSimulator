import pygame
import sys
from Logica import calculate_resistance, calculate_current, calculate_power, drift_velocity, electron_travel_time 
import random
import math
# Initialize pygame
pygame.init()
error_message = ""
fps = pygame.time.Clock()
# Window Configuration
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF) # Added DOUBLEBUF for double buffering
pygame.display.set_caption("Electrical Conduction Simulation")
MATERIALS = {
    "Gold": {"resistivity": 2.44e-8, "particle_density": 5.9e28},
    "Silver": {"resistivity": 1.59e-8, "particle_density": 5.86e28},
    "Copper": {"resistivity": 1.68e-8, "particle_density": 8.5e28},
    "Aluminum": {"resistivity": 2.82e-8, "particle_density": 6.02e28},
    "Graphite": {"resistivity": 7.837e-5, "particle_density": 2.2e23}
}
btn_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 50)
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 0, 255)
LIGHT_BLUE = (255, 255, 255)

# Font
font = pygame.font.Font(None, 28)
# Cylinder representation
CYLINDER_RECT = pygame.Rect(WIDTH // 4, HEIGHT - 345, WIDTH // 2, 100)

# Random walk option
random_walk_option = {"rect": pygame.Rect(WIDTH // 4, HEIGHT - 85, 20, 20), "checked": False, "label": "Show Random Walk"}
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



# Constants
WIDTH, HEIGHT = 800, 600
CYLINDER_COLOR = (150, 150, 150)  # Esto es un color gris para el cilindro. Puedes cambiarlo a lo que quieras.
CYLINDER_RECT = pygame.Rect(WIDTH // 4, HEIGHT - 345, WIDTH // 2, 100)
LIGHT_BLUE = (173, 216, 230)  # Un color azul claro para los círculos.
ELECTRON_RADIUS = 0.05
NUM_ELECTRONS = 100
NUM_COLUMNS = 10
COLUMN_SPACING = CYLINDER_RECT.width // (NUM_COLUMNS + 1)
ELECTRON_SPACING = 10  # Vertical spacing between electrons
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

    if error_message:
        error_surface = font.render(error_message, True, RED)
        screen.blit(error_surface, (WIDTH // 2 - error_surface.get_width() // 2, 400))
class Atom:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 5

    def draw(self, screen):
        pygame.draw.circle(screen, LIGHT_BLUE, (self.x, self.y), self.radius)


ELECTRON_SPEED = 1

class Electron:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 2
        self.color = BLUE
        self.speed = 0.2  # Esta será la velocidad base para el movimiento preferencial

    def move(self):
        # Este método movería al electrón con una velocidad constante
        self.x += self.speed
    def draw(self, screen):
            # Dibuja el electrón en la pantalla
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def brownian_motion(self, step_size = 10):
        # Elige una dirección aleatoria
        angle = random.uniform(0, 2 * math.pi)
        dx = step_size * math.cos(angle)
        dy = step_size * math.sin(angle)

        # Actualiza la posición del electrón
        self.x += dx
        self.y += dy

    def distance_to(self, target_x, target_y):
        # Calcula la distancia euclidiana hasta un objetivo
        return math.sqrt((self.x - target_x)**2 + (self.y - target_y)**2)
    
    def random_walk_with_preference(self, ELECTRON_SPEED):
        # Elige aleatoriamente una dirección con preferencia hacia la derecha
        directions = [-ELECTRON_SPEED, 0, ELECTRON_SPEED]
        self.x += random.choices(directions, weights=[1, 1, 3])[0]  # Mayor peso hacia la derecha
        self.y += random.choice(directions)
    def set_position(self, x, y):
        self.x = x
        self.y = y

def move_electron_to_random_circle(electron, circles):
    # Elige un círculo destino aleatoriamente de la lista, exceptuando el círculo actual
    current_circle_index = circles.index((electron.x, electron.y))
    possible_next_circles = circles[current_circle_index+1:]
    if not possible_next_circles:  # Si no hay más círculos, el electrón 'sale' del cilindro
        return 'exit'
    target_circle = random.choice(possible_next_circles)
    
    # Establece la posición del electrón a la del círculo destino
    electron.set_position(target_circle[0], target_circle[1])
    return 'moved'
        
pygame.init()

def start_simulation():
    global error_message

    try:
        length = float(input_boxes["length"]["text"])
        diameter_unit = dropdowns["diameter_unit"]["selected"]
        if diameter_unit == "AWG":
            awg_value = input_boxes["awg"]["text"]
            diameter = awg_to_mm(awg_value)
        else:
            diameter = float(input_boxes["diameter_mm"]["text"])
        material = dropdowns["material"]["selected"]
        voltage = float(input_boxes["voltage"]["text"])

        if not (length and diameter and material and voltage):
            error_message = "Por favor, ingrese todos los valores necesarios."
            return

    except ValueError:
        error_message = "Por favor, ingrese valores válidos."
    except ZeroDivisionError:
        error_message = "Error: División por cero."
    except Exception as e:
        error_message = f"Error: {str(e)}"

    if error_message:
        print(error_message)

    simulation_running = True
    length = float(input_boxes["length"]["text"])
    diameter_unit = dropdowns["diameter_unit"]["selected"]
    if diameter_unit == "AWG":
        awg_value = input_boxes["awg"]["text"]
        special_awgs = ["0000", "000", "00"]
        if awg_value.isdigit() and 0 <= int(awg_value) <= 40 or awg_value in special_awgs:
            diameter = awg_to_mm(awg_value)
        else:
            print("Invalid AWG value.")
            return
    else:
        diameter = float(input_boxes["diameter_mm"]["text"])
    material = dropdowns["material"]["selected"]

    if not diameter or not material:
        
        error_message = "Por favor, ingrese todos los valores necesarios."
        return

    # Convertir los valores de cadena a flotante (si es necesario)
    length = float(length)
    diameter = float(diameter)

    exit_button = pygame.Rect(WIDTH - 100, 10, 80, 30)

    # Definir el número de columnas y el espacio entre columnas
    NUM_COLUMNS = 10
    COLUMN_SPACING = CYLINDER_RECT.width // (NUM_COLUMNS )
    ELECTRON_SPACING = 10  # Espacio vertical entre electrones

    # Crear electrones en múltiples columnas
    electrons = []
    for i in range(NUM_COLUMNS):
        column_x = CYLINDER_RECT.left + (i + 1) * COLUMN_SPACING
        for j in range(NUM_ELECTRONS // NUM_COLUMNS):
            electron_y = CYLINDER_RECT.top + j * ELECTRON_SPACING + ELECTRON_SPACING // 2
            electrons.append(Electron(column_x, electron_y))
    # Crear átomos
    atoms = []
    for i in range(0, CYLINDER_RECT.width, 20):  # Espaciado horizontal de 20 píxeles
        for j in range(0, CYLINDER_RECT.height, 20):  # Espaciado vertical de 20 píxeles
            atoms.append(Atom(CYLINDER_RECT.left + i, CYLINDER_RECT.top + j))

 # Variables para la caminata aleatoria
    random_walk_active = False
    circles = []
    num_circles = 15
    circle_radius = 8
    horizontal_spacing = 5 * circle_radius 
    vertical_spacing = 2 * circle_radius

    while simulation_running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                simulation_running = False
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.collidepoint(event.pos):
                    simulation_running = False
                    return
                if random_walk_option["rect"].collidepoint(event.pos):
                    random_walk_option["checked"] = not random_walk_option["checked"]
                    random_walk_active = not random_walk_active
                    if random_walk_active:
                         # Inicializa la simulación de caminata aleatoria con círculos estáticos
                        circles.clear()
                        num_circles = 45
                        circle_radius = 5
                        horizontal_spacing = 5 * circle_radius + 5
                        vertical_spacing = 4 * circle_radius +4

                        circles_horizontal = int(CYLINDER_RECT.width / horizontal_spacing)
                        circles_vertical = int(CYLINDER_RECT.height / vertical_spacing)
                        circles_to_draw = min(num_circles, circles_horizontal * circles_vertical)



                        total_vertical_space = circles_vertical * (circle_radius * 2 + vertical_spacing) - vertical_spacing
                        total_horizontal_space = circles_horizontal * (2 * circle_radius) + (circles_horizontal - 1) * horizontal_spacing

                       
                        vertical_margin = (CYLINDER_RECT.height - total_vertical_space) // 2

                        # Asegúrate de que el margen vertical no sea negativo
                        if vertical_margin < 0:
                            print("Los círculos no caben verticalmente dentro del cilindro con el espaciado actual.")
                            vertical_margin = 0

                        start_y = CYLINDER_RECT.top + vertical_margin
                        start_x = CYLINDER_RECT.left + (CYLINDER_RECT.width - total_horizontal_space) // 2
                        count = 0
                        for i in range(circles_horizontal):
                            for j in range(circles_vertical):
                                if count >= circles_to_draw:
                                    break
                                x = start_x + i * (2 * circle_radius + horizontal_spacing)
                                y = start_y + j * (2 * circle_radius + vertical_spacing)
                                circles.append((x, y))
                                count += 1

        if random_walk_active:
            # Dibuja los círculos estáticos en la pantalla
            pygame.draw.rect(screen, LIGHT_GRAY, CYLINDER_RECT)
            for x, y in circles:
                if CYLINDER_RECT.inflate(-circle_radius * 2, -circle_radius * 2).collidepoint(x, y):
                    pygame.draw.circle(screen, BLUE, (x, y), circle_radius)

            # Mueve el electrón a un círculo aleatorio
            status = move_electron_to_random_circle(electron, circles)

            if status == 'exit':
                print("El electrón ha salido del cilindro.")
                simulation_running = False  # O cualquier otra acción que desees realizar
                continue
            # Verifica los límites para mantener al electrón dentro del cilindro
            if electron.x - electron.radius < CYLINDER_RECT.left:
                electron.x = CYLINDER_RECT.left + electron.radius
            elif electron.x + electron.radius > CYLINDER_RECT.right:
                electron.x = CYLINDER_RECT.right - electron.radius

            if electron.y - electron.radius < CYLINDER_RECT.top:
                electron.y = CYLINDER_RECT.top + electron.radius
            elif electron.y + electron.radius > CYLINDER_RECT.bottom:
                electron.y = CYLINDER_RECT.bottom - electron.radius

            # Dibuja el electrón
            electron.draw(screen)
        else:
            # Aquí irá la lógica de la simulación y la visualización de los electrones

            # Dibuja el cilindro
            pygame.draw.rect(screen, LIGHT_GRAY, CYLINDER_RECT)
            cylinder_label_surface = font.render("Conductor", True, BLACK)
            screen.blit(cylinder_label_surface, (CYLINDER_RECT.centerx - cylinder_label_surface.get_width() // 2, CYLINDER_RECT.top - 60))

            # Dibuja la diferencia de potencial debajo del cilindro
            pygame.draw.circle(screen, BLUE, (CYLINDER_RECT.left+180, CYLINDER_RECT.bottom + 50), 20)
            pygame.draw.circle(screen, RED, (CYLINDER_RECT.right-180, CYLINDER_RECT.bottom + 50), 20)
            plus_surface = font.render("-", True, WHITE)
            minus_surface = font.render("+", True, WHITE)
            screen.blit(plus_surface, (CYLINDER_RECT.left+177, CYLINDER_RECT.bottom + 40))
            screen.blit(minus_surface, (CYLINDER_RECT.right-185, CYLINDER_RECT.bottom + 40))

            # Coordenadas de inicio y fin para el cable positivo (rojo)
            start_pos_red = (CYLINDER_RECT.left, CYLINDER_RECT.bottom)
            end_pos_red = (CYLINDER_RECT.left, CYLINDER_RECT.bottom + 50)
            start_pos_red2 = (CYLINDER_RECT.left, CYLINDER_RECT.bottom+50)
            end_pos_red2 = (CYLINDER_RECT.left+160, CYLINDER_RECT.bottom + 50)
            # Coordenadas de inicio y fin para el cable negativo (azul)
            start_pos_blue = (CYLINDER_RECT.right, CYLINDER_RECT.bottom)
            end_pos_blue = (CYLINDER_RECT.right , CYLINDER_RECT.bottom + 50)
            start_pos_blue2 = (CYLINDER_RECT.right, CYLINDER_RECT.bottom+50)
            end_pos_blue2 = (CYLINDER_RECT.right-160 , CYLINDER_RECT.bottom + 50)
            # Dibuja los cables
            pygame.draw.line(screen, BLACK, start_pos_red, end_pos_red, 3)  # Cable positivo (rojo)
            pygame.draw.line(screen, BLACK, start_pos_red2, end_pos_red2, 3)
            pygame.draw.line(screen, BLACK, start_pos_blue, end_pos_blue, 3)  # Cable negativo (azul)
            pygame.draw.line(screen, BLACK, start_pos_blue2, end_pos_blue2, 3)  
            # Coordenadas para la flecha de corriente
        # Coordenadas para la flecha de corriente
            # Coordenadas para la flecha de corriente
        # Coordenadas para la flecha de corriente
            start_arrow = (CYLINDER_RECT.left, CYLINDER_RECT.top - 20)  # 40 píxeles arriba del cilindro
            end_arrow = (CYLINDER_RECT.right, CYLINDER_RECT.top - 20)

            # Dibuja el cuerpo de la flecha
            pygame.draw.line(screen, PINK, start_arrow, end_arrow, 3)

            # Dibuja la punta de la flecha (triángulo) en el extremo izquierdo
            pygame.draw.polygon(screen, PINK, [(start_arrow[0], start_arrow[1]), 
                                                (start_arrow[0] + 10, start_arrow[1] - 10), 
                                                (start_arrow[0] + 10, start_arrow[1] + 10)])

            # Renderiza y dibuja la letra "I" encima de la flecha
            current_label = font.render("I", True, PINK)
            screen.blit(current_label, (CYLINDER_RECT.centerx - current_label.get_width() // 2, start_arrow[1] - 21)) 
        
            # Coordenadas para la flecha de diferencia de potencial
            
            start_vd_arrow = (CYLINDER_RECT.right-50, CYLINDER_RECT.bottom + 25)  # 20 píxeles debajo del cilindro
            end_vd_arrow = (CYLINDER_RECT.left+50, CYLINDER_RECT.bottom + 25)

            # Dibuja el cuerpo de la flecha
            pygame.draw.line(screen, GREEN, start_vd_arrow, end_vd_arrow, 3)

            # Dibuja la punta de la flecha (triángulo) en el extremo derecho
            pygame.draw.polygon(screen, GREEN, [(start_vd_arrow[0], start_vd_arrow[1]), 
                                                (start_vd_arrow[0] - 10, start_vd_arrow[1] - 10), 
                                                (start_vd_arrow[0] - 10, start_vd_arrow[1] + 10)])

            # Renderiza y dibuja la etiqueta "V_d" encima de la flecha
            main_text = "V"
            sub_text = "d"

            # Renderiza el texto principal
            main_surface = font.render(main_text, True, GREEN)

            # Ajusta el tamaño de la fuente y la posición vertical para el subíndice
            sub_font = pygame.font.Font(None, 20)  # Ajusta el tamaño de la fuente según tus preferencias
            sub_surface = sub_font.render(sub_text, True, GREEN)

            # Calcula la posición total
            total_width = main_surface.get_width() + sub_surface.get_width()
            x_position = CYLINDER_RECT.centerx - total_width // 2
            y_position = start_vd_arrow[1] - 20  # Centra la etiqueta "V_d" sobre la flecha

            # Dibuja el texto principal y el subíndice en la pantalla
            screen.blit(main_surface, (x_position, y_position))
            screen.blit(sub_surface, (x_position + main_surface.get_width(), y_position + main_surface.get_height() - sub_surface.get_height()))


            # Calcular la resistencia, corriente, potencia, velocidad de arrastre y tiempo de viaje del electrón
            resistance = calculate_resistance(length, diameter, material)

            voltage = float(input_boxes["voltage"]["text"])  # Asegúrate de que el usuario haya ingresado un voltaje
            current = calculate_current(voltage, resistance)
            power = calculate_power(voltage, current)
            area = 3.141592653589793 * (diameter / 2)**2
            drift_v = drift_velocity(current, area, MATERIALS[material]["particle_density"])
            travel_time = electron_travel_time(length, drift_v)
            # Mostrar los resultados en la pantalla de simulación
            resistance_text = f"Resistencia: {resistance:.2e} ohms"
            current_text = f"Corriente: {current:.2e} A"
            power_text = f"Potencia: {power:.2e} W"
            drift_v_text = f"Velocidad de arrastre: {drift_v:.2e} m/s"
            travel_time_text = f"Tiempo de viaje del electrón: {travel_time:.2e} s"
            # Verificar que los valores ingresados son válidos
        
            # Dibujar los textos en la pantalla
            screen.blit(font.render(resistance_text, True, BLACK), (50, 50))
            screen.blit(font.render(current_text, True, BLACK), (50, 80))
            screen.blit(font.render(power_text, True, BLACK), (50, 110))
            screen.blit(font.render(drift_v_text, True, BLACK), (50, 140))
            screen.blit(font.render(travel_time_text, True, BLACK), (50, 170))
            for electron in electrons:
                        electron.move()
                        # Si el electrón llega al final del cilindro, reinícialo en el lado izquierdo
                        if electron.x > CYLINDER_RECT.right:
                            electron.x = CYLINDER_RECT.left
                        electron.draw(screen)
            # Dibuja la casilla de verificación de caminata aleatoria
            pygame.draw.rect(screen, BLACK, random_walk_option["rect"], 2)
            if random_walk_option["checked"]:
                pygame.draw.line(screen, BLACK, random_walk_option["rect"].topleft, random_walk_option["rect"].bottomright, 2)
                pygame.draw.line(screen, BLACK, random_walk_option["rect"].bottomleft, random_walk_option["rect"].topright, 2)
            label_surface = font.render("Show Random Walk", True, BLACK)
            screen.blit(label_surface, (random_walk_option["rect"].x + 30, random_walk_option["rect"].y))
            
            
            # Dibuja el botón de salida
            pygame.draw.rect(screen, RED, exit_button)
            exit_surface = font.render("Salir", True, WHITE)
            screen.blit(exit_surface, (exit_button.x + 10, exit_button.y + 5))

            pygame.draw.rect(screen, BLACK, random_walk_option["rect"], 2)
        if random_walk_option["checked"]:
            pygame.draw.line(screen, BLACK, random_walk_option["rect"].topleft, random_walk_option["rect"].bottomright, 2)
            pygame.draw.line(screen, BLACK, random_walk_option["rect"].bottomleft, random_walk_option["rect"].topright, 2)
        label_surface = font.render("Show Random Walk", True, BLACK)
        screen.blit(label_surface, (random_walk_option["rect"].x + 30, random_walk_option["rect"].y))

        pygame.draw.rect(screen, RED, exit_button)
        exit_surface = font.render("Salir", True, WHITE)
        screen.blit(exit_surface, (exit_button.x + 10, exit_button.y + 5))

        pygame.display.flip()
        fps.tick(60)




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

        # Show error message if exists
        if error_message:
            error_surface = font.render(error_message, True, (255, 0, 0))
            screen.blit(error_surface, (WIDTH // 2 - error_surface.get_width() // 2, 400))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()