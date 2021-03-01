
import operator

import ticker as tckr
import string
import nltk
from collections import Counter

# nltk.download("stopwords")
# nltk.download("punkt")


def progbar(curr, total, full_progbar):
    frac = curr/total
    filled_progbar = round(frac*full_progbar)
    print('\r', '#'*filled_progbar + '-'*(full_progbar-filled_progbar), '[{:>7.2%}]'.format(frac), end='')


def BinarySearch(lys, val):
    first = 0
    last = len(lys)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first+last)//2
        if lys[mid] == val:
            index = mid
        else:
            if val < lys[mid]:
                last = mid - 1
            else:
                first = mid + 1
    return index


def getTickerCount(tickers, oneText, subreddit, caseInsensitive=True):

    # Remove punctuation that shouldn't have a space
    oneText = oneText.replace("'", "").replace("’", "")

    if caseInsensitive:
        oneText = oneText.lower()

    oneText = oneText.translate(
        str.maketrans(string.punctuation, " "*len(string.punctuation)))

    tokens = nltk.word_tokenize(
        oneText.translate(dict.fromkeys(string.punctuation)))

    tickerFilter = [w for w in tokens if BinarySearch(tickers, w) != -1]
    tickerCounter = Counter(tickerFilter)

    totalCnt = 0
    for ticker in tickerCounter:
        totalCnt += tickerCounter[ticker]

    tickerTracker = list()
    for ticker in tickers:
        if tickerCounter[ticker] > 0:
            item = tckr.Ticker(ticker)
            item.cnt[subreddit] = tickerCounter[ticker]
            item.normalize(subreddit, totalCnt)
            tickerTracker.append(item)

    return tickerTracker
