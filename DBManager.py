import sqlite3

test_data = [
    {
        'report': 'Report #1',
        'offense': 'Theft',
        'building': 'Library',
        'location': 'Main Campus',
        'stolen': '$100.00',
        'damaged': '$0.00',
        'desc': 'Laptop stolen from library desk.'
    },
    {
        'report': 'Report #2',
        'offense': 'Vandalism',
        'building': 'Student Center',
        'location': 'North Campus',
        'stolen': '$200.00',
        'damaged': '$50.00',
        'desc': 'Graffiti found in the restroom.'
    },
    {
        'report': 'Report #3',
        'offense': 'Burglary',
        'building': 'Science Building',
        'location': 'East Campus',
        'stolen': '$500.00',
        'damaged': '$100.00',
        'desc': 'Equipment stolen from the lab.'
    },
    {
        'report': 'Report #4',
        'offense': 'Assault',
        'building': 'Gymnasium',
        'location': 'West Campus',
        'stolen': '$0.00',
        'damaged': '$0.00',
        'desc': 'Physical altercation in the gym.'
    },
    {
        'report': 'Report #5',
        'offense': 'Fraud',
        'building': 'Administration Building',
        'location': 'Central Campus',
        'stolen': '$300.00',
        'damaged': '$0.00',
        'desc': 'Unauthorized access to student records.'
    }
]

class DBManager:
    def __init__(self, db_path='tweets.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        # check if the table exists, if not create it
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                report TEXT NOT NULL,
                offense TEXT NOT NULL,
                building TEXT,
                location TEXT,
                stolen TEXT,
                damaged TEXT,
                description TEXT
            )
        ''')
        self.connection.commit()

    def insert_tweet(self, tweet_data):
        '''
        Inserts a tweet into the database.
        :param tweet_data: A dictionary containing tweet data.
        '''
        if tweet_data == 'test':
            for data in test_data:
                self.cursor.execute('''
                    INSERT INTO tweets (report, offense, building, location, stolen, damaged, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['report'],
                    data['offense'],
                    data['building'],
                    data['location'],
                    data['stolen'],
                    data['damaged'],
                    data['desc']
                ))
            self.connection.commit()
            return
        self.cursor.execute('''
            INSERT INTO tweets (report, offense, building, location, stolen, damaged, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            tweet_data['report'],
            tweet_data['offense'],
            tweet_data['building'],
            tweet_data['location'],
            tweet_data['stolen'],
            tweet_data['damaged'],
            tweet_data['desc']
        ))
        self.connection.commit()

    def fetch_today_tweets(self):
        '''
        Fetches all tweets from today.
        :return: A list of dictionaries containing tweet data.
        '''
        self.cursor.execute('''
            SELECT * FROM tweets WHERE DATE(created_at) = DATE('now')
        ''')
        rows = self.cursor.fetchall()
        return [dict(zip([column[0] for column in self.cursor.description], row)) for row in rows]

    def fetch_tweet_by_data(self, tweet_data):
        '''
        Fetches a tweet by its data.
        :param tweet_data: A dictionary containing tweet data.
        :return: A dictionary containing the tweet data if found, else None.
        '''
        self.cursor.execute('''
            SELECT * FROM tweets WHERE report = ? AND offense = ? AND building = ? AND location = ? AND stolen = ? AND damaged = ? AND description = ?
        ''', (
            tweet_data['report'],
            tweet_data['offense'],
            tweet_data['building'],
            tweet_data['location'],
            tweet_data['stolen'],
            tweet_data['damaged'],
            tweet_data['desc']
        ))
        row = self.cursor.fetchone()
        if row:
            return dict(zip([column[0] for column in self.cursor.description], row))
        return None

    def clear_table(self):
        '''
        Clears the tweets table.
        '''
        self.cursor.execute('DELETE FROM tweets')
        self.connection.commit()