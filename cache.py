

import pickle
from os import path


def readTickerFile(file="tickers.txt"):
    with open("cache/tickers.txt", 'rb') as file:
        return pickle.load(file)


def writeTickerFile(tickers, file="tickers.txt"):
    with open("cache/tickers.txt", 'wb') as file:
        pickle.dump(tickers, file)


def readRedditFile(subreddit, dateStr):
    with open('cache/reddit/' + subreddit + '-' + dateStr + '.txt', 'r') as file:
        oneText = file.read()
        return oneText


def writeTickerData(subreddit, dateStr, tickerTracker):
    with open('cache/history/history-{}.bin'.format(dateStr), 'wb') as file:
        pickle.dump(tickerTracker, file)


def readTickerData(dateStr):
    fileName = 'cache/history/history-{}.bin'.format(dateStr)
    if path.exists(fileName):
        with open(fileName, 'rb') as file:
            return pickle.load(file)
    return None


if __name__ == "__main__":
    readTickerData('2021-1-31')
