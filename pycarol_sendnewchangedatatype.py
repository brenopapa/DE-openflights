import json
import pandas as pd
from pycarol import PwdAuth, Carol, Staging, ApiKeyAuth, Connectors
from pycarol.bigquery import BQ

mytenants = {
    'brenopapa4': '7d9419d145794cda94c8be5c06a542fb',

}

for tenant, connector in mytenants.items():
    print(tenant, connector)
    credential_file = "/Users/brenozipoli/Desktop/carol.json"
    with open(credential_file, encoding="utf-8") as f:
        auth = json.loads(f.read())

    carol = Carol(domain=tenant, #app_name='MinhaCoop',
                auth=PwdAuth(auth['username'], auth['password']), organization='datascience') 

    api_key = carol.issue_api_key()

    print(api_key)

    d = {'endereco_num': ['true' , 'false', 'false']}
    df = pd.DataFrame(data=d)

    # df = pd.read_csv("./data/planes.dat", names=["Name", "IATA_code", "ICAO_code"])
    # # print(df.head())

    staging = Staging(carol)
    staging.send_data(staging_name = 'changedatatype', data = df, step_size = 1000,
                    connector_id=connector, print_stats = True, force=True)
