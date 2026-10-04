import json,sys,subprocess
from pathlib import Path
from urllib.parse import urlsplit
c=json.loads(Path('/data/settings.json').read_text());i=json.load(sys.stdin)
for key in ['uri','hold_uri']:
 u=urlsplit(i[key])
 if u.scheme!='https' or u.hostname!=c['tls_host'] or not u.port or u.username or u.password or u.path not in ('','/') or u.query or u.fragment:
  raise SystemExit('Use HTTPS endpoints matching the configured TLS hostname and the ports shown in Interfaces.')
p=Path('/data/lightning')/c['network']
node=json.loads(subprocess.check_output(['lightning-cli','--lightning-dir=/data/lightning','getinfo']))['id']
print(json.dumps(dict(format='paperclip-cln-connection',version=1,network=c['network'],node_id=node,uri=i['uri'],hold_uri=i['hold_uri'],ca=(p/'ca.pem').read_text(),client_cert=(p/'client.pem').read_text(),client_key=(p/'client-key.pem').read_text())))
