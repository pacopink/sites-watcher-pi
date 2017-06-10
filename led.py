#!/bin/env python
#coding:utf8
import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
DS = 6
SHCP = 19
STCP = 13
 
def init():
    GPIO.setup(DS, GPIO.OUT)
    GPIO.setup(SHCP, GPIO.OUT)
    GPIO.setup(STCP, GPIO.OUT)
 
    GPIO.output(DS, GPIO.LOW)
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.LOW)
 
def writeBit(data):
    GPIO.output(DS, data)
 
    GPIO.output(SHCP, GPIO.LOW)
    GPIO.output(SHCP, GPIO.HIGH)
 
#写入8位LED的状态
def writeByte(data):
    for i in range (0, 8):
        writeBit((data >> i) & 0x01)
    #状态刷新信号
    GPIO.output(STCP, GPIO.LOW)
    GPIO.output(STCP, GPIO.HIGH)

def turn_on(data):
    writeByte(data)
    time.sleep(1)

def blink(data):
    for i in xrange(0,5):
        writeByte(data)
        time.sleep(0.1)
        writeByte(0x00)
        time.sleep(0.1)

#x should be within (0~8)
def translate_led_to_byte(x):
    byte=0
    for i in xrange(0,x):
        byte = (byte<<1)+0x01
    return byte
 
if __name__=="__main__":
    try:
        init()
        while True:
            #以下一组8个编码由一组二进制转换而成：
            #00000001,00000010,00000100,00001000,00010000,00100000,01000000,10000000
            #分别对应8个LED点亮状态
            for i in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
                blink(i)
                #writeByte(i)
                #time.sleep(0.2)
            #LED组全开
            #writeByte(0xff)
            #time.sleep(0.1)
     
    except KeyboardInterrupt:
        print "except"
        #LED组全关
        writeByte(0x00)
        GPIO.cleanup()
