# coding=utf-8

import sixquant as sq
import pandas as pd

log = sq.logger.get(__name__)

# sq.daily_updater.update(start_date='2017-11-06')

print(sq.get_used_memory_size_str())

df = sq.get_day('000001', date='2017-11-01', fields=['prev_price'])
#df = sq.get_day('000001', date='2017-11-01', fields=['prev_price', 'close'])

print(type(df))
print(df)
if isinstance(df, pd.Series):
    print(df.to_dict())

print(sq.get_used_memory_size_str())
