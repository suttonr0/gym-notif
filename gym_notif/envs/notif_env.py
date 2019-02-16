import gym
import pandas as pd
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
        self.notification_list = []  # A list of Notification objects from the CSV file
        self.total_states = 0  # The total number of different notification states

        # ----- Load in CSV file -----
        # Obtain action, appPackage, category and postedTimeOfDay
        df = pd.read_csv(self.CSV_FILE)
        notif_action = df.action  # you can also use df['column_name']
        for n in range(0, len(notif_action)):
            self.notification_list.append(Notification(df.appPackage[n], df.category[n], df.postedTimeOfDay[n]))
            print(self.notification_list[n])

        self.state = self.notification_list[0]  # Initialize to first value
        print(self.notification_list[2].appPackage)

        # Find all possible values for packages, categories and ToD
        package_states = []
        category_states = []
        time_of_day_states = []
        for item in self.notification_list:
            if item.appPackage not in package_states:
                package_states.append(item.appPackage)
            if item.category not in category_states:
                category_states.append(item.category)
            if item.postedTimeOfDay not in time_of_day_states:
                time_of_day_states.append(item.postedTimeOfDay)

        print("Total unique Package States: ")
        print(package_states)
        print("Total unique Category States: ")
        print(category_states)
        print("Total unique ToD States: ")
        print(time_of_day_states)

        self.total_states = len(package_states) * len(category_states) * len(time_of_day_states)
        print("Total number of Notification states: " + str(self.total_states))

    def step(self, action):
        # "Accepts an action and returns a tuple (observation, reward, done, info)."
        # Should take in the action, change the state dependent on that action, calculate
        # the reward and return the [self.state, self.reward, self.done, self.info]
        if self.done:
            return [self.state, self.reward, self.done, self.info]
        else:
            self.reward = 0
            if action == "A1":
                self.reward = 1
                self.state = "AIR"
            else:
                print(self.notification_list[self.counter])
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
