import json,sys,socket,urllib.error
from common import validate,verify_chain
try:
    verify_chain(validate('cln',json.load(sys.stdin)))
except urllib.error.HTTPError as e:
    raise SystemExit('Node RPC returned HTTP %s. Check the RPC username/password and node allowlist.' % e.code)
except urllib.error.URLError as e:
    if isinstance(e.reason,socket.gaierror):
        raise SystemExit('Cannot resolve the Knots RPC hostname. Use the node LAN IP and exposed RPC port instead of a Docker hostname or .local name.')
    raise SystemExit('Cannot reach node RPC. Check the LAN IP, exposed port, firewall and RPC allowlist.')
except Exception:
    raise SystemExit('Node check failed. Check the configuration and select the correct Bitcoin network.')
print('Node RPC connection and network verified.')
