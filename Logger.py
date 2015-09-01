# -*- coding: utf8 -*-
__author__ = 'alkarps'

import logging

def initLogger(logfile='default.log', loggername='default', level = logging.INFO):
    import os
    logging.basicConfig(filename=os.path.normpath(os.getcwd() + '//' + logfile),
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=level)
    global log
    log = logging.getLogger(loggername)

def info(text):
    global log
    log.info(text)

def error(text):
    global log
    log.error(text)



log = None