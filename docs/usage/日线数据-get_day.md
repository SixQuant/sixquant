## 日线数据 get_day

get_day 函数用于获取历史日线数据

```
import sixquant as sq

df = sq.get_day('000001', date='2017-11-01', fields=['close', 'pt_close'])

print(type(df))
print(df)
```

输出：

       <class 'pandas.core.frame.DataFrame'>
            close  pt_close
    code                   
    000001  11.40     -1.21
    000002  29.15      0.66
### 特性

**功能特性**：

- 支持常用字段 fields=[ 'open', 'high', 'low', 'close', 'volume', 'amount']
  - open 开盘价
  - high 最高价
  - low 最低价
  - close 收盘价
  - volume 成交量
  - amount 成交额
- 支持动态字段(临时计算获得) fields=[ 'prev_close', 'pt_close', 'pt_ampl']
  - prev_close前一日收盘价
  - pt_close 今日涨幅
  - pt_ampl 今日振幅
- 支持前复权 adjust_type='pre'
  - 缺省为前复权
  - 注意：前复权导致股价变化，因此需要在回测时每一个历史日期都重新获得前复权后的股价
- 支持字段别名，以便兼容用户使用习惯
  - price 等价于 close
  - pt_price 等价于 pt_close
  - prev_price 等价于 prev_close
  - money 等价于 amount

**性能特性**：

* 数据会一次性加载因此性能很高
* 数据会在内存中自动缓存因此性能很高
* 如果本地没有数据则会自动从服务器下载并缓存在本地

### 使用举例

#### 获得单只股票单日数据(推荐)

```python
data = sq.get_day('000001', date='2017-11-01', fields='close')
data = sq.get_day('000001', date='2017-11-01', fields=['open','close'])
```

#### 获得单只股票多日数据(推荐)

```python
# 获取5个交易日的数据，date表示结束日期，backs表示往前多少个交易日(如果中间有停牌则往前顺延)
data = sq.get_day('000001', date='2017-11-01', backs=5, fields='close')
```

#### 获得多只股票单日数据(推荐)

```python
data = sq.get_day(['000001','000002'], date='2017-11-01', fields='close')
data = sq.get_day(['000001','000002'], date='2017-11-01', fields=['open','close'])
```

#### 获得多只股票多日数据(<font color='red'>不推荐</font>)

```python
data = sq.get_day(['000001','000002'], date='2017-11-01', fields=['open','close'])
```

#### 获得多只股票多日数据(<font color='red'>不推荐</font>)

```python
# 使用 start_date、end_date 和 使用 date、backs 的区别在于，
# 前者如果中间有停牌日期则不错处理，最终数据个数少于天数
# 后者如果中间有停牌日期则往前顺延，最终数据个数等于 backs
data = sq.get_day(['000001','000002'], 
                  start_date='2017-10-27', 
                  end_date='2017-11-01', 
                  fields=['open','close'])
```

### 详细说明

#### 函数声明

