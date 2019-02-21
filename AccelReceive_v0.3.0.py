from microbit import *
import gc
import radio

class RemoteAccelReceive:
	def __init__(self):
		gc.collect()
		self.stand_by()

	def remote_accel_database(self, message='ERRO', verbose=True, log=True):
		gc.collect()
		if log:
			datalogfilename = 'AccelLog.csv'
			datalog = open(datalogfilename, 'w')
			datalog.write(str(message))
		if verbose:
			print(message)
     
	def stand_by(self, putoffms=0):
		sleep(putoffms)
		display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)
		
    def run(self):
		while True:
			gc.collect()
			if button_a.was_pressed():
				display.show(Image.TRIANGLE)
				count = 0
				radio.on()
				while not(button_a.was_pressed()):
					msg= radio.receive()
					if msg != 'None':
						try:
							if int(msg):
								self.remote_accel_database(message=msg)
								count += 1
						except:
							print("msg not is a integer number")
					gc.collect()
				radio.off()
				display.show(str(count))
				self.stand_by(1000)
				
			if button_b.was_pressed():
				display.show(str(count))
				self.stand_by(1000)

receiver = RemoteAcellReceive()
receiver.run()	
