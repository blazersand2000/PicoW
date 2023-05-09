import queue
import uasyncio
import output
from settings import Settings


class State:
    _temperature = None
    _connected = None
    _status = None
    _ip = None
    _settings: Settings = None
    _output_q = queue.Queue()
    state_q = queue.Queue()

    @classmethod
    async def state_loop(cls):
        out = output.Output()
        uasyncio.create_task(out.output_loop(cls._output_q))
        while True:
            if not cls.state_q.empty():
                op, value = await cls.state_q.get()
                await op(value)
            await uasyncio.sleep_ms(0)

    # @classmethod
    # async def queue_method(cls, method):
    #     await cls.state_q.put(method)

    @classmethod
    async def set_temperature(cls, value):
        if cls._temperature != value:
            cls._temperature = value
            await cls._output_q.put(OutputState(cls))

    @classmethod
    async def set_wifi_status(cls, value):
        new_connected = value['connected']
        new_status = value['status']
        new_ip = value['ip']
        if cls._connected != new_connected or cls._status != new_status or cls._ip != new_ip:
            cls._connected = new_connected
            cls._status = new_status
            cls._ip = new_ip
            await cls._output_q.put(OutputState(cls))

    @classmethod
    async def get_settings(cls):
        return cls._settings

    @classmethod
    async def set_settings(cls, value: Settings):
        if cls._settings == value:
            return
        cls._settings = value
        cls._settings.save_settings()
        await cls._output_q.put(OutputState(cls))


class OutputState:
    def __init__(self, state: State):
        self.temperature = state._temperature
        self.connected = state._connected
        self.status = state._status if state._status is not None else ''
        self.ip = str(state._ip)
        self.hostname = state._settings.hostname if state._settings is not None else ''
        self.min_temp = state._settings.minTemp if state._settings is not None else -1000000
        self.max_temp = state._settings.maxTemp if state._settings is not None else 1000000
        self.brightness = state._settings.brightness if state._settings is not None else 0.5
        self.rotated = state._settings.rotated if state._settings is not None else False
