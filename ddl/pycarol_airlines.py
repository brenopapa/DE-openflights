import json
import pandas as pd
from pycarol import PwdAuth, Carol, Staging, ApiKeyAuth, Connectors
from pycarol.bigquery import BQ

credential_file = "/Users/brenozipoli/Desktop/carol.json"
with open(credential_file, encoding="utf-8") as f:
    auth = json.loads(f.read())

carol = Carol(domain='brenopapa', #app_name='MinhaCoop',
              auth=PwdAuth(auth['username'], auth['password']), organization='datascience')

api_key = carol.issue_api_key()

print(api_key)

connector = '3de64ff45e5943b9ad52b44b4206316f'

df = pd.read_csv("./data/airlines.dat", names=["Airline_ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"])
print(df.head())

staging = Staging(carol)
schema = staging.create_schema(staging_name='airlines', data = df.astype(str),
                      crosswalk_name= 'CrosswalkId' ,crosswalk_list=['Airline_ID'],
                        connector_name='myconnector')