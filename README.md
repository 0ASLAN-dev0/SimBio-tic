# Agent Simulation with Neural Networks

This project simulates a population of agents with different personalities interacting in a 2D environment. The agents have neural networks that guide their behavior, and their interactions and evolution are based on their decisions and environmental factors. The goal is to create a dynamic and evolving simulation where agents can search for food, reproduce, and interact based on their personalities.

## Features

- **Agent Personalities**: Agents can have different personalities such as "aggressive", "friendly", "shy", "curious", or "neutral", influencing their behavior and interactions.
- **Neural Networks**: Each agent has a neural network guiding its decisions based on the environment, including food, other agents, and its own energy.
- **Evolution**: Agents can reproduce, and their neural networks and personalities evolve through mutation.
- **Food and Energy Dynamics**: Agents need energy to survive and reproduce. They can gather food, which regenerates over time, but they must manage their energy carefully.
- **Agent Interaction**: Agents interact with each other, avoiding collisions or engaging in aggressive behavior based on their personality.
- **Simulation Lifespan**: Each agent has a lifespan, and the population evolves over time as agents live and reproduce.

## Requirements

- Python 3.x
- Pygame
- NumPy

Install the necessary dependencies:

```bash
pip install pygame numpy
```

## How to Run

To run the simulation, simply execute the following:

```bash
python SimBio-tic.py
```

This will start a Pygame window where the agents will begin moving, searching for food, and interacting based on their neural networks and personalities.

This is how it should look like:
![SimBio-tic Preview](https://github.com/0ASLAN-dev0/SimBio-tic/raw/main/image_2025-04-13_021442265.png)

## Settings

The following settings can be adjusted in the code to modify the behavior and dynamics of the simulation:

- **Grid Size**: The size of the simulation grid (default: 600x600).
- **Number of Agents**: The initial population of agents (default: 20).
- **Food Regeneration Rate**: The rate at which food regenerates (default: 1.8).
- **Energy Dynamics**: Rewards and penalties associated with food collection and energy consumption (default: reward = 5, penalty = -3).
- **Agent Radius**: The radius of each agent (default: 8).
- **Perception Radius**: The distance at which agents can perceive food and other agents (default: 75).
- **Max Population**: The maximum number of agents allowed in the simulation (default: 250).
- **Lifespan and Reproduction**: Lifespan of agents and reproduction mechanics (default: 12000 - 18000 ticks lifespan, reproduction cost = 90 energy).

## Agent Behavior

Agents are controlled by neural networks that are responsible for:

- **Movement**: Based on the combination of neural network output, food behavior, avoidance behavior, and personality-based behavior.
- **Personality**: Each agent has a personality that affects how they interact with other agents (e.g., "aggressive" agents will attack weaker agents, while "friendly" agents may seek companionship).
- **Reproduction**: Agents reproduce when their energy is sufficient, creating offspring with mutated neural networks and personalities.

## Evolution and Mutation

- Agents mutate both their neural network weights and personalities during reproduction, allowing for evolving behavior over generations.
- Mutation rates and strengths can be adjusted to control the speed and extent of evolution.

## License

This project is open-source and available under the [MIT License](LICENSE).

## Contributing

Feel free to fork the project, make changes, and submit pull requests. If you encounter any bugs or have suggestions for improvement, please open an issue.

