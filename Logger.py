from FormatDate import formatDate as FD
import re

class Logger:
    def __init__(self, f):
        self.file = f

    def changeFile(self, f) -> None:
        '''
        Changes the file that the logger will write to
        Args:
            f (str): the new file path
        '''
        self.file = f

    def add(self, s) -> bool:
        '''
        Adds a string to the log file
        Args:
            s (str): the string to add to the log file
        Returns:
            True  - string was added successfully
            False - string was not added successfully
        '''
        try:
            with open(self.file, 'a') as file:
                file.write(s)
            self.clearBlankLines()
            return True
        except:
            return False

    def clearBlankLines(self) -> bool:
        '''
        Clears all blank lines from the log file
        Returns:
            None  - if successful
            False - if unsuccessful
        '''
        try:
            with open(self.file, 'r') as file:
                lines = file.readlines()
            with open(self.file, 'w') as file:
                for line in lines:
                    if not line.isspace():
                        file.write(line)
            return True
        except:
            return False

    def clearFile(self) -> bool:
        '''
        Clears the log file
        Returns:
            None  - if successful
            False - if unsuccessful
        '''
        try:
            with open(self.file, 'w') as file:
                file.write('')
            return True
        except:
            return False

    def findNumberOfLogs(self) -> int | bool:
        '''
        Finds the number of logs in the log file for today
        Returns:
            int  - number of logs for today
            bool - False if there was an error
        '''
        try:
            today = FD().getDate()
            counter = 0
            with open(self.file, 'r') as file:
                day, month, year = today['day'], today['month'], today['year']
                lines = re.findall(f'S\sDate:\s{day}/{month}/{year}', file.read())
                for _ in lines:
                    counter += 1
                file.close()
            return counter
        except:
            return False