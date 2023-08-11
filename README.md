<div align="center">
  <img alt="logo tradingview screener api library" src="https://raw.githubusercontent.com/houseofai/tvscreener/main/.github/img/logo-tradingview-screener-api.png"><br>
</div>

-----------------

# TradingView Screener API: simple Python library to retrieve data from TradingView Screener

[![PyPI version](https://badge.fury.io/py/tvscreener.svg)](https://badge.fury.io/py/tvscreener)
[![Downloads](https://pepy.tech/badge/tvscreener)](https://pepy.tech/project/tvscreener)
[![Coverage](https://codecov.io/github/houseofai/tvscreener/coverage.svg?branch=main)](https://codecov.io/gh/houseofai/tvscreener)
![tradingview-screener.png](https://raw.githubusercontent.com/houseofai/tvscreener/main/.github/img/tradingview-screener.png)

Get the results as a Pandas Dataframe

![dataframe.png](https://github.com/houseofai/tvscreener/blob/main/.github/img/dataframe.png?raw=true)

# Main Features

- Query **Stock**, **Forex** and **Crypto** Screener
- All the **fields available**: ~300 fields - even hidden ones)
- **Any time interval** (`no need to be a registered user` - 1D, 5m, 1h, etc.)
- Filters by any fields, symbols, markets, countries, etc.
- Get the results as a Pandas Dataframe

## Installation

The source code is currently hosted on GitHub at:
https://github.com/houseofai/tvscreener

Binary installers for the latest released version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/tvscreener)

```sh
# or PyPI
pip install tvscreener
```

From pip + GitHub:

```sh
$ pip install git+https://github.com/houseofai/tradingview-screener@main
```

## Usage

For Stocks screener:

```python
import tvscreener as tvs

ss = tvs.StockScreener()
df = ss.get()

# ... returns a dataframe with 150 rows by default
``` 

For Forex screener:

```python
import tvscreener as tvs

fs = tvs.ForexScreener()
df = fs.get()
```

For Crypto screener:

```python
import tvscreener as tvs

cs = tvs.CryptoScreener()
df = cs.get()
```

## Parameters

For Options and Filters, please check the [notebooks](https://github.com/houseofai/tvscreener/tree/main/notebooks) for
examples.