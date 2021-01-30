import time

from Data import Converters


class TemperatureLog:
    @property
    def tempFahrenheit(self) -> float:
        return Converters.c_to_f(self.tempCelsius)

    def __init__(self, tempCelsius: float, timestamp=None):
        self.tempCelsius = tempCelsius
        self.timestamp = timestamp
        if self.timestamp is None:
            self.timestamp = time.time()
        self.timestamp = int(self.timestamp)
