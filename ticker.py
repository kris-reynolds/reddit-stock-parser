import robin_stocks
import cache
import credentials
import time

class Ticker:

    def __init__(self, symbol, cnt):
        self.cnt = cnt
        self.symbol = symbol
        self.normalizedCnt = 0

    def normalize(self, maxCnt):
        self.normalizedCnt = self.cnt / maxCnt

    def toJson(self):
        return {
            'symbol': self.symbol,
            'RedditCnt': self.cnt,
            'RedditNormalizedCnt': self.normalizedCnt
            }

    @classmethod
    def fromCsv(csvStr):
        items = csvStr.split(",")
        symbol = items[0]
        cnt = int(items[1])
        ticker = Ticker(symbol, cnt)
        ticker.normalizedCnt = float(items[2])
        return ticker



def stripNaturalWordTickers(tickers):
    tickersThatAreWords = [
      'SO', 'ALOT', 'ARE', 'AT', 'BIG', 'BOOM',
      'BRO', 'BUY', 'CAN', 'CUT', 'NEXT', 'NICE',
      'SAVE', 'SEE', 'SHOP', 'STAY', 'TECH',
      'TOO', 'WORK', 'WOW', 'YOLO', 'WANT', 'VERY'
      'ALL', 'AM', 'ANY', 'BE', 'COLD', 'GOOD',
      'OLD', 'USA', 'FUND', 'IT', 'SEND', 'WELL',
      'FL', 'FLEX', 'I', 'GAME', 'A', 'ALL', 'FOR',
      'KIDS', 'LOVE', 'ONE', 'HOLD', 'MUST', 'NEED',
      'NOW', 'ON', 'OR', 'VERY', 'TV', 'TD', 'ROCK',
      'DO', 'DUST', 'EDIT', 'JUST', 'GO', 'DARE',
      'CARE', 'INFO', 'GAIN', 'TRUE', 'HUGE',
      'AWAY', 'CEO', 'EAT', 'ONTO', 'TELL', 'CASH',
      'MAN', 'LEAD', 'BAR', 'PLAY', 'LIVE', 'NEW',
      'TURN', 'PLAN', 'KNOW', 'TWO', 'POST', 'ELSE',
      'SUB', 'BEAT', 'HAS', 'COST', 'HOPE', 'GOLD',
      'SELF', 'SHIP', 'FOLD', 'TRIP', 'FORM', 'CLUB',
      'MOM', 'SEED', 'EYES', 'PINS', 'HEAR', 'RUN',
      'FAN', 'DOG', 'TEAM', 'EYE', 'MIND', 'FREE',
      'FOUR', 'EVER', 'GLAD', 'SAFE', 'AGO', 'NEAR',
      'PICK', 'fast', 'plus', 'apps', 'pass', 'star',
      'nyt', 'haha', 'main', 'nine', 'ten', 'lack',
      'imo', 'elon', 'bill', 'nail', 'lack', 'fit',
      'bond', 'pays', 'gem', 'icon', 'fad', 'bud',
      'cars', 'chad', 'age', 'mid', 'cry', 'cake',
      'east', 'fix', 'wire', 'she', 'by', 'best',
      'life', 'min', 'real', 'she', 'job', 're', 'rh',
      'dd', 'll', 'don', 'deep']
    for ticker in tickersThatAreWords:
        if ticker.lower() in tickers:
            tickers.remove(ticker.lower())

    return tickers


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def cleanTickerList(tickers):

    robin_stocks.login(
        credentials.robinhood_username,
        credentials.robinhood_password)

    tickerChunks = chunks(tickers, 100)

    badTickers = list()
    for tickerChunk in tickerChunks:
        # Throttle to a max of 2 requests/second so we don't timeout
        time.sleep(0.5)
        result = robin_stocks.stocks.get_quotes(tickerChunk)

        # if the ticker is not in the results, it is a bad ticker
        for ticker in tickerChunk:
            found = False
            for item in result:
                if item['symbol'].lower() == ticker.lower():
                    found = True
                    break
            if not found:
                print('Removing ticker {}'.format(ticker))
                badTickers.append(ticker)

    for ticker in badTickers:
        tickers.remove(ticker)

    return tickers


if __name__ == "__main__":
    tickers = cache.readTickerFile(file='cache/tickers.txt')
    startingSize = len(tickers)
    print("Starting size {}".format(startingSize))
    tickers = cleanTickerList(tickers)
    print("Ending size {} {}".format(len(tickers), startingSize))
    cache.writeTickerFile(tickers, file='cache/tickers.txt')
