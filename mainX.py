#!/usr/bin/env python3
import argparse
import time
from datetime import datetime
from ReadPage import Reader
from UploadTweet import Tweeter
from Logger import Logger
from FormatDate import formatDate as FD

SLEEP_TIME = 5*60 # 5 minutes
UNO_URL = 'https://scsapps.unl.edu/UNO-PoliceReports/MainPage.aspx'
TWEETED_LOG = 'Tweeted_logs.txt'
UNODCL_LOG = 'UNODCL_log.txt'

'''
This is the main file that will run the program. It will read the UNO Police Reports page, log the data, and tweet it out.
It will run indefinitely, checking for updates every SLEEP_TIME seconds.
'''
def main():
    while True:
        try:
            DEBUG and print('Setting up variables')
            logger = Logger(UNODCL_LOG)
            logger_tweeted = Logger(TWEETED_LOG)
            r = Reader(UNO_URL, logger)
            DEBUG and print('Reading page')
            data = r.readPage()
            dater = FD()
            if not data:
                DEBUG and print('No data found')
                b = f'\nF Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tNothing to update C&F log\n'
                logger.add(b)
            else:
                DEBUG and print('Data found')
                b = f'\nS Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tSuccessful GET Request\n'
                b_tweeted = f'\n{dater.prettyPrint()}\n\t{str(datetime.now())[11:]}\n\t'
                logger.add(b)
                logger_tweeted.add(b_tweeted)
                twit = Tweeter(data)
                DEBUG and print('Creating tweet')
                twit.tweet()
                logger.add('\n\tTweet created')
            DEBUG and print('We logged results')
        except:
            b = f'\nF Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tCould not update C&F log\n'
            logger.add(b)
            DEBUG and print('ERROR: Something went wrong')
        else:
            DEBUG and print('Happy ending')
        time.sleep(SLEEP_TIME)

def testing():
    '''
    This is a testing function that will run the program once and then exit.
    It is used for testing purposes only.
    We won't actually tweet anything, just log the results to Test_UNODCL_log.txt and Test_Tweeted_logs.txt.
    '''
    DEBUG and print('Setting up variables for testing')
    logger = Logger('Test_' + UNODCL_LOG)
    logger_tweeted = Logger('Test_' + TWEETED_LOG)
    DEBUG and print('Clearing log files for testing')
    logger.clearFile()
    logger_tweeted.clearFile()
    DEBUG and print('Reading page for testing')
    r = Reader(UNO_URL, logger)
    data = r.readPage()
    dater = FD()
    if not data:
        DEBUG and print('No data found for testing')
        b = f'\nF Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tNothing to update C&F log\n'
        logger.add(b)
        pass
    else:
        DEBUG and print('Data found for testing')
        b = f'\nS Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tSuccessful GET Request\n'
        b_tweeted = f'\n{dater.prettyPrint()}\n\t{str(datetime.now())[11:]}\n\t'
        logger.add(b)
        logger_tweeted.add(b_tweeted)
        print(data)
        logger.add('\n\tTweet created')
    print('We logged results')

def setupGlobals():
    '''
    This function is used to set up the global variables for the program.
    It is called at the beginning of the main function.
    '''
    global DEBUG, TESTING
    # check if the script is run in testing mode or normal mode
    parser = argparse.ArgumentParser(description="Run the program in testing or normal mode.")
    parser.add_argument('--testing', action='store_true', help="Run the program in testing mode.")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode.")
    args = parser.parse_args()
    DEBUG = args.debug
    TESTING = args.testing

if __name__ == '__main__':
    setupGlobals()
    DEBUG and print('Starting main')
    if TESTING:
        DEBUG and print('Running in testing mode')
        testing()
    else:
        DEBUG and print('Running in normal mode')
        main()
    DEBUG and print('Ending main')