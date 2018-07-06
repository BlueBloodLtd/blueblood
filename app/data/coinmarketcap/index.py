import datetime
from os.path import dirname, join, abspath

from pandas import read_html, to_datetime, DataFrame

from .coinmarketcappy import total_market_cap, dominance, historical_snapshots, available_snaps
BASE_PATH = join(dirname(dirname(dirname(abspath(__file__)))), "storage", "cmc")
from utils import filenames


def get(params):
    if params['end_date'] is None:
        params['end_date'] = datetime.date.today().strftime("%Y%M$d")
    url = "https://coinmarketcap.com/currencies/{0}/historical-data/?start={1}&end={2}".format(params['symbol'], params['start_date'], params['end_date'])
    df = read_html(url)[0]
    df['Date'] = to_datetime(df['Date'])
    df = df.sort_values('Date')
    df.index = df['Date']
    del df['Date']
    df = df.rename(columns={"Open*": "Open", "Close**": "Close"})
    return df

def _cap(date):
    snaps = historical_snapshots(date)
    df = DataFrame(snaps[date], columns=['id', 'symbol', 'name', 'cap', 'price', 'supply', 'volume'])
    df.to_pickle(join(BASE_PATH, '{}.p'.format(date)))

def get_capitalization():
    fs = filenames(BASE_PATH)
    dates = available_snaps()
    if len(fs) == 0:
        for i in range(len(dates)):
            _cap(date=dates[i])
    else:
        _cap(date=dates[0])