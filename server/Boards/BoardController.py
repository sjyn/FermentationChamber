#!/usr/bin/env python
import time

import Boards
from Data import Database


def runBoards():
    tempBoard = Boards.TemperatureBoard()
    lightBoard = Boards.LightBoard()
    fanBoard = Boards.FanBoard()

    database = Database.Database.getInstance()
    sleepTimeSeconds = 180
    # don't leave the light on for more than 3 minutes
    lightFailsafeSeconds = 180
    lightOnSeconds = 0

    print('========================')
    print('| Celsius | Fahrenheit |')
    fmt = '|{cel:.2f}|{fah:.2f}|'
    try:
        while True:
            latestLog = tempBoard.logTemperature()
            print(fmt.format(cel=latestLog.tempCelsius, fah=latestLog.tempFahrenheit))
            if latestLog.tempCelsius < database.getLowerTemp():
                lightBoard.turnOn()
                sleepTimeSeconds = 60
                fanBoard.turnOff()
            elif latestLog.tempCelsius > database.getUpperTemp():
                lightBoard.turnOff()
                sleepTimeSeconds = 180
                fanBoard.turnOn()
            else:
                lightBoard.turnOff()
                sleepTimeSeconds = 180
                fanBoard.turnOff()

            if lightBoard.turnedOn and lightOnSeconds >= lightFailsafeSeconds:
                lightBoard.turnOff()

            if not lightBoard.turnedOn:
                lightOnSeconds = 0

            if lightBoard.turnedOn:
                lightOnSeconds += sleepTimeSeconds

            time.sleep(sleepTimeSeconds)
    finally:
        lightBoard.turnOff()
        fanBoard.turnOff()


if __name__ == '__main__':
    runBoards()
