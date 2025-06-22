from FormatDate import formatDate as FD
import re

class Logger:
    def __init__(self, f):
        self.file = f

    def changeFile(self, f):
        self.file = f

    def add(self, s) -> bool:
        try:
            with open(self.file, 'a') as file:
                file.write(s)
            self.clearBlankLines()
            return True
        except:
            return False

    def clearBlankLines(self) -> None | bool:
        try:
            with open(self.file, 'r') as file:
                lines = file.readlines()
            with open(self.file, 'w') as file:
                for line in lines:
                    if not line.isspace():
                        file.write(line)
        except:
            return False

    def findNumberOfLogs(self) -> int | bool:
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