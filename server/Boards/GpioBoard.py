import RPi.GPIO as GPIO


class GpioBoard:
    def __init__(self, boardPin):
        self._pin = boardPin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self._pin, GPIO.OUT)
        self.turnedOn = False

    def turnOn(self):
        if not self.turnedOn:
            GPIO.output(self._pin, GPIO.HIGH)
            self.turnedOn = True

    def turnOff(self):
        if self.turnedOn:
            GPIO.output(self._pin, GPIO.LOW)
            self.turnedOn = False
