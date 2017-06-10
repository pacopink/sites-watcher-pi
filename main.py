#!/bin/env python
#coding:utf-8

from sakshat import SAKSHAT
import led
from web_checker import WebChecker
from beeper import Beeper
import time
import traceback

INTERVAL=60 #do http req test interval

def ledOn(x, blink=False):
    '''to contrl led on or blink for 1 second, x should be within [0,8]'''
    byte = led.translate_led_to_byte(x)
    if blink:
        led.blink(byte)
    else:
        led.turn_on(byte)

if __name__=="__main__":
    led.init()
    SAKS = SAKSHAT()
    web_checker = WebChecker(interval=INTERVAL,thread_pool_size=16)
    #Beeper to run in a thread, so that the beep and blink can be simultaneously
    beeper = Beeper()
    beeper.start()

    try:
        while True:
            web_checker.do_check()
            res=web_checker.get_result()
            for i in xrange(0,len(res)):
                led_index=0x01<<i
                delay = res[i]
                #show the index of the site, +1 offset to make it more readable
                SAKS.digital_display.show("%04d"%(i+1)) 
                #use num of leds to show the delay level measured in ms
                if delay is not None:
                    if delay <= 250: #(<250ms)
                        ledOn(1)
                    elif delay <= 500: #(<500ms)
                        ledOn(2)
                    elif delay <= 1000:
                        ledOn(3)
                    elif delay <= 1500:
                        ledOn(4)
                    elif delay <= 2000:
                        ledOn(5)
                    else:
                        ledOn(6)
                else:
                    #alarm with a beep and blink all light
                    beeper.beep = True
                    ledOn(8, blink=True)
            SAKS.digital_display.show("8888") #show 8888 when requesting 
    except Exception,e:
        traceback.print_exc()
        beeper.stop = True
        beeper.join()
    except KeyboardInterrupt: 
        beeper.stop = True
        beeper.join()
