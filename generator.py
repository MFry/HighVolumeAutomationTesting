import random, logging, specialist, stateExpert, os, oracle
__author__ = 'Michal'
__doc__ = ''
seed = None
tests = None
testFilePath = ''
#statistics
convRun = 0

#Given the knowledge of the specialist generate the tests
#Output the test generated

def init(path, s=42):
    global seed, tests, testFilePath
    logger = logging.getLogger("Manager.generator.set")
    seed = s
    random.seed(seed)
    testFilePath = path
    logger.info("{:8}[Seed]: {}".format('',seed))
    logger.info("{:8}[Tests]: {}".format('',tests))

#TODO: Add control to how many tests we wish to run
def runTests(songs):
    logger = logging.getLogger('Manager.generator.runTests')
    songsGen = []
    #runs a single test for each song
    while songs.__len__() > 0:
        incCount()
        ele = random.randint(0,songs.__len__()-1)
        #TODO: Its possible to make this less convoluted by poping the element and then working on it
        testPos = stateExpert.getTest(songs[ele])
        #logger.debug('{:2} Element Picked: {}, song: {} '.format('',ele,songs[ele]))
        logger.debug('{:2}[Conversion] #{:4} [Song:] {}'.format('',convRun, songs[ele][songs[ele].find('\\')+1:]))
        songsGen.append(specialist.getFunc(testPos[0][0])(songs[ele][songs[ele].find('\\')+1:]))
        songs.pop(ele)
    return songsGen

def cleanUp (songs):
    '''
        @Param songs - list of files we wish to delete
        Deletes all the files (within the list songs) from the default directory set by bob for testing data storage
    '''
    logger = logging.getLogger('Manager.generator.cleanUp')
    while songs.__len__() > 0:
        toDel = songs.pop()
        logger.debug('{:3}[Deletion] [{}] from path {}'.format('', toDel, testFilePath))
        os.remove(testFilePath+'/'+toDel)

def findRef (song):
    if 'test ' in song:
     return song[:song.find('test ')-1]+oracle.refType
    else:
        return song

def incCount():
    global convRun
    convRun += 1

def sanitizeFiles(files):
    cleanFiles = []
    for file in files:
        cleanFiles.append(specialist.cleanFile(file))
    return cleanFiles