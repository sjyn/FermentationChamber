#!/usr/bin/env python
import time
import pytz
import datetime

import Boards
from Data import Database
from Data.Converters import c_to_f


def runBoards():
    tempBoard = Boards.TemperatureBoard()
    lightBoard = Boards.LightBoard()
    fanBoard = Boards.FanBoard()

    database = Database.Database.getInstance()
    sleepTimeSeconds = 180
    # don't leave the light on for more than 3 minutes
    lightFailsafeSeconds = 180
    lightOnSeconds = 0

    # print('| Celsius | Fahrenheit | Light Status | Min Temp C | Min Temp F | Max Temp C | Max Temp F |')
    # fmt = '|{cel:.2f<9}|{fah:.2f<12}|{light<14}|{minc:.2f<12}|{minf:.2f<12}|{maxc:.2f<12}|{maxf:.2f<12}|'
    try:
        while True:
            latestLog = tempBoard.logTemperature()
            if latestLog.tempCelsius < database.getLowerTemp():
                lightBoard.turnOn()
                # sleepTimeSeconds = 60
                fanBoard.turnOff()
            elif latestLog.tempCelsius > database.getUpperTemp():
                lightBoard.turnOff()
                # sleepTimeSeconds = 180
                fanBoard.turnOn()
            else:
                lightBoard.turnOff()
                # sleepTimeSeconds = 180
                fanBoard.turnOff()

            if lightBoard.turnedOn and lightOnSeconds >= lightFailsafeSeconds:
                lightBoard.turnOff()

            if not lightBoard.turnedOn:
                lightOnSeconds = 0

            if lightBoard.turnedOn:
                lightOnSeconds += sleepTimeSeconds
            sleepTimeSeconds = 60 if lightBoard.turnedOn else 180
            now = datetime.datetime.now(tz=pytz.timezone('America/Denver'))
            print(('=' * 30) + now.strftime('%H:%M:%S') + ('=' * 30))
            print('\tCelsius:               ',latestLog.tempCelsius)
            print('\tFahrenheit:            ', latestLog.tempFahrenheit)
            print('\tLight                  ', 'ON' if lightBoard.turnedOn else 'OFF')
            print('\t Min Celsius           ', database.getLowerTemp())
            print('\t  Min Fahrenheit       ', c_to_f(database.getLowerTemp()))
            print('\t Max Celsius           ', database.getUpperTemp())
            print('\t  Max Fahrenheit       ', c_to_f(database.getUpperTemp()))
            print('\tChecking in {0} seconds'.format(sleepTimeSeconds))
            time.sleep(sleepTimeSeconds)
    finally:
        lightBoard.turnOff()
        fanBoard.turnOff()


if __name__ == '__main__':
    runBoards()