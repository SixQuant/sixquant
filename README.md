# SixQuant

[![PyPI Version](https://img.shields.io/pypi/v/sixquant.svg)](https://pypi.python.org/pypi/sixquant)
[![Build Status](https://img.shields.io/travis/SixQuant/sixquant/master.svg)](https://travis-ci.org/SixQuant/sixquant)
[![Wheel Status](https://img.shields.io/badge/wheel-yes-brightgreen.svg)](https://pypi.python.org/pypi/sixquant)
[![Coverage report](https://img.shields.io/codecov/c/github/SixQuant/sixquant/master.svg)](https://codecov.io/github/SixQuant/sixquant?branch=master)
[![Powered by SixQuant](https://img.shields.io/badge/powered%20by-SixQuant-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://sixquant.cn)

## Overview
A quick and stable data source for finance data.

提供快速稳定的金融(主要是股票)相关数据，包括实时和历史数据，数据会尽可能缓存在本地，以便提高性能同时减少服务器压力。同时，也提供了一些常用的金融辅助函数画图函数等。将来接口会全面兼容使用 RQAlpha 的 RiceQuant 和 TuShare 等常用相关库，方便用户移植代码！

## Install

#### Install sixquant
```bash
$ pip3 install sixquant
```

#### Upgrade sixquant
```bash
pip3 install sixquant --upgrade
```

## Quick Start

```python
import sixquant as sq

print(rq.__version__)

df = sq.get_day_today_quote(dropna=True)
print(len(df))
print(df.head())
```

## Docs

### 基本使用
* [SixQuant-Demo](docs/demo/SixQuant-Demo.ipynb)

## Todo

* ......

## Change Logs
* 0.0.1 2017-11-03 
  - 初始版本

## License

[MIT](https://tldrlegal.com/license/mit-license)

