import pygame
import random
import math
import numpy as np
import settings  # Import settings

# Pygame setup
pygame.init()
screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 18)


# Use settings values wherever needed
GRID_SIZE = settings.GRID_SIZE
NUM_AGENTS = settings.NUM_AGENTS
NUM_FOOD = settings.NUM_FOOD
FOOD_REGEN_RATE = settings.FOOD_REGEN_RATE
MIN_LIFESPAN = settings.MIN_LIFESPAN
MAX_LIFESPAN = settings.MAX_LIFESPAN
MUTATION_RATE = settings.MUTATION_RATE
MUTATION_STRENGTH = settings.MUTATION_STRENGTH
MAX_POPULATION = settings.MAX_POPULATION
AGENT_RADIUS = settings.AGENT_RADIUS
PERCEPTION_RADIUS = settings.PERCEPTION_RADIUS
INITIAL_ENERGY = settings.INITIAL_ENERGY
MAX_ENERGY = settings.MAX_ENERGY
SPEED = settings.SPEED
REPRODUCE = settings.REPRODUCE
REPRODUCTION_AGE = settings.REPRODUCTION_AGE
REWARD = settings.REWARD
PENALTY = settings.PENALTY
NN = settings.NN
FOOD = settings.FOOD
AVOID = settings.AVOID
PERSONALITY = settings.PERSONALITY



# Pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)
small_font = pygame.font.SysFont(None, 18)


def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def mutate(brain):
    return [
        w + np.random.randn(*w.shape) * MUTATION_STRENGTH
        if random.random() < MUTATION_RATE else w.copy() for w in brain
    ]


def forward_pass(brain, x):
    for i in range(len(brain)):
        x = np.dot(x, brain[i])
        if i != len(brain) - 1:
            x = np.tanh(x)  # activation for hidden layers
    return x


