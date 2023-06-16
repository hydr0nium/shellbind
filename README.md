# shellbind

Shellbind is a python script that allows to bind a semi-interactive shell from the terminal to an existing crude webshell.

### Installation:

```bash
git clone https://github.com/hydr0nium/shellbind.git
python shellbind.py
```

### Usage
```bash
usage: shellbind.py [-h] -p PARAMETER NAME [-X METHOD] -u HOST [-D]

options:
  -h, --help            show this help message and exit
  -p PARAMETER NAME, --parameter PARAMETER NAME
                        The parameter the is used to run shell commands
  -X METHOD, --method METHOD
                        The method (GET/POST) that that is used ( Default: GET)
  -u HOST, --host HOST  The host that is attacked. Example: http://www.victim.com/vuln.php
  -D, --debug           If set the programm does print debug messages
```
