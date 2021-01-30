from Boards import GpioBoard


class LightBoard(GpioBoard.GpioBoard):
    def __init__(self):
        super().__init__(11)
