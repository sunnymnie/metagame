import json

def key(site: str, api_type: str, path: str)->str:
    """gets api keys stored in api-keys/api-keys.txt
    site: 'binance'
    api_type: 'api', 'secret'"""
    with open(path + 'api-keys/api-keys.txt') as json_file:
        return json.load(json_file)[site][api_type]