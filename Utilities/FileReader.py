import pandas as pd

class FileReader:
    
    def readExcel(self, excelFileName):
        df = pd.read_excel(excelFileName, sheet_name='Sheet1')
        df = df.fillna('')
        if 'dates' in df:
            if type(df['dates'][0]) is pd._libs.tslib.Timestamp:
                df['dates'] = df['dates'].astype(str)
        return df
