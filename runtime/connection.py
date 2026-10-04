import json,subprocess
from pathlib import Path
c=json.loads(Path('/data/settings.json').read_text());p=Path('/data/lightning')/c['network']
def rpc(method):
    return json.loads(subprocess.check_output(['lightning-cli','--lightning-dir=/data/lightning',method]))
print(json.dumps({'uri':'https://'+c['tls_host']+':REPLACE_WITH_GRPC_PORT','hold_uri':'https://'+c['tls_host']+':REPLACE_WITH_HOLD_PORT','ca':(p/'ca.pem').read_text(),'client_cert':(p/'client.pem').read_text(),'client_key':(p/'client-key.pem').read_text(),'node_id':rpc('getinfo')['id'],'onchain_address':rpc('newaddr')['bech32']}))
