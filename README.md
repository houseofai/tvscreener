# TradingView Screener Scraper

Retrieve data from TradingView screener for Stocks, Forex and Crypto into a Pandas dataframe.

Check the Jupyter Notebook in the notebooks folder for examples.
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

# ... do something with the dataframe
``` 
For Forex screener:
```
import tvscreener as tvs

fs = tvs.ForexScreener()
df = fs.get()

# ... do something with the dataframe
```
For Crypto screener:
```
import tvscreener as tvs

cs = tvs.CryptoScreener()
df = cs.get()

# ... do something with the dataframe
```

## Options

### Range
By default, it gets the 150 first results. You can change this by setting the `range` option:
```
ss = tvs.StockScreener()
ss.set_range(0, 10000)
df = ss.get()
```

### Sorting
While it is easier to sort on the Pandas Dataframe, you can also sort directly on the screener:
```
ss = tvs.StockScreener()
ss.sort_by('market_cap_basic', 'desc')
df = ss.get()
```
Note that `market_cap_basic` is the default sorting option.

## Filters

### Markets
Filter by markets:

Default: america
```
ss = tvs.StockScreener()
ss.set_markets('america')
df = ss.get()
```
You can list the markets with:
```
print(tvs.data.markets)
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
