from json import load, dump


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
        self.minTemp = dict['minTemp']
        self.maxTemp = dict['maxTemp']
        self.screenOnTimeOfDay = self.TimeOfDay(
            dict['screenOnTimeOfDay']['hour'], dict['screenOnTimeOfDay']['minute'])
        self.screenOffTimeOfDay = self.TimeOfDay(
            dict['screenOffTimeOfDay']['hour'], dict['screenOffTimeOfDay']['minute'])
        self.brightness = dict['brightness']
        self.rotated = dict['rotated']

    def save_settings(self):
        settings_dict = {
            'hostname': self.hostname,
            'tempPublishIntervalSeconds': self.tempPublishIntervalSeconds,
            'minTemp': self.minTemp,
            'maxTemp': self.maxTemp,
            'screenOnTimeOfDay': {'hour': self.screenOnTimeOfDay.hour, 'minute': self.screenOnTimeOfDay.minute},
            'screenOffTimeOfDay': {'hour': self.screenOffTimeOfDay.hour, 'minute': self.screenOffTimeOfDay.minute},
            'brightness': self.brightness,
            'rotated': self.rotated
        }
        with open('settings.json', 'w') as settings_file:
            dump(settings_dict, settings_file)

    def __eq__(self, other):
        if not isinstance(other, Settings):
            return NotImplemented
        return (self.hostname, self.tempPublishIntervalSeconds, self.minTemp, self.maxTemp, self.screenOnTimeOfDay.hour, self.screenOnTimeOfDay.minute, self.screenOffTimeOfDay.hour, self.screenOffTimeOfDay.minute, self.brightness, self.rotated) == (other.hostname, other.tempPublishIntervalSeconds, other.minTemp, other.maxTemp, other.screenOnTimeOfDay.hour, other.screenOnTimeOfDay.minute, other.screenOffTimeOfDay.hour, other.screenOffTimeOfDay.minute, other.brightness, other.rotated)
