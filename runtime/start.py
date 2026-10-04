import os,json,subprocess,shutil,ipaddress
from pathlib import Path
from common import config,write,verify_chain
os.umask(0o077)
c=config('cln'); verify_chain(c)
root=Path('/data/lightning'); root.mkdir(exist_ok=True,mode=0o700)
net=root/c['network']; net.mkdir(exist_ok=True,mode=0o700)
# Preserve all identity keys and refuse implicit TLS identity changes.
identity=net/'tls-host'
if identity.exists() and identity.read_text()!=c['tls_host']: raise SystemExit('TLS hostname changed; preserve the original hostname or explicitly migrate credentials')
if not (net/'ca.pem').exists():
    def run(*args): subprocess.run(['openssl',*args],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    run('req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(net/'ca-key.pem'),'-out',str(net/'ca.pem'),'-days','3650','-subj','/CN=Paperclip test CLN CA')
    try: ipaddress.ip_address(c['tls_host']); san='IP:'+c['tls_host']
    except ValueError: san='DNS:'+c['tls_host']
    for role,usage in [('server','serverAuth'),('client','clientAuth')]:
        run('req','-newkey','rsa:2048','-nodes','-keyout',str(net/(role+'-key.pem')),'-out',str(net/(role+'.csr')),'-subj','/CN=Paperclip '+role)
        write(net/(role+'.ext'),'extendedKeyUsage='+usage+'\nsubjectAltName='+san+',DNS:localhost,IP:127.0.0.1\n')
        run('x509','-req','-in',str(net/(role+'.csr')),'-CA',str(net/'ca.pem'),'-CAkey',str(net/'ca-key.pem'),'-CAcreateserial','-out',str(net/(role+'.pem')),'-days','3650','-extfile',str(net/(role+'.ext')))
    hold=net/'hold';hold.mkdir(exist_ok=True,mode=0o700)
    for f in ['ca.pem','ca-key.pem','server.pem','server-key.pem','client.pem','client-key.pem']: shutil.copyfile(net/f,hold/f)
    write(identity,c['tls_host'])
if not identity.exists(): raise SystemExit('Incomplete TLS initialization; inspect before starting')
from urllib.parse import urlsplit
u=urlsplit(c['rpc_url'])
if u.scheme!='http' or u.path not in ('','/'): raise SystemExit('CLN bcli requires a private HTTP base RPC URL')
lines=['network='+c['network'],'alias='+c['alias'],'bitcoin-rpcconnect='+u.hostname,'bitcoin-rpcport='+str(u.port or 8332),'bitcoin-rpcuser='+c['rpc_user'],'bitcoin-rpcpassword='+c['rpc_password'],'bind-addr=0.0.0.0:9735','announce-addr-discovered=false','grpc-host=0.0.0.0','grpc-port=9737','plugin=/usr/local/bin/hold','hold-grpc-host=0.0.0.0','hold-grpc-port=9738','plugin=/opt/sideflash/run','log-level=info']
if c.get('trusted_server_key'): lines.append('sideflash-server-pubkey='+c['trusted_server_key'])
write(root/'config','\n'.join(lines)+'\n')
os.environ['HOME']='/data'
os.execvp('lightningd',['lightningd','--lightning-dir=/data/lightning'])
