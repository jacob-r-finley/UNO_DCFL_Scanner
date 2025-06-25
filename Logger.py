import re
import logging
from FormatDate import formatDate as FD

class Logger:
    def __init__(self, f):
        self.file = f
        logger = logging.getLogger(__name__)  # Create a logger with the name of the current module
        console_handler = logging.StreamHandler()  # Create a console handler to output logs to the console
        file_handler = logging.FileHandler('test_logger_' + self.file, mode='a', encoding='utf-8')  # Create a file handler to output logs to a file
        formatter = logging.Formatter(
            '{asctime} - {levelname} - {message}',  # Define the format of the log messages
            style='{',  # Use curly braces for formatting
            datefmt='%Y-%m-%d %H:%M:%S'  # Define the date format for 'asctime'
        )
        console_handler.setFormatter(formatter)  # Set the formatter for the console handler
        file_handler.setFormatter(formatter)  # Set the formatter for the file handler
        logger.addHandler(console_handler)  # Add the console handler to the logger
        logger.addHandler(file_handler)  # Add the file handler to the logger
        logger.setLevel('INFO')  # Set the logging level to INFO
        # logging.basicConfig(
        #     level=logging.INFO, # Set the logging level so that anything at INFO level or higher is logged
        #     style='{',
        #     format='{asctime} - {levelname} - {message}',
        #     datefmt='%Y-%m-%d %H:%M:%S', # Date format for 'asctime'
        #     filename='test_logger_' + self.file,  # will need to modify this to use the actual file path
        #     filemode='a',  # Append mode
        #     encoding='utf-8',
        # )
        self.logger = logger  # Store the logger instance for later use

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