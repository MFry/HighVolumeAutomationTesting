__author__ = 'Michal'
import specialist, logging
#interface between generator and the speacilist

tests = {}


def setTests(WAVTest, MP3Test, MP3Options):
    '''
        @Param WAVTest - The function containing WAV conversion
        @Param MP3Test - The function containing MP3 conversion
        @Param MP3Options - This contains certain parameters than can be changed that would effect the conversion, such as bitrates and the codec
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
    #find the file extension so that we can give an option of what tests make sense to perform
    file = file[::-1] # reverse file
    songType = file[:file.find('.')+1]
    songType = songType[::-1]
    if songType == '.wav':
        out = [tests['mp3Tests'], []], [tests['mp3Op'], []]
    elif songType == '.mp3':
        out = [tests['wavTests'], tests['mp3Tests']], [tests['mp3Op'], []]
    logger.debug(out)
    return out
