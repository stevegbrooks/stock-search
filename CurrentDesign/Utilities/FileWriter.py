import pandas as pd

class FileWriter:
    
    def __init__(self):
        pass
    
    def writeToExcel(dataFrame, nameOfFileToPrintTo):
        writer = pd.ExcelWriter((nameOfFileToPrintTo), engine = 'xlsxwriter')
        dataFrame.to_excel(writer, 'Sheet1', index = False)
        writer.save()