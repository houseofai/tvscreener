import pandas
from setuptools import setup, find_packages

VERSION = '0.0.1-alpha'
DESCRIPTION = 'Tradingview Screener Scraper'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="tradingview-screener",
    version=VERSION,
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['pandas', 'requests>=2.27.1'],
    keywords=['finance', 'tradingview', 'technical analysis']
)
