# -*- coding: utf-8 -*-
"""
日志记录
"""
import logging
import os
from logzero import setup_logger

from ocrstock.config.config import gvariable

class mylogger():
    """日志"""
    def __init__(self, logfile='ocrstock.log', name='me'):
        self.logpath=gvariable.logpath
        self.logfile=logfile
        self.name=name
        self.log=None
        self.errlog=None
        self.__init_log()

    def __init_log(self):
        """初始化日志参数"""
        file=os.path.join(self.logpath, self.logfile)
        formatter=logging.Formatter('%(asctime)s-%(name)s-\n  %(message)s')
        log=setup_logger(self.name, file, formatter=formatter, maxBytes=1e6, backupCount=3)
        self.log=log

    def __init_errorlog(self):
        """初始化错误日志"""
        file = self.logfile.split('.')[0] + '_important_error.log'
        file = os.path.join(self.logpath, file)
        formatter = logging.Formatter('%(asctime)s-%(name)s-%(pathname)s-%(module)s-\n  %(message)s')
        log = setup_logger(self.name, file, formatter=formatter, maxBytes=1e6, backupCount=3)
        self.errlog = log

    def info(self,string):
        """记录日志"""
        self.log.info(string)

    def error(self,string):
        """记录错误日志"""
        if not self.errlog:
            self.__init_errorlog()
        # 记录日志
        self.log.error(string)
        self.errlog.error(string)


def test():
    log=mylogger('sdfsf.log')
    log.info('heiheihei')
    log = mylogger('sdfsf.log','you')
    log.info('123')
    log = mylogger('sdfsf.log')
    log.info('234')
    log.error('error')

