import pandas as pd

class FileReader:
    
    def __init__(self):
        pass
    
    def readExcelColumn(excelFileName, columnNumber):
        output = []
        df = pd.ExcelFile(excelFileName).parse('Sheet1')
        for index, row in df.iterrows():
            output.append((row[list(df)[columnNumber]]))
        return output
