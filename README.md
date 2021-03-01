# reddit-stock-parser
Scrapes Reddit WSB for information on trending stock symbols

## Usage

- Modify the `credentials.py` with your Reddit Credentials.  Currently RobinHood credentials is not used.

- Run `daily.py` every day to fetch all the raw data from the chosen subreddits and save the data.
    - I would recommend a chron job, the more history you have, the more useful this will be!
- Run `plot.py` to plot out the results from the subreddits.
    - Edit the `plot.py` to choose which subreddits/plots.  Eventually this will have command line options


