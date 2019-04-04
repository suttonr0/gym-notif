
class MobileNotification:
    def __init__(self, index, action, app_package, category, posted_time_of_day, posted_day_of_week):
        self.index = index
        self.action = action
        self.appPackage = app_package
        self.category = category
        self.postedTimeOfDay = posted_time_of_day
        self.postedDayOfWeek = posted_day_of_week

    def __str__(self):
        rep = "Notification {} (Action: {}, Package: {}, Category: {}, TimeOfDay: {}, DayOfWeek)"\
            .format(self.index, self.action, self.appPackage, self.category, self.postedTimeOfDay, self.postedDayOfWeek)
        return rep
