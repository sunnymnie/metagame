import binance_helpers as bh
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

client = bh.new_binance_client()
PATH = "data/"


def get_timeseries_data(pair:str):
    """gets the binance past timeseries"""    
    df = update_data(pair, get_past_bars(pair))
    df['timestamp'] = list(map(lambda x: datetime.utcfromtimestamp(x/1e3), df.timestamp))
    df = df.set_index('timestamp')
    return df


def update_data(pair:str, df_past):
    """smartly updates and returns minutely data. Enter pair with USDT"""     
    df_now = binance_download(pair, df_past.iloc[-1].timestamp)

    df = df_past[df_past.timestamp < df_now.iloc[0].timestamp]
    df = df.append(df_now, ignore_index=True)
    save_df_fast(pair, df, df_past.iloc[-1].timestamp, buffer=10)
    return df

def get_past_bars(pair, span="m", full=False):
    """returns downloaded data if it exists, else downloads and returns"""
    try:
        return read_df(pair)
    except:
        df = binance_download(pair=pair)
        save_df(df, pair)
        return df


def binance_download(pair:str, start=1000000000000):
    """
    downloads binance data and returns it. Set save to true to save
    pair: BTCUSDT
    start: float date. Leave as is for from the very beginning (2001). 
    """
    start_date = get_str_date(get_date_from_int(start))
    klines = client.get_historical_klines(pair, client.KLINE_INTERVAL_1HOUR, start_date, limit=1000)
    data = get_filtered_dataframe(klines)
    return data

def get_filtered_dataframe(klines):
    """filters columns and converts columns to floats and ints respectively"""
    df = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    df = df.astype(np.float64)
    df["timestamp"] = df.timestamp.astype(np.int64)
    return df

def get_date_from_int(date:int, delay=600):
    """returns datetime object from int minus delay in seconds"""
    return datetime.utcfromtimestamp(date/1000) - timedelta(seconds=delay)

def get_str_date(date):
    """returns the string date given datetime date. Use for getting klines"""
    return date.strftime("%d %b %Y %H:%M:%S")

def save_df(df, pair):
    """saves the dataframe"""
    df.to_csv(f"{PATH + pair}.csv", index=False)

def save_df_fast(pair, df, timestamp, buffer=10):
    """update saved df by writing only what it is missing minus buffer minutes"""
    df = df[df.timestamp > timestamp]
    df[:-buffer].to_csv(f"{PATH + pair}.csv", mode='a', header=False, index=False)


def read_df(pair):
    """reads the dataframe"""
    return pd.read_csv(f"{PATH + pair}.csv")

def get_all_isolated_margin_assets():
    """returns client.get_all_isolated_margin_symbols()"""
    client = bh.new_binance_client()
    return client.get_all_isolated_margin_symbols()


