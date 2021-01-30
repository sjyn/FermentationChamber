import json
import time

import redis
from Data import TemperatureLog


class Database:
    instance = None

    @classmethod
    def getInstance(cls):
        if Database.instance is None:
            Database.instance = cls()
        return Database.instance

    def __init__(self):
        self.database = redis.StrictRedis(host='localhost', port=6379, db=0)

    def logTemp(self, log: TemperatureLog.TemperatureLog):
        self.database.zadd('temp_log', {str(log.tempCelsius): log.timestamp})

    def getLast24HoursTemps(self) -> [TemperatureLog.TemperatureLog]:
        oneDayMs = 24 * 60 * 60 * 1000
        upperBound = int(time.time())
        lowerBound = upperBound - oneDayMs
        rawData = self.database.zrange('temp_log', lowerBound, upperBound, withscores=True)
        return [TemperatureLog.TemperatureLog(float(data[0]), data[1]) for data in rawData]

    def setFanState(self, fansOn: bool):
        self.database.set('fan_state', str(fansOn))

    # whether or not the fans are running
    def getFanState(self) -> bool:
        return bool(self.database.get('fan_state'))

    # ms between temperature checks
    def getTempRefreshTime(self) -> int:
        return self.database.get('temp_refresh') or 180000

    def setTempRefreshTime(self, timeMs: int):
        self.database.set('temp_refresh', timeMs)

    def setUpperTemp(self, tempCelsius: float):
        self.database.set('temp_upper', tempCelsius)

    def setLowerTemp(self, tempCelsius: float):
        self.database.set('temp_lower', tempCelsius)

    # celsius upper threshold
    def getUpperTemp(self) -> float:
        return float(self.database.get('temp_upper')) or 26.0

    # celsius lower threshold
    def getLowerTemp(self) -> float:
        return float(self.database.get('temp_lower')) or 21.0

    def createItem(self, itemDict: dict):
        # self.database.set(itemDict['id'], itemDict)
        self.database.hset('items', itemDict['id'], json.dumps(itemDict))

    def deleteItem(self, itemId: str):
        self.database.hdel('items', itemId)

    def listItems(self) -> [dict]:
        idToDict = self.database.hgetall('items')
        items = []
        for itemId, itemBody in idToDict.items():
            items.append(json.loads(itemBody))
        return items
