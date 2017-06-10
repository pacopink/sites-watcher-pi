#!/bin/env python
#coding:utf-8
from sakshat import SAKSHAT
import threading
import time
SAKS = SAKSHAT()

class Beeper(threading.Thread):
    '''to make it beep and blink at the same time, this should be in another thread'''
    def run(self):
        self.beep = False
        self.stop = False
        while not self.stop:
            if self.beep:
                self.beep = False
                SAKS.buzzer.beepAction(0.02,0.02,30)
            time.sleep(0.1)
