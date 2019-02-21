from microbit import *
import radio
import gc

gc.collect()

def remote_accel_log(numAccelReadings, pausems, lsbvaluemg, verbose=True, flaglog=True):
    if flaglog:
        radio.send("Aceleracao no eixo x (mg), Tempo (ms)\n")
    accelmglist = [0]*numAccelReadings
    timemslist = [0]*numAccelReadings
    initialtimems = running_time()
    i = 0
    while (i < numAccelReadings):
        accelmg = int(accelerometer.get_x()/lsbvaluemg)
        accelmglist[i] = accelmg
        timems = (running_time()) - initialtimems
        timemslist[i] = timems
        if verbose:
            print("Accelerometer x axis reading = %4d mg, %d ms" % (accelmg, timems))
        sleep(pausems) 
        i += 1
    finaltimems = running_time()
    gc.collect()
    if flaglog:
        ti = running_time()
        i = 0
        while (i < numAccelReadings):
            radio.send("%d, %4d\n" % (timemslist[i], accelmglist[i]))
            i += 1
        tf = running_time()
    deltatimems = finaltimems - initialtimems
# remote_accel_log envia os coletados ao 2º BBC

# Set the accelerometer mode
i2c.write(0x1d, b'\x2a\x00')  # Disable to be able to configure
i2c.write(0x1d, b'\x0e\x00')  # 2g scale
lsbvaluemg = 1.024
i2c.write(0x1d, b'\x2b\x02')  # High-resolution
i2c.write(0x1d, b'\x2a\x19')  # Sample rate of 100Hz

display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)

while True:
    if button_a.was_pressed():
        display.show(Image.YES)
        sleep(1000)
        gc.collect()
        radio.on()
        display.show(Image.TRIANGLE)
        while not(button_b.was_pressed()):
            sleep(1000)
            remote_accel_log(400, 7.5, lsbvaluemg, verbose=False, flaglog=True)
            gc.collect()
        display.show('X')
        sleep(1000)
        display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)
        radio.off()

