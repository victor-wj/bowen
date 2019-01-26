import requests
import pandas
import io
import datetime
import os

my_apikey = '42KMTDTEQSQAWJXP'
def dataframe_fromUrl(url):
	data_string	  = requests.get(url).content
	parse_result  = pandas.read_csv(io.StringIO(data_string.decode('utf-8')), index_col=0)
	return parse_result

def stockPrice_intraday(my_ticker, csv_file):
	# 1, get data online
	alphavantage_url = 'https://www.alphavantage.co/query?apikey={apikey}&function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=1min&outputsize=full&datatype=csv'.format(apikey=my_apikey, ticker=my_ticker)
	print (alphavantage_url)
	intraday = dataframe_fromUrl(alphavantage_url)

	# 2. append if history exist
	if os.path.exists(csv_file):
		history = pandas.read_csv(csv_file, index_col=0)
		intraday.append(history)

	# 3. sort based on the first column timestampe
	intraday.sort_index(inplace=True)

	# 4. save 
	intraday.to_csv(csv_file)


# 1. get ticker list 
nasdaq_url 	= 'http://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ&render=download'
data_string			= requests.get(nasdaq_url).content
nasdaq_tickers_raw  = pandas.read_csv(io.StringIO(data_string.decode('utf-8')))
nasdaq_tickers = nasdaq_tickers_raw['Symbol'].tolist()

# 2. save te ticker list to a local file
datae_today = datetime.datetime.today().strftime('%Y%m%d')
nasdaq_tickers_raw.to_csv('nasdaq_tickers_'+datae_today+'.csv', index=False)

# 3. get stock price (intraday)
for i, ticker in enumerate(nasdaq_tickers):
	print (i, ticker, len(nasdaq_tickers))
	stockPrice_intraday(ticker, csv_file=ticker+'.csv')
	
