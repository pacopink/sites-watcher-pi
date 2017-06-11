#!/bin/env python
#coding:utf-8

import multiprocessing.dummy as multithreading 
import urllib2
from config import web_sites_to_watch
import time
import traceback

class WebChecker:
    def __init__(self, interval=60, thread_pool_size=16):
        '''init a list of check result'''
        self.res = list()
        for i in web_sites_to_watch:
            self.res.append(None)
        self.pool = multithreading.Pool(16)
        self.interval = interval
        #to record the last time
        self.last_check_sec = 0

    def get_result(self):
        '''simply get the result'''
        return self.res

    def check_in_thread(self, x):
        '''this function to do check and set result in a thread'''
        index=web_sites_to_watch.index(x)
        self.res[index] = WebChecker.check(*x)

    def do_check(self, cb):
        '''if reach interval, check all sites, avoid long blocking, run in thread pool, cb is a function to call before check, for example, to set digital display off'''
        now_sec = time.time()
        if now_sec - self.last_check_sec>=self.interval:
            cb()
            self.pool.map(self.check_in_thread, web_sites_to_watch)
            print "do_check: %f"%(time.time()-now_sec)
            self.last_check_sec = now_sec

    @staticmethod
    def check(url, expectation):
        delay = None
        try:  
            t0 = time.time()
            res = urllib2.urlopen(url, timeout=2)
            code = res.getcode()
            if (code==200):
                if (expectation is not None):
                    content = res.read()
                    if (expectation != content):
                        raise Exception("content not match expectation")
                delay = (time.time()-t0)*1000 #the delay is measured in ms
            print "url:[{url}] get resp_code:[{code}]".format(code=code, url=url)
        except urllib2.URLError, e:  
            print "URL:%s exception: %s"%(url,e)
            #traceback.print_exc()
        except Exception,e:
            print "URL:%s exception: %s"%(url,e)
            #traceback.print_exc()

        return delay

