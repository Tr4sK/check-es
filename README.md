ldapslap
========
Nagios check for Elasticsearch; should work with any monitoring tools that support the nagios NRPE check "API". I have tested it and it works fine with ZenOSS.

License
=======
GPLv3

Author
======
Josten Landtroop

Features
========
* Check the cluster "color" status; red, yellow.
* Check how many nodes are in the cluster.
* Check if a node is up at all (if it tries to connect and fails it throws back proper error).
* Check if nodes are initializing.
* Check data nodes.
* Supports boolean operators.

Installation
============
* `python setup.py install` or `pip install check_es`

Switches
========
* `check_es --help` for a complete list of switches.
* `-x` is the status to check; supported values are: status, initializing_shards, number_of_data_nodes, number_of_nodes.
* `-w` is the warning value.
* `-c` is the critical value.
* `-C` is the comparison type such as `<=`, `<`, `>`, `>=`, `==`, `!=`.
* `-a` is the host to connect to. Default is localhost.
* `-p` is the HTTP port to connect to. Default is 9200.

Examples
========
* `check_es -x status -w yellow -c red -c '=='` thrown a warning or critical alert if the cluster status is red or yellow.
* `check_es -x number_of_nodes -w 2 -c 2 -c '<='` throws a critical alert if the amount of nodes is less than or equal to two.

Contact
=======
* j [at] no-io [dot] net
