import glob
import time

from Data import Database
from Data import TemperatureLog


class TemperatureBoard:
    _baseDir = '/sys/bus/w1/devices/'
    _deviceFolder = glob.glob(_baseDir + '28*')[0]
    _deviceFile = _deviceFolder + '/w1_slave'

    def logTemperature(self) -> TemperatureLog.TemperatureLog:
        database = Database.Database.getInstance()
        log = TemperatureLog.TemperatureLog(self._readTemperature()[0])
        database.logTemp(log)
        return log

    def _readRawTemp(self):
        f = open(self._deviceFile, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def _readTemperature(self) -> (float, float):
        lines = self._readRawTemp()
        while lines[0].strip()[-3:] != 'YES':
            time.sleep(0.2)
            lines = self._readRawTemp()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2:]
            temp_c = float(temp_string) / 1000.0
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            return temp_c, temp_f
