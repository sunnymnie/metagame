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

def update_profile(assets=None):
    """
    updates profile given list of assets, else fetches lest of all margin available binance assets
    Takes ~10 minutes due to messari constraints
    """
    if assets is None: assets = list(map(lambda x: x['base'], get_all_margin_assets()))
    iteration = 0
    total = len(assets)
    for asset in assets:
        ui.printProgressBar(iteration, total)
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




def get_all_margin_assets(quote="BTC"):
    """gets all margin-trable assets on binance"""
    all_assets = client.get_all_isolated_margin_symbols()
    all_assets = list(filter(lambda x: x['quote']==quote, all_assets))
    all_assets = list(filter(lambda x: x['isMarginTrade']==True, all_assets))
    return all_assets