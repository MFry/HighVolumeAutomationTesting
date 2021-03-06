__author__ = 'Michal'
from string import Template
import subprocess, shutil, logging, os, time, datetime, glob

#interface between generator and the speacilist
#drives the application under test

#be able to drive application videoLAN
#provide several conversion options
#convert a song to a specified format
#convert it back
specLogger = logging.getLogger('Manager.specialist')
handledConv = ['.mp3','.wav']
unhandledSpecChar = ["'", ',', '_']
optionsMP3 = ['128','160','192','320'] #options for MP3
VLCpath= ''
testPath= ''
#TODO: A bug occurs when a file name ends with "test "
#NOTE: Files that may have an extension more than three chars (or less) long will not work at the moment

def init (VLC, testFilesLoc):
    setPaths(VLC, testFilesLoc)
    for conv in handledConv:
        testFiles = glob.glob(testPath+'/*'+conv)
        sanitizeFiles(testFiles)

def setPaths (VLC, testFilesLoc):
    '''
        @param VLC -- Path to a VLC folder
        @param testFilesLoc -- Path to the folder which contains all of your test files
    '''
    global VLCpath,testPath
    logger = logging.getLogger('Manager.specialist.setPaths')
    VLCpath=VLC
    logger.debug('{:1}[PATH]: VLC: {}'.format('',VLC))
    testPath=testFilesLoc
    logger.debug('{:1}[PATH] Test Files: {}'.format('',testFilesLoc))

def convertToWAVE(fileName, codec='s16l', channels='2', outputBitRate='128', sampleRate='48000', type='wav'):
    '''
        Given a filename this function will attempt to call VLC and convert it into a WAVE format
        @param fileName -- The name of the file to be converted
        @param codec -- the codec used to do the conversion (VLC command line parameter)
        @param channels -- (VLC command line parameter)
        @param outputBitRate -- (VLC command line parameter)
        @param sampleRate -- For the purposes of this particular oracle implementation, we should always keep it at 48kHz(VLC command line parameter)
        @param type
        Returns a string necessary to be called to convert the file to a WAVE file
    '''
    outputSongName = getOutputName(fileName[:-4], '.wav')
    shutil.copy2(testPath+'/'+fileName,VLCpath+'/'+fileName)
    #adding -vvv after dummy creates no cmd screen but dumps everything to stderr
    t = Template ('vlc -I dummy $song ":sout=#transcode{acodec=$codec,channels=$channels,ab=$outputBitRate,samplerate=$sampleRate}:std{access=file,mux=$type,dst=$outputSongName}" vlc://quit')
    command = t.substitute(song='"'+fileName+'"', codec=codec, channels=channels, outputBitRate=outputBitRate,
                        sampleRate=sampleRate,type=type, outputSongName=outputSongName)
    print (command)
    p = subprocess.Popen(command, cwd=VLCpath, shell=True)
    stdout, stderr = p.communicate()
    #TODO: log stderr and stdout
    #clean up
    os.remove(VLCpath+'/'+fileName)
    shutil.move(VLCpath+'/'+outputSongName,testPath+'/'+outputSongName)
    return outputSongName

def convertToMP3(fileName,codec='mpga',outputBitRate='192'):
    """
        Given a filename this function will attempt to convert it (via VLC) to MP3 with the codec and the outputbitrate
        @outputBitRate - 128,160,192,320
             INFO: Uncompressed audio as stored on an audio-CD has a bit rate of 1,411.2 kbit/s,[note 2]
                   so the bitrates 128, 160 and 192 kbit/s represent compression ratios of approximately 11:1, 9:1 and 7:1 respectively.

              Non-standard bit rates up to 640 kbit/s can be achieved with the LAME encoder and the freeformat option,
               although few MP3 players can play those files. According to the ISO standard, decoders are only required to be able to decode streams up to 320 kbit/s.[45]
    """
    outputSongName = getOutputName(fileName[:-4], '.mp3')
    shutil.copy2(testPath+'/'+fileName,VLCpath+'/'+fileName)
    t = Template('vlc -I dummy $song ":sout=#transcode{acodec=$codec,ab=$outputBitRate}:std{dst=$outputSongName,access=file}" vlc://quit')
    command = t.substitute(song='"'+fileName+'"', codec=codec, outputBitRate=outputBitRate, outputSongName=outputSongName)
    print (command)
    p = subprocess.Popen(command, cwd=VLCpath, shell=True)
    stdout, stderr = p.communicate()
    #log stderr and stdout
    os.remove(VLCpath+'/'+fileName)
    shutil.move(VLCpath+'/'+outputSongName,testPath+'/'+outputSongName)
    return outputSongName


