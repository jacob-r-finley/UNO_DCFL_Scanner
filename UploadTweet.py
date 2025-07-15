import tweepy
import json
from DBManager import DBManager as DBM

TWEET_LIMIT = 280

class Tweeter:
    '''
    This class is responsible for tweeting the data from the UNO Police Reports page.
    It will use the Tweepy library to interact with the Twitter API.
    It will read the keys from a JSON file and use them to authenticate with the Twitter API
    and then tweet the data.
    '''
    def __init__(self, data: str):
        '''
        Tweeter object designed to tweet the data from the UNO Police Reports page
        Args:
            data (dict | str): the data to tweet
        '''
        self.__consumerKey = None
        self.__consumerSecret = None
        self.__accessToken = None
        self.__accessTokenSecret = None
        self.__bearerToken = None
        self.data = data
        self.grabData()
        self.client = tweepy.Client(
            consumer_key=self.__consumerKey,
            consumer_secret=self.__consumerSecret,
            access_token=self.__accessToken,
            access_token_secret=self.__accessTokenSecret,
        )
        self.dbm = DBM('UNODCL.db')

    def grabData(self) -> bool:
        '''
        Grabs the keys from the keys.json file and sets them as class variables
        Raises:
            FileNotFoundError: if the keys.json file is not found
            KeyError: if any of the keys are not found in the JSON file
        '''
        try:
            jsonFile = open('keys.json')
            jsonData = json.load(jsonFile)
            self.__consumerKey = jsonData.get('consumerKey')
            self.__consumerSecret = jsonData.get('consumerSecret')
            self.__accessToken = jsonData.get('accessToken')
            self.__accessTokenSecret = jsonData.get('accessTokenSecret')
            self.__bearerToken = jsonData.get('bearerToken')
        except:
            return False
        finally:
            jsonFile.close()

    def tweet(self, args) -> tweepy.client.Response:
        '''
        Tweets the data from the UNO Police Reports page
        Raises:
            tweepy.TweepyException: if there is an error with the Twitter API
        '''
        writtenData = self.parseData()

        # need to check if we already tweeted this data.
        if not self.didWeAlreadyTweetThis() or args['status'] == 'testing':
            return False
        
        # since we know we didn't tweet this data, we can insert it into the database
        self.dbm.insert_tweet(self.data)
        response = self.client.create_tweet(
            text=writtenData,
        )
        return response

    def parseData(self) -> str:
        '''
        Parses the data from the UNO Police Reports page and formats it for tweeting
        Returns:
            str: the formatted data ready for tweeting
        '''
        builder = ''
        tags = ['#KnowTheO', '#MavSpirit', '#NUforNE']

        # add data from the report to be built for the tweet
        if 'offense' in self.data:
            builder += f'{self.data["offense"]}\n'
        if 'report' in self.data:
            builder += f'{self.data["report"]} '
        if 'building' in self.data:
            loc = self.data['location'][0:self.data['location'].find('(')]
            if self.data['building'] == 'N/A' and len(loc) == 0:
                builder += 'at No listed location'
            elif self.data['building'] != 'N/A' and len(loc) > 0:
                builder += f'at {self.data["building"]} on {loc}'
            elif self.data['building'] == 'N/A':
                builder += f'at {loc}'
            else:
                builder += f'at {self.data["building"]}'
            builder += '\n'
        if 'stolen' in self.data and self.data['stolen'] != '$0.00':
            builder += f'Stolen: {self.data["stolen"]}\n'
        if 'damaged' in self.data and self.data['damaged'] != '$0.00':
            builder += f'Damaged: {self.data["damaged"]}\n'
        if 'desc' in self.data:
            if self.data['desc'] is None:
                builder += 'No further details provided\n'
            else:
                builder += f'{self.data["desc"]}\n'

        # add hashtags to the tweet as long as they fit within the tweet limit
        for tag in tags:
            if len(f'{builder + tag}') <= TWEET_LIMIT:
                builder += f'{tag} '

        # truncate the tweet if it exceeds the limit
        return builder[:TWEET_LIMIT]

    def didWeAlreadyTweetThis(self) -> bool:
        '''
        Checks if we have already tweeted this data today
        Returns:
            bool: True if we have not tweeted this data today, False if we have
        '''
        return self.dbm.fetch_tweet_by_data(self.data) is None