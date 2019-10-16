import requests
import json
import pandas as pd


with open("api_key.json") as f:
    API_KEY = json.load(f)["key"]

def get_contracts(version="v3"):
    """ Get list of contracts (cities) from the API. """
    resp = requests.get(url=f"https://api.jcdecaux.com/vls/{version}/contracts", params={"apiKey": API_KEY})
    return resp.json()

def get_contract_names():
    contracts = get_contracts()
    contract_names = pd.DataFrame(contracts)['name']
    return contract_names

def get_stations_in_contract(contract_name, version="v3"):
    """ Get a list of the stations in a certain city with their live information. """
    resp = requests.get(url=f"https://api.jcdecaux.com/vls/{version}/stations?contract={contract_name}",
                        params={"apiKey": API_KEY})
    return resp.json()

def get_station_info(station_number, contract_name, version="v3"):
    """ Get live information for a particular station. Note that the station number is unique only within a city."""
    url = f"https://api.jcdecaux.com/vls/{version}/stations/{station_number}?contract={contract_name}"
    resp = requests.get(url=url, params={"apiKey": API_KEY})
    return resp.json()

def stations_to_pandas(stations):
    """ Parses the station information json to a pandas dataframe. """
    df = pd.DataFrame(stations)
    # Data cleaning : create a column with lat and another with lon
    df['latitude'] = df['position'].map(lambda pos: pos['latitude'])
    df['longitude'] = df['position'].map(lambda pos: pos['longitude'])
    # Flatten the bike availability observations
    df['bikes_available_main'] = df['mainStands'].map(lambda stands: stands['availabilities']['bikes'])
    df['stands_available_main'] = df['mainStands'].map(lambda stands: stands['availabilities']['stands'])
    df['capacity_main'] = df['mainStands'].map(lambda stands: stands['capacity'])
    df['bikes_available_total'] = df['totalStands'].map(lambda stands: stands['availabilities']['bikes'])
    df['stands_available_total'] = df['totalStands'].map(lambda stands: stands['availabilities']['stands'])
    df['capacity_total'] = df['totalStands'].map(lambda stands: stands['capacity'])
    # drop the nested cols
    df.drop(columns=['position', 'mainStands', 'totalStands'], inplace=True)
    return df

def get_all_bike_data():
    contracts = get_contracts()
    contract_names = pd.DataFrame(contracts)['name']
    stations_list = []
    for name in contract_names:
        try:
            stations = get_stations_in_contract(contract_name=name)
            stations_list.append(stations_to_pandas(stations))
        except:
            print(f"Failed to pull data from {name}")
            pass
    print("Loaded data from %d out of %d cities"%(len(stations_list),len(contract_names)))
    return pd.concat(stations_list)
