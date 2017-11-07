# coding=utf-8

import objgraph

import sixquant as sq

log = sq.logger.get(__name__)

import pandas as pd
df = pd.DataFrame()
objgraph.show_refs(df, refcounts=True, filename='profile-memory-leak-graph.png')

print(objgraph.show_most_common_types())

print('used memory', sq.get_used_memory_size_str())
df = sq.get_day('600648', start_date='2017-09-01', end_date='2017-11-06')
del df
print('used memory', sq.get_used_memory_size_str())
print(objgraph.show_growth(limit=3))

df = sq.get_day('600648', start_date='2017-09-01', end_date='2017-11-06')
del df
print('used memory', sq.get_used_memory_size_str())
print(objgraph.show_growth(limit=3))

#roots = objgraph.get_leaking_objects()
#objgraph.show_refs(roots[:3], refcounts=True, filename='profile-memory-leak-graph.png')
