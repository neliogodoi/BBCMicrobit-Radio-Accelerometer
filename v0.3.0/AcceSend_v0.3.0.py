from microbit import *
import radio
import gc

class RemoteAcellSend:
	
	def __init__(self):
		gc.collect()
		# Set the accelerometer mode
		i2c.write(0x1d, b'\x2a\x00')  # Disable to be able to configure
		i2c.write(0x1d, b'\x0e\x00')  # 2g scale
		i2c.write(0x1d, b'\x2b\x02')  # High-resolution
		i2c.write(0x1d, b'\x2a\x19')  # Sample rate of 100Hz
		self.lsbvaluemg = 1.024
		self.count = 0
		self._stand_by()

	def _stand_by(self, putoffms=0):
		sleep(putoffms)
		display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)

	def run(self):
		while True:
			if button_a.was_pressed():
				gc.collect()
				radio.on()
				display.show(Image.TRIANGLE)
				self.count = 0
				while not (button_a.was_pressed()):
					radio.send("%d\n" % int(accelerometer.get_x()/self.lsbvaluemg))
					sleep(7.5)
					self.count += 1
				display.show('X')
				self._stand_by(1000)
				radio.off()
				
			if button_b.was_pressed():
				display.show(str(self.count))
				self._stand_by(1000)

sender = RemoteAcellSend()
sender.run()		
