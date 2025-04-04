import gym
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stable_baselines3 import A2C
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy

from gym import spaces

class TradingEnv(gym.Env):
    def __init__(self, df):
        super(TradingEnv, self).__init__()
        self.df = df
        self.action_space = spaces.Discrete(3)  # Buy, Sell, Hold
        self.observation_space = spaces.Box(low=0, high=1, shape=(df.shape[1],), dtype=np.float32)
        self.current_step = 0

    def reset(self):
        """ 
        Resets the environment to the starting state.

        Returns:
            A numpy array containing the state of the environment
        """
        self.current_step = 0
        return self.df.iloc[self.current_step].values

    def step(self, action):
        """
        Run one step of the environment.

        Args:
            action (int): The action to take (buy, sell, hold)

        Returns:
            obs (numpy array): The new state of the environment
            reward (float): The reward gained from taking the action
            done (bool): Whether the episode has finished
            info (dict): Additional information about the episode
        """
        self.current_step += 1
        reward = self._take_action(action)
        done = self.current_step >= len(self.df) - 1
        obs = self.df.iloc[self.current_step].values
        return obs, reward, done, {}

    def _take_action(self, action):
        # Define your reward logic here
        """
        Compute the reward for the given action.

        Args:
            action (int): The action to take (buy, sell, hold)

        Returns:
            reward (float): The reward gained from taking the action
        """
        return 0 # Replace with your actual reward