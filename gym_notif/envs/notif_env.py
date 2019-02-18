import gym
import pandas as pd
from gym import error, spaces, utils
from gym.utils import seeding
from gym_notif.envs.mobile_notification import MobileNotification


# NEED TO INSTALL ENVIRONMENT WITH "pip install -e ." IN PROJECT PARENT DIR
class NotifEnv(gym.Env):
    metadata = {'render.modes': ['human']}
    CSV_FILE = "notif_user_2.csv"

    def __init__(self):
        # ----- Initialize environment variables -----
        self.state = []  # Current notification to make a decision for
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.info = 0  # Extra diagnostic info (can also be useful for learning)
        self.counter = 0  # A counter to use so that there's a limited number of iterations
        self.notification_list = []  # A list of Notification objects from the CSV file
        self.previous_action = []  # The last action taken as input to the environment

        # ----- Load in CSV file -----
        # Obtain action, appPackage, category and postedTimeOfDay
        df = pd.read_csv(self.CSV_FILE)
        notif_action = df.action  # you can also use df['column_name']
        # Make a list of Notification objects
        for n in range(0, len(notif_action)):
            self.notification_list.append(MobileNotification(df.action[n], df.appPackage[n], df.category[n],
                                                             df.postedTimeOfDay[n]))
        self.state = self.notification_list[0]  # Initialize to first value

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

        print("ENV: Total unique Package States: ")
        print(package_states)
        print("ENV: Total unique Category States: ")
        print(category_states)
        print("ENV: Total unique ToD States: ")
        print(time_of_day_states)

        self.total_states = len(package_states) * len(category_states) * len(time_of_day_states)
        print("ENV: Total number of Notification states: " + str(self.total_states))

        # Get One-Hot encodings for each category's values
        print(pd.Series(package_states).str.get_dummies(', '))
        print(pd.Series(category_states).str.get_dummies(', '))
        print(pd.Series(time_of_day_states).str.get_dummies(', '))

        # pd.Series(time_of_day_states).str.get_dummies(', ') is of pandas.core.frame.DataFrame
        # Can be indexed by pd.Series(...)...["afternoon"], returning a
        # pandas.core.series.Series with its one-hot encoding. This encoding can then be indexed as a normal array


        # 0 = False (no user interation)
        # 1 = True (user interaction)
        self.action_space = spaces.Discrete(2)

    def step(self, action):
        # "Accepts an action and returns a tuple (observation, reward, done, info)."
        # Should take in the action, change the state dependent on that action, calculate
        # the reward and return the [self.state, self.reward, self.done, self.info]
        if type(action) != bool:
            print("ENV: ERROR: Incorrect type for 'action'. Requires type bool.")
            return -1
        if self.done:
            # Finished, just return data
            return [self.state, self.reward, self.done, self.info]
        else:
            self.reward = 0
            if action == self.notification_list[self.counter].action:
                # If the action taken by the user matches the action provided by the RL system
                self.reward = 1
            elif action:
                self.reward = -1
            self.counter += 1
            # Update state
            self.state = self.notification_list[self.counter]
            if self.counter > 9:
                self.done = True
            self.previous_action = action
            self.render()
        return [self.state, self.reward, self.done, self.info]

    def reset(self):
        self.state = self.notification_list[0]  # Initialize to first value
        self.reward = 0  # Initial reward of zero
        self.done = False  # We are not finished at the start
        self.info = 0  # Extra diagnostic info (can also be useful for learning)
        self.counter = 0  # A counter to use so that there's a limited number of iterations

        return self.state

    def render(self, mode='human', close=False):
        if mode == 'human':
            print("ENV: Current notification: {}\n\t with calculated reward: {}\n\t based on input action: {}".format(
                self.state, self.reward, self.previous_action))
