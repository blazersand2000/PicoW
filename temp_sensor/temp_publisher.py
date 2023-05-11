import urequests
import uasyncio
from state import State
import variables
from logger import log_info
from utime import gmtime, time
from phew.logging import info, warn, error

class TempPublisher:
    _last_publish_time = None
    _next_publish_time = None
    _interval = None

    async def publish_temp_loop(self):
        while True:
            current_time = time()
            await self.__set_interval(current_time)
            current_temperature = await State.get_temperature()
            is_wifi_connected = (await State.get_wifi_status())[0]

            if self.__publish_is_due(current_time):
                self.__try_publish(current_time, current_temperature, is_wifi_connected)

            await uasyncio.sleep(1)

    def __try_publish(self, current_time, current_temperature, is_wifi_connected):
        if current_temperature is None:
            warn('Skipping temperature publish because of missing temperature')
        elif self._interval is None:
            warn('SKipping temperature publish because of missing interval')
        elif not is_wifi_connected:
            warn('Skipping temperature publish because WiFi is not connected')
        else:
            try:
                self.__publish(current_temperature)
            except Exception as ex:
                error(f'Temperature publish failed. Exception: {str(ex)}')
                pass
            else:
                info(f'Temperature publish successful. Temperature value: {current_temperature}')
                self._last_publish_time = current_time
                self.__set_next_publish_time(current_time)

    def __publish_is_due(self, current_time):
        return self._last_publish_time is None or current_time >= self._next_publish_time

    async def __set_interval(self, current_time):
        settings = await State.get_settings()
        new_interval = settings.tempPublishIntervalSeconds if settings is not None else new_interval
        if new_interval != self._interval:
            self._interval = new_interval
            info(f'New temperature publish interval: {new_interval}')
            self.__set_next_publish_time(current_time)

    def __set_next_publish_time(self, current_time):
        time_past_last_interval = current_time % self._interval
        self._next_publish_time = current_time - time_past_last_interval + self._interval
        info(f'Next temperature publish time: {self._next_publish_time}')

    def __publish(self, current_temperature):
        url = variables.url(current_temperature)
        r = urequests.get(url)
        r.close()
