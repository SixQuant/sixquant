# SixQuant

[![PyPI Version](https://img.shields.io/pypi/v/sixquant.svg)](https://pypi.python.org/pypi/sixquant)
[![Build Status](https://img.shields.io/travis/SixQuant/sixquant/master.svg)](https://travis-ci.org/SixQuant/sixquant)
[![Wheel Status](https://img.shields.io/badge/wheel-yes-brightgreen.svg)](https://pypi.python.org/pypi/sixquant)
[![Coverage report](https://img.shields.io/codecov/c/github/SixQuant/sixquant/master.svg)](https://codecov.io/github/SixQuant/sixquant?branch=master)
[![Powered by SixQuant](https://img.shields.io/badge/powered%20by-SixQuant-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://sixquant.cn)

## Overview
A quick data source for finance data

## Install

### Install sixquant
```bash
$ pip3 install sixquant
```

### Upgrade sixquant
```bash
pip install sixquant --upgrade
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

