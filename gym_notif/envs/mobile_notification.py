
class MobileNotification:
    def __init__(self, action, app_package, category, posted_time_of_day):
        self.action = action
        self.appPackage = app_package
        self.category = category
        self.postedTimeOfDay = posted_time_of_day

    def __str__(self):
        rep = "Notification(Action: " + str(self.action) + ", Package: " + self.appPackage + ", Category: " +\
              self.category + ", TimeOfDay: " + self.postedTimeOfDay + ")"
        return rep
