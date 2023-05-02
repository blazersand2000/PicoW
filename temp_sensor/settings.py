from json import load
import time

def load_settings():
    with open('settings.json', 'r') as content:
        settings_dict = load(content)
        print(settings_dict)
        return Settings(settings_dict)    

class Settings:
    class TimeOfDay:
        def __init__(self, hour, minute):
            self.hour = hour
            self.minute = minute
    def __init__(self, dict):
        self.hostname = dict['hostname']
        self.tempPublishIntervalSeconds = dict['tempPublishIntervalSeconds']
        self.screenOnTimeOfDay = self.TimeOfDay(dict['screenOnTimeOfDay']['hour'], dict['screenOnTimeOfDay']['minute'])
        self.screenOffTimeOfDay = self.TimeOfDay(dict['screenOffTimeOfDay']['hour'], dict['screenOffTimeOfDay']['minute'])

    def save_settings(self):
        settings_dict = {
            'hostname': self.hostname,
            'tempPublishIntervalSeconds': self.tempPublishIntervalSeconds,
            'screenOnTimeOfDay': { 'hour': self.screenOnTimeOfDay.hour, 'minute': self.screenOnTimeOfDay.minute },
            'screenOffTimeOfDay': { 'hour': self.screenOffTimeOfDay.hour, 'minute': self.screenOffTimeOfDay.minute }
        }