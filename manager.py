__author__ = 'Michal'
from optparse import OptionParser
import inspect, specialist, logging, bob, stateExpert, generator, random, oracle, glob

#    The manager is the point of contact between the user and the rest of the modules
#      it directly


logName = ''
logHandle = None
#logging set up

def init():
    global logHandle, logName
    bob.getConfigData('config.txt')
    logName = bob.logFileName
    #logging set up
    logger = logging.getLogger("Manager")
    logger.setLevel(logging.DEBUG)
    logHandle = logging.FileHandler(logName)
    formatting = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandle.setFormatter(formatting)
    logger.addHandler(logHandle)
    #check bob paths
    logger.info('LOGGING STARTED')
    bob.testConfig()
    specialist.init(bob.VLCpath,bob.testPath)
    tests = getTests()
    mp3Opt = specialist.optionsMP3
    stateExpert.setTests(tests['WAVE'],tests['MP3'],mp3Opt)
    generator.init(bob.testPath)
    #TODO: Bug, if we have multiple ['] we only sanitize it once
    bob.updateTestData()

def getTests():
    '''
        Returns all the tests that are available based on the convention
            convertToXXX.
    '''
    loggerT = logging.getLogger("Manager.getTests")
    testsAvail = {}
    for name, data in inspect.getmembers(specialist):
        if name == '__builtins__':
            continue
        if inspect.isfunction(data):
            substring = 'convert'
            if substring in repr(data):
                testsAvail[name[name.find('To')+2:]]=name #keys currently become MP3, WAVE
                loggerT.debug('{:11} [Specialist]: Function {} :{}'.format('',name, repr(data)))
    return testsAvail

def runBase():
    generator.runBaseLine()

def sanitizeFiles(files):
    cleanFiles = []
    for file in files:
        cleanFiles.append(specialist.cleanFile(file))
    return cleanFiles

def testAll (fileFormat):
    songsComp = glob.glob(bob.testPath+'/*'+fileFormat)
    testIt = []
    for song in songsComp:
        if 'test ' in song:
            print (song)
            testIt.append(song)
    for test in testIt:
        test = test[test.find('\\')+1:]
        ref = generator.findRef(test)
        ref = ref[ref.find('\\')+1:]
        oracle.compare(ref,test)



init()

songsComp = generator.runTests(bob.testData)
toTest = generator.runTests(songsComp)
print(songsComp)
generator.cleanUp(songsComp)
res = []
for test in toTest:
    test = test[test.find('\\')+1:]
    ref = generator.findRef(test)
    ref = ref[ref.find('\\')+1:]
    res.append(oracle.compare(ref,test))
#generator.cleanUp(toTest)
#generator.cleanUp(songsComp)
res.append(oracle.compare('A Ja Tzo Saritsa.wav', 'A Ja Tzo SaritsaBAD.wav')) #testing bad data
oracle.resultStats(res)
