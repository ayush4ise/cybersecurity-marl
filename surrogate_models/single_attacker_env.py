"""
Gym environment for single attacker game setting

Inspired from:
https://github.com/ayush4ise/repeated-attack-defense-game/blob/main/phase1_stackelberg/envs/single_attacker_env.py
"""

from dataclasses import dataclass
import numpy as np
import gymnasium as gym
from gymnasium import spaces

@dataclass
class BaseParams:
    """Game Parameters"""
    n: int = 3 # number of targets
    defender_budget: float = 100.0 # total defense budget ($ million)

    # Consequence matrix D[i] ($ million) 
    # If None, auto-generated in __post_init__ from (n)
    consequence_matrix: np.ndarray = None

    # True cost-effectiveness  λ[i]
    # If None, auto-generated in __post_init__ from (n)
    lambda_true: np.ndarray = None

    # Simulation settings
    T: int = 200 # total periods per run
    n_instances: int = 100 # Monte Carlo runs

    seed: int = 42 # for reproducibility

    def __post_init__(self):
        if self.D is None:
            rng = np.random.default_rng(0)
            self.D = rng.uniform(10.0, 100.0, size=self.n)
        if self.lambda_true is None:
            rng = np.random.default_rng(1)
            self.lambda_true = rng.uniform(0.005, 0.025, size=self.n)

        assert self.D.shape == self.n, \
            f"D must be (n) = ({self.n}), got {self.D.shape}"
        assert self.lambda_true.shape == self.n, \
            f"lambda_true must be (n) = ({self.n}), got {self.lambda_true.shape}"

class SingleAttackerEnv(gym.Env):
    """
    Environment class, with separate defender and attacker action consideration
    """
    def __init__(self, params: BaseParams, seed: int = None):
        """
        Parameters
        ----------
        params   : BaseParams instance (holds D, lambda_true, B, T, etc.)
        seed     : optional RNG seed (overrides params.seed if provided)
        """
        self.params = params
        self._rng = np.random.default_rng(seed if seed is not None else params.seed)

	    # Action space for the defender
        self.action_space = spaces.Box(
            low=0.0,
            high=params.defender_budget,
            shape=self.n,
            dtype=np.float32
        )

        # State variables
        self.history = None
        self.t = 0
        self.episode_losses = []

    def render(self):
        pass

    def reset(self, *, seed=None, options=None):
        if seed is not None:
            self._rng = np.random.default_rng(seed)

        self.history = History(self.n)
        self.t = 0
        self.episode_losses = []
        obs = self._build_obs()
        info = {}
        return obs, info

    def step(self, action):
        """
        Execute one step of the environment.
	Re-populate the function string based on understanding of the step function.
        """
	# Action might be in probabilities for the attacker, so that needs to be
	# projected to the budget simplex
	# Check if this is really required or not
        c = self._project_to_budget(np.asarray(action, dtype=float))

	# Additionally the action needs to be an array with both players's actions

	# Enable better logging, or simply use print statements

	# Check what exactly needs to be recorded in history.
        # Update history and MLE
        self.history.add(i_star, j_star, c[i_star], y)
        self.episode_losses.append(true_loss)
        self.t += 1

	# if model chooses to update every k steps
        # if self.t % self.p.k_update == 0:

        # Compute step outcome
        terminated = self.t >= self.p.T
        truncated = False
        reward = -true_loss

        info = {
            "t": self.t,
            "i_star": i_star,
            "j_star": j_star,
            "y": y,
            "c": c.copy(),
            "true_loss": true_loss
        }

        return self._build_obs(), reward, terminated, truncated, info

    def _project_to_budget(self, c):
        # Project c onto the budget simplex (sum(c) = B, c >= 0)
        c = np.maximum(c, 0)
        s = c.sum()
        if s == 0:
            # If all zeros, assign budget uniformly
            return np.full_like(c, self._budget / len(c))
        return c * (self._budget / s)
