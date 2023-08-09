from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.0.12'
DESCRIPTION = 'TradingView Screener API'
LONG_DESCRIPTION = 'A simple Python library to retrieve data from TradingView Screener'

# Setting up
setup(
    name="tvscreener",
    url="https://github.com/houseofai/tvscreener",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="House of AI",
    license='Apache License 2.0',
    packages=find_packages(),
    install_requires=['pandas', 'requests>=2.27.1'],
    keywords='finance tradingview technical-analysis',
    python_requires='>=3.10',
)
