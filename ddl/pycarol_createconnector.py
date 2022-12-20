from pycarol import PwdAuth, Carol, Staging, ApiKeyAuth, Connectors
from pycarol.bigquery import BQ

import json

credential_file = "/Users/brenozipoli/Desktop/carol.json"
with open(credential_file, encoding="utf-8") as f:
    auth = json.loads(f.read())


carol = Carol(domain='brenopapa', #app_name='MinhaCoop',
                auth=PwdAuth(auth['username'], auth['password']), organization='datascience') 
connector_id = Connectors(carol).create(name='myconnector', label="myconnector", group_name="myconnector")
print(f"This is the connector id: {connector_id}")