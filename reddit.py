
# System imports
import datetime
import matplotlib.pyplot as plt
import praw
from os import path


# Local imports
import credentials
import ticker as tckr
import natruallanguage as nl
import cache

# nltk.download('punkt')

reditPath = "cache/reddit"

# TODO:
#  - Refine ticker list so it is only tickers that currently exist
#  - Save previous day into a file (for > 1%)
#  - Compare today and yesterday
reddit = praw.Reddit(
     client_id=credentials.client_id,
     client_secret=credentials.client_secret,
     user_agent=credentials.user_agent
 )


def loadReddit(subreddit, dateStr):

    filePath = '{}/{}-{}.txt'.format(reditPath, subreddit, dateStr)
    # if the file exists, use that
    if path.exists(filePath):
        return cache.readRedditFile(subreddit, dateStr)

    allText = list()
    for submission in reddit.subreddit(subreddit).hot(limit=50):

        allText.append(submission.title)
        allText.append(submission.selftext)

        for comment in submission.comments:
            if 'body' in vars(comment):
                allText.append(comment.body)

    oneText = ' '.join(map(str, allText))

    with open(filePath, 'w') as file:
        file.write(oneText)


def redditCount(subreddit, dateStr):
    oneText = cache.readRedditFile(subreddit, dateStr)

    tickers = cache.readTickerFile(file='cache/tickers.txt')
    tickers = tckr.stripNaturalWordTickers(tickers)

    tickerTracker = nl.getTickerCount(
        tickers,
        oneText,
        subreddit,
        caseInsensitive=True)

    # tickerTracker.extend(
    #     nl.getTickerCount(
    #         tckr.tickersThatAreWords,
    #         oneText,
    #         subreddit,
    #         caseInsensitive=False))

    return tickerTracker


def parseRedditToday(subreddit, dateStr):
    loadReddit(subreddit, dateStr)
    tickerTracker = redditCount(subreddit, dateStr)
    cache.writeTickerData(subreddit, dateStr, tickerTracker)

    return tickerTracker

def plotTrending(subreddit, symbol=None):
    numDays = 14
    trendingHistory = list()

    # Read the last week of data (if available)
    for dayDelta in range(numDays, -1, -1):
        day = datetime.datetime.today() - datetime.timedelta(dayDelta)
        dayStr = "{}-{}-{}".format(day.year, day.month, day.day)

        history = cache.readTickerData(dayStr)
        if history is not None:
            trendingHistory.append(history)

    history = dict()

    prevDays = 0

    for tickerList in trendingHistory:
        for ticker in tickerList:
            if subreddit in ticker.normalizedCnt:
                if ticker.symbol not in history:
                    history[ticker.symbol] = [0] * (len(trendingHistory))
                history[ticker.symbol][prevDays] = ticker.normalizedCnt[subreddit]
        prevDays += 1

    plt.title('Ticker Mentions over time last week' + subreddit)
    plt.xlabel('Days')
    plt.ylabel('Mentions')

    x = range(1, (len(trendingHistory))+1)

    for ticker in history:
        if max(history[ticker]) > 0.03:
            if symbol is None or symbol.lower() == ticker.lower():
                plt.plot(x, history[ticker], label=ticker)

    plt.legend(
               ncol=2, mode="expand", borderaxespad=0.)


    plt.show()



def plotDay(subreddit, dayStr):

    tickerTracker = cache.readTickerData(dayStr)

    for ticker in tickerTracker:
        ticker.subreddit = subreddit

    tickerTracker = sorted(tickerTracker)
    tickersFound = list()
    tickerCnt = list()
    for ticker in tickerTracker:
        if subreddit in ticker.normalizedCnt and ticker.normalizedCnt[subreddit] > 0.005:
            tickerCnt.append(ticker.normalizedCnt[subreddit])
            tickersFound.append(ticker.symbol)

    plt.bar(tickersFound, tickerCnt)
    plt.title('Ticker Vs Mentions on ' + subreddit + ' ' + dayStr)
    plt.xlabel('Ticker')
    plt.ylabel('Mentions')

    plt.show()



if __name__ == "__main__":
    today = datetime.datetime.today()
    dayStr = "{}-{}-{}".format(today.year, today.month, today.day)

    subreddit = 'wallstreetbets'
    parseRedditToday('pennystocks', dayStr)
    parseRedditToday('wallstreetbets', dayStr)
    #parseRedditToday(subreddit, '2021-1-31')

    #plotTrending(subreddit)
    plotDay('pennystocks', dayStr)
    plotDay('wallstreetbets', dayStr)
