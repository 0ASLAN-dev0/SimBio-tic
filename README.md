# SimBio-tic: Agent Simulation with Evolving Neural Networks

**SimBio-tic** is a simulation where agents with unique personalities interact, adapt, and reproduce in a 2D environment. Each agent is powered by a neural network, making decisions based on its surroundings. Over time, agents evolve through natural selection, mutation, and energy-based survival mechanics.

---

## Features

- **Diverse Personalities**: Agents have personalities like `aggressive`, `friendly`, `shy`, `curious`, or `neutral`, which influence their behavior.
- **Neural Network Brain**: Agents use feedforward neural networks to decide how to move, avoid, or approach food and other agents.
- **Evolution Through Mutation**: Agents reproduce by duplicating and mutating their neural networks and personalities.
- **Food & Energy Mechanics**: Agents collect food to gain energy, which is needed for survival and reproduction.
- **Agent Interaction**: Personality affects how agents react to others—some avoid, some engage.
- **Lifespan & Death**: Agents have a finite lifespan and gradually die out, allowing newer generations to take over.

---

## Requirements

- Python 3.x
- Pygame
- NumPy



---

## How to Run

```bash
git clone https://github.com/0ASLAN-dev0/SimBio-tic
cd SimBio-tic
pip install -r requirements.txt
python SimBio-tic.py
```

A Pygame window will open, and the simulation will begin with agents moving, feeding, reproducing, and evolving.

---

## Preview

![SimBio-tic Preview](https://github.com/0ASLAN-dev0/SimBio-tic/raw/main/image_2025-04-13_021442265.png)

---

## Agent Personalities and Colors

Agents are visually color-coded based on their personality:

| Personality | Description                         | Color                |
|-------------|-------------------------------------|----------------------|
| Aggressive  | Hunts weaker agents                 | Red `(255, 0, 0)`    |
| Friendly    | Seeks others, avoids conflict       | Green `(0, 255, 0)`  |
| Shy         | Avoids others, focused on survival  | Orange `(255, 165, 0)` |
| Curious     | Explores randomly                   | Yellow `(255, 255, 0)` |
| Neutral     | Balanced behavior                   | White `(255, 255, 255)` |

---

## Simulation Settings

You can adjust the following parameters in the source code to change how the simulation behaves:

| Setting                  | Default       | Description                                       |
|--------------------------|---------------|---------------------------------------------------|
| `GRID_SIZE`              | `600x600`     | Size of the simulation window                     |
| `NUM_AGENTS`             | `20`          | Initial number of agents                          |
| `FOOD_REGENERATION_RATE` | `1.8`         | How fast food respawns                            |
| `ENERGY_REWARD`          | `+5`          | Energy gained per food item                       |
| `ENERGY_PENALTY`         | `-3`          | Energy lost over time or by movement              |
| `AGENT_RADIUS`           | `8`           | Visual size of agents                             |
| `PERCEPTION_RADIUS`      | `75`          | How far agents can detect others and food         |
| `MAX_POPULATION`         | `250`         | Maximum number of agents                          |
| `LIFESPAN_RANGE`         | `12000–18000` | Lifespan of each agent in ticks                   |
| `REPRODUCTION_COST`      | `90`          | Minimum energy needed to reproduce                |

---

## Neural Network Architecture

Each agent’s brain is a simple feedforward neural network:

- **Inputs**: Nearby food, agents, energy levels, etc.
- **Hidden Layer**: Processes inputs and combines signals.
- **Outputs**: Movement decisions (direction, speed, behavior).

Neural networks are initialized randomly and mutate during reproduction, allowing complex behaviors to evolve over generations.

---

## Evolution and Mutation

- During reproduction, each agent's neural network and personality mutate slightly.
- This leads to adaptive behavior over generations.
- Mutation rates can be tuned for faster or slower evolutionary changes.

---

## License

This project is open-source under the [MIT License](LICENSE).

---

## Contributing

If you have suggestions or want to contribute:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request
4. Or open an issue for feedback or ideas

