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

    def showChecking():
        SAKS.digital_display.off() #digital display off  
        led.turn_on(0x0c)

    #initially read dip switch#2 to the flag
    status=SAKS.dip_switch.is_on
    beep_flag = status[1] 
    #callback function when dip_switch status change to turn on/off beeper
    def dipStatus(status):
        #user can set off dip_switch #2 to supress beeper
        print "DIP Status:"
        print status
        global beep_flag
        beep_flag = status[1] #read dip switch #2 to the flag
    #set it to handler
    SAKS.dip_switch_status_changed_handler=dipStatus

    try:
        while True:
            web_checker.do_check(showChecking)
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
                    if(beep_flag):
                        beeper.beep = True
                    led.blink(0xf0)
    except Exception,e:
        traceback.print_exc()
    except KeyboardInterrupt: 
        pass
    finally:
        beeper.stop = True
        beeper.join()
        SAKS.digital_display.off() #digital display off  
        led.turn_on(0x00)

