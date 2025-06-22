import datetime

class formatDate:
    def __init__(self):
        '''
        Object that returns formatted version of today's date
        '''
        self.date = self.getDate()
                
    def getDate(self) -> dict:
        '''
        Grabs a dict that can be spliced for individual date data
        Returns:
            {
                day - DD
                month - MMM
                year - YYYY
            }
        '''
        months = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December',
        }
        return {
            'day': datetime.date.today().day,
            'month': months[datetime.date.today().month],
            'year': datetime.date.today().year,
        }

    def prettyPrint(self) -> str:
        '''
        returns a pretty string version of the current date
        '''
        return f'{self.date['day']}/{self.date['month']}/{self.date['year']}'