def getFunc(funcName):
    if 'convertToMP3' == funcName:
        return convertToMP3
    elif 'convertToWAVE' == funcName:
        return convertToWAVE


def getOutputName(song, type):
    files = glob.glob(testPath+'/*'+type)
    found = []
    for file in files:
        if song in file:
            candidate = file[file.find('\\')+2:]
            if 'test' in candidate:
                found.append(candidate)
    testNum = findNextTestNumber(found, type)
    outName = ''
    if 'test' in song:
        outName = song[:song.find('test ')+'test '.__len__()]+str(testNum)+type
    else:
        outName = song+' test '+ str(testNum)+type
    return(outName)

def findNextTestNumber(list, type):
    testNum = 0
    for file in list:
        curNum = file[file.find('test ')+'test '.__len__():file.find(type)]
        curNum = int(curNum)
        if testNum < curNum:
            testNum = curNum
    testNum += 1
    return testNum

def sanitizeFiles(files):
    cleanFiles = []
    for file in files:
        cleanFiles.append(cleanFile(file))
    return cleanFiles

#TODO: Make it work for arbitrary number of special chars
def cleanFile(fileName):
    logger = logging.getLogger('Manager.specialist.cleanFile')
    fileName = fileName[fileName.find('\\')+1:]
    out = fileName
    sanitized = False
    for specChar in unhandledSpecChar:
        if specChar in fileName:
            sanitized = True
            out = removeSpecialChar(out, specChar)
    if sanitized:
        logger.info('{:1}[Sanitized] file {} rename to {}'.format('', fileName, out))
    os.rename(testPath+'/'+fileName, testPath+'/'+out)
    return out


def removeSpecialChar (name, char):
    return name[:name.find(char)]+name[name.find(char)+1:]

def prep(refSong, testSong):
    '''
        Attempts to clean up the songs, by changing the db gain and resampling the songs to improve the accuracy of the oracle
        NOTE: Proper resampling within the library that the oracle uses does not work, even using their sample code
               this may be the lack of understanding of the code or a bug
    '''
    logger = logging.getLogger('Manager.specialist.prep')
    #make testSong into a tempFile
    #clean it up
    command = 'CompAudio "'+ refSong +'" "' + testSong + '"'
    p = subprocess.Popen(command, cwd=testPath, shell=True, stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if stderr is None:
        pass
    else:
        logger.error(stderr)
    output = str(stdout)
    dbGain = output[output.find('File B = ')+'File B = '.__len__(): output.find(')\\r\\n Seg.')]
    samplesNum = []
    samples = output.split('Number of samples : ')
    for samp in samples:
        if ' (' in samp:
            offset = samp.find(' (')
            samplesNum.append(samp[:offset])
    logger.debug('{:5}[Sample Rates]: {} [db Gain]: {}'.format('', samplesNum, dbGain))

    #db gain of one implies that the file does not need to be adjusted, through testing
    #   adjusting the db improves accuracy of the oracle
    if dbGain != 1:
        tempName = 'tempf.wav'
        os.rename(testPath+'/'+testSong, testPath+'/'+tempName)
        command = 'ResampAudio -i 1 -g ' + str(dbGain) + ' "' + tempName + '" "' + testSong + '"'
        p = subprocess.Popen(command, cwd=testPath, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stderr is None:
            pass
        else:
            logger.error(stderr)
        #print(str(stdout))
        os.remove(testPath+'/'+tempName)
    # different sampling rates significantly distorts the accuracy of the oracle
    if samplesNum[0] > samplesNum[1]:
        logger.debug('{:5}[Resampling]: {}'.format('', refSong))
        tempName = 'tempf.wav'
        os.rename(testPath+'/'+refSong, testPath+'/'+tempName)
        command = 'CopyAudio -l 0:' + str(samplesNum[0]) + ' "' + tempName + '" "' + refSong + '"'
        p = subprocess.Popen(command, cwd=testPath, shell=True, stdout=subprocess.PIPE)
        stdout, stderr = p.communicate()
        if stderr is None:
            pass
        else:
            logger.error(stderr)
        #print(str(stdout))
        os.remove(testPath+'/'+tempName)
