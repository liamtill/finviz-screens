from finvizfinance.screener.overview import Overview
import numpy as np
from time import sleep
import datetime as dt
import pandas as pd
import argparse
import yfinance as yf


def scrape_finviz(liquidity=10, monthly=False, longterm=False, perf=True):
    """
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

    if monthly:
        monthly_screen = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                          '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                          'Current Volume': 'Over 100K', 'IPO Date': 'More than a year ago',
                          'Industry': 'Stocks only (ex-Funds)'}
        filters = {'IPO>1YR Monthly': monthly_screen}
    elif longterm:
        largecap_earns_screen = {'Market Cap.': '+Large (over $10bln)', 'EPS growthpast 5 years': 'Over 10%',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Industry': 'Stocks only (ex-Funds)',
                           'EPS growththis year': 'Over 5%', 'Country': 'USA', 'EPS growthnext year': 'Over 10%',
                           'Volatility': 'Month - Over 3%'}
        longterm_screen = {'Market Cap.': '+Mid (over $2bln)', '200-Day Simple Moving Average': 'Price above SMA200',
                           'Industry': 'Stocks only (ex-Funds)', 'EPS growththis year': 'Over 10%',
                           'EPS growthnext year': 'Over 10%', 'EPS growthqtr over qtr': 'Over 10%',
                           'Sales growthqtr over qtr': 'Over 10%', 'Gross Margin': 'Over 20%',
                           'Volatility': 'Month - Over 3%', 'Average Volume': 'Over 500K'}
        filters = {'+Large Cap - Earnings': largecap_earns_screen, 'Longterm': longterm_screen}
    elif perf:
        near_high = {'Market Cap.': '+Mid (over $2bln)', 'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                              '52-Week High/Low': '0-10% below High', 'Industry': 'Stocks only (ex-Funds)',
                              'Average Volume': 'Over 200K'}

        performing = {'Market Cap.': '+Mid (over $2bln)', 'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                      'Industry': 'Stocks only (ex-Funds)', 'Average Volume': 'Over 200K',
                      'Performance': 'Year +30%'}
        filters = {'Near High': near_high, 'Performing': performing}
    else:
        tml_sales = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', '200-Day Simple Moving Average': 'Price above SMA200',
                     'Average Volume': 'Over 100K', 'Gross Margin': 'Over 20%', 'Sales growthqtr over qtr': 'Over 30%',
                     'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}

        tml_eps = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', '200-Day Simple Moving Average': 'Price above SMA200',
                   'Average Volume': 'Over 100K', 'Gross Margin': 'Over 20%', 'EPS growththis year': 'Over 30%',
                   'EPS growthqtr over qtr': 'Over 30%', 'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}

        ipo_5yr = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                   '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 500K',
                   'IPO Date': 'In the last 5 years', 'Industry': 'Stocks only (ex-Funds)'}

        ipo_lastyr = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Average Volume': 'Over 100K',
                      'Industry': 'Stocks only (ex-Funds)', 'IPO Date': 'In the last year'}

        eps_sales_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                               'EPS growththis year': 'Over 30%', 'EPS growthqtr over qtr': 'Over 30%',
                               'Sales growthqtr over qtr': 'Over 30%', 'Industry': 'Stocks only (ex-Funds)'}

        forward_eps_sales = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                             '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                             'EPS growthnext year': 'Over 20%', 'Sales growthqtr over qtr': 'Over 30%',
                             'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}

        year_plus100pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Year +100%',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                           'Industry': 'Stocks only (ex-Funds)'}

        eps_neg_to_pos = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', '52-Week High/Low': '70% or more above Low',
                          'Industry': 'Stocks only (ex-Funds)', '200-Day Simple Moving Average': 'Price above SMA200',
                          'Average Volume': 'Over 100K', 'EPS growthnext year': 'Positive (>0%)',
                          'EPS growththis year': 'Negative (<0%)', 'InstitutionalOwnership': 'Over 10%'}

        half_year_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Half +30%',
                               'Industry': 'Stocks only (ex-Funds)',
                               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}

        qtr_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Quarter +30%',
                           'Industry': 'Stocks only (ex-Funds)',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}

        month_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Performance': 'Month +30%',
                           'Industry': 'Stocks only (ex-Funds)',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}

        longterm = {'Volatility': 'Month - Over 3%', '200-Day Simple Moving Average': 'Price above SMA200',
                    'Average Volume': 'Over 500K', 'EPS growththis year': 'Over 10%', 'EPS growthqtr over qtr': 'Over 10%',
                    'EPS growthnext year': 'Over 5%', 'Sales growthqtr over qtr': 'Over 10%', 'Gross Margin': 'Over 20%',
                    'Market Cap.': '+Mid (over $2bln)', 'Industry': 'Stocks only (ex-Funds)'}

        eps_growth_yoy = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                          '200-Day Simple Moving Average': 'Price above SMA200', 'Industry': 'Stocks only (ex-Funds)',
                          '52-Week High/Low': '70% or more above Low', 'Average Volume': 'Over 100K',
                          'EPS growththis year': 'Over 20%', 'EPS growthnext year': 'Over 20%',
                          'Gross Margin': 'Over 20%', 'InstitutionalOwnership': 'Over 10%'}

        near_52w_high_base = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%',
                              '52-Week High/Low': '0-10% below High', 'Industry': 'Stocks only (ex-Funds)',
                               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}

        pba_best_of_best = {'Price': 'Over $5', 'Volatility': 'Month - Over 3%', 'Return on Equity': 'Over +10%',
                          '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                          '200-Day Simple Moving Average': 'Price above SMA200',
                          'Average Volume': 'Over 500K', 'Sales growthqtr over qtr': 'Over 25%',
                          'EPS growththis year': 'Over 25%'}

        filters = {'TML Sales': tml_sales, 'TML EPS': tml_eps, '5YR IPO': ipo_5yr, 'IPO Last Year': ipo_lastyr,
                   'EPS+Sales +30%': eps_sales_plus30pct, 'Forward EPS+Sales': forward_eps_sales,
                   'EPS -ve to +ve YoY': eps_neg_to_pos, 'Year +100%': year_plus100pct,
                   'Half +30%': half_year_plus30pct, 'Quarter +30%': qtr_plus30pct, 'Month +30%': month_plus30pct,
                   'Longterm': longterm, 'EPS Growth YoY': eps_growth_yoy, 'Near 52W High (BASE)': near_52w_high_base,
                   'PBA Best of Best': pba_best_of_best}

    foverview = Overview()
    all_tickers = []
    #failed = []
    count = 0

    for screen, filters_dict in filters.items():
        print('Running screen: ', screen)
        foverview.set_filter(filters_dict=filters_dict)
        df = foverview.screener_view(order='52-Week High (Relative)', ascend=False)

        for ticker in df['Ticker'].values:
            all_tickers.append(ticker)

        sleep(0.2)
        print("\n")

    unique_tickers = np.unique(all_tickers)

    if liquidity > 0:
        print(f'Checking liquidity of {len(unique_tickers)} tickers')
        final_tickers = []
        failed = 0
        for ticker in unique_tickers:
            price_data = get_stock_price_data(ticker)
            avg_vol = price_data['Volume'].rolling(window=30).mean()
            if (price_data['Adj Close'].iloc[-1] * avg_vol.iloc[-1]) / 1e6 > liquidity:
                final_tickers.append(ticker)
                count += 1
            else:
                failed += 1
        print('Liquidity of tickers checked')
    else:
        final_tickers = unique_tickers
        failed = 0
        count = len(unique_tickers)

    return final_tickers, count, failed


def save_tickers(filename, tickers):

    tickers.to_csv(filename, mode='w', index_label='Date')

def get_stock_price_data(ticker):
    """
    Get stock price data using yfinance

    :param ticker: stock ticker
    :return price data dict with OHLCV
    """

    today = dt.datetime.today()

    price_data = yf.download(ticker, start=(today-dt.timedelta(days=65)).strftime('%Y-%m-%d'),
                             end=today.strftime('%Y-%m-%d'), progress=False)

    return price_data

def ADR(price_data, lookback):
    """
    Average daily range. Based on Qullamaggie. Similar to ATR but % based for daily ranges

    :param price_data: data to check
    :param lookback: lookback period
    :return: % ADR value
    """

    high = price_data['High'][-lookback:]
    low = price_data['Low'][-lookback:]

    drange = high/low

    # calc daily range averaged over 20 days
    ADR = 100. * ((drange.rolling(window=20).mean()) - 1)

    return ADR

def main():

    parser = argparse.ArgumentParser(description='Finviz Scraper')
    parser.add_argument('-monthly', action='store_true', help='Run IPO>1YR Monthly screen')
    parser.add_argument('-longterm', action='store_true', help='Long term big cap growth screen')
    parser.add_argument('-perf', action='store_true', help='Near highs and performers')
    args = parser.parse_args()

    today = dt.datetime.now()
    datadir = 'screens/'
    if args.monthly:
        filename = datadir+today.strftime('%Y%m%d')+'_MONTHLY'+'.csv'
        liq = 0 # want to check all monthly charts
    elif args.perf:
        filename = datadir + today.strftime('%Y%m%d') + '_PERFORMERS' + '.csv'
        liq = float(input('Liquidity filter [M]: '))
    elif args.longterm:
        filename = datadir+today.strftime('%Y%m%d')+'_LONGTERM_BIGCAP'+'.csv'
        liq = float(input('Liquidity filter [M]: '))
    else:
        filename = datadir + today.strftime('%Y%m%d') + '_' + today.strftime('%H%M%S') + '.csv'
        liq = float(input('Liquidity filter [M]: '))

    print('Finviz Screens')
    print('Liquidity: ', str(liq)+'M')

    tickers, count, failed = scrape_finviz(liquidity=liq, monthly=args.monthly, longterm=args.longterm)
    print("\n")
    print('Screened ', count, ' tickers')
    print('Failed liquidity: ', failed)
    print('Passed liquidity: ', len(tickers))

    save_tickers(filename, pd.DataFrame(tickers))
    print('Saved screens to: ', filename)


if __name__ == '__main__': main()
