#
# check_es.py
#   Switches:
#     -x (required): status; status, number_of_nodes, etc.
#     -w (required): warning value
#     -c (required): critical value
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

    # setup -x
    if tmp_args["-x"] == "status" or tmp_args["-x"] == "initializing_shards" or tmp_args["-x"] == "number_of_data_nodes" or tmp_args["-x"] == "number_of_nodes":
        STATUS_CHECK = tmp_args["-x"]

        if tmp_args["-x"] == "status":
            COMPARISON_TYPE = "str"
        elif tmp_args["-x"] == "initializing_shards":
            COMPARISON_TYPE = "int"
        elif tmp_args["-x"] == "number_of_data_nodes":
            COMPARISON_TYPE = "int"
        elif tmp_args["-x"] == "number_of_nodes":
            COMPARISON_TYPE = "int"
    else:
        print("%s is not supported; see help." % (tmp_args["-x"]) )
        sys.exit(1)

    # setup -w
    try:
        x_val = None
        if COMPARISON_TYPE == "str" and STATUS_CHECK == "status":
            x_val = str(tmp_args["-w"])
            
            if tmp_args["-w"] != "red" and tmp_args["-w"] != "yellow":
                print("Invalid warning for %s." % (STATUS_CHECK))
                sys.exit(1)
        elif COMPARISON_TYPE == "int":
            x_val = int(tmp_args["-w"])
            STATUS_WARN = x_val
    except Exception, e:
        print(e)

    print(x_val)

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
