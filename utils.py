import requests
import json
import pandas as pd


with open("api_key.json") as f:
    API_KEY = json.load(f)["key"]

def get_contracts():
    """ Get list of contracts (cities) from the API. """
    resp = requests.get(url="https://api.jcdecaux.com/vls/v1/contracts", params={"apiKey": API_KEY})
    return resp.json()

def get_stations_in_contract(contract_name):
    """ Get a list of the stations in a certain city with their live information. """
    resp = requests.get(url=f"https://api.jcdecaux.com/vls/v1/stations?contract={contract_name}",
                        params={"apiKey": API_KEY})
    return resp.json()

def get_station_info(station_number, contract_name):
    """ Get live information for a particular station. Note that the station number is unique only within a city."""
    url = f"https://api.jcdecaux.com/vls/v1/stations/{station_number}?contract={contract_name}"
    resp = requests.get(url=url, params={"apiKey": API_KEY})
    return resp.json()

def stations_to_pandas(stations):
    """ Parses the station information json to a pandas dataframe. """
    df = pd.DataFrame(stations)
    # Data cleaning: have one column for latitude and one for longitude instead of a 'position' col with dict entries
    df['lat'] = df['position'].map(lambda pos: pos['lat'])
    df['lng'] = df['position'].map(lambda pos: pos['lng'])
    df.drop(columns=['position'], inplace=True)
    return df
