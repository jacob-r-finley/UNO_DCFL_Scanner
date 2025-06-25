#!/usr/bin/env python3
import time
from datetime import datetime
from ReadPage import Reader
from UploadTweet import Tweeter
from Logger import Logger
from FormatDate import formatDate as FD

SLEEP_TIME = 5*60 # 5 minutes
UNO_URL = 'https://scsapps.unl.edu/UNO-PoliceReports/MainPage.aspx'

DEBUG = False

'''
This is the main file that will run the program. It will read the UNO Police Reports page, log the data, and tweet it out.
It will run indefinitely, checking for updates every SLEEP_TIME seconds.
'''
def main():
    while True:
        try:
            DEBUG and print('Setting up variables')
            logger = Logger('UNODCL_log.txt')
            logger_tweeted = Logger('Tweeted_logs.txt')
            r = Reader(UNO_URL, logger)
            DEBUG and print('Reading page')
            data = r.readPage()
            dater = FD()
            if not data:
                DEBUG and print('No data found')
                b = f'\nF Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tNothing to update C&F log\n'
                logger.add(b)
                pass
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


if __name__ == '__main__':
    DEBUG and print('Starting main')
    main()
    DEBUG and print('Ending main')
