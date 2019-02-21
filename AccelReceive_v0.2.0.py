from microbit import *
import gc
import radio

gc.collect()

def remote_accel_database(message='ERRO', verbose=True, log=True):
    gc.collect()
    if log:
        datalogfilename = 'AccelLog.csv'
        datalog = open(datalogfilename, 'w')
        datalog.write(str(message))
	if verbose:
		print(message)
     
def stand_by(putoffms=0):
    sleep(putoffms)
    display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)
    
stand_by()

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
						remote_accel_database(message=msg)
						count += 1
				except:
					print("msg not is a integer number")
            gc.collect()
        radio.off()
        display.show(str(count))
        stand_by(1000)
        
    if button_b.was_pressed():
        display.show(str(count))
        stand_by(1000)
        
    if button_a.is_pressed() and button_b.is_pressed():
        break

