import tweepy
import json


TWEET_LIMIT = 280


class Tweeter:
    def __init__(self, data: dict | str):
        self.__consumerKey = None
        self.__consumerSecret = None
        self.__accessToken = None
        self.__accessTokenSecret = None
        self.__bearerToken = None
        self.data = data
        self.grabData()
        
    def grabData(self):
        jsonFile = open('keys.json')
        jsonData = json.load(jsonFile)
        for i in jsonData:
            match i:
                case 'consumerKey':
                    self.__consumerKey = jsonData[i]
                case 'consumerSecret':
                    self.__consumerSecret = jsonData[i]
                case 'accessToken':
                    self.__accessToken = jsonData[i]
                case 'accessTokenSecret':
                    self.__accessTokenSecret = jsonData[i]
                case 'bearerToken':
                    self.__bearerToken = jsonData[i]
        jsonFile.close()
    
    def tweet(self) -> None:
        writtenData = self.parseData()
        client = tweepy.Client(consumer_key=self.__consumerKey,
                               consumer_secret=self.__consumerSecret,
                               access_token=self.__accessToken,
                               access_token_secret=self.__accessTokenSecret)
        # Replace the text with whatever you want to Tweet about
        response = client.create_tweet(text=writtenData)
        
    def test_tweet(self) -> None:
        client = tweepy.Client(consumer_key=self.__consumerKey,
                               consumer_secret=self.__consumerSecret,
                               access_token=self.__accessToken,
                               access_token_secret=self.__accessTokenSecret)
        # Replace the text with whatever you want to Tweet about
        response = client.create_tweet(text=self.data)
        
    def parseData(self) -> str:
        builder = ""
        tags = ["#KnowTheO", "#MavSpirit", "#NUforNE"]
        for key in self.data.keys():
            match key:
                case "offense":
                    builder += f"{self.data[key]}\n"
                case "report":
                    builder += f"{self.data[key]}"
                case "building":
                    loc = self.data['location'][0:self.data['location'].find("(")]
                    if self.data["building"] == "N/A" and len(loc) == 0:
                        builder += " at No listed location\n"
                    elif self.data["building"] != "N/A" and len(loc) > 0:
                        builder += f" at {self.data['building']} on {loc}\n"
                    elif self.data["building"] == "N/A":
                        builder += f" at {loc}\n"
                    else:
                        builder += f" at {self.data['building']}\n"
                case "stolen":
                    if self.data[key] == "$0.00":
                        continue
                    else:
                        builder += f"Stolen: {self.data[key]}\n"
                case "damaged":
                    if self.data[key] == "$0.00":
                        continue
                    else:
                        builder += f"Damaged: {self.data[key]}\n"
                case "desc":
                    if self.data[key] is None:
                        builder += "No further details provided\n"
                    else:
                        builder += f"{self.data[key]}\n"     
        for tag in tags:
            if len(f"{builder + tag}") <= TWEET_LIMIT:
                builder += f"{tag} "
        return builder[:TWEET_LIMIT]