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
#   Dependencies: ipaddress

import httplib
import json
import sys
import socket
import ipaddress

COMPARISON_TYPE = "str"
COMPARISON_OP   = "=="
IP_HOSTNAME     = "localhost"
IP_PORT         = 9200
STATUS_CHECK    = ""
STATUS_WARN     = ""
STATUS_CRIT     = ""

def check_es_help():
    print("Usage: check_es -x <status> -w <warn> -c <crit> [options]")
    print("Options:")
    print("\t-x: The status to check; supported values are: status, initializing_shards, number_of_data_nodes, number_of_nodes")
    print("\t-w: warning value (dependent upon status).")
    print("\t-c: critical value (dependent upon status).")
    print("\t-C: Comparison type: <,<=,>,>=,!=,== . This is ignored if -x is status.")
    print("\t-a: Elasticsearch server to connect to. Default localhost.")
    print("\t-p: Elasticsearch server HTTP port. Default 9200.")
    print("\t-h / --help: Prints out this help document.")
    print("Note: -x, -w, -c are required.")

def init_data():
    http_conn = httplib.HTTPConnection(IP_HOSTNAME, IP_PORT)
    http_conn.request("GET", "/_cluster/health")
    resp = json.loads(http_conn.getresponse().read())
    
    return resp

def check_status(health_resp):
    if health_resp["status"] == STATUS_WARN:
        sys.exit(1)
    elif health_resp["status"] == STATUS_CRIT:
        sys.exit(2)

def check_initializing_shards():
    pass

def check_number_of_data_nodes():
    pass

def check_number_of_nodes():
    pass

# help
if "--help" in sys.argv or "-h" in sys.argv:
    check_es_help()
    sys.exit(0)

# setup check
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
        if STATUS_CHECK == "status":
            x_val = str(tmp_args["-w"])
            
            if tmp_args["-w"] != "red" and tmp_args["-w"] != "yellow":
                print("Invalid warning for %s." % (STATUS_CHECK))
                sys.exit(1)
            else:
                STATUS_WARN = x_val
    except Exception, e:
        print(e)

    # setup -c
    try:
        if STATUS_CHECK == "status":
            x_val = str(tmp_args["-c"])
    
            if tmp_args["-c"] != "red" and tmp_args["-c"] != "yellow":
                print("Invalid critical for %s." % (STATUS_CHECK))
                sys.exit(1)
            else:
                if tmp_args["-w"] == tmp_args["-c"]:
                    print("You cant warn and crit at the same time!")
                    sys.exit(1)
                else:
                    STATUS_CRIT = x_val
    except Exception, e:
        print(e)
    

    # setup -C
    if "-C" in tmp_args:
        if tmp_args["-C"] == "<=" or tmp_args["-C"] == "<" or tmp_args["-C"] == ">" or tmp_args["-C"] == ">=" or tmp_args["-C"] == "==" or tmp_args["-C"] == "!=":
            COMPARISON_OP = tmp_args["-C"]
        else:
            print("%s is an invalid comparison operator; only >,>=,<,<=,==,!= are supported")
            sys.exit(1)

    # setup -a
    if "-a" in tmp_args:
        bad_host_count = 0
        
        # check if IP
        try:
            ipaddress.ip_address(tmp_args["-a"].decode("utf-8"))
        except ValueError:
            bad_host_count += 1
        
        # check if host
        try:
            socket.gethostbyname(tmp_args["-a"])
        except socket.gaierror:
            bad_host_count += 1

        if bad_host_count > 1:
            print("Invalid IP/hostname %s" % tmp_args["-a"])
            sys.exit(1)
        
        IP_HOSTNAME = tmp_args["-a"]

    # setup -p
    if "-p" in tmp_args:
        try:
            int(tmp_args["-p"])
            
            if int(tmp_args["-p"]) < 1 or int(tmp_args["-p"]) > 65535:
                print("%s is not a valid port." % tmp_args["-p"])
                sys.exit(1)

            IP_PORT = int(tmp_args["-p"])
        except ValueError:
            print("%s is not a valid port." % tmp_args["-p"])
            sys.exit(1)

print(IP_HOSTNAME)
print(IP_PORT)
print(COMPARISON_OP)
print(STATUS_WARN)
print(STATUS_CRIT)
print(STATUS_CHECK)
