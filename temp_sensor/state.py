import queue

class State:
    def __init__(self, output_q: queue.Queue):
        self._temperature = None
        self._output_q = output_q
    
    @property
    def temperature(self):
        return self._temperature
    async def set_temperature(self, value):
        if self._temperature != value:
            self._temperature = value
            await self._output_q.put(OutputState(value))

class OutputState:
    def __init__(self, temperature):
        self._temperature = temperature