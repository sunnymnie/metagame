import json

def key(site: str):
    """returns api keys for site"""
    with open('keys.json') as json_file:
        return json.load(json_file)[site]