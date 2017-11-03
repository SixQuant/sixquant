# coding=utf-8

import time
from sixquant import *
from sixquant.TimeProfiler import TimeProfiler
from sixquant.db import db

log = logger.get(__name__)

path = '/Volumes/Cloud/DataSet/sixquant'

option.set_data_path(path)

log.debug("local data path: " + path)

# print(fq.get_concepts_list_no_black())

daily_updater.update(start_date='2017-10-18')

with TimeProfiler(verbose=True):
    for i in range(1):
        df = db.get_day('600846', fields=['open', 'close'], start_date='2017-10-18', end_date='2017-10-20')
        # df = db.get_day('600846')
        #df = db.get_day('600846', fields=['close'])
print(df)

#stocks = get_stocks()

#path = '/Volumes/Cloud/DataSet/stock'
#option.set_data_path(path)
#df = get_day(stocks, start_date='2017-09-01', end_date='2017-10-01')
# print(df.head(5))
"""
with TimeProfiler(verbose=True):
    df = get_day('600846')
df['code'] = '600846'
db.put_day(df)
df = db.get_day('600846')

"""
"""
stocks = fq.get_stocks()
print(stocks[:5])


def callback():
    df = fq.get_day_today_quote(dropna=True)
    if df is not None:
        df = df.sort_values(by='pt_price', ascending=False)
        print(df[['close', 'volume', 'amount', 'pt_price', 'pt_turn']].head(3))

    df = fq.get_day_today_money(dropna=True)
    if df is not None:
        df = df.sort_values(by='money_major', ascending=False)
        print(df[['price', 'pt_price', 'money_major', 'money_small']].head(3))


timer = fq.Timer(interval=5, callback=callback, async=False)
timer.start()
"""
# while True:
#    time.sleep(1)
