# TradingView Screener API

Python library to retrieve data from TradingView Screener.

![tradingview-screener.png](images%2Ftradingview-screener.png)

# Features
- Query Stock, Forex and Crypto Screener
- All the fields available (~250 fields)
- Any time interval (no need to be a registered user)
- Filters by any fields, symbols, markets, countries, etc.
- Get the results as a Pandas Dataframe

![dataframe.png](images%2Fdataframe.png)


## Installation
```
pip install git+https://github.com/houseofai/tradingview-screener@main
```
## Usage

For Stocks screener:
```
import tvscreener as tvs

ss = tvs.StockScreener()
df = ss.get()

# ... returns a dataframe with 150 rows by default
``` 
For Forex screener:
```
import tvscreener as tvs

fs = tvs.ForexScreener()
df = fs.get()
```
For Crypto screener:
```
import tvscreener as tvs

cs = tvs.CryptoScreener()
df = cs.get()
```

## Options

### Range
By default, it gets the 150 first results. You can change this by setting the `range` option:
```
ss = tvs.StockScreener()
ss.set_range(0, 10000)
df = ss.get()

# or to get the last 500 rows:
ss.set_range(9500, 10000)
df = ss.get()
```

### Sorting
While it is easier to sort on the Pandas Dataframe, you can also sort directly on the screener:
```
ss = tvs.StockScreener()
ss.sort_by('market_cap_basic', 'desc')
df = ss.get()
```
Note that `market_cap_basic` is the default sorting option for stocks

## Filters

### Markets
Filter by markets:

Default: america
```
ss = tvs.StockScreener()
ss.set_markets('america') # or ss.set_markets('america', 'france', 'japan')
df = ss.get()
```
You can list the markets with:
```
from tvscreener import tvdata

print(tvdata.stock['markets'])
```

### By Columns
Filter by columns:
```
ss = tvs.StockScreener()
ss.add_filter('Recommend.All', tvs.FilterOperation.IN_RANGE, values=[0.5, 1]) # Strong BUY
df = ss.get()
```
`Recommend.All` corresponds to the 'TECHNICAL RATING' column.
You can get a list of all columns available with:
```
print(tvs.data.columns_stocks)
print(tvs.data.columns_forex)
print(tvs.data.columns_crypto)
```


## Time intervals
Change the time interval of the technical data:

Default: Daily (`TimeInterval.DAILY`)
```

ss = tvs.StockScreener()
df = ss.get(tvs.TimeInterval.THIRTY_MINUTES)
```

## Debugging
Print the request URL and the payload:
```
ss = tvs.StockScreener()
df = ss.get(print_request=True)
```

# TODO
- [ ] Crypto Coins screener
- [ ] ETF screener
- [ ] More Built-in filters
- [ ] Query historical data