```python
def get_day(code_or_codes,
            start_date=None,
            end_date=None,
            date=None,
            backs=0,
            drop_suspended=False,
            fields=None,
            adjust_type='pre'
            ):
    """
    得到股票日线数据

    Features
    ---------
    * 专为性能优化
    * 支持真正历史日期的复权数据
    * 支持字段兼容，可以使用不同的的字段名称表示同一个数据
    *

    Parameters
    ----------
    code_or_codes : str/str array
        单个股票代码或股票代码数组
    start_date : date str/date
        数据开始日期
        start_date 和 backs 同时出现时忽略 start_date 参数
    end_date : date str/date
        数据结束日期
    date : date str/date
        等价于 end_date
        一般表示只取某一天的数据
        和 backs 参数配套使用时表示取某一天以及前 backs 个数据
    backs : int
        保证所有数据从结束日期往前有 n 条记录，以便用来画图等
        start_date 和 backs 同时出现时忽略 start_date 参数
    drop_suspended : bool
        是否直接丢弃中间有停牌的数据
        和 backs 配套使用
    fields : str/str array
        单个字段名称或字段名称数组
    adjust_type : str
        复权类型 pre/None

    Notes
    -----
    请尽可能的用的时候取数据，而不是一次性取

    Returns
    -------
    # 1. 传入一个code、单日date、一个field，返回一个数据，数据类型为 np.float64
    data = sq.get_day('000001', date='2017-11-01', fields='close')
    self.assertTrue(isinstance(data, np.float64))
    self.assertEqual(11.4, data)

    # 2. 传入一个code、单日date、多个field，返回一行数据，数据类型为 Pandas Series
    data = sq.get_day('000001', date='2017-11-01', fields=['open', 'close'])
    self.assertTrue(isinstance(data, pd.Series))
    self.assertEqual(2, len(data))
    self.assertEqual({'open': 11.56, 'close': 11.4}, data.to_dict())

    # 3. 传入一个code、多日date、一个field，返回一列数据，数据类型为 Pandas Series
    data = sq.get_day('000001', start_date='2017-11-01', end_date='2017-11-02', fields='close')
    self.assertTrue(isinstance(data, pd.Series))
    self.assertEqual(2, len(data))
    self.assertEqual(['2017-11-01', '2017-11-02'], data.index.strftime('%Y-%m-%d').tolist())
    self.assertEqual([11.4, 11.54], data.values.tolist())

    # 4. 传入一个code、多日date、多个field，返回一列数据，数据类型为 Pandas DataFrame
    data = sq.get_day('000001', start_date='2017-11-01', end_date='2017-11-02', fields=['open', 'close'])
    self.assertTrue(isinstance(data, pd.DataFrame))
    self.assertEqual(2, len(data))
    self.assertEqual(['2017-11-01', '2017-11-02'], data.index.strftime('%Y-%m-%d').tolist())
    self.assertEqual([[11.56, 11.4], [11.36, 11.54]], data.values.tolist())

    # --------

    # 5. 传入多个code、单日date、一个field，返回一列数据，数据类型为 Pandas Series
    data = sq.get_day(['000001', '000002'], date='2017-11-01', fields='close')
    self.assertTrue(isinstance(data, pd.Series))
    self.assertEqual(2, len(data))
    self.assertEqual({'000001': 11.4, '000002': 29.15}, data.to_dict())

    # 6. 传入多个code、单日date、多个field，返回多行数据，数据类型为 Pandas DataFrame
    data = sq.get_day(['000001', '000002'], date='2017-11-01', fields=['open', 'close'])
    self.assertTrue(isinstance(data, pd.DataFrame))
    self.assertEqual(2, len(data))
    self.assertEqual(['000001', '000002'], data.index.tolist())
    self.assertEqual([[11.56, 11.4], [28.96, 29.15]], data.values.tolist())

    # 7. 传入多个code、多日date、一个field，返回多行数据，数据类型为 Pandas DataFrame
    data = sq.get_day(['000001', '000002'], start_date='2017-11-01', end_date='2017-11-02', fields='close')
    self.assertTrue(isinstance(data, pd.DataFrame))
    self.assertEqual(4, len(data))
    self.assertEqual(['2017-11-01', '2017-11-01', '2017-11-02', '2017-11-02'],
                     data.index.strftime('%Y-%m-%d').tolist())
    self.assertEqual([['000001', 11.4], ['000002', 29.15], ['000001', 11.54], ['000002', 29.45]],
                     data.values.tolist())

    # 8. 传入多个code、多日date、多个field，返回多行数据，数据类型为 Pandas DataFrame
    data = sq.get_day(['000001', '000002'], start_date='2017-11-01', end_date='2017-11-02',
                      fields=['open', 'close'])
    self.assertTrue(isinstance(data, pd.DataFrame))
    self.assertEqual(4, len(data))
    self.assertEqual(['2017-11-01', '2017-11-01', '2017-11-02', '2017-11-02'],
                     data.index.strftime('%Y-%m-%d').tolist())
    self.assertEqual([['000001', 11.56, 11.4],
                      ['000002', 28.96, 29.15],
                      ['000001', 11.36, 11.54],
                      ['000002', 29.3, 29.45]], data.values.tolist())

    # --------

    # 因为有可能股票个数是动态变化的，希望处理结果时统一处理
    # 因此 '000001' 和 ['000001'] 是不同的，前者表示单个股票，后者表示多个股票

    # 5. 传入多个code、单日date、一个field，返回一列数据，数据类型为 Pandas Series
    data = sq.get_day(['000001'], date='2017-11-01', fields='close')
    self.assertTrue(isinstance(data, pd.Series))
    self.assertEqual(1, len(data))
    self.assertEqual({'000001': 11.4}, data.to_dict())

    Examples
    --------
    df = sq.get_day('000001', date='2017-11-06', fields=['close', 'pt_price'])

    """
```