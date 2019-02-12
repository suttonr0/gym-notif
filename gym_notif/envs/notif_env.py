import gym
from gym import error, spaces, utils
from gym.utils import seeding


# NEED TO INSTALL ENVIRONMENT WITH "pip install -e ." IN PROJECT PARENT DIR
class NotifEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.state = "GROUND"  # State of notifications?
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.info = 0  # Extra diagnostic info (can also be useful for learning)
        self.counter = 0  # A counter to use so that there's a limited number of iterations

    def step(self, action):
        # "Accepts an action and returns a tuple (observation, reward, done, info)."
        # Should take in the action, change the state dependent on that action, calculate
        # the reward and return the [self.state, self.reward, self.done, self.info]
        if self.done:
            return [self.state, self.reward, self.done, self.info]
        else:
            if action == "JUMP":
                if self.state == "GROUND":
                    self.reward = 1
                    self.state = "AIR"
                if self.state == "AIR":
                    self.reward = 0
            elif action == "DUCK":
                if self.state == "AIR":
                    self.reward = 1
                    self.state = "GROUND"
                if self.state == "GROUND":
                    self.reward = 0
            self.counter += 1
            if self.counter > 9:
                self.done = True
            self.render()

        return [self.state, self.reward, self.done, self.info]

    def reset(self):
        self.state = "GROUND"  # State of notifications?
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.info = 0
        return self.state

    def render(self, mode='human', close=False):
        if mode == 'human':
            print("Currently in: " + self.state + "with reward: " + self.reward)