class Agent:

    def __init__(self, x, y, brain=None, personality="neutral"):
        self.x = x
        self.y = y
        self.energy = INITIAL_ENERGY
        self.birth_time = pygame.time.get_ticks()
        self.lifespan = random.randint(MIN_LIFESPAN, MAX_LIFESPAN)
        self.personality = personality
        self.health = random.uniform(0.5, 1.5)  # added for threat detection

        personality_colors = {
            "aggressive": (255, 0, 0), #Red
            "friendly": (0, 255, 0), #Green
            "shy": (255, 165, 0), #Orange
            "curious": (255, 255, 0), #Yellow
            "neutral": (255, 255, 255), #White
        }

        self.color = personality_colors.get(self.personality, (255, 255, 255))

        if brain:
            self.brain = mutate(brain)
        else:
            self.brain = [
                np.random.randn(20, 128) * 0.05,
                np.random.randn(128, 128) * 0.05,
                np.random.randn(128, 64) * 0.05,
                np.random.randn(64, 32) * 0.05,
                np.random.randn(32, 6) * 0.05
            ]

    def reproduce(self, agents):
            """ Reproduction mechanism with multiple offspring """
            current_time = pygame.time.get_ticks()

            if self.energy >= REPRODUCE and (current_time - self.birth_time > REPRODUCTION_AGE):
                if len(agents) < MAX_POPULATION:
                    print(f"{self.personality} agent is reproducing")

                    num_offspring = random.randint(1, 5)
                    self.energy -= REPRODUCE / 2  # Cost of reproduction

                    offspring_list = []
                    for _ in range(num_offspring):
                        child_personality = self.mutate_personality()
                        new_agent_brain = mutate(self.brain)  
                        offspring = Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT), brain=new_agent_brain, personality=child_personality)
                        offspring_list.append(offspring)

                    agents.extend(offspring_list)  # Add offspring to agents list
                    return True
            return False


    def mutate_personality(self):
       
        personality_choices = ["aggressive", "curious", "shy", "friendly", "neutral"]
        if random.random() < MUTATION_RATE:
            return random.choice(personality_choices)
        return self.personality
    
    def perceive(self, food_list, agents):
        inputs = []

        # Closest food
        sorted_food = sorted(food_list,
                             key=lambda f: distance((self.x, self.y), (f.x, f.y)))[:3]
        for f in sorted_food:
            dx = (f.x - self.x) / PERCEPTION_RADIUS
            dy = (f.y - self.y) / PERCEPTION_RADIUS
            dist = distance((self.x, self.y), (f.x, f.y)) / PERCEPTION_RADIUS
            inputs.extend([dx, dy, dist])
        while len(inputs) < 9:
            inputs.extend([0, 0, 1])

        # Closest agents
        sorted_agents = sorted([a for a in agents if a != self],
                               key=lambda a: distance((self.x, self.y), (a.x, a.y)))[:2]
        for a in sorted_agents:
            dx = (a.x - self.x) / PERCEPTION_RADIUS
            dy = (a.y - self.y) / PERCEPTION_RADIUS
            dist = distance((self.x, self.y), (a.x, a.y)) / PERCEPTION_RADIUS
            inputs.extend([dx, dy, dist])
        while len(inputs) < 18:
            inputs.extend([0, 0, 1])

        inputs.append(self.energy / MAX_ENERGY)
        inputs.append((pygame.time.get_ticks() - self.birth_time) / self.lifespan)
        return np.array(inputs)

    def think_and_act(self, food_list, agents):
        inputs = self.perceive(food_list, agents)
        out = forward_pass(self.brain, inputs)
        nn_dx, nn_dy = out[0], out[1]

        # Move toward nearest food
        food_dx, food_dy = 0, 0
        if food_list:
            nearest_food = min(food_list, key=lambda f: distance((self.x, self.y), (f.x, f.y)))
            dx = nearest_food.x - self.x
            dy = nearest_food.y - self.y
            dist = math.hypot(dx, dy)
            if dist > 0:
                food_dx = dx / dist
                food_dy = dy / dist

        # Avoid nearest agent
        avoid_dx, avoid_dy = 0, 0
        nearest_agent = None
        min_dist = float('inf')
        for a in agents:
            if a is self:
                continue
            dist = distance((self.x, self.y), (a.x, a.y))
            if dist < min_dist:
                min_dist = dist
                nearest_agent = a

        if nearest_agent and min_dist < PERCEPTION_RADIUS:
            avoid_dx = self.x - nearest_agent.x
            avoid_dy = self.y - nearest_agent.y
            mag = math.hypot(avoid_dx, avoid_dy)
            if mag > 0:
                avoid_dx /= mag
                avoid_dy /= mag

        # Personality-based behavior
        pers_dx, pers_dy = 0, 0
        if self.personality == "aggressive":
            # Hunt the weakest agent
            target = None
            min_health = float('inf')
            for a in agents:
                if a is not self and a.health < self.health:
                    d = distance((self.x, self.y), (a.x, a.y))
                    if d < min_health:
                        target = a
                        min_health = d
            if target:
                dx = target.x - self.x
                dy = target.y - self.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    pers_dx = dx / dist
                    pers_dy = dy / dist

                # If close enough, consume the weaker agent
                if dist < 1.0:  # Adjust threshold as needed
                    if self.health > target.health:
                        self.health += target.health * 0.5
                        target.health = -1  # Mark for removal

        elif self.personality == "friendly":
            # Move toward nearby agent
            friend = None
            min_dist = float('inf')
            for a in agents:
                if a is not self:
                    d = distance((self.x, self.y), (a.x, a.y))
                    if d < min_dist:
                        friend = a
                        min_dist = d
            if friend:
                dx = friend.x - self.x
                dy = friend.y - self.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    pers_dx, pers_dy = dx / dist, dy / dist

        elif self.personality == "shy":
            shy_dx, shy_dy = 0, 0
            for a in agents:
                if a is not self:
                    dx = self.x - a.x
                    dy = self.y - a.y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        shy_dx += dx / dist
                        shy_dy += dy / dist
            mag = math.hypot(shy_dx, shy_dy)
            if mag > 0:
                pers_dx, pers_dy = shy_dx / mag, shy_dy / mag

        elif self.personality == "curious":
            if random.random() < 0.5 and len(agents) > 1:
                target = random.choice([a for a in agents if a is not self])
                dx = target.x - self.x
                dy = target.y - self.y
                dist = math.hypot(dx, dy)
                if dist > 0:
                    pers_dx = dx / dist
                    pers_dy = dy / dist
            else:
                angle = random.uniform(0, 2 * math.pi)
                pers_dx = math.cos(angle)
                pers_dy = math.sin(angle)

        # Combine behaviors
        self.x += (
            nn_dx * SPEED * NN +
            food_dx * SPEED * FOOD +
            avoid_dx * SPEED * AVOID +
            pers_dx * SPEED * PERSONALITY
        )
        self.y += (
            nn_dy * SPEED * NN +
            food_dy * SPEED * FOOD +
            avoid_dy * SPEED * AVOID +
            pers_dy * SPEED * PERSONALITY
        )

        # Wall wrapping
        self.x = (self.x + GRID_SIZE) % GRID_SIZE
        self.y = (self.y + GRID_SIZE) % GRID_SIZE

        

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), AGENT_RADIUS)
        age = (pygame.time.get_ticks() - self.birth_time) // 1000
        age_text = small_font.render(f"{age}", True, (255, 255, 255))
        screen.blit(age_text, (self.x - 5, self.y - 20))


