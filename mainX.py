#!/usr/bin/env python3
from ReadPage import Reader
from UploadTweet import Tweeter
from Logger import Logger
import time
from datetime import datetime
from FormatDate import formatDate as FD


SLEEP_TIME = 45*60 # 2700
TEST_SLEEP_TIME = 20*3 # 60


def main():
    while True:
        print("Hopeful beginning")
        try:
            logger = Logger('UNODCL_log.txt')
            logger_tweeted = Logger('Tweeted_logs.txt')
            r = Reader('https://scsapps.unl.edu/UNO-PoliceReports/MainPage.aspx', logger)
            data = r.readPage()
            dater = FD()
            if type(data) == bool:
                # b = f"\nF Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tNothing to update C&F log\n"
                # logger.add(b)
                pass
            else:
                b = f"\nS Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tSuccessful GET Request\n"
                b_tweeted = f"\n{dater.prettyPrint()}\n\t{str(datetime.now())[11:]}\n\t"
                logger.add(b)
                logger_tweeted.add(b_tweeted)
                twit = Tweeter(data)
                twit.tweet()
                logger.add("\n\tTweet created")
            print("We loggin")
        except:
            b = f"\nF Date: {dater.prettyPrint()}\n\tTime: {str(datetime.now())[11:]}\n\tStatus: {r.request.status_code}\n\tCould not update C&F log\n"
            logger.add(b)
            print("Something went wrong")
        else:
            print("Happy ending")
        for i in range(int(SLEEP_TIME/300)):
            time.sleep(SLEEP_TIME/300)
            print(f"We slept #{i}")
    

def tester():
    string_to_test = "This is a test #HopeThisWorked"
    twit = Tweeter(string_to_test)
    twit.test_tweet()


if __name__ == "__main__":
    main()
    # tester()
