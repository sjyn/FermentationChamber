from Data import Database, Converters


class BoardApi:
    database = Database.Database.getInstance()

    @classmethod
    def getState(cls):
        temps = cls.database.getLast24HoursTemps()
        temps = [{'time': t.timestamp, 'f': t.tempFahrenheit, 'c': t.tempCelsius} for t in temps]

        bounds = (cls.database.getLowerTemp(), cls.database.getUpperTemp())
        return {
            'lower_temp_bound': {
                'c': bounds[0],
                'f': Converters.c_to_f(bounds[0])
            },
            'upper_temp_bound': {
                'c': bounds[1],
                'f': Converters.c_to_f(bounds[1])
            },
            'temperatures': temps,
            'fan_status': cls.database.getFanState()
        }

    @classmethod
    def setTempBounds(cls, lowerCelsius: float, upperCelsius: float):
        cls.database.setLowerTemp(lowerCelsius)
        cls.database.setUpperTemp(upperCelsius)

        bounds = (cls.database.getLowerTemp(), cls.database.getUpperTemp())
        return {
            'lower_temp_bound': {
                'c': bounds[0],
                'f': Converters.c_to_f(bounds[0])
            },
            'upper_temp_bound': {
                'c': bounds[1],
                'f': Converters.c_to_f(bounds[1])
            },
        }
