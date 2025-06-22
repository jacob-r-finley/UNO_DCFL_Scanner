import requests
from bs4 import BeautifulSoup
from Logger import Logger

# Links:
# https://scsapps.unl.edu/UNO-PoliceReports/MainPage.aspx
# https://www.geeksforgeeks.org/python-web-scraping-tutorial/
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all

'''
This is the Reader class that will read the UNO Police Reports page and return the data from today's log.
It will use BeautifulSoup to parse the HTML and extract the relevant information.
It will return a dictionary with the following keys:
- offense: the offense reported
- report: the report number
- disposition: the disposition of the case
- occurred: the date and time the offense occurred
- building: the building where the offense occurred
- location: the location of the offense
- stolen: the value of stolen property
- damaged: the value of damaged property
- desc: a description of the offense
'''
class Reader:
    def __init__(self, link: str, l: Logger):
        '''Reader object designed to read from the UNODCL and return objects from todays log

        Args:
            link (str): the http link for the UNODCL
        '''
        self.link = link
        self.request = self.testLink()
        self.soup = BeautifulSoup(self.request.content, 'html.parser')
        self.logger = l

    def testLink(self):
        '''tests the link for UNOCDL
        
        Raises:
            ValueError: will return an error if webpage was unaccessible 

        Returns:
            False if webpage was unaccessible
            
            Response object if link was accessible
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
        '''meat and potatoes of program. Reads the UNODCL and will splice the data accordingly

        Returns:
            bool: True if read was successful
                  False if read was unsuccessful
        '''
        if not(self.link):
            return False
        i = str(self.logger.findNumberOfLogs())
        try:
            offense = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label5').string
            reported = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label2').string
            disp = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label3').string
            occ = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_OccurredDateRange').string
            build = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label8').string
            loc = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Location').string
            stolen = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label12').string
            damage = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label13').string
            desc = self.soup.find('span', id=f'ctl00_ContentPlaceHolder1_ResultList2_ctl{i.zfill(2)}_Label14').string
        except AttributeError:
            return False
        else:
            return {'offense': offense,
                    'report': reported,
                    'disposition': disp,
                    'occurred': occ,
                    'building': build,
                    'location': loc,
                    'stolen': stolen,
                    'damaged': damage,
                    'desc': desc}