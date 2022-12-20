import json
import pandas as pd
from pycarol import PwdAuth, Carol, Staging, ApiKeyAuth, Connectors
from pycarol.bigquery import BQ

mytenants = {
    'brenopapa1': 'd5b0068fc0c0487eb52fc2a7b5e626ba',
    'brenopapa2': 'a007680ea1874bb5a337ca399bd4cf60',
    'brenopapa3': 'ea9db33535f4455a901568effc9607f5',
}

for tenant, connector in mytenants.items():
    print(tenant, connector)
    credential_file = "/Users/brenozipoli/Desktop/carol.json"
    with open(credential_file, encoding="utf-8") as f:
        auth = json.loads(f.read())

    carol = Carol(domain=tenant, #app_name='MinhaCoop',
                auth=PwdAuth(auth['username'], auth['password']), organization='datascience') 

    api_key = carol.issue_api_key()

    d = {'Description': ['moredata', 'anotherdata'], 'code': ['3', '4']}
    df = pd.DataFrame(data=d)
    print(df)

    # df = pd.read_csv("./data/planes.dat", names=["Name", "IATA_code", "ICAO_code"])
    # # print(df.head())

    staging = Staging(carol)
    staging.send_data(staging_name = 'customstaging', data = df.astype(str), step_size = 1000,
                    connector_id=connector, print_stats = True, force=True)
