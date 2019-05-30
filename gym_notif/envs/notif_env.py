import gym
import random
import pandas as pd
import os
from gym import error, spaces, utils
from gym.utils import seeding
from gym_notif.envs.mobile_notification import MobileNotification


# NEED TO INSTALL ENVIRONMENT WITH "pip install -e ." IN PROJECT PARENT DIR
class NotifEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    CSV_FILE = "csv_files/50Balanced.csv"  # CHANGE TO INPUT CSV PATH FROM PWD OF PROJECT USING THIS ENVIRONMENT

    def __init__(self):
        # ----- Initialize environment variables -----
        self.state = []  # Current notification to make a decision for
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.info = {}  # Extra diagnostic info (can also be useful for learning)

        self.counter = 1  # A counter to limit the number of iterations. Represents the step number we're currently on
        self.notification_list = []  # A list of Notification objects from the CSV file

        # Cross Validation Parameters
        self.training = True
        self.training_data = []  # Current set of training data for k-fold cross validation
        self.testing_data = []  # Current set of testing data for k-fold cross validation
        self.training_sample_space = []  # Remaining unused training data for k-fold cross validation
        self.testing_sample_space = []  # Remaining unused testing data for k-fold cross validation

        # ----- Load in CSV file -----
        # Obtain action, appPackage, category and postedTimeOfDay
        try:
            df = pd.read_csv(self.CSV_FILE)
        except FileNotFoundError:
            print("CSV file '{}' not found. Must be in current working directory of {}".format(self.CSV_FILE, os.getcwd()))
            exit(-1)
        notif_action = df.action  # you can also use df['column_name']
        # Make a list of Notification objects
        for n in range(0, len(notif_action)):
            self.notification_list.append(MobileNotification(n, df.action[n], df.appPackage[n], df.category[n],
                                                             df.postedTimeOfDay[n]))
        self.info['number_of_notifications'] = len(notif_action)

        # ----- Find all possible values for packages, categories and ToD -----
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

        print("ENV: Number of Notifications Imported: {}".format(len(self.notification_list)))
        print("ENV: Total unique Package States: ")
        print(package_states)
        print("ENV: Total unique Category States: ")
        print(category_states)
        print("ENV: Total unique ToD States: ")
        print(time_of_day_states)

        total_states = len(package_states) * len(category_states) * len(time_of_day_states)
        print("ENV: Total number of Notification states: " + str(total_states))

        self.info['package_states'] = package_states
        self.info['category_states'] = category_states
        self.info['time_of_day_states'] = time_of_day_states
        self.info['total_number_of_states'] = total_states

        # 0 = False (no user interation)
        # 1 = True (user interaction)
        self.action_space = spaces.Discrete(2)

        # State space is 1-D with the value corresponding to the combination of notification features
        self.observation_space = spaces.Discrete(total_states)

        # Random shuffle the data list to prepare for 10-fold cross validation
        random.shuffle(self.notification_list)

    def step(self, action):
        # "Accepts an action and returns a tuple (observation, reward, done, info)."
        # Should take in the action, change the state dependent on that action, calculate
        # the reward and return [self.state, self.reward, self.done, self.info]
        if type(action) != bool:
            print("ENV: ERROR: Incorrect type for 'action'. Requires type bool.")
            return -1
        if (self.training and self.counter > len(self.training_data) - 1) or \
                (not self.training and self.counter > len(self.testing_data) - 1):
            self.done = True
        if self.done:
            # Finished, just return data
            return [self.state, self.reward, self.done, self.info]
        else:
            self.reward = 0
            if action == self.state.action:
                # If the action taken by the user matches the action provided by the RL system
                self.reward = 1
            else:
                self.reward = 0

            # Update state
            if self.training:
                self.state = self.training_data[self.counter]  # Can iterate linearly since data is shuffled on reset()
            else:
                self.state = self.testing_data[self.counter]  # Can iterate linearly since data is shuffled on reset()
            # self.render()
            self.counter += 1
        return [self.state, self.reward, self.done, self.info]

    def reset(self):
        if self.training:
            random.shuffle(self.training_data)
            self.state = self.training_data[0]  # Initialize state to first value
        else:
            random.shuffle(self.testing_data)
            self.state = self.testing_data[0]  # Initialize state to first value
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.counter = 1  # A counter to limit the number of iterations. Represents the step number we're currently on

        return self.state

    def render(self, mode='human', close=False):
        if mode == 'human':
            print("ENV: Current notification: {}\n\t with calculated reward: {}".format(
                self.state, self.reward))

