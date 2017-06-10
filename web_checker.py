#!/bin/env python
#coding:utf-8

import multiprocessing.dummy as multithreading 
import urllib2
from config import web_sites_to_watch
import time

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

    def do_check(self):
        '''if reach interval, check all sites, avoid long blocking, run in thread pool'''
        now_sec = time.time()
        if now_sec - self.last_check_sec>=self.interval:
            self.pool.map(self.check_in_thread, web_sites_to_watch)
            self.last_check_sec = now_sec

    @staticmethod
    def check(url, expectation):
        delay = None
        try:  
            t0 = time.time()
            res = urllib2.urlopen(url, timeout=3)
            code = res.getcode()
            content = res.read()
            print "url:[{url}] get resp_code:[{code}]".format(code=code, url=url)
            if (code==200):
                if (expectation is None) or (expectation is not None and content  == expectation):
                    delay = (time.time()-t0)*1000 #the delay is measured in ms
        except urllib2.URLError, e:  
            print e.reason  
            #print len(f)  
        return delay