class Food:

    def __init__(self, x=None, y=None):
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        self.energy = 20

    def draw(self):
        pygame.draw.circle(screen, (255, 255, 100), (int(self.x), int(self.y)), 4)


# Initialize
agents = [
    Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT),
          personality=random.choice(["aggressive", "curious", "shy", "friendly", "neutral"]))
    for _ in range(NUM_AGENTS)
]
food = [Food() for _ in range(NUM_FOOD)]


def mutate_personality_for_new_agents(last_personality):
    if random.random() < MUTATION_RATE:
        return random.choice(["aggressive", "curious", "shy", "friendly", "neutral"])
    return last_personality

# Main loop
running = True
last_dead_agent = None

while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Loop through all agents to update and check for reproduction
    for agent in list(agents):
        # Perform actions like movement, perception, and decision-making
        agent.think_and_act(food, agents)

        # Attempt to reproduce after agent's actions
        if agent.reproduce(agents):  
            print(f"{agent.personality} agent has reproduced.")

        # Handle food collection and energy consumption
        for f in food[:]:
            if distance((agent.x, agent.y), (f.x, f.y)) < AGENT_RADIUS + 5:
                agent.energy += f.energy
                agent.energy = min(agent.energy, MAX_ENERGY)
                food.remove(f)

        # If agent runs out of energy or its lifespan ends, remove it
        if agent.energy <= 0 or pygame.time.get_ticks() - agent.birth_time > agent.lifespan:
            last_dead_agent = agent
            agents.remove(agent)
            food.append(Food(agent.x, agent.y))  # Respawn food at agent's position

        # Draw agent on the screen
        agent.draw()

        for f in food:
            f.draw()


    # Handle food regeneration
    while len(food) < NUM_FOOD:
        food.append(Food())

            # If all agents die, respawn new agents from the last dead agent with slight mutations
    if len(agents) == 0 and last_dead_agent:
                print("All agents died. Respawning from last agent with mutations...")
                for _ in range(5):  # Respawn 5 new agents
                    new_agent_brain = mutate(last_dead_agent.brain)
                    new_agent_personality = mutate_personality_for_new_agents(last_dead_agent.personality)
                    agents.append(
                        Agent(random.randint(0, WIDTH), random.randint(0, HEIGHT),
                              brain=new_agent_brain,
                              personality=new_agent_personality)
                    )

    # Display population count on screen
    population_text = font.render(f"{len(agents)}", True, (200, 20, 0))
    screen.blit(population_text, (10, 10))

    # Update display
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
