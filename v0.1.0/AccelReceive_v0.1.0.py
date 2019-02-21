from microbit import *
import gc
import radio
gc.collect()

def remote_accel(message='ERRO', verbose=True, flaglog=True):
    gc.collect()
    if flaglog:
        datalogfilename = 'AccelLog.csv'
        log = open(datalogfilename, 'w')
        log.write(str(message))
        if verbose:
            print(message)
# remote_accell recebee os dados 1° BBC       
def aguarde():
    sleep(1000)
    display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)
# aguarde, mostra imagem na tela enquanto o dispositivo está ocioso
aguarde()
while True:
    gc.collect()
    if button_a.was_pressed():
        radio.on()
        display.show(Image.HAPPY)
        sleep(1000)
        display.show(Image.TRIANGLE)
        count = 0
        while not(button_a.was_pressed()):
            sleep(1000)            
            msg= radio.receive()
            if msg != 'None':
                remote_accel(message=msg)
                count += 1
            gc.collect()
        # gc.collect()
        sleep(1000)
        display.show(Image.SAD)
        sleep(1000)
        display.show(str(count))
        aguarde()
        radio.off()
        
    if button_b.was_pressed():
        sleep(1000)
        display.show(str(count))
        aguarde()


