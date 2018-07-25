import pandas as pd

class FileReader:
    
    def readExcelColumn(self, excelFileName, columnNumber):
        output = []
        df = pd.ExcelFile(excelFileName).parse('Sheet1')
        for index, row in df.iterrows():
            output.append((row[list(df)[columnNumber]]))
        return output
    
    def readExcel(self, excelFileName):
        import pandas as pd
        df = pd.read_excel(excelFileName, sheet_name='Sheet1')
        return df
