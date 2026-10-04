import unittest,runpy,io,sys,socket,urllib.error
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'runtime'))
class ConnectionTests(unittest.TestCase):
 def run_check(self,error=None):
  with patch('common.validate',return_value={}),patch('common.verify_chain',side_effect=error),patch('sys.stdin',io.StringIO('{}')),patch('sys.stdout',io.StringIO()):
   runpy.run_path(str(Path(__file__).resolve().parents[1]/'runtime/check-connection.py'),run_name='__main__')
 def test_success(self):self.run_check()
 def test_dns_hint(self):
  with self.assertRaisesRegex(SystemExit,'LAN IP'):self.run_check(urllib.error.URLError(socket.gaierror(-2,'missing')))
 def test_auth_hint(self):
  with self.assertRaisesRegex(SystemExit,'username/password'):self.run_check(urllib.error.HTTPError('http://node',401,'Unauthorized',{},None))
 def test_connection_hint(self):
  with self.assertRaisesRegex(SystemExit,'Cannot reach'):self.run_check(urllib.error.URLError(ConnectionRefusedError()))
 def test_errors_do_not_echo_secrets(self):
  with self.assertRaises(SystemExit) as err:self.run_check(ValueError('sensitive-secret'))
  self.assertNotIn('sensitive-secret',str(err.exception))
