from microbit import *
import time
import radio
import gc

class RemoteAccel:
    """BBC Microbit Remote Accelerometer"""

    def __init__(self):
        gc.collect()
        # Set the accelerometer settings
        i2c.write(0x1d, b'\x2a\x00')  # Disable to be able to configure
        i2c.write(0x1d, b'\x0e\x00')  # 2g scale
        i2c.write(0x1d, b'\x2b\x02')  # High-resolution
        i2c.write(0x1d, b'\x2a\x19')  # Sample rate of 100Hz
        self.lsbvaluemg = 1.024
        self.count = 0
        self.exit = False

    def _stand_by(self, putoffms=0):
        sleep(putoffms)
        display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)

    def _send(self):
        x = int(accelerometer.get_x()/self.lsbvaluemg)
        y = int(accelerometer.get_y()/self.lsbvaluemg)
        z = int(accelerometer.get_z()/self.lsbvaluemg)
        t = time.ticks_ms() / 1000
        msg = "BMAS {},{},{},{} \n".format(x, y, z, t)
        radio.send(msg)


    def run(self):
        self._stand_by()
        while self.exit is False:
            gc.collect()
            if button_a.was_pressed():
                display.show(Image.TRIANGLE)
                radio.on()
                self.count = 0
                while not (button_b.was_pressed()):
                    self._send()
                    sleep(0.1)
                    self.count += 1
                radio.off()
                self._stand_by(1000)

            if button_b.was_pressed():
                display.show(str(self.count))
                self._stand_by(1000)

sender = RemoteAccel()
sender.run()