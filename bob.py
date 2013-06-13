__author__ = 'Michal'

#    Initializes the basics and does some basic sanity checks to see whether the parameters set make sense.

import glob, os, sys, logging
fileFormat = "/*.wav"
testData = []

VLCpath=''
testPath=''
testDataType=''
logFileName=''
#read the user defined parameters
#Folder with test data
#File Format
#Seed
params = ['files' , 'vlc', 'testDataType', 'logFileName']

def getConfigData (fileName):
    '''
        Given a config file bob will set up the necessary paths for VLC, test data and the log
        fileName - Name of the configuration file
        @param fileName -- Config file that will be loaded
    '''
    try:
        config = open(fileName, 'r').read()
    except FileNotFoundError as err:
        print("Log file {} could not be found".format(err),file=sys.stderr)
        sys.exit(1)
    config = config.split('\n')
    for line in config:
        toUpdate = line[:line.find('=')]
        data = line[line.find('=')+1:]
        update(toUpdate,data)

def update (toUpdate, data):
    '''
        Sets a given variable to data based on the string toUpdate
    '''
    global testPath, VLCpath, testDataType, logFileName
    #TODO: Log the set paths
    #print (data)
    if toUpdate == 'vlc': #update vlc
        VLCpath = data
    elif toUpdate == 'files': #update file path
        testPath = data
    elif toUpdate == 'testDataType': #update the test data types
        testDataType = data
    elif toUpdate == 'logFileName': #update the logFileName
        logFileName = data

#TODO: Improve error handling, tell the user what was not found
def testConfig():
    '''
        Ensures that the paths provided are at least real and contain the data types declared earlier.
    '''
    global testData
    logger = logging.getLogger('Manager.bob.testConfig')
    if os.path.isdir(VLCpath):
        logger.info("{:7}Directory {} found.".format('',VLCpath))
    else:
        logger.error("VLC directory not found!")
    if os.path.isdir(testPath):
        logger.info("{:7}Directory {} found.".format('',testPath))
    else:
        logger.error("Test file directory not found!")
    testData = glob.glob(testPath+'/*'+testDataType)
    if testData.__len__() > 0:
        logger.info("{:7}Test files count: {}".format('',testData.__len__()))
    else:
        logger.error("No test files found")



def updateTestData():
    '''
        Finds all the test data within the folder, counts them and stores them
    '''
    global testData
    logger = logging.getLogger('Manager.bob.updateTestData')
    testData = glob.glob(testPath+'/*'+testDataType)
    if testData.__len__() > 0:
        logger.info("{:3}[Updated] Test files count {}".format('',testData.__len__()))
    else:
        logger.error("No test files found")

'''
#Unit test

getConfigData('config3.txt')
print (testPath)
print (VLCpath)
print (testDataType)
print (logFileName)
testConfig()
'''
