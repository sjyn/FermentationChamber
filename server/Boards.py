import time
import datetime
import pytz

import Boards
from Data import Database
from Data.Converters import c_to_f


class BoardRunner:
    _TMP_FORMAT = '|{time:<10}|{minF:<12.2f}|{currF:<12.2f}|{maxF:<12.2f}|{light:<8}|'
    _HEADER = '|{:<10}|{:<12}|{:<12}|{:<12}|{:<8}|'.format('Time', 'Min F', 'Current F', 'Max F', 'Light')

    def __init__(self):
        self.tempBoard = Boards.TemperatureBoard()
        self.lightBoard = Boards.LightBoard()
        self.database = Database.Database.getInstance()
        self.latestLog = None
        self._logCount = 0

    def run(self):
        try:
            while True:
                self.latestLog = self.tempBoard.logTemperature()
                sleepTime = self._manageLight()
                self._logInfo(self.latestLog.tempFahrenheit, self.lightBoard.turnedOn)
                time.sleep(sleepTime)
        finally:
            self.lightBoard.turnOff()

    def _manageLight(self) -> int:
        sleepTime = 20
        if self.latestLog.tempCelsius < self.database.getLowerTemp():
            self.lightBoard.turnOn()
            sleepTime = 10
        elif self.latestLog.tempCelsius > self.database.getUpperTemp():
            self.lightBoard.turnOff()
        else:
            self.lightBoard.turnOff()
        return sleepTime

    def _logInfo(self, currF, lightState):
        now = datetime.datetime.now(tz=pytz.timezone('America/Denver'))
        timeStr = now.strftime('%H:%M:%S')
        minF = c_to_f(self.database.getLowerTemp())
        maxF = c_to_f(self.database.getUpperTemp())
        lightStr = 'ON' if lightState else 'OFF'
        if self._logCount % 10 == 0:
            self._printHeader()
            self._logCount = 0
        print(self._TMP_FORMAT.format(time=timeStr, minF=minF, currF=currF, maxF=maxF, light=lightStr))
        self._logCount += 1

    def _printHeader(self):
        header = '|{:<10}|{:<12}|{:<12}|{:<12}|{:<8}|'.format('Time', 'Min F', 'Current F', 'Max F', 'Light')
        dashes = '-' * (len(header) - 2)
        print('|' + dashes + '|')
        print(header)
        print('|' + dashes + '|')


def main():
    boardRunner = BoardRunner()
    boardRunner.run()


if __name__ == '__main__':
    main()