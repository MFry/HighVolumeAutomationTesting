__author__ = 'Michal'
import subprocess,re,glob,bob, numpy,logging, specialist

testPath = 'C:/Users/Michal/PycharmProjects/HiVAT/testFiles'
answer = 'Objective Difference Grade:'
refType = '.wav'
testsRun = 0

#bob.init()
#extract file names

def init(path):
    testPath = path

def testRun():
    output = None
    p = subprocess.Popen('PQevalAudio "'+'test1.wav'+'" "'+'test1.wav'+'"',shell=True,cwd=testPath, stdout=subprocess.PIPE)
    output, stderr = p.communicate()
    print(findResults(output))

def compareToSelf(song):
    '''
        Establishes a baseline of what is considered a perfect score
    '''
    return compare(song,song)

def compare(reference, test):
    '''
        Compares two songs which need to be .wav at 48000Khz, this will attempt to isolate an identical sample size and account for
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
        Parses the output to find the results
    '''
    output = str(output)
    output = output[output.find(answer)+answer.__len__()+1:]
    return output[:output.find('\\')]

def incCount():
    global testsRun
    testsRun += 1
    return testsRun
#testRun()

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
        if result <= avg-2*stdDev:
            problems += 1
            #TODO: Create a dictionary of keys -> results and store the names to give more information
    logger.info('{:3}[Possible Bugs]: {}'.format('', problems))
