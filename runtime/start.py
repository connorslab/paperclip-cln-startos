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
lines=['network='+c['network'],'alias='+c['alias'],'bitcoin-rpcconnect='+u.hostname,'bitcoin-rpcport='+str(u.port or 8332),'bitcoin-rpcuser='+c['rpc_user'],'bitcoin-rpcpassword='+c['rpc_password'],'bind-addr=0.0.0.0:9735','announce-addr-discovered=false','grpc-host=0.0.0.0','grpc-port=9737','plugin=/usr/local/bin/hold','hold-grpc-host=0.0.0.0','hold-grpc-port=9738','plugin=/opt/sideflash/run','log-level=info','clnrest-host=127.0.0.1','clnrest-port=3010','clnrest-protocol=http']
if c.get('trusted_server_key'): lines.append('sideflash-server-pubkey='+c['trusted_server_key'])
write(root/'config','\n'.join(lines)+'\n')
os.environ['HOME']='/data'
# CLN remains supervised so its Unix RPC can provision RTL's private local rune.
import signal,time,sys
child=subprocess.Popen(['lightningd','--lightning-dir=/data/lightning'])
def stop(signum,frame):
    if child.poll() is None: child.send_signal(signum)
for sig in (signal.SIGTERM,signal.SIGINT): signal.signal(sig,stop)
try:
    auth=Path('/data/rtl');auth.mkdir(exist_ok=True,mode=0o700)
    rune=auth/'access.rune'
    for attempt in range(120):
        if child.poll() is not None: raise RuntimeError('CLN exited before RTL initialization')
        probe=subprocess.run(['lightning-cli','--lightning-dir=/data/lightning','getinfo'],capture_output=True)
        if probe.returncode==0: break
        time.sleep(1)
    else: raise RuntimeError('CLN RPC did not become ready for RTL')
    if not rune.exists():
        restrictions=json.dumps([['method/stop'],['method/createrune'],['method/makesecret'],['method/setconfig'],['method/plugin']])
        result=subprocess.run(['lightning-cli','--lightning-dir=/data/lightning','createrune','restrictions='+restrictions],capture_output=True,text=True,check=True)
        write(rune,json.loads(result.stdout)['rune'])
    sys.exit(child.wait())
except Exception:
    print('CLN/RTL initialization failed; check node connectivity and local RPC.',file=sys.stderr)
    if child.poll() is None:
        child.terminate()
        try:child.wait(timeout=30)
        except subprocess.TimeoutExpired:child.kill();child.wait()
    raise SystemExit(1)
