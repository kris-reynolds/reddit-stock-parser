
import reddit as rdt
import datetime

# TODO: Plot Trending does not agree with day
# for the highest percentage
if __name__ == "__main__":

    today = datetime.datetime.today()
    dayStr = "{}-{}-{}".format(today.year, today.month, today.day)

    # days = ['2021-1-31', '2021-2-1', '2021-2-2', '2021-2-3']
    days = [dayStr]
    subreddits = ['wallstreetbets', 'pennystocks']

    for subreddit in subreddits:
        rdt.plotTrending(subreddit)
        rdt.plotDay(subreddit, dayStr)
