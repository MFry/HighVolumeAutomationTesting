__author__ = 'Michal'

#    This module takes a set of files for testing, moves them and renames them so that they can be easily accessed.

testFileLoc = ''
testData = []

def init (testPath):
    testFileLoc = testPath



def convertTestingItems():
    '''
        Converts all items under test to a specific naming convention so that we do not get any collisions
         or break the script that needs to run via the command console. This module has a somewhat stronger coupling with
    '''