# Constantes
MATERIALS = {
    "Gold": {"resistivity": 2.44e-8, "particle_density": 5.9e28},
    "Silver": {"resistivity": 1.59e-8, "particle_density": 5.86e28},
    "Copper": {"resistivity": 1.68e-8, "particle_density": 8.5e28},
    "Aluminum": {"resistivity": 2.82e-8, "particle_density": 6.02e28},
    "Graphite": {"resistivity": 7.837e-5, "particle_density": 2.2e23}
}

ELECTRON_CHARGE = 1.602e-19

def calculate_resistance(length, diameter, material):
    resistivity = MATERIALS[material]["resistivity"]
    area = 3.141592653589793 * (diameter / 2)**2
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

# ... otras funciones relacionadas con los cálculos ...
