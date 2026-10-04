import json, os, re, tempfile, urllib.request, base64
from pathlib import Path
from urllib.parse import urlsplit

def write(path, text):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if path.is_symlink(): raise ValueError("Symlink storage refused")
    fd,tmp=tempfile.mkstemp(dir=path.parent)
    try:
        with os.fdopen(fd,'w') as f: f.write(text); f.flush(); os.fsync(f.fileno())
        os.chmod(tmp,0o600); os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def url(value, tls=False):
    u=urlsplit(value)
    if u.scheme not in (('https',) if tls else ('http','https')) or not u.hostname or u.username or u.password or u.query or u.fragment: raise ValueError('Invalid service URL')
    return u

def validate(kind,c):
    if c.get('network') not in ('bitcoin','regtest'): raise ValueError('Unsupported network')
    if kind!='wallet':
        url(c['rpc_url'])
        for key in ['rpc_user','rpc_password']:
            if not c.get(key) or any(x in c[key] for x in ['\r','\n','\0']): raise ValueError('Invalid RPC credentials')
    else: url(c['asp_url'])
    if kind=='cln':
        if not re.fullmatch(r'[A-Za-z0-9.-]{1,253}',c['tls_host']): raise ValueError('Invalid TLS hostname')
        pin=c.get('trusted_server_key','')
        if pin and not re.fullmatch(r'0[23][0-9a-fA-F]{64}',pin): raise ValueError('Invalid full server public key')
        if not re.fullmatch(r'[A-Za-z0-9 _.-]{1,32}',c['alias']): raise ValueError('Invalid alias')
    if kind=='ark':
        for key in c.get('recipient_allowlist',[]):
            if not re.fullmatch(r'0[23][0-9a-fA-F]{64}',key): raise ValueError('Invalid recipient public key')
        if c.get('cln'):
            for key in ['uri','hold_uri']: url(c['cln'][key],True)
            for key in ['ca','client_cert','client_key']:
                if '-----BEGIN ' not in c['cln'][key]: raise ValueError('PEM credentials required')
    return c

def verify_chain(c):
    def rpc(method,args=[]):
        req=urllib.request.Request(c['rpc_url'],json.dumps({'jsonrpc':'1.0','id':1,'method':method,'params':args}).encode(),{'Content-Type':'application/json','Authorization':'Basic '+base64.b64encode((c['rpc_user']+':'+c['rpc_password']).encode()).decode()})
        with urllib.request.urlopen(req,timeout=15) as r: reply=json.load(r)
        if reply.get('error'): raise ValueError('Node RPC rejected chain check')
        return reply['result']
    info=rpc('getblockchaininfo')
    if info['chain'] != ('main' if c['network']=='bitcoin' else 'regtest'): raise ValueError('Backend network mismatch')
    if c['network']=='bitcoin' and len(rpc('getblockheader',[info['bestblockhash'],False]))!=328: raise ValueError('XBT backend required; incompatible chain header')
    return info

def config(kind):
    c=validate(kind,json.loads(Path('/data/settings.json').read_text()))
    lock=Path('/data/network.lock')
    if lock.exists() and lock.read_text()!=c['network']: raise ValueError('Network changes require a fresh test app')
    if not lock.exists(): write(lock,c['network'])
    return c
