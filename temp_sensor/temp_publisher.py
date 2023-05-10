import urequests
import uasyncio
from state import State
from logger import log_info
from utime import gmtime, time

class TempPublisher:
    _last_publish_time = None
    _next_publish_time = None
    _interval = None

    async def publish_temp_loop(self):
        while True:
            current_time = time()
            print(f'CURRENT TIME: {current_time}')
            await self.__set_interval(current_time)
            current_temperature = await State.get_temperature()

            if (self._last_publish_time is None or current_time >= self._next_publish_time) and current_temperature is not None and self._interval is not None:
                # try:
                log_info('Time to publish...')
                self.__publish(current_temperature)
                self._last_publish_time = current_time
                self.__set_next_publish_time(current_time)
                # except Exception:
                #     pass
            await uasyncio.sleep(1)

    async def __set_interval(self, current_time):
        settings = await State.get_settings()
        new_interval = settings.tempPublishIntervalSeconds if settings is not None else new_interval
        if new_interval != self._interval:
            self._interval = new_interval
            log_info(f'New interval: {new_interval}')
            self.__set_next_publish_time(current_time)

    def __set_next_publish_time(self, current_time):
        time_past_last_interval = current_time % self._interval
        self._next_publish_time = current_time - time_past_last_interval + self._interval
        print(f'Next publish time: {self._next_publish_time}')

    def __publish(self, current_temperature):
        # try:
        log_info(f'Trying to publish {current_temperature}')
        url = f'https://groker.init.st/api/events?accessKey=ist_cbEBACcP7paCPBnFEUHwYtV0JHMuRwp3&bucketKey=NLGDECR8HXN5&fridge={current_temperature}'
        r = urequests.get(url)
        r.close()
        log_info(f'Published {current_temperature}')
        # except Exception as ex:
        #     log_info('Failed to publish')