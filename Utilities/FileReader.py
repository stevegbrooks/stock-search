import pandas as pd

class FileReader:
    
    def readExcel(self, excelFileName):
        df = pd.read_excel(excelFileName, sheet_name='Sheet1')
        return df
