
# StockAPICaller

This package is meant to automate some of the tedium of doing research on stocks. The problem is that there isn't a one-stop shop for stock data. For many investors, the desired data points reside on multiple, often subscription-based, websites.

Fortunately these websites often have APIs, like Gurufocus. Intrinio is a great API to use with this application as they are completely focused on their API product, and nothing else. 

This application is meant to bring multiple different APIs together into a single interface, so that one can simply specify data points and not have to worry about visiting different websites and cobbling the information together.

## Dates and Historical Mode

There are currently two modes to the program, default and historical. If you toggle historical mode to 'True', then it will look at the date that you provided and pull the stock info for that date. 

Currently, the program has no good way to deal with holidays, so if you inadvertantly enter 2018-07-04, for example, it wouldn't return much. 

If you don't provide a date and historical mode is set to 'True', then it defaults to todays date.

## SingleRun.py

This module is the interface if you just want to run the program for a single stock symbol. It will print the results to the console.

## MultiRun.py

Use this if you have multiple tickers. First put them into an .xlsx file, which must have a column labeled 'tickers' and a column labeled 'dates'. You don't have to enter anything into the 'dates' column, but there must be a column there called 'dates'.

## User Settings

In order to use this program you'll need to have an account with an API. After you have an account and have your keys (or username and password), you can enter those credentials by building a subclass to `APIKeys`.

You'll have to build out subclasses of `StockAPICaller` for each API that you want to use. See my examples of `Intrinio` and `GuruFocus`.

You'll then have to enter your desired datapoints in a subclass of `AppSettings`, build out a subclass of `OutputManager`, and amend the `AppSettingsFactory` to accomdate your settings. 

The `APIKeys` subclass and the `OutputManager` subclass should be constructed by the `AppSettings` subclass.

### Contact:

If you need assistance, please contact me at stevegbrooks@gmail.com. I'll be happy to help or answer any questions!