import gym
import csv
from gym import error, spaces, utils
from gym.utils import seeding
from gym_notif.envs.mobile_notification import Notification


# NEED TO INSTALL ENVIRONMENT WITH "pip install -e ." IN PROJECT PARENT DIR
class NotifEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    CSV_FILE = "notif_user_2.csv"

    def __init__(self):
        # ----- Initialize environment variables -----
        self.state = []  # State of notifications?
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.info = 0  # Extra diagnostic info (can also be useful for learning)
        self.counter = 0  # A counter to use so that there's a limited number of iterations

        # ----- Load in CSV file -----
        # Takes columns in order as they are presented in csv
        fieldnames = ("index", "action", "appPackage", "category", "postedTimeOfDay")

        with open(self.CSV_FILE) as csvfile:
            reader = csv.DictReader(csvfile, fieldnames)
            for row in reader:
                self.state.append(Notification(row["appPackage"], row["category"], row["postedTimeOfDay"]))

        self.state.pop(0)  # Remove Notif object containing table headers

        print("OOOOOOOOOOOO")
        print(self.state[0])
        print("OOOOOOOOOOOO")

        # Find all possible values for packages, categories and ToD
        package_states = []
        category_states = []
        time_of_day_states = []
        for item in self.state:
            if item.appPackage not in package_states:
                package_states.append(item.appPackage)
            if item.category not in category_states:
                    category_states.append(item.category)
            if item.postedTimeOfDay not in time_of_day_states:
                    time_of_day_states.append(item.postedTimeOfDay)

        print(package_states)
        print(category_states)
        print(time_of_day_states)

        total_num_states = len(package_states) * len(category_states) * len(time_of_day_states)
        print("Total number of Notification states: " + str(total_num_states))

    def step(self, action):
        # "Accepts an action and returns a tuple (observation, reward, done, info)."
        # Should take in the action, change the state dependent on that action, calculate
        # the reward and return the [self.state, self.reward, self.done, self.info]
        if self.done:
            return [self.state, self.reward, self.done, self.info]
        else:
            self.reward = 0
            if action == "JUMP":
                if self.state == "GROUND":
                    self.reward = 1
                    self.state = "AIR"
            elif action == "DUCK":
                if self.state == "AIR":
                    self.reward = 1
                    self.state = "GROUND"
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
            print("Currently in: with reward: " + str(self.reward))
