from Boards import GpioBoard
from Data import Database


class FanBoard(GpioBoard.GpioBoard):
    def __init__(self):
        super().__init__(boardPin=8)

    def turnOn(self):
        super().turnOn()
        database = Database.Database.getInstance()
        database.setFanState(True)

    def turnOff(self):
        super().turnOff()
        database = Database.Database.getInstance()
        database.setFanState(False)
