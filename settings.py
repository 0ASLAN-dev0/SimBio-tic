#----------SETTINGS----------

# Grid and Population
GRID_SIZE = 600
WIDTH, HEIGHT = GRID_SIZE, GRID_SIZE
NUM_AGENTS = 20
NUM_FOOD = 25
FOOD_REGEN_RATE = 1.8

# Lifespan & Evolution
CLOCK_TICK = 60 # Simulation speed
SMIN_LIFESPAN = 12000
MAX_LIFESPAN = 18000
MUTATION_RATE = 0.18
MUTATION_STRENGTH = 0.06
MAX_POPULATION = 250

# Physical/Functional
AGENT_RADIUS = 8
PERCEPTION_RADIUS = 75
INITIAL_ENERGY = 50
MAX_ENERGY = 200
SPEED = 3.5
REPRODUCE = 90
REPRODUCTION_AGE = 10000  # In milliseconds

# Energy dynamics
REWARD = 5
PENALTY = -3

# Behavior weights (sum = 1.0)
NN = 0.4
FOOD = 0.2
AVOID = 0.1
PERSONALITY = 0.3
