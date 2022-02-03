import binance_helpers as bh
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import binance_downloader as bdl
import json
import requests
import ui
import time

client = bh.new_binance_client()
PATH = "data/"
PROFILE = "profile.json"
BACKTESTING = "backtesting.csv"

def get_all_assets():
    """
    gets all the margin assets with messari page
    - returns list without quote asset
    """
    # orig = list(read_profile().keys())
    # return orig
    
    # account=client.get_margin_account()
    # account = list(map(lambda x: x['asset'], account['userAssets']))
    # return account
    
    all_assets = client.get_all_isolated_margin_symbols()
    all_assets = list(filter(lambda x: x['quote']=="USDT", all_assets))
    all_assets = list(filter(lambda x: x['isMarginTrade']==True, all_assets))
    all_assets = list(map(lambda x: x['base'], all_assets))
    return all_assets

    # return list(filter(lambda x: x not in , a))
def get_must_be_in_assets():
    account=client.get_margin_account()
    account = list(map(lambda x: x['asset'], account['userAssets']))
    return account

def get_backtesting_df(assets=None, length=None, quote="USDT", progress=False, sleep=0.5, save=True):
    """
    gets backtesting df with closing prices of all assets in profile.
    - assets: list of assets without quote
    - length: limit the length of the df
    - progress: to show progress bar or not
    - sleep: >=0. Time to sleep before binance call
    - save: whether to save the df
    """
    if assets is None: assets = get_all_assets()
    if "BTC" in assets: assets.remove("BTC")
    df = bdl.get_timeseries_data("BTCUSDT").close.rename("btc").to_frame()
    
    iteration = 0
    total = len(assets)
    
    for asset in assets:
        if progress: ui.printProgressBar(iteration, total)
        iteration += 1
        time.sleep(sleep)
        
        try:
            new = (bdl.get_timeseries_data(asset+quote)['close']/df.btc).rename(asset.lower())
            # new = bdl.get_timeseries_data(asset+quote)['close'].rename(asset.lower())
            df = pd.concat([df, new], axis=1)
        except:
            print(f"Warning: No symbol exists: {asset+quote}")
                    
    ui.printProgressBar(iteration, total)
    
    if save: df.to_csv(PATH+BACKTESTING)
    
    return df
    

def update_profile(assets=None, progress=False):
    """
    updates profile given list of assets, else fetches lest of all margin available binance assets
    Takes ~10 minutes due to messari constraints
    - progress: whether to show progress bar or not
    """
    if assets is None: assets = list(map(lambda x: x['base'], get_all_margin_assets()))
    iteration = 0
    total = len(assets)
    for asset in assets:
        if progress: ui.printProgressBar(iteration, total)
        iteration += 1
        time.sleep(3.1)
        response = requests.get(f"https://data.messari.io/api/v2/assets/{asset.lower()}/profile")
        if response.status_code != 200: continue
        
        profile = read_profile()
        profile[asset] = response.json()['data']
        save_profile(profile)
    
    ui.printProgressBar(iteration, total)
        
    


def read_profile():
    """Reads and returns profile"""
    try:
        with open(PATH + PROFILE, 'r') as f:
            data = json.load(f)
        return data
    except:
        print("Warning: Error in opening profile, returning empty json")
        return {}
    
def save_profile(profile):
    """takes in json of profile and saves it """
    with open(PATH + PROFILE, 'w') as f:
        json.dump(profile, f, indent=4)




def get_all_margin_assets(quote="USDT"):
    """gets all margin-trable assets on binance"""
    all_assets = client.get_all_isolated_margin_symbols()
    all_assets = list(filter(lambda x: x['quote']==quote, all_assets))
    all_assets = list(filter(lambda x: x['isMarginTrade']==True, all_assets))
    return all_assets