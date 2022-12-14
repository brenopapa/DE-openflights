import json
import pandas as pd
from pycarol import PwdAuth, Carol, Staging, ApiKeyAuth, Connectors
from pycarol.bigquery import BQ

credential_file = "/Users/brenozipoli/Desktop/login.json"
with open(credential_file, encoding="utf-8") as f:
    auth = json.loads(f.read())

carol = Carol(domain='brenopapa', #app_name='MinhaCoop',
              auth=PwdAuth(auth['username'], auth['password']), organization='datascience')

api_key = carol.issue_api_key()

connector = 'f85319e5c6f04042b10c127d0e66dbcf'

df = pd.read_csv("./data/airports.dat", names=["Airport_ID", "Name", "City", "Country", "IATA", "ICAO", "Latitude", "Longitude", "Altitude", "Timezone", "DST", "Tz_database_time_zone", "Type", "Source"])
print(df.head())

staging = Staging(carol)
staging.send_data(staging_name = 'airports', data = df.astype(str), step_size = 1000,
                 connector_id=connector, print_stats = True, force=True)

df = pd.read_csv("./data/airlines.dat", names=["Airline_ID", "Name", "Alias", "IATA", "ICAO", "Callsign", "Country", "Active"])
print(df.head())

staging = Staging(carol)
staging.send_data(staging_name = 'airlines', data = df.astype(str), step_size = 1000,
                 connector_id=connector, print_stats = True, force=True)

df = pd.read_csv("./data/countries.dat", names=["name", "iso_code", "dafif_code"])
print(df.head())

staging = Staging(carol)
staging.send_data(staging_name = 'countries', data = df.astype(str), step_size = 1000,
                 connector_id=connector, print_stats = True, force=True)

df = pd.read_csv("./data/planes.dat", names=["Name", "IATA_code", "ICAO_code"])
print(df.head())

staging = Staging(carol)
staging.send_data(staging_name = 'planes', data = df.astype(str), step_size = 1000,
                 connector_id=connector, print_stats = True, force=True)

df = pd.read_csv("./data/routes.dat", names=["Airline", "Airline_ID", "Source_airport", "Source_airport_ID", "Destination_airport", "Destination_airport_ID", "Codeshare", "Stops", "Equipment"])
print(df.head())

staging = Staging(carol)
staging.send_data(staging_name = 'routes', data = df.astype(str), step_size = 1000,
                 connector_id=connector, print_stats = True, force=True)