__author__ = 'Michal'
import subprocess, numpy, logging, specialist


#    This module is used to interface with an oracle from the TSP Lab
#     (url http://www-mmsp.ece.mcgill.ca/documents/Software/Packages/AFsp/AFsp.html)
#     Currently, because of the weakness of the oracle and the lack of mathematical sophistication
#     the false negative rate is rather high.


testPath = '' #location of folder containing test files
answer = 'Objective Difference Grade:' #string we are looking for
refType = '.wav'
testsRun = 0
sensitivity = 1

def init(path):
    testPath = path

def testRun():
    '''
        Assuming the file test1.wav exists this allows us to test whether we have the proper oracle and things are correctly setup
    '''
    output = None
    p = subprocess.Popen('PQevalAudio "'+'test1.wav'+'" "'+'test1.wav'+'"',shell=True,cwd=testPath, stdout=subprocess.PIPE)
    output, stderr = p.communicate()
    print(findResults(output))

def compareToSelf(song):
    '''
        Establishes a baseline of what is considered a perfect score by comparing a song against itself
    '''
    return compare(song,song)

def compare(reference, test):
    '''
        @param reference -- The original "untouched" song (should be a .wav at 48kHz)
        @param test -- The copy of the song which was modified through a conversion (or synthetic means to create a "bad" song (static noise, drop in volume, ect.)
        Compares two songs which need to be .wav at 48000Khz (for accuracy), this will attempt to isolate an identical sample size and account for db variation
        @return the value within the string outputed by PQevalAudio, more information about the value can be found here (http://www-mmsp.ece.mcgill.ca/documents/Software/Packages/AFsp/PQevalAudio.html)
    '''
    specialist.prep(reference, test)
    testNum = incCount()
    logger = logging.getLogger('Manager.oracle.compare')
    logger.debug('{:6}[PQevalAudio] Reference: {} test file {}'.format('', reference,test))
    p = subprocess.Popen('PQevalAudio "'+reference +'" "'+ test +'"', shell=True, cwd=testPath, stdout=subprocess.PIPE)
    output, stderr = p.communicate()
    if stderr is None:
        pass
    else:
        logger.error(stderr)
    res = findResults(output)
    print(res)
    logger.info('{:7}[PQevalAudio] [Test]#: {} [Results]: {}'.format('', testNum, res))
    return res

def findResults(output):
    '''
        Parses the output string to find the desired numeric value and ignore the extra information
        @param output -- String outputed by PQevalAudio
    '''
    output = str(output)
    output = output[output.find(answer)+answer.__len__()+1:]
    return output[:output.find('\\')]

def incCount():
    '''
        Increments the count for the number of test cases evaluated
        @return -- the current number of evaluated tests
    '''
    global testsRun
    testsRun += 1
    return testsRun


def resultStats(res):
    '''
        Returns the statistical results of the numerical scores given by the compare function
        Flags any score that is bellow the average - 2 standard deviations (This is due to the numbers being negative) and more negative meaning worse.
    '''
    results = []
    for result in res:
        results.append(float(result))
    stdDev = numpy.std(results)
    avg = numpy.average(results)
    logger = logging.getLogger('Manager.oracle.resultStats')
    logger.info('{:3}[Statistical Information]: '.format(''))
    logger.info('{:3}[Data]: {} '.format('', str(res)))
    logger.info('{:3}[Total]: {} '.format('', str(res.__len__())))
    logger.info('{:3}[Average]: {}'.format('', avg))
    logger.info('{:3}[Standard Deviation]: {}'.format('', stdDev))
    problems = 0
    for result in results:
        if result <= avg-sensitivity*stdDev:
            problems += 1
            #TODO: Create a dictionary of keys -> results and store the names to give more information
    logger.info('{:3}[Possible Bugs]: {}'.format('', problems))
