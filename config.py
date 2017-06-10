#!/bin/env python
#coding:utf-8

# list of websites to watch
# param[0] is the URL to send http request to
# param[1] is the expected content, if it is None, 
#          only check if the response status is 200, 
#          else the response content should equals to param[1]

web_sites_to_watch=[
        ["http://www.github.com", None],
        ["http://www.baidu.com", None],
        ["http://www.google.com", None],
        ["http://www.bing.com", None],
        ["http://my_site/heartbeat.html","my-heart-will-go-on"],
]
