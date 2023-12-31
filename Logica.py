import math  

# Constantes
MATERIALS = {
    "Oro": {"resistivity": 2.44e-8, "particle_density": 5.9e28},
    "Plata": {"resistivity": 1.47e-8, "particle_density": 5.86e28},
    "Cobre": {"resistivity": 1.72e-8, "particle_density": 8.5e28},
    "Aluminio": {"resistivity": 2.75e-8, "particle_density": 6.02e28},
    "Grafito": {"resistivity": 7.837e-5, "particle_density": 1.133e29}
}

ELECTRON_CHARGE = 1.602e-19

def calculate_resistance(length, diameter, material):
   
    resistivity = MATERIALS[material]["resistivity"]
    area = math.pi* (diameter / 2)**2
    resistance = resistivity * (length / area)
    return resistance

def calculate_current(voltage, resistance):
    return voltage / resistance

def calculate_power(voltage, current):
    return voltage * current

def drift_velocity(current, area, particle_density):
    return current / (ELECTRON_CHARGE * area * particle_density)

def electron_travel_time(length, drift_v):
    return length / drift_v

