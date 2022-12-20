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

d = {'Description': ['mydata', 'thisdata'], 'code': ['1', '2']}
df = pd.DataFrame(data=d)
print(df)

staging = Staging(carol)
schema = staging.create_schema(staging_name='customstaging', data = df.astype(str),
                      crosswalk_name= 'CrosswalkId' ,crosswalk_list=['code'],
                        connector_name='myconnector')