__author__ = 'Michal'
import logging, bob
bob.getConfigData('config.txt')
logName = bob.logFileName

def setLogHandle(fileName):
    '''
        Returns -  s log handle for the logger
    '''
    return logging.FileHandler(fileName)

def setFormat(logHandle):
    format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandle.setFormatter(format)