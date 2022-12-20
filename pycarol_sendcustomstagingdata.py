import json
import pandas as pd
from pycarol import PwdAuth, Carol, Staging, ApiKeyAuth, Connectors
from pycarol.bigquery import BQ

mytenants = {
    'brenopapa': '3de64ff45e5943b9ad52b44b4206316f',
}

for tenant, connector in mytenants.items():
    print(tenant, connector)
    credential_file = "/Users/brenozipoli/Desktop/carol.json"
    with open(credential_file, encoding="utf-8") as f:
        auth = json.loads(f.read())

    carol = Carol(domain=tenant, #app_name='MinhaCoop',
                auth=PwdAuth(auth['username'], auth['password']), organization='datascience') 

    api_key = carol.issue_api_key()

    d = {'Description': ['mydata', 'thisdata'], 'code': ['1', '2']}
    df = pd.DataFrame(data=d)
    print(df)

    # df = pd.read_csv("./data/planes.dat", names=["Name", "IATA_code", "ICAO_code"])
    # # print(df.head())

    staging = Staging(carol)
    staging.send_data(staging_name = 'customstaging', data = df.astype(str), step_size = 1000,
                    connector_id=connector, print_stats = True, force=True)
