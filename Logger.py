# -*- coding: utf8 -*-
__author__ = 'work'

import logging;
import os;

def initLogger(logfile='default.log', loggername='default', level = logging.INFO):
    import os;
    logging.basicConfig(filename=os.path.normpath(os.getcwd() + '//' + logfile),
                        format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                        level=level);
    global log;
    log = logging.getLogger(loggername);

def info(text):
    global log;
    log.info(text);

def error(text):
    global log;
    log.error(text);



logging.basicConfig(filename=os.path.normpath(os.getcwd() + '//' + 'ESSDZ_everyday_stat_log.log'),
                    format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO);
log = logging.getLogger('ESSDZ_everyday_stat_log');