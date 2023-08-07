from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

VERSION = '0.0.1-alpha'
DESCRIPTION = 'TradingView Screener API'


# Setting up
setup(
    name="tvscreener",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'requests>=2.27.1'],
    keywords=['finance', 'tradingview', 'technical analysis']
)
