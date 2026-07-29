# Notes on MARL --verbose

Multi-Agent Reinforcement Learning (MARL), as the name suggests, has multiple learning agents, that coexist in an environment. Each agent has its own rewards and does actions in its own interest.

## Cybersecurity Attack-Defense Games

There could be two game settings: sequential and simultaneous.

- For the simultaneous game, both the attacker and the defender make their moves simultaenously. A *Nash Equilibrium* solution is obtained.

- For the sequential game, the defender makes the first move; the attacker observes the defender's move and makes an informed decision. This game form is also knows as *Stackelberg Game*. A *Stackelberg Equilibrium* solution is obtained.

> This project only considers the Stackelberg game setting.
