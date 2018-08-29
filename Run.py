from UserInterface import UserInterface

ui = UserInterface()

ui.readTickerInput('tickers.xlsx')
ui.isHistoricalMode == True
ui.run()