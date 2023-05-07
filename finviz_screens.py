from finvizfinance.screener.overview import Overview
from time import sleep
import datetime as dt
import pandas as pd
import os


def scrape_finviz(choices):
    """
    Run finviz screen for choices

    Args:
        choices (list): list of choices from menu
    
    Returns:
        unique_tickers (list): list of unique tickers froms screens
    
    finviz package uses below strings to scrape website:

    FILTERS

    Exchange
    Index
    Sector
    Industry
    Country
    Market Cap.
    P/E
    Forward P/E
    PEG
    P/S
    P/B
    Price/Cash
    Price/Free Cash Flow
    EPS growththis year
    EPS growthnext year
    EPS growthpast 5 years
    EPS growthnext 5 years
    Sales growthpast 5 years
    EPS growthqtr over qtr
    Sales growthqtr over qtr
    Dividend Yield
    Return on Assets
    Return on Equity
    Return on Investment
    Current Ratio
    Quick Ratio
    LT Debt/Equity
    Debt/Equity
    Gross Margin
    Operating Margin
    Net Profit Margin
    Payout Ratio
    InsiderOwnership
    InsiderTransactions
    InstitutionalOwnership
    InstitutionalTransactions
    Float Short
    Analyst Recom.
    Option/Short
    Earnings Date
    Performance
    Performance 2
    Volatility
    RSI (14)
    Gap
    20-Day Simple Moving Average
    50-Day Simple Moving Average
    200-Day Simple Moving Average
    Change
    Change from Open
    20-Day High/Low
    50-Day High/Low
    52-Week High/Low
    Pattern
    Candlestick
    Beta
    Average True Range
    Average Volume
    Relative Volume
    Current Volume
    Price
    Target Price
    IPO Date
    Shares Outstanding
    Float
    """

    filters = {}

    # select screens to run and store in filters to run them
    if 1 in choices:
        monthly_screen = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                          '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                          'Current Volume': 'Over 100K', 'IPO Date': 'More than a year ago',
                          'Industry': 'Stocks only (ex-Funds)'}
        filters['IPO>1YR Monthly'] = monthly_screen
    if 2 in choices:
        largecap_earns_screen = {'Market Cap.': '+Large (over $10bln)', 'EPS growthpast 5 years': 'Over 10%',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Industry': 'Stocks only (ex-Funds)',
                           'EPS growththis year': 'Over 5%', 'Country': 'USA', 'EPS growthnext year': 'Over 10%',
                           'Volatility': 'Month - Over 3%'}
        filters['+Large Cap - Earnings'] = largecap_earns_screen
    if 3 in choices:
        near_high = {'Market Cap.': '+Mid (over $2bln)', 'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                              '52-Week High/Low': '0-10% below High', 'Industry': 'Stocks only (ex-Funds)',
                              'Average Volume': 'Over 200K'}
        filters['Near High'] = near_high
    if 4 in choices:
        performing = {'Market Cap.': '+Mid (over $2bln)', 'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                      'Industry': 'Stocks only (ex-Funds)', 'Average Volume': 'Over 200K',
                      'Performance': 'Year +30%'}
        filters['Performing'] = performing
    if 5 in choices:
        tml_sales = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', '200-Day Simple Moving Average': 'Price above SMA200',
                     'Average Volume': 'Over 100K', 'Gross Margin': 'Over 20%', 'Sales growthqtr over qtr': 'Over 30%',
                     'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}
        filters['TML Sales'] = tml_sales
    if 6 in choices:
        tml_eps = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', '200-Day Simple Moving Average': 'Price above SMA200',
                   'Average Volume': 'Over 100K', 'Gross Margin': 'Over 20%', 'EPS growththis year': 'Over 30%',
                   'EPS growthqtr over qtr': 'Over 30%', 'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}
        filters['TML EPS'] = tml_eps
    if 7 in choices:
        ipo_5yr = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                   '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 500K',
                   'IPO Date': 'In the last 5 years', 'Industry': 'Stocks only (ex-Funds)'}
        filters['5YR IPO'] = ipo_5yr
    if 8 in choices:
        ipo_lastyr = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Average Volume': 'Over 100K',
                      'Industry': 'Stocks only (ex-Funds)', 'IPO Date': 'In the last year'}
        filters['IPO Last Year'] = ipo_lastyr
    if 9 in choices:
        eps_sales_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                               'EPS growththis year': 'Over 30%', 'EPS growthqtr over qtr': 'Over 30%',
                               'Sales growthqtr over qtr': 'Over 30%', 'Industry': 'Stocks only (ex-Funds)'}
        filters['EPS+Sales +30%'] = eps_sales_plus30pct
    if 10 in choices:
        forward_eps_sales = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                             '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                             'EPS growthnext year': 'Over 20%', 'Sales growthqtr over qtr': 'Over 30%',
                             'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}
        filters['Forward EPS+Sales'] = forward_eps_sales
    if 11 in choices:
        eps_neg_to_pos = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', '52-Week High/Low': '70% or more above Low',
                          'Industry': 'Stocks only (ex-Funds)', '200-Day Simple Moving Average': 'Price above SMA200',
                          'Average Volume': 'Over 100K', 'EPS growthnext year': 'Positive (>0%)',
                          'EPS growththis year': 'Negative (<0%)', 'InstitutionalOwnership': 'Over 10%'}
        filters['EPS -ve to +ve YoY'] = eps_neg_to_pos
    if 12 in choices:
        year_plus100pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Year +100%',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                           'Industry': 'Stocks only (ex-Funds)'}
        filters['Year +100%'] = year_plus100pct
        
    if 13 in choices:
        half_year_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Half +30%',
                               'Industry': 'Stocks only (ex-Funds)',
                               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}
        filters['Half Year +30%'] = half_year_plus30pct
    if 14 in choices:
        qtr_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Quarter +30%',
                           'Industry': 'Stocks only (ex-Funds)',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}
        filters['Quarter +30%'] = qtr_plus30pct
    if 15 in choices:
        month_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Month +30%',
                           'Industry': 'Stocks only (ex-Funds)',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}
        filters['Month +30%'] = month_plus30pct
    if 16 in choices:
        longterm = {'Volatility': 'Month - Over 3%', '200-Day Simple Moving Average': 'Price above SMA200',
                    'Average Volume': 'Over 500K', 'EPS growththis year': 'Over 10%', 'EPS growthqtr over qtr': 'Over 10%',
                    'EPS growthnext year': 'Over 5%', 'Sales growthqtr over qtr': 'Over 10%', 'Gross Margin': 'Over 20%',
                    'Market Cap.': '+Mid (over $2bln)', 'Industry': 'Stocks only (ex-Funds)'}
        filters['Longterm'] = longterm
    if 17 in choices:
        eps_growth_yoy = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                          '200-Day Simple Moving Average': 'Price above SMA200', 'Industry': 'Stocks only (ex-Funds)',
                          '52-Week High/Low': '70% or more above Low', 'Average Volume': 'Over 100K',
                          'EPS growththis year': 'Over 20%', 'EPS growthnext year': 'Over 20%',
                          'Gross Margin': 'Over 20%', 'InstitutionalOwnership': 'Over 10%'}
        filters['EPS Growth YoY'] = eps_growth_yoy
    if 18 in choices:
        near_52w_high_base = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                              '52-Week High/Low': '0-10% below High', 'Industry': 'Stocks only (ex-Funds)',
                               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}
        filters['Near 52W High (Possible Base)'] = near_52w_high_base
    if 19 in choices:
        pba_best_of_best = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Return on Equity': 'Over +10%',
                          '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                          '200-Day Simple Moving Average': 'Price above SMA200',
                          'Average Volume': 'Over 500K', 'Sales growthqtr over qtr': 'Over 25%',
                          'EPS growththis year': 'Over 25%'}
        filters['PBA Best of Best'] = pba_best_of_best
    if 20 in choices:
        trending = {'Price': 'Over $10', 'Market Cap.': '+Small (over $300mln)', '50-Day Simple Moving Average': 'Price above SMA50',
                    '200-Day Simple Moving Average': 'Price above SMA200', 'Volatility': 'Month - Over 2%', 'Average Volume': 'Over 300K'}
        filters['Trending'] = trending

    foverview = Overview()
    all_tickers = []

    # loop screens and use finviz scraper to get tickers, sort by 52 week high desc
    for screen, filters_dict in filters.items():
        print('Running screen: ', screen)
        foverview.set_filter(filters_dict=filters_dict)
        df = foverview.screener_view(order='52-Week High (Relative)', ascend=False)

        # append a list of all tickers from all screens
        for ticker in df['Ticker'].values:
            all_tickers.append(ticker)

        # slight delay to not sned to many requests quickly
        sleep(0.2)
        print("\n")

    # find unique tickers from all screens
    unique_tickers = set(all_tickers)

    return unique_tickers


def save_tickers(filename: str, tickers):
    """Save tickers to file

    Args:
        filename (str): filename
        tickers (dataframe): pandas dataframe of tickers
    """

    tickers.to_csv(filename, mode='w')


def menu():
    """Screen menu selection

    Returns:
        str: menu choices
    """

    print('1. IPO>1YR Monthly')
    print('2. +Large Cap - Earnings')
    print('3. Near High')
    print('4. Performing')
    print('5. TML Sales')
    print('6. TML EPS')
    print('7. 5YR IPO')
    print('8. IPO Last Year')
    print('9. EPS+Sales +30%')
    print('10. Forward EPS+Sales')
    print('11. EPS -ve to +ve YoY')
    print('12. Year +100%')
    print('13. Half Year +30%')
    print('14. Quarter +30%')
    print('15. Month +30%')
    print('16. Longterm')
    print('17. EPS Growth YoY')
    print('18. Near 52W High (Possible Base)')
    print('19. PBA Best of Best')
    print('20. Trending')

    return input('\nSelect screens(s): ')


def main():

    today = dt.datetime.now().strftime('%Y-%m-%d_%H%M')
    datadir = os.path.join(os.getcwd(), 'screens/')
    if not os.path.exists(datadir):
        os.makedirs(datadir)

    print('** Finviz Screens **')
    print('Select one or more choices by separating with a comma:\n')

    choices = menu()
    # make int list form choices string
    choices = [int(x) for x in choices.split(',')]

    # run screen with choices
    tickers = scrape_finviz(choices)
    print(f'Screened: {len(tickers)} tickers')

    filename = f'finviz_screen_{today}'

    save_tickers(os.path.join(datadir, filename), pd.DataFrame(tickers))
    print('Saved screens to: ', filename)


if __name__ == '__main__': main()
