__author__ = 'Michal'
import specialist, logging

tests = {}

def setTests(WAVTest, MP3Test, MP3Options):
    '''
        @Param WAVTest -
        @Param MP3Test -
        @Param MP3Options -
        Sets the necessary information to work with the specialist class and run tests properly
    '''
    global tests
    logger = logging.getLogger('Manager.stateExpert.setTests')
    tests['mp3Tests'] = MP3Test
    tests['mp3Op'] = MP3Options
    tests['wavTests'] =   WAVTest
    logger.debug("[Tests]: {}".format(tests))

def getTest(file):
    '''
        Returns a possible test and options with it based on the file
        @Param file - string name of the file we may wish to test
        Returns - a tuple containing two lists
                    1. List of functions we can run
                    2. List of parameters that vary the function
    '''
    global tests
    logger = logging.getLogger('Manager.stateExpert.getTest')
    #handles certain special character combinations within file names
    file = file[::-1] # reverse file
    songType = file[:file.find('.')+1]
    songType = songType[::-1]
    if songType == '.wav':
        out = [tests['mp3Tests'], []], [tests['mp3Op'], []]
        return out
    elif songType == '.mp3':
        out = [tests['wavTests'], tests['mp3Tests']], [tests['mp3Op'], []]
    #logger.debug(out)
        return out
