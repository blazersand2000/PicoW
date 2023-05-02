import queue
from settings import Settings


class State:
    def __init__(self, output_q: queue.Queue):
        self._temperature = None
        self._connected = None
        self._status = None
        self._ip = None
        self._settings: Settings = None
        self._output_q = output_q

    @property
    def temperature(self):
        return self._temperature

    async def set_temperature(self, value):
        if self._temperature != value:
            self._temperature = value
            await self._output_q.put(OutputState(self))

    async def set_wifi_status(self, value):
        new_connected = value['connected']
        new_status = value['status']
        new_ip = value['ip']
        if self._connected != new_connected or self._status != new_status or self._ip != new_ip:
            self._connected = new_connected
            self._status = new_status
            self._ip = new_ip
            await self._output_q.put(OutputState(self))

    async def set_settings(self, value: Settings):
        if self._settings == value:
            return
        self._settings = value
        self._settings.save_settings()

class OutputState:
    def __init__(self, state: State):
        self.hostname = state._settings.hostname if state._settings is not None else ''
        self.temperature = state._temperature
        self.connected = state._connected
        self.status = state._status if state._status is not None else ''
        self.ip = str(state._ip)
