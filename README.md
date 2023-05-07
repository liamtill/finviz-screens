## Finviz Screener

Wrapper around [finvizfinance](https://finvizfinance.readthedocs.io/en/stable/index.html) to run multiple finviz screens and save unique stock tickers to a CSV file in a folder called `screens/.

This is useful for running one or more screens, finding the unique tickers for all screens and outputting to a CSV file. The list of tickers in the CSV can then be imported into TradingView or your favourite charting platform that supports importing.


## Usage

After cloning the repo, cd into the repo directory

Set up venv:

```
python -m venv venv
```

Install requirements

```
pip install -r requirements.txt
```

Run `python3 finviz_screens.py` and select one of my pre-built screens from the menu.

## Adding screens

You can fork the repo to make your own modifications.

Take a look at the code in `scrape_finviz()` to see how the `finvizfinance` module uses the screener filters text on the finviz website. You can then build the screen you want based on the dropdown selection you would make on the website. Use one of the existing screens as a template to add a choice and add the filter to the dictionary that is used to run screens. For example:

The `trending` screen is coded like so
```
if 20 in choices:
    trending = {'Price': 'Over $10', 'Market Cap.': '+Small (over $300mln)', '50-Day Simple Moving Average': 'Price above SMA50',
                '200-Day Simple Moving Average': 'Price above SMA200', 'Volatility': 'Month - Over 2%', 'Average Volume': 'Over 300K'}
    filters['Trending'] = trending
```

You would add another if statement for your new screen, create the dict endtry and add it to the filters dict.

Dont forget to add the menu choice to the `menu()`