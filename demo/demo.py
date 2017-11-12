# coding=utf-8

import sixquant as sq
import pandas as pd

log = sq.logger.get(__name__)

# print(fq.get_concepts_list_no_black())

# sq.daily_updater.update(start_date='2017-11-06')

print(sq.get_used_memory_size_str())

df = sq.get_day('000001', date='2017-11-06', backs=1, fields=['open', 'close'])
# df = sq.get_day(['000001'], date='2017-11-06', fields='close')
# df = sq.get_day(['000001', '000002'], date='2017-11-06', backs=1, fields=['open', 'close'])

print(type(df))
print(df)
if isinstance(df, pd.Series):
    print(df.to_dict())

print(sq.get_used_memory_size_str())

"""
print(sq.get_used_memory_size_str())
df = sq.get_day('600648', start_date='2017-09-01', end_date='2017-11-06')
for i in range(100):
    with sq.TimeProfiler(verbose=True):
        df = sq.get_day('600648', fields=['open', 'close'], start_date='2017-10-09', end_date='2017-11-06')
print(df)
print(sq.get_used_memory_size_str())


print(sq.get_used_memory_size_str())
with sq.TimeProfiler(verbose=True):
    df = sq.get_day(['000001', '600648'], fields=['open', 'close'], start_date='2017-10-18', end_date='2017-11-06')
print(sq.get_used_memory_size_str())

stocks = sq.get_stocks()
with sq.TimeProfiler(verbose=True):
    df = sq.get_day(stocks, fields=['open', 'close'], start_date='2017-10-18', end_date='2017-11-06')
print(sq.get_used_memory_size_str())
with sq.TimeProfiler(verbose=True):
    df = sq.get_day(fields=['open', 'close', 'low'], start_date='2017-10-01', end_date='2017-10-18')
print(len(df))
with sq.TimeProfiler(verbose=True):
    df = sq.get_day(fields=['open', 'close', 'low'], start_date='2017-10-17', end_date='2017-10-18')
print(df)


stocks = sq.get_stocks()
with sq.TimeProfiler(verbose=True):
    for i in range(1):
        df = sq.get_day(stocks, fields=['open', 'close'], start_date='2017-10-01', end_date='2017-11-06')
        # df = db.get_day('600846')
        # df = db.get_day('600846', fields=['close'])

with sq.TimeProfiler(verbose=True):
    for i in range(1):
        df = sq.db.get_day_all()
        # df = db.get_day('600846')
        # df = db.get_day('600846', fields=['close'])

import pandas as pd
filename = sq.option.get_data_filename('tmp', 'all.csv' + '.gzip')
with sq.TimeProfiler(verbose=True):
    df = pd.read_csv(filename, compression='gzip')
    df.set_index(df.columns[0], inplace=True)
    df.index.name = None
    df.index = pd.to_datetime(df.index)
    print(df)
df.to_csv(filename, compression='gzip')

print(sq.get_used_memory_size_str())
"""
# stocks = get_stocks()

# path = '/Volumes/Cloud/DataSet/stock'
# option.set_data_path(path)
# df = get_day(stocks, start_date='2017-09-01', end_date='2017-10-01')
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
