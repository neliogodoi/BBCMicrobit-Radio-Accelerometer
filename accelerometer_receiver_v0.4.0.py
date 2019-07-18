from microbit import *
import gc
import radio

class AccelReceiver:
    """BBC Microbit Radio Accelerometer Receiver"""

    def __init__(self):
        gc.collect()
        self.msg = ()
        self.count_session = 0
        self.last_sequence_item = 0

    def stand_by(self, putoffms=0):
        sleep(putoffms)
        display.show(Image.ALL_CLOCKS, wait=False, loop=True, delay=100)

    def receive(self):
        gc.collect()
        self.count_session += 1
        new_msg = str(radio.receive()).replace("b'", "").replace("'","").replace("\n","")
        if(new_msg.find('BMAS') == 0):
            message = new_msg.split(' ')
            x, y, z, t, s = message[1].split(',')
            sequence = int(t)
            if ( sequence > self.last_sequence_item ):
                self.msg = '{},{},{},{}'.format(x,y,z,t)
                self.last_sequence_item = sequence
                print(self.msg)

    def run(self):
        self.stand_by()
        while True:

            if button_a.was_pressed():
                display.show(Image.TRIANGLE)
                radio.on()

                while not button_b.was_pressed():
                    gc.collect()
                    self.receive()
                    sleep(0.1)

                radio.off()
                self.stand_by(1000)

            sleep(0.5)

receiver = AccelReceiver()
receiver.run()
