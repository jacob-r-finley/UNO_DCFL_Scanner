import requests
from bs4 import BeautifulSoup
from Logger import Logger
from DBManager import DBManager as DBM
from time import sleep

class Reader:
    '''
    This is the Reader class that will read the UNO Police Reports page
    and return the data from today's log.
    It will use BeautifulSoup to parse the HTML and extract the relevant information.
    '''
    def __init__(self, link: str, l: Logger):
        '''
        Reader object designed to read from the UNODCL and return objects from todays log
        Args:
            link (str): the http link for the UNODCL
            l (Logger): the Logger object to log the results
        '''
        try:
            self.link = link
            self.request = self.testLink()
            if not self.request.content:
                raise ValueError('Webpage was unaccessible')
            self.soup = BeautifulSoup(self.request.content, 'html.parser')
            self.logger = l
            self.counter = 0
            self.dbm = DBM('Test_UNODCL.db')
        except ValueError as err:
            print('Error:', err)
            return err

    def testLink(self) -> requests.Response:
        '''tests the link for UNOCDL
        Raises:
            ValueError: will return an error if webpage was unaccessible 
        Returns:
            False           - webpage was unaccessible
            Response object - link was accessible
        '''
        try:
            r = requests.get(self.link)
            status = r.status_code

            # status 429 means that there are too many requests to the page and we need to wait.
            # we will try this 10 times and then give up
            if status == 429 and 'retry-after' in r.headers._store and self.counter < 10:
                # print('trying after '+ str(r.headers._store['retry-after'][1]) + ' seconds')
                retry_after = int(r.headers._store['retry-after'][1])
                # self.logger.add(f'Rate limit exceeded. Retrying after {retry_after} seconds.')
                sleep(retry_after)
                self.counter += 1
                self.testLink()
            if status == 429 and 'retry-after' in r.headers._store:
                self.counter = 0
                raise TimeoutError
            if not(199 < status < 300):
                    raise ValueError
        except ValueError or TimeoutError as err:
            return err
        else:
            return r

    def readUNOPage(self) -> dict:
        '''
        Reads the UNODCL and will splice the data accordingly
        Returns:
            True  - read was successful
            False - read was unsuccessful
        '''
        if not(self.link):
            return False
        i = str(len(self.dbm.fetch_today_tweets())).zfill(2)
        try:
            reported = self.soup.select_one(f'span[id$="ctl{i}_Label2"]')
            offense = self.soup.select_one(f'span[id$="ctl{i}_Label5"]')
            if not offense:
                offense = self.soup.select_one(f'span[id$="ctl{i}_IncidentCode"]')
            build = self.soup.select_one(f'span[id$="ctl{i}_Label8"]')
            if not build:
                build = self.soup.select_one(f'span[id$="ctl{i}_BuildingDescription"]')
            loc = self.soup.select_one(f'span[id$="ctl{i}_Location"]')
            stolen = self.soup.select_one(f'span[id$="ctl{i}_Label12"]')
            damage = self.soup.select_one(f'span[id$="ctl{i}_Label13"]')
            desc = self.soup.select_one(f'span[id$="ctl{i}_Label14"]')

            return {
                'report': reported.string,
                'offense': offense.string,
                'building': build.string,
                'location': loc.string,
                'stolen': stolen.string,
                'damaged': damage.string,
                'desc': desc.string
            }
        except AttributeError as err:
            return err