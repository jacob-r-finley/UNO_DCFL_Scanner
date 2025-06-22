import tweepy
import json

TWEET_LIMIT = 280

class Tweeter:
    '''
    This class is responsible for tweeting the data from the UNO Police Reports page.
    It will use the Tweepy library to interact with the Twitter API.
    It will read the keys from a JSON file and use them to authenticate with the Twitter API
    and then tweet the data.
    '''
    def __init__(self, data: dict | str):
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

    def grabData(self) -> None | bool:
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

    def tweet(self) -> None:
        '''
        Tweets the data from the UNO Police Reports page
        Raises:
            tweepy.TweepyException: if there is an error with the Twitter API
        '''
        writtenData = self.parseData()
        client = tweepy.Client(
            consumer_key=self.__consumerKey,
            consumer_secret=self.__consumerSecret,
            access_token=self.__accessToken,
            access_token_secret=self.__accessTokenSecret,
        )
        # Replace the text with whatever you want to Tweet about
        response = client.create_tweet(
            text=writtenData,
        )

    def parseData(self) -> str:
        '''
        Parses the data from the UNO Police Reports page and formats it for tweeting
        Returns:
            str: the formatted data ready for tweeting
        '''
        builder = ''
        tags = ['#KnowTheO', '#MavSpirit', '#NUforNE']
        for key in self.data.keys():
            match key:
                case 'offense':
                    builder += f'{self.data[key]}\n'
                case 'report':
                    builder += f'{self.data[key]}'
                case 'building':
                    loc = self.data['location'][0:self.data['location'].find('(')]
                    if self.data[key] == 'N/A' and len(loc) == 0:
                        builder += ' at No listed location\n'
                    elif self.data[key] != 'N/A' and len(loc) > 0:
                        builder += f' at {self.data[key]} on {loc}\n'
                    elif self.data[key] == 'N/A':
                        builder += f' at {loc}\n'
                    else:
                        builder += f' at {self.data[key]}\n'
                case 'stolen':
                    if self.data[key] == '$0.00':
                        continue
                    else:
                        builder += f'Stolen: {self.data[key]}\n'
                case 'damaged':
                    if self.data[key] == '$0.00':
                        continue
                    else:
                        builder += f'Damaged: {self.data[key]}\n'
                case 'desc':
                    if self.data[key] is None:
                        builder += 'No further details provided\n'
                    else:
                        builder += f'{self.data[key]}\n'     
        for tag in tags:
            if len(f'{builder + tag}') <= TWEET_LIMIT:
                builder += f'{tag} '
        return builder[:TWEET_LIMIT]