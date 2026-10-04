import unittest,sys,tempfile,json,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
from common import validate,write,url
KIND='cln'
class ConfigurationTests(unittest.TestCase):
 def valid(self):
  return dict(network='bitcoin',rpc_url='http://127.0.0.1:8332',rpc_user='test',rpc_password='test',asp_url='http://127.0.0.1:3535',alias='Test node',tls_host='192.168.1.100',trusted_server_key='',sweep_address='bc1q'+'q'*38,recipient_allowlist=[])
 def test_valid_config(self):self.assertEqual(validate(KIND,self.valid())['network'],'bitcoin')
 def test_wrong_network_rejected(self):
  c=self.valid();c['network']='signet'
  with self.assertRaises(ValueError):validate(KIND,c)
 def test_urls_do_not_embed_credentials(self):
  for bad in ['http://user:secret@host:8332','file:///etc/passwd','http://host/?password=secret','http://host/#fragment']:
   with self.assertRaises(ValueError):url(bad)
 def test_tls_required_for_grpc(self):
  with self.assertRaises(ValueError):url('http://host:9737',True)
 def test_newline_cannot_inject_cln_config(self):
  c=self.valid();c['rpc_password']='secret\nplugin=bad';c['pruned']=True
  with self.assertRaises(ValueError):validate(KIND,c)
 def test_atomic_secret_write_and_symlink_refusal(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'secret';write(p,'first');write(p,'second');self.assertEqual(p.read_text(),'second')
   if os.name!='nt':self.assertEqual(p.stat().st_mode&0o777,0o600)
   q=Path(d)/'link'
   try:q.symlink_to(p)
   except OSError:return
   with self.assertRaises(ValueError):write(q,'replace')
   self.assertEqual(p.read_text(),'second')
 def test_sideflash_controls(self):
  c=self.valid()
  if KIND=='cln':c['trusted_server_key']='short key'
  elif KIND=='ark':c['recipient_allowlist']=['untrusted']
  else:c['asp_url']='ftp://example.com'
  with self.assertRaises(ValueError):validate(KIND,c)
if __name__=='__main__':unittest.main()
