
class Notification:
    def __init__(self, app_package, category, posted_time_of_day):
        self.appPackage = app_package
        self.category = category
        self.postedTimeOfDay = posted_time_of_day

    def __str__(self):
        rep = "Notification(Package: " + self.appPackage + " Category: " + self.category +\
              " TimeOfDay: " + self.postedTimeOfDay
        return rep

    def setValues(self, app_package, category, posted_time_of_day):
        self.appPackage = app_package
        self.category = category
        self.postedTimeOfDay = posted_time_of_day

    # def getAppPackage(self):
    #     return self.appPackage
    #
    # def getPostedTimeOfDay(self):
    #     return self.posted_time_of_day
    #
    # def getCategory(self):
    #     return self.category


