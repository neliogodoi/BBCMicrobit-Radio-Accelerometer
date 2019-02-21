from microbit import *
import radio
import gc

gc.collect()

# Set the accelerometer mode
i2c.write(0x1d, b'\x2a\x00')  # Disable to be able to configure
i2c.write(0x1d, b'\x0e\x00')  # 2g scale
i2c.write(0x1d, b'\x2b\x02')  # High-resolution
i2c.write(0x1d, b'\x2a\x19')  # Sample rate of 100Hz
lsbvaluemg = 1.024
count = 0

def stand_by(putoffms=0):
	sleep(putoffms)
	display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)

stand_by()

while True:
	if button_a.was_pressed():
		gc.collect()
		radio.on()
		display.show(Image.TRIANGLE)
		count = 0
		while not (button_a.was_pressed()):
			radio.send("%d\n" % int(accelerometer.get_x()/lsbvaluemg))
			sleep(7.5)
			count += 1
		display.show('X')
		stand_by(1000)
		radio.off()
		
	if button_b.was_pressed():
		display.show(str(count))
		stand_by(1000)
	
	if button_a.is_pressed() and button_b.is_pressed():
        break
		
