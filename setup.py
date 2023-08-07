from setuptools import setup, find_packages

VERSION = '0.0.1-alpha'
DESCRIPTION = 'TradingView Screener API'
LONG_DESCRIPTION = 'Python library to retrieve data from TradingView Screener.'

# Setting up
setup(
    name="tvscreener",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'requests>=2.27.1'],
    keywords=['finance', 'tradingview', 'technical analysis']
)
