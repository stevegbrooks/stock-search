import pandas as pd
import re
import os
from Utilities.FileReader import FileReader

class FileWriter:
    global fr
    
    def __init__(self):
        self.fr = FileReader()
        
    def __writeToExcel(self, dataFrame, fileName):
        writer = pd.ExcelWriter((fileName), engine = 'xlsxwriter', datetime_format = 'mm/dd/yyyy')
        dataFrame.to_excel(writer, 'Sheet1', index = False)
        writer.save()
    
    def __appendToExcel(self, dataFrame, fileName):
        existing = self.fr.readExcel(fileName)
        existing = existing.append(dataFrame, ignore_index = True)
        self.__writeToExcel(existing, fileName)
        
    def writeToFile(self, dataFrame, fileName):
        match = re.search('\\.[a-zA-Z]*$', fileName, flags = 0)
        if match:
            if match.group(0) == '.xlsx':
                if os.path.isfile(fileName) == True:
                    self.__appendToExcel(dataFrame, fileName)
                else:
                    self.__writeToExcel(dataFrame, fileName)
            else:
                raise Exception('Currently only writing to .xlsx and .csv files is supported.')
        else:
            raise Exception('You did not provide a file extension - ' + 
                            'I dont know what kind of file to write to!')
        
        