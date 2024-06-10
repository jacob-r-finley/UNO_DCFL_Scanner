# UNO_DCFL_Scanner
## Basic Info
This was a personal project that and I do not get paid for this so I will try to update this project when needed. 

With that said, this program is simply a webscrapper and auto tweeter. I grab data from the University of Nebraska at Omaha's Daily Crime & Fire Log (https://scsapps.unl.edu/uno-policereports/MainPage.aspx) and tweet it whenever there is an update (https://x.com/UNO_DCL_Scanner). 

## Imports
The required packages for this project are: datetime, re, time, requests, BeautifulSoup, tweepy, and json.

## Download
>[!NOTE]
> 
> In order to use the program, you MUST create an account with X's API (tweepy) at this site (https://developer.x.com/en/products/twitter-api). I have may own API keys and I do not have them listed on here for obvious reasons. If you would like use the tweepy library and have set up API tokens, keys, etc. you will have to intigrate them here. As a basic setup, I have a ```keys.json``` setup for this app. 


1. Use the following commands:

```
git clone https://github.com/jacob-r-finley/UNO_DCFL_Scanner.git

cd UNO_DCFL_Scanner
```
2. Import any of the packages that are not currently installed on your machine.

3. Update ```keys.json``` file to your specific keys, token, secret, etc.

4. Run main:
```
python main.py
```

5. Watch the log files as the program runs



## Additional Details
- The program runs on an infinite loop from wherever you call ```python main.py```. 
- The current program reads specific table data from the Daily Crime & Fire Log, so if you would like to use this code for a different project, edit the ```ReadPage.py``` file so that you grab the data that you would like. 
- BeautifulSoup is used as the webscrapper from the Crime & Fire Log page. The data is grabbed from a table and other packages (like pandas) to grab the data. I may also update to this in the future to more reliably read data.
- If you plan to use this double check the code to make sure that none of my current code and added text is not added to your tweets.