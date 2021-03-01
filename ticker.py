import robin_stocks
import cache
import credentials
import time

tickersThatAreWords = [
    'A',
    'AG',
    'AGE',
    'AGO',
    'AI',
    'AIN',
    'AIR',
    'ALL',
    'ALOT',
    'AM',
    'AMP',
    'AN',
    'ANY',
    'APPS',
    'ARE',
    'AT',
    'AWAY',
    'BAR',
    'BE',
    'BEAT',
    'BEST',
    'BIG',
    'BILL',
    'BIT',
    'BOND',
    'BOOM',
    'BRO',
    'BUD',
    'BY',
    'CAKE',
    'CALM',
    'CAN',
    'CAR',
    'CARE',
    'CARS',
    'CASH',
    'CBD',
    'CEO',
    'CHAD',
    'CO',
    'COLD',
    'COM',
    'CORP',
    'COST',
    'CRY',
    'CUT',
    'CUZ',
    'DARE',
    'DD',
    'DEEP',
    'DOG',
    'DON',
    'DUST',
    'EAST',
    'EAT',
    'EDIT',
    'ELSE',
    'EVER',
    'EYE',
    'EYES',
    'FAD',
    'FAN',
    'FAST',
    'FILL',
    'FIVE',
    'FIX',
    'FL',
    'FLEX',
    'FLOW',
    'FOLD',
    'FOR',
    'FORM',
    'FOUR',
    'FREE',
    'FUN',
    'FUND',
    'GAIN',
    'GEM',
    'GLAD',
    'GO',
    'GOLD',
    'GOOD',
    'GROW',
    'HA',
    'HAS',
    'HE',
    'HEAR',
    'HES',
    'HI',
    'HOLD',
    'HOME',
    'HON',
    'HOPE',
    'HUGE',
    'ICON',
    'IMO',
    'INFO',
    'IPO',
    'IT',
    'IVE',
    'JAN',
    'JOB',
    'JOE',
    'JUST',
    'KEY',
    'KIDS',
    'LAND',
    'LAWS',
    'LEAD',
    'LEE',
    'LIFE',
    'LIVE',
    'LL',
    'LOAN',
    'LOVE',
    'LOW',
    'MAIN',
    'MAN',
    'MARK',
    'MID',
    'MIN',
    'MIND',
    'MOD',
    'MOM',
    'MSM',
    'MUST',
    'NAIL',
    'NEAR',
    'NET',
    'NEW',
    'NEXT',
    'NICE',
    'NINE',
    'NOW',
    'NYT',
    'OIL',
    'OLD',
    'ON',
    'ONE',
    'ONTO',
    'OR',
    'PAYS',
    'PEAK',
    'PICK',
    'PINS',
    'PLAN',
    'PLAY',
    'PLUS',
    'POST',
    'PPL',
    'PRO',
    'PS',
    'PUMP',
    'R',
    'RE',
    'REAL',
    'RH',
    'ROCK',
    'RUN',
    'SAFE',
    'SAVE',
    'SEE',
    'SEED',
    'SELF',
    'SHE',
    'SHE',
    'SHIP',
    'SHOP',
    'SITE',
    'SKY',
    'SO',
    'SON',
    'STAR',
    'STAY',
    'SUB',
    'SUM',
    'TD',
    'TEAM',
    'TECH',
    'TELL',
    'TEN',
    'TERM',
    'THO',
    'TRIP',
    'TRUE',
    'TURN',
    'TV',
    'TWO',
    'USA',
    'USD',
    'VERY',
    'WANT',
    'WELL',
    'WIRE',
    'WORK',
    'WOW',
    'WWW',
    'Y',
    'YOLO',
    'HERO',
    'FOX',
    'FAT',
    'POOL',
    'MEN',
    'ITM',
    'RARE',
    'AUTO',
    'ECHO',
    'SIZE'
    'LIT',
    'TOWN',
    'BOSS',
    'FLY',
    'HAIL',
    'ADS',
    'CTO',
    'TXT',
    'DOOR',
    'SNAP',
    'PIN',
    'EOD',
    'SALT',
    'PACK',
    'ROAD',
    'ROLL',
    'WOOD',
    'FAM',
    'BOUT',
    'BLUE',
    'HAIL',
    'SPOT',
    'SIX',
    'ROOF',
    'CURE']


class Ticker:

    def __init__(self, symbol):
        self.cnt = dict()
        self.symbol = symbol
        self.normalizedCnt = dict()
        self.subreddit = ""

    def normalize(self, sr, maxCnt):
        self.normalizedCnt[sr] = self.cnt[sr] / maxCnt

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Ticker):
            return self.symbol == other.symbol
        return False

    def __gt__(self, ticker2):
        if self.subreddit in self.normalizedCnt \
           and self.subreddit in ticker2.normalizedCnt:

            return self.normalizedCnt[self.subreddit] > \
                ticker2.normalizedCnt[self.subreddit]
        if self.subreddit in self.normalizedCnt:
            return True
        if self.subreddit in ticker2.normalizedCnt:
            return False
        return self.symbol > ticker2.symbol


def stripNaturalWordTickers(tickers):
    for ticker in tickersThatAreWords:
        if ticker.lower() in tickers:
            tickers.remove(ticker.lower())

    return tickers


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def cleanTickerList(tickers):

    tickers.extend(tickersThatAreWords)
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
