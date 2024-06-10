import datetime

class formatDate:
    def __init__(self):
        """Object that returns formatted version of today's date
        """
        self.date = self.getDate()
                
    def getDate(self) -> dict:
        """Grabs a dict that can be spliced for individual date data

        Returns:
            dict: of form
            
            day - DD
            
            month - [name of month]
            
            year - YYYY
        """
        date = {'day': None,
                'month': None,
                'year': None}
        date['day'] = datetime.date.today().day
        month = datetime.date.today().month
        match month:
            case 1:
                date['month'] = 'January'
            case 2:
                date['month'] = 'February'
            case 3:
                date['month'] = 'March'
            case 4:
                date['month'] = 'April'
            case 5:
                date['month'] = 'May'
            case 6:
                date['month'] = 'June'
            case 7:
                date['month'] = 'July'
            case 8:
                date['month'] = 'August'
            case 9:
                date['month'] = 'September'
            case 10:
                date['month'] = 'October'
            case 11:
                date['month'] = 'November'
            case 12:
                date['month'] = 'December'
        date['year'] = datetime.date.today().year
        return date
    
    def prettyPrint(self) -> str:
        """returns a pretty string version of the current date
        """
        return f"{self.date['day']}/{self.date['month']}/{self.date['year']}"