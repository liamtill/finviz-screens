from finvizfinance.screener.overview import Overview
import numpy as np
from time import sleep
import utils
import datetime as dt
import pandas as pd


def scrape_finviz(liquidity=10):
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

    tml_sales = {'Price': 'Over $5', 'Average True Range': 'Over 1', '200-Day Simple Moving Average': 'Price above SMA200',
                 'Average Volume': 'Over 1M', 'Gross Margin': 'Over 20%', 'Sales growthqtr over qtr': 'Over 30%',
                 'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}

    tml_eps = {'Price': 'Over $5', 'Average True Range': 'Over 1', '200-Day Simple Moving Average': 'Price above SMA200',
               'Average Volume': 'Over 1M', 'Gross Margin': 'Over 20%', 'EPS growththis year': 'Over 30%',
               'EPS growthqtr over qtr': 'Over 30%', 'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}

    ipo_5yr = {'Price': 'Over $5', 'Average True Range': 'Over 1', '50-Day Simple Moving Average': 'Price above SMA50',
               '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 500K',
               'IPO Date': 'In the last 5 years', 'Industry': 'Stocks only (ex-Funds)'}

    ipo_lastyr = {'Price': 'Over $5', 'Average True Range': 'Over 1', 'Average Volume': 'Over 100K',
                  'Industry': 'Stocks only (ex-Funds)', 'IPO Date': 'In the last year'}

    eps_sales_plus30pct = {'Price': 'Over $5', 'Average True Range': 'Over 1',
                           '50-Day Simple Moving Average': 'Price above SMA50',
                           '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K',
                           'EPS growththis year': 'Over 30%', 'EPS growthqtr over qtr': 'Over 30%',
                           'Sales growthqtr over qtr': 'Over 30%', 'Industry': 'Stocks only (ex-Funds)'}

    forward_eps_sales = {'Price': 'Over $5', 'Average True Range': 'Over 1',
                         '50-Day Simple Moving Average': 'Price above SMA50',
                         '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 500K',
                         'EPS growthnext year': 'Over 20%', 'Sales growthqtr over qtr': 'Over 30%',
                         'InstitutionalOwnership': 'Over 10%', 'Industry': 'Stocks only (ex-Funds)'}

    year_plus100pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 4%', 'Performance': 'Year +100%',
                       '50-Day Simple Moving Average': 'Price above SMA50',
                       '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 1M',
                       'Industry': 'Stocks only (ex-Funds)'}

    eps_neg_to_pos = {'Price': 'Over $5', 'Average True Range': 'Over 1', '52-Week High/Low': '70% or more above Low',
                      '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                      '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 1M',
                      'EPS growthnext year': 'Positive (>0%)', 'EPS growththis year': 'Negative (<0%)',
                      'InstitutionalOwnership': 'Over 10%'}

    half_year_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 4%', 'Performance': 'Half +30%',
                       '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                       '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 1M'}

    qtr_plus30pct = {'Price': 'Over $5', 'Volatility': 'Month - Over 4%', 'Performance': 'Quarter +30%',
                       '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                       '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 1M'}

    month_plus30pct = {'Price': 'Over $1', 'Volatility': 'Month - Over 4%', 'Performance': 'Month +30%',
                       '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                       '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 100K'}

    longterm = {'Average True Range': 'Over 1', '200-Day Simple Moving Average': 'Price above SMA200',
                'Average Volume': 'Over 500K', 'EPS growththis year': 'Over 10%', 'EPS growthqtr over qtr': 'Over 10%',
                'EPS growthnext year': 'Over 5%', 'Sales growthqtr over qtr': 'Over 10%', 'Gross Margin': 'Over 20%',
                'Market Cap.': '+Mid (over $2bln)', 'Industry': 'Stocks only (ex-Funds)'}

    eps_growth_yoy = {'Price': 'Over $5', 'Average True Range': 'Over 1',
                      '50-Day Simple Moving Average': 'Price above SMA50',
                      '200-Day Simple Moving Average': 'Price above SMA200', 'Industry': 'Stocks only (ex-Funds)',
                      '52-Week High/Low': '70% or more above Low', 'Average Volume': 'Over 100K',
                      'EPS growththis year': 'Over 20%', 'EPS growthnext year': 'Over 20%',
                      'Gross Margin': 'Over 20%', 'InstitutionalOwnership': 'Over 10%'}

    near_52w_high_base = {'Price': 'Over $3', 'Average True Range': 'Over 1', '52-Week High/Low': '0-10% below High',
                      '50-Day Simple Moving Average': 'Price above SMA50', 'Industry': 'Stocks only (ex-Funds)',
                      '200-Day Simple Moving Average': 'Price above SMA200', 'Average Volume': 'Over 1M'}

    pba_best_of_best = {'Price': 'Over $5', 'Average True Range': 'Over 1', 'Return on Equity': 'Over +10%',
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
    failed = []
    count = 0

    for screen ,filters_dict in filters.items():
        print('Running screen: ', screen)
        foverview.set_filter(filters_dict=filters_dict)
        df = foverview.ScreenerView(order='52-Week High (Relative)', ascend=False)
        try:
            liquid = (df['Volume']*df['Price'])/1e6 > liquidity
        except TypeError:
            liquid = (float(df['Volume']) * float(df['Price'])) / 1e6 > float(liquidity)
        updated = df[liquid]
        count += len(df)
        all_tickers.append(updated['Ticker'].values)
        failed.append(len(df) - len(updated))
        sleep(0.2)
        print("\n")

    final_tickers = []
    for s in all_tickers:
        for t in s:
            final_tickers.append(t)

    return np.unique(final_tickers), count, np.sum(failed)


def save_tickers(filename, tickers):

    utils.save_data(tickers, filename, mode='w')


def main():

    today = dt.datetime.now()
    datadir = '~/scripts/backtesting_algos/finviz_screens/'
    filename = datadir+today.strftime('%Y%m%d')+'_'+today.strftime('%H%M%S')+'.csv'
    liq = float(input('Liquidity filter [M]: '))#10

    print('Finviz Screens')
    print('Liquidity: ', str(liq)+'M')

    tickers, count, failed = scrape_finviz(liquidity=liq)
    print("\n")
    print('Screened ', count, ' tickers')
    print('Failed liquidity: ', failed)
    print('Passed liquidity: ', len(tickers))
    #print(tickers)

    save_tickers(filename, pd.DataFrame(tickers))
    print('Saved screens to: ', filename)


if __name__ == '__main__': main()