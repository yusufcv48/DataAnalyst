from MetatradeAccount import *
import pandas as pd
# pd.set_option('display.max_columns', 500) # number of columns to be displayed
# pd.set_option('display.width', 1500)      # max table width to display
import pytz
from datetime import datetime

DATA = {
    "GBPUSD": None,
    "USDCHF": None,
    "USDJPY": None,
    "USDCNH": None,
    "USDRUB": None,
}

def historical(symbol : str, timeframe, date_from=None, date_to=None):

    if login(ACCOUNT["login"], ACCOUNT["password"], ACCOUNT["server"]):
        timezone = pytz.timezone("Etc/UTC")
        utc_from = datetime(2020, 1, 1, tzinfo=timezone)
        utc_to = datetime(2023, 1, 1, tzinfo=timezone)

        try:
            if date_from == None and date_to == None:
                date_from = utc_from
                date_to = utc_to
            rates = mt5.copy_rates_range(symbol, timeframe, date_from, date_to)
            if rates is None:
                print("error: ", mt5.last_error())
                return None
        except Exception as e:
            print(e)
        else:
            # create DataFrame out of the obtained data
            rates_frame = pd.DataFrame(rates)
            # convert time in seconds into the 'datetime' format
            rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
            # display data
            print("\nDisplay dataframe with data")
            print(rates_frame.head(10))
            return rates_frame
        finally:
            mt5.shutdown()
    else:
        print("failed to try again connect at account #{}, error code: {}".format(loginid, mt5.last_error()))


def find_outlier(dataframe):
    quantile_1 = dataframe.open.quantile(0.25)
    quantile_3 = dataframe.open.quantile(0.75)
    iqr = quantile_3 - quantile_1
    outlier = dataframe[((dataframe.open < (quantile_1 - 1.5*iqr)) | (dataframe.open > (quantile_3 + 1.5*iqr)))].set_index(["time"]).copy().open
    return [quantile_1, quantile_3, outlier]

def find_corr():
    dataset = {}
    for stock in DATA:
        dataset[stock] = DATA[stock]["data"].set_index(["time"]).copy().open
    df = pd.DataFrame(dataset)

    return {"data": df, "corr": df.corr()}


def get_all_stock_outlier():
    for stock in DATA:
        datasheet =  historical(stock, mt5.TIMEFRAME_D1)
        try:
            data_outlier = find_outlier(datasheet)
            DATA[stock] = { "data": datasheet,
                            "q1": data_outlier[0],
                            "q3": data_outlier[1],
                            "outlier": data_outlier[2]}
        except Exception as e:
            print(e)
        finally:
            del datasheet