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

connector = 'ebc4e1f503944aeda32d2003914a4bbc'

df = pd.read_csv("./data/countries.dat", names=["name", "iso_code", "dafif_code"])
print(df.head())

staging = Staging(carol)
schema = staging.create_schema(staging_name='countries', data = df.astype(str),
                      crosswalk_name= 'CrosswalkId' ,crosswalk_list=['name'],
                        connector_name='pycarol')

