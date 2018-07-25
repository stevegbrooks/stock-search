import pandas as pd
from Utilities.FileReader import FileReader

class FileWriter:
    fr = FileReader()
    
    def __init__(self):
        self.fr = FileReader()
        
    def writeToExcel(self, dataFrame, nameOfFileToPrintTo):
        writer = pd.ExcelWriter((nameOfFileToPrintTo), engine = 'xlsxwriter')
        dataFrame.to_excel(writer, 'Sheet1', index = False)
        writer.save()
    
    def appendToExcel(self, dataFrame, nameOfFileToPrintTo):
        existing = self.fr.readExcel(nameOfFileToPrintTo)
        existing = existing.append(dataFrame, ignore_index = True)
        self.writeToExcel(existing, nameOfFileToPrintTo)
        
        