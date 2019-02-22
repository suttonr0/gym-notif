
class MobileNotification:
    def __init__(self, index, action, app_package, category, posted_time_of_day):
        self.index = index
        self.action = action
        self.appPackage = app_package
        self.category = category
        self.postedTimeOfDay = posted_time_of_day

    def __str__(self):
        rep = "Notification {} (Action: {}, Package: {}, Category: {}, TimeOfDay: {})"\
            .format(self.index, self.action, self.appPackage, self.category, self.postedTimeOfDay)
        return rep
