#
# check_es.py
#   Switches:
#     -x (required): status; status, number_of_nodes, etc.
#     -w (required): warning value
#     -c (required): critical value
#     -t (optional): comparison type; str or int; default str
#     -C (optional): comparison operator: >, >=, <, <=, ==, !=; default ==
#     -a (optional): IP/hostname; default localhost
#     -p (optional): port; default 9200
#     -h / --help (optional): help
#

import httplib
import json
import sys

COMPARISON_TYPE = "str"
COMPARISON_OP   = "=="
IP_HOSTNAME     = "localhost"
IP_PORT         = 9200
STATUS_CHECK    = ""
STATUS_WARN     = ""
STATUS_CRIT     = ""


if "-x" not in sys.argv or "-w" not in sys.argv or "-c" not in sys.argv:
    print("-x, -w, and -c are required")
    sys.exit(1)
else:
    tmp_args = sys.argv[1:]
    tmp_args = dict([(tmp_args[i],tmp_args[i+1]) for i,b in enumerate(tmp_args[1:]) if i % 2 == 0])
    
    STATUS_CHECK = tmp_args["-x"]
    STATUS_WARN  = tmp_args["-w"]
    STATUS_CRIT  = tmp_args["-c"]

    print(STATUS_CHECK)
    print(STATUS_WARN)
    print(STATUS_CRIT)
    

#http_conn = httplib.HTTPConnection("localhost", 9200)
#http_conn.request("GET", "/_cluster/health")
#resp = json.loads(http_conn.getresponse().read())
#
#print(resp)
