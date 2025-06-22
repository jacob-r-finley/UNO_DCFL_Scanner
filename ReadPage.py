import requests
from bs4 import BeautifulSoup
from Logger import Logger

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
        self.link = link
        self.request = self.testLink()
        self.soup = BeautifulSoup(self.request.content, 'html.parser')
        self.logger = l

    def testLink(self) -> bool | requests.Response:
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
            if not(199 < status < 300):
                    raise ValueError
        except ValueError:
            return False
        else:
            return r

    def readPage(self) -> bool | dict:
        '''
        Reads the UNODCL and will splice the data accordingly
        Returns:
            True  - read was successful
            False - read was unsuccessful
        '''
        if not(self.link):
            return False
        i = str(self.logger.findNumberOfLogs())
        try:
            reported = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label2').string
            offense = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label5').string
            if not offense:
                offense = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_IncidentCode').string
            build = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label8').string
            if not build:
                build = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_BuildingDescription').string
            loc = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Location').string
            stolen = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label12').string
            damage = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label13').string
            desc = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label14').string
        except AttributeError:
            return False
        else:
            return {
                'report': reported,
                'offense': offense,
                'building': build,
                'location': loc,
                'stolen': stolen,
                'damaged': damage,
                'desc': desc
            }