

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
    fileName = 'cache/history/history-{}.bin'.format(dateStr)

    if path.exists(fileName):
        cachedData = readTickerData(dateStr)
        # If the symbol exists, update for the given subreddit
        for ticker in tickerTracker:
            if ticker in cachedData:
                index = cachedData.index(ticker)
                cachedData[index].cnt[subreddit] = ticker.cnt[subreddit]
                cachedData[index].normalizedCnt[subreddit] = ticker.normalizedCnt[subreddit]
            else:
                cachedData.append(ticker)
        with open(fileName, 'wb') as file:
            pickle.dump(cachedData, file)
    else:
        with open(fileName, 'wb') as file:
            pickle.dump(tickerTracker, file)


def readTickerData(dateStr):
    fileName = 'cache/history/history-{}.bin'.format(dateStr)
    if path.exists(fileName):
        with open(fileName, 'rb') as file:
            return pickle.load(file)
    return None


if __name__ == "__main__":
    print(readTickerData('2021-2-1'))
