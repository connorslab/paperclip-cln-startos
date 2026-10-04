import json,sys
from common import validate
validate(sys.argv[1],json.load(sys.stdin))
