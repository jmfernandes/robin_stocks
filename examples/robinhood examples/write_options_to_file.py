import robin_stocks.robinhood as r
import os
import datetime
import time as t

'''
This is an example script that will print out options data every 10 seconds for 1 minute.
It also saves the data to a txt file. The txt file is saved in the same directory as this code.
'''

#!!! Fill out username and password
username = ''
password = ''
#!!!

login = r.login(username=username, password=password)

#!!! fill out the specific option information
strike = 300
date = "2020-07-02"
stock = "AAPL"
optionType = "call" #or "put"
#!!!

# File saving variables
minutesToTrack = 1 #in minutes
PrintInterval = 10 #in seconds
endTime = t.time() + 60 * minutesToTrack
fileName = "options.txt"
writeType = "w" #or enter "a" to have it continuously append every time script is run
#

os.chdir(os.path.dirname(__file__))
path = os.getcwd()
filename = os.path.join(path,fileName)
fileStream = open(filename, mode=writeType)

while t.time() < endTime:
    time = str(datetime.datetime.now())
    #Both write and print the data so that you can view it as it runs.
    fileStream.write("\n")
    fileStream.write(time)
    print(time)
    #Get the data
    instrument_data = r.get_option_instrument_data(symbol=stock,expirationDate=date,strikePrice=strike,optionType=optionType)
    market_data = r.get_option_market_data(inputSymbols=stock, expirationDate=date,strikePrice=strike,optionType=optionType)

    fileStream.write("\n")
    fileStream.write("{} Instrument Data {}".format("="*30,"="*30))
    print("{} Instrument Data {}".format("="*30,"="*30))
    # instrument_data is a dictionary, and the key/value pairs can be accessed with .items()
    for key, value in instrument_data.items():
        fileStream.write("\n")
        fileStream.write("key: {:<25} value: {}".format(key,value))
        print("key: {:<25} value: {}".format(key,value))

    fileStream.write("\n")
    fileStream.write("{} Market Data {}".format("="*30,"="*30))
    print("{} Market Data {}".format("="*30,"="*30))

    for key, value in market_data[0].items():
        fileStream.write("\n")
        fileStream.write("key: {:<25} value: {}".format(key,value))
        print("key: {:<25} value: {}".format(key,value))

    t.sleep(PrintInterval)

# make sure to close the file stream when you are done with it.
fileStream.close()
