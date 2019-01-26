import requests
import pandas
import io
import datetime

# 1. get ticker list 
nasdaq_url 			= 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
data_string			= requests.get(nasdaq_url).content
nasdaq_tickers_raw  = pandas.read_csv(io.StringIO(data_string.decode('utf-8')))
nasdaq_tickers      = nasdaq_tickers_raw['Symbol'].tolist()

# 2. save te ticker list to a local file
datae_today = datetime.datetime.today().strftime('%Y%m%d')
nasdaq_tickers_raw.to_csv('nasdaq_tickers_'+datae_today+'.csv', index=False